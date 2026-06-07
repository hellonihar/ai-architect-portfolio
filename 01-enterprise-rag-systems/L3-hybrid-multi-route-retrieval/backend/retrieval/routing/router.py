import logging

from retrieval.routing.base import RouterDecision
from retrieval.routing.classifier import ClassifierRouter, QUERY_TYPE_EXPLANATIONS, QUERY_TYPE_ROUTES

logger = logging.getLogger(__name__)


class QueryRouter:
    def __init__(self, classifier: ClassifierRouter):
        self.classifier = classifier

    def route(self, query: str) -> RouterDecision:
        result = self.classifier.classify(query)
        retrievers, fusion = QUERY_TYPE_ROUTES.get(result.query_type, (["dense"], "rrf"))
        return RouterDecision(
            query=query,
            classified_type=result.query_type,
            confidence=result.confidence,
            selected_retrievers=retrievers,
            fusion_method=fusion,
            explanation=result.explanation,
        )
