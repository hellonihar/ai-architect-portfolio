from django.test import TestCase
from apps.indexing.services.retriever import HybridRetriever


class RetrieverTest(TestCase):
    def test_retriever_initialization(self):
        retriever = HybridRetriever()
        self.assertIsNotNone(retriever.embedding_fn)
        self.assertIsNotNone(retriever.pinecone)
