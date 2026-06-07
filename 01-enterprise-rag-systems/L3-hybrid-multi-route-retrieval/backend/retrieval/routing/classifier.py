import logging
import re

from retrieval.embedder import Embedder
from retrieval.routing.base import BaseClassifier, ClassifierResult

logger = logging.getLogger(__name__)

QUERY_PROTOTYPES: dict[str, list[str]] = {
    "factual": [
        "What is the CAP theorem",
        "Define gradient descent",
        "Explain ACID properties",
        "What is CQRS pattern",
    ],
    "semantic": [
        "How do vector databases compare to traditional databases",
        "Which deep learning techniques work best for images",
        "What are the tradeoffs between REST and gRPC",
        "Compare relational and NoSQL databases",
    ],
    "exploratory": [
        "What are the latest trends in LLM research",
        "Tell me about distributed systems patterns",
        "How can I improve search relevance in RAG",
        "What technologies should I use for a new AI project",
    ],
    "relational": [
        "Which databases work well with LangChain",
        "What technologies does Pinecone integrate with",
        "Which ML frameworks support distributed training",
        "How do embedding models connect to vector databases",
    ],
}

QUERY_TYPE_EXPLANATIONS = {
    "factual": "Factual definition or explanation query — best served by keyword (BM25) precision or dense semantic search",
    "semantic": "Comparative or conceptual query — hybrid search with weighted fusion balances precision and meaning",
    "exploratory": "Broad exploration query — dense vector search captures semantic similarity across diverse topics",
    "relational": "Relationship-oriented query — graph traversal finds entity connections that keyword/semantic search may miss",
}

QUERY_TYPE_ROUTES: dict[str, tuple[list[str], str]] = {
    "factual": (["sparse", "dense"], "rrf"),
    "semantic": (["dense", "sparse"], "weighted"),
    "exploratory": (["dense"], "rrf"),
    "relational": (["graph", "dense"], "rrf"),
}


class EmbeddingClassifier(BaseClassifier):
    def __init__(self, embedder: Embedder):
        self.embedder = embedder
        self.prototypes: dict[str, list[list[float]]] = {}
        for qtype, examples in QUERY_PROTOTYPES.items():
            self.prototypes[qtype] = embedder.encode(examples)

    def classify(self, query: str) -> ClassifierResult:
        query_emb = self.embedder.encode_single(query)
        best_type = "semantic"
        best_score = -1.0
        for qtype, proto_embs in self.prototypes.items():
            for proto_emb in proto_embs:
                score = sum(a * b for a, b in zip(query_emb, proto_emb))
                if score > best_score:
                    best_score = score
                    best_type = qtype
        return ClassifierResult(
            query_type=best_type,
            confidence=float(best_score),
            explanation=QUERY_TYPE_EXPLANATIONS.get(best_type, ""),
        )


class LLMClassifier(BaseClassifier):
    def __init__(self, groq_client=None, model: str = "qwen/qwen3-32b"):
        self.client = groq_client
        self.model = model

    def classify(self, query: str) -> ClassifierResult | None:
        if not self.client:
            return None
        try:
            prompt = f"""Classify this query into one of these types and explain why:
- factual: asking for definition, explanation, or fact about a specific concept
- semantic: comparing concepts, asking about relationships between ideas
- exploratory: broad open-ended exploration or trend discovery
- relational: asking about connections between specific technologies, tools, or entities

Query: {query}

Respond with JSON: {{"type": "<type>", "confidence": <0.0-1.0>, "explanation": "<brief reason>"}}"""
            response = self.client.invoke(prompt)
            text = response.content.strip()
            import json
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                data = json.loads(match.group())
                return ClassifierResult(
                    query_type=data.get("type", "semantic"),
                    confidence=float(data.get("confidence", 0.5)),
                    explanation=data.get("explanation", QUERY_TYPE_EXPLANATIONS.get(data.get("type", "semantic"), "")),
                )
        except Exception as e:
            logger.warning("LLM classification failed: %s", e)
        return None


class ClassifierRouter:
    def __init__(self, embedder: Embedder, groq_client=None):
        self.llm = LLMClassifier(groq_client)
        self.embed = EmbeddingClassifier(embedder)

    def classify(self, query: str) -> ClassifierResult:
        llm_result = self.llm.classify(query)
        if llm_result and llm_result.confidence > 0.3:
            return llm_result
        embed_result = self.embed.classify(query)
        return embed_result
