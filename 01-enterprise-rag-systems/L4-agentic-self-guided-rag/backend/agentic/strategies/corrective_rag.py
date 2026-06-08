import time

from agentic.llm_client import LLMClient
from agentic.reflection.quality_scorer import QualityScorer
from agentic.reflection.relevance_checker import RelevanceChecker
from agentic.strategies.base import BaseAgenticStrategy
from api.schemas import AgenticResponse, Document, ReflectionStep
from data.web_fallback import get_web_documents
from retrieval.engine import RetrievalEngine


class CorrectiveRAG(BaseAgenticStrategy):
    def __init__(self, llm: LLMClient, retrieval: RetrievalEngine):
        self.llm = llm
        self.retrieval = retrieval
        self.quality = QualityScorer(llm)
        self.relevance = RelevanceChecker(llm)

    @property
    def name(self) -> str:
        return "corrective_rag"

    def execute(self, query: str, top_k: int = 10, **kwargs) -> AgenticResponse:
        start = time.perf_counter()
        reflections: list[ReflectionStep] = []
        all_docs: list[Document] = []

        docs, _ = self.retrieval.search(query, retriever_name="hybrid", top_k=top_k)
        all_docs = docs

        quality_label, quality_conf, quality_expl, quality_reflection = self.quality.score(
            query, [d.model_dump() for d in docs]
        )
        reflections.append(quality_reflection)

        needs_correction, action = self.quality.needs_correction(quality_label)

        if needs_correction and action == "rewrite_needed":
            rewrite_result = self.llm.rewrite_query(query, [d.content for d in docs])
            rewritten = rewrite_result.get("rewritten_query", query)
            reflections.append(ReflectionStep(
                step_type="query_rewrite",
                input=f"Original: {query}\nPoor quality: {quality_expl}",
                output=f"Rewritten: {rewritten}",
                confidence=quality_conf,
            ))

            new_docs, _ = self.retrieval.search(rewritten, retriever_name="hybrid", top_k=top_k)
            all_docs = new_docs

            new_quality, _, _, recheck_reflection = self.quality.score(
                rewritten, [d.model_dump() for d in new_docs]
            )
            reflections.append(recheck_reflection)

            if new_quality == "low":
                web_docs_data = get_web_documents()
                web_docs = [Document(
                    id=d["id"],
                    content=d["content"],
                    score=1.0,
                    route="web_fallback",
                    metadata={"source": d.get("source", "web")},
                ) for d in web_docs_data]
                all_docs.extend(web_docs)

                relevant_web, web_reflections = self.relevance.filter_relevant(
                    query, [d.model_dump() for d in web_docs]
                )
                reflections.extend(web_reflections)
                reflections.append(ReflectionStep(
                    step_type="fallback",
                    input=f"Query: {query}",
                    output="Fell back to simulated web corpus and LLM knowledge",
                    confidence=0.5,
                ))

                if relevant_web:
                    gen_result = self.llm.generate_answer(query, [Document(**d) for d in relevant_web])
                else:
                    gen_result = self.llm.generate_direct(query)
            else:
                gen_result = self.llm.generate_answer(query, new_docs)

        elif needs_correction and action == "fallback_needed":
            gen_result = self.llm.generate_direct(query)
            reflections.append(ReflectionStep(
                step_type="fallback",
                input=f"Query: {query}",
                output="Quality too low, using LLM parametric knowledge",
                confidence=0.4,
            ))
        else:
            gen_result = self.llm.generate_answer(query, docs)

        answer = gen_result.get("answer", "No answer generated.")
        citations = gen_result.get("citations", [])
        gen_conf = gen_result.get("confidence", 0.0)

        reflections.append(ReflectionStep(
            step_type="generate",
            input=f"Query: {query}",
            output=f"Answer: {answer[:200]}...",
            confidence=gen_conf,
        ))

        elapsed = (time.perf_counter() - start) * 1000

        return AgenticResponse(
            original_query=query,
            strategy=self.name,
            answer=answer,
            reflections=reflections,
            retrieved_docs=all_docs,
            timing_ms=round(elapsed, 1),
            citations=citations,
        )
