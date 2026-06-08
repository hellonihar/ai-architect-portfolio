import time

from agentic.llm_client import LLMClient
from agentic.reflection.citation_checker import CitationChecker
from agentic.reflection.relevance_checker import RelevanceChecker
from agentic.strategies.base import BaseAgenticStrategy
from api.schemas import AgenticResponse, Document, ReflectionStep
from retrieval.engine import RetrievalEngine


class SelfRAG(BaseAgenticStrategy):
    def __init__(self, llm: LLMClient, retrieval: RetrievalEngine):
        self.llm = llm
        self.retrieval = retrieval
        self.relevance = RelevanceChecker(llm)
        self.citations = CitationChecker(llm)

    @property
    def name(self) -> str:
        return "self_rag"

    def execute(self, query: str, top_k: int = 10, **kwargs) -> AgenticResponse:
        start = time.perf_counter()
        reflections: list[ReflectionStep] = []
        all_docs: list[Document] = []

        decision = self.llm.should_retrieve(query)
        reflections.append(ReflectionStep(
            step_type="retrieve_decision",
            input=f"Query: {query}",
            output=f"Retrieve: {decision.get('retrieve', True)}, Reason: {decision.get('reason', '')}",
            confidence=decision.get("confidence", 0.5),
        ))

        if decision.get("retrieve", True):
            docs, _ = self.retrieval.search(query, retriever_name="hybrid", top_k=top_k)
            all_docs = docs

            reflection_docs = [d.model_dump() for d in docs]
            relevant_docs, relevance_reflections = self.relevance.filter_relevant(query, reflection_docs)
            reflections.extend(relevance_reflections)

            relevant_docs_obj = [Document(**d) for d in relevant_docs]

            if relevant_docs:
                gen_result = self.llm.generate_answer(query, relevant_docs_obj)
                answer = gen_result.get("answer", "No answer generated.")
                raw_citations = gen_result.get("citations", [])
                confidence = gen_result.get("confidence", 0.0)

                reflections.append(ReflectionStep(
                    step_type="generate",
                    input=f"Query: {query}\nPassages: {[d.id for d in relevant_docs_obj]}",
                    output=f"Answer: {answer[:200]}...",
                    confidence=confidence,
                ))

                verified_citations, citation_reflections = self.citations.verify_answer(
                    answer, reflection_docs
                )
                reflections.extend(citation_reflections)
            else:
                gen_result = self.llm.generate_direct(query)
                answer = gen_result.get("answer", "No relevant passages found.")
                raw_citations = []
                verified_citations = []

                reflections.append(ReflectionStep(
                    step_type="generate_direct",
                    input=f"Query: {query}",
                    output=f"Answer: {answer[:200]}...",
                    confidence=gen_result.get("confidence", 0.0),
                ))
        else:
            gen_result = self.llm.generate_direct(query)
            answer = gen_result.get("answer", "")
            raw_citations = []
            verified_citations = []

            reflections.append(ReflectionStep(
                step_type="generate_direct",
                input=f"Query: {query}",
                output=f"Answer: {answer[:200]}...",
                confidence=gen_result.get("confidence", 0.0),
            ))

        elapsed = (time.perf_counter() - start) * 1000

        return AgenticResponse(
            original_query=query,
            strategy=self.name,
            answer=answer,
            reflections=reflections,
            retrieved_docs=all_docs,
            timing_ms=round(elapsed, 1),
            citations=verified_citations or raw_citations,
        )
