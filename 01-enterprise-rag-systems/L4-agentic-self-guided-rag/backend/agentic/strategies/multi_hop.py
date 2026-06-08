import time

from agentic.llm_client import LLMClient
from agentic.strategies.base import BaseAgenticStrategy
from api.schemas import AgenticResponse, Document, ReflectionStep
from retrieval.engine import RetrievalEngine


class MultiHop(BaseAgenticStrategy):
    def __init__(self, llm: LLMClient, retrieval: RetrievalEngine):
        self.llm = llm
        self.retrieval = retrieval

    @property
    def name(self) -> str:
        return "multi_hop"

    def execute(self, query: str, top_k: int = 10, **kwargs) -> AgenticResponse:
        start = time.perf_counter()
        max_hops = kwargs.get("max_hops", 3)
        reflections: list[ReflectionStep] = []
        all_docs: list[Document] = []
        sub_answers: list[dict] = []

        decomposition = self.llm.decompose_query(query)
        sub_questions = decomposition.get("sub_questions", [query])
        synthesis_instruction = decomposition.get("synthesis_instruction", "")
        decomposition_explanation = decomposition.get("explanation", "")

        reflections.append(ReflectionStep(
            step_type="decompose",
            input=f"Query: {query}",
            output=f"Sub-questions: {sub_questions}\nSynthesis: {synthesis_instruction}",
            confidence=0.7,
            metadata={"sub_questions": sub_questions, "explanation": decomposition_explanation},
        ))

        for i, sub_q in enumerate(sub_questions[:max_hops]):
            docs, _ = self.retrieval.search(sub_q, retriever_name="hybrid", top_k=top_k)
            all_docs.extend(docs)

            reflections.append(ReflectionStep(
                step_type="retrieve",
                input=f"Sub-question [{i+1}]: {sub_q}",
                output=f"Retrieved {len(docs)} documents",
                confidence=0.7,
                metadata={"hop": i + 1, "doc_ids": [d.id for d in docs]},
            ))

            gen_result = self.llm.generate_answer(sub_q, docs)
            answer = gen_result.get("answer", "")
            conf = gen_result.get("confidence", 0.0)

            sub_answers.append({
                "question": sub_q,
                "answer": answer,
                "confidence": conf,
            })

            completeness = self.llm.reflect_completeness(sub_q, answer)
            is_complete = completeness.get("complete", True)

            reflections.append(ReflectionStep(
                step_type="reflect_completeness",
                input=f"Sub-question [{i+1}]: {sub_q}\nAnswer: {answer[:200]}...",
                output=f"Complete: {is_complete}, Follow-up: {completeness.get('follow_up', 'None')}",
                confidence=completeness.get("confidence", 0.5),
                metadata={"hop": i + 1, "complete": is_complete},
            ))

            follow_up = completeness.get("follow_up")
            if not is_complete and follow_up and i < max_hops - 1:
                next_questions = [follow_up]
                sub_questions = sub_questions[:i+1] + next_questions + sub_questions[i+1:]
                if len(sub_questions) > max_hops:
                    sub_questions = sub_questions[:max_hops]

        synthesis = self.llm.synthesize_answers(query, sub_answers)

        reflections.append(ReflectionStep(
            step_type="synthesize",
            input=f"Original query: {query}\nSub-answers: {len(sub_answers)}",
            output=f"Synthesis: {synthesis[:200]}...",
            confidence=0.7,
        ))

        elapsed = (time.perf_counter() - start) * 1000

        doc_ids = list(set(d.id for d in all_docs))

        return AgenticResponse(
            original_query=query,
            strategy=self.name,
            answer=synthesis,
            reflections=reflections,
            retrieved_docs=list({d.id: d for d in all_docs}.values()),
            timing_ms=round(elapsed, 1),
            citations=doc_ids,
        )
