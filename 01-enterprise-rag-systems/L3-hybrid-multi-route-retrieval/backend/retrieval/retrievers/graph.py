import logging
import re

import networkx as nx

from retrieval.retrievers.base import BaseRetriever

logger = logging.getLogger(__name__)


class GraphRetriever(BaseRetriever):
    def __init__(self, documents: list[dict], entity_map: dict[str, list[str]]):
        self.documents = documents
        self.entity_map = entity_map
        self.graph = nx.Graph()
        self._build_graph()

    def _build_graph(self):
        doc_by_id = {d["id"]: d for d in self.documents}
        for doc in self.documents:
            self.graph.add_node(doc["id"], type="document", content=doc["content"], category=doc.get("category", ""))
            for entity in doc.get("entities", []):
                entity_node = f"entity:{entity}"
                if not self.graph.has_node(entity_node):
                    self.graph.add_node(entity_node, type="entity", name=entity)
                self.graph.add_edge(doc["id"], entity_node, relation="mentions")
        for cat, entities in self.entity_map.items():
            for e1 in entities:
                for e2 in entities:
                    if e1 < e2:
                        n1 = f"entity:{e1}"
                        n2 = f"entity:{e2}"
                        if self.graph.has_node(n1) and self.graph.has_node(n2):
                            self.graph.add_edge(n1, n2, relation="same_category")
        logger.info("Graph built: %d nodes, %d edges", self.graph.number_of_nodes(), self.graph.number_of_edges())

    @property
    def num_nodes(self) -> int:
        return self.graph.number_of_nodes()

    @property
    def num_edges(self) -> int:
        return self.graph.number_of_edges()

    def retrieve(self, query: str, top_k: int = 10) -> list[dict]:
        matched_entities = []
        for entity_name in self._collect_all_entities():
            if entity_name.lower() in query.lower():
                matched_entities.append(entity_name)
        if not matched_entities:
            logger.info("No entities matched in query")
            return []
        matched_doc_ids: set[str] = set()
        for entity_name in matched_entities:
            entity_node = f"entity:{entity_name}"
            if not self.graph.has_node(entity_node):
                continue
            for neighbor in self.graph.neighbors(entity_node):
                if self.graph.nodes[neighbor].get("type") == "document":
                    matched_doc_ids.add(neighbor)
            for neighbor in self.graph.neighbors(entity_node):
                if self.graph.nodes[neighbor].get("type") == "entity":
                    for second_neighbor in self.graph.neighbors(neighbor):
                        if self.graph.nodes[second_neighbor].get("type") == "document":
                            matched_doc_ids.add(second_neighbor)
        scored = []
        for doc_id in matched_doc_ids:
            doc = self.documents_by_id().get(doc_id)
            if doc:
                overlap = sum(1 for e in doc.get("entities", []) if e.lower() in query.lower())
                scored.append({
                    "id": doc["id"],
                    "content": doc["content"],
                    "score": overlap / max(len(doc.get("entities", [])), 1),
                    "route": "graph",
                    "metadata": {
                        "category": doc.get("category", ""),
                        "matched_entities": matched_entities,
                        "entity_overlap": overlap,
                    },
                })
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def _collect_all_entities(self) -> list[str]:
        seen: set[str] = set()
        for doc in self.documents:
            for e in doc.get("entities", []):
                seen.add(e)
        return sorted(seen)

    def documents_by_id(self) -> dict[str, dict]:
        return {d["id"]: d for d in self.documents}
