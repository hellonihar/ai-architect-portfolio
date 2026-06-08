import time

from agentic.llm_client import LLMClient
from agentic.strategies.base import BaseAgenticStrategy
from agentic.strategies.multi_hop import MultiHop
from agentic.strategies.self_rag import SelfRAG
from api.schemas import AgenticResponse, ReflectionStep
from retrieval.engine import RetrievalEngine


class AdaptiveRAG(BaseAgenticStrategy):
    def __init__(self, llm: LLMClient, retrieval: RetrievalEngine):
        self.llm = llm
        self.retrieval = retrieval
        self.self_rag = SelfRAG(llm, retrieval)
        self.multi_hop = MultiHop(llm, retrieval)

    @property
    def name(self) -> str:
        return "adaptive_rag"

    def execute(self, query: str, top_k: int = 10, **kwargs) -> AgenticResponse:
        start = time.perf_counter()
        complexity_threshold = kwargs.get("complexity_threshold", 0.7)
        reflections: list[ReflectionStep] = []

        complexity_result = self.llm.classify_complexity(query)
        complexity = complexity_result.get("complexity", "moderate")
        confidence = complexity_result.get("confidence", 0.5)
        explanation = complexity_result.get("explanation", "")

        reflections.append(ReflectionStep(
            step_type="complexity_classification",
            input=f"Query: {query}",
            output=f"Complexity: {complexity}, Explanation: {explanation}",
            confidence=confidence,
            metadata={"complexity": complexity},
        ))

        if complexity == "simple" and confidence >= complexity_threshold:
            gen_result = self.llm.generate_direct(query)
            answer = gen_result.get("answer", "")
            citations = []

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
                timing_ms=round(elapsed, 1),
            )

        elif complexity == "moderate":
            response = self.self_rag.execute(query, top_k=top_k)
            response.strategy = self.name
            response.reflections = reflections + response.reflections
            response.timing_ms = round((time.perf_counter() - start) * 1000, 1)
            return response

        else:
            response = self.multi_hop.execute(query, top_k=top_k)
            response.strategy = self.name
            response.reflections = reflections + response.reflections
            response.timing_ms = round((time.perf_counter() - start) * 1000, 1)
            return response
