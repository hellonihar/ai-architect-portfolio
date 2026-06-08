from unittest.mock import patch

from agentic.strategies.adaptive_rag import AdaptiveRAG
from agentic.strategies.corrective_rag import CorrectiveRAG
from agentic.strategies.multi_hop import MultiHop
from agentic.strategies.self_rag import SelfRAG
from agentic.llm_client import LLMClient
from retrieval.engine import RetrievalEngine


class TestSelfRAG:
    def setup_method(self):
        self.retrieval = RetrievalEngine()
        self.llm = LLMClient()
        self.strategy = SelfRAG(self.llm, self.retrieval)

    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_execute_returns_response(self, mock_llm):
        mock_llm.return_value = '{"answer": "test answer", "citations": [], "confidence": 0.8}'
        response = self.strategy.execute("What is Kafka?")
        assert response.strategy == "self_rag"
        assert "answer" in response.model_dump()

    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_execute_without_retrieval(self, mock_llm):
        mock_llm.return_value = '{"answer": "direct answer", "confidence": 0.8}'
        response = self.strategy.execute("Say hello")
        assert response.strategy == "self_rag"


class TestCorrectiveRAG:
    def setup_method(self):
        self.retrieval = RetrievalEngine()
        self.llm = LLMClient()
        self.strategy = CorrectiveRAG(self.llm, self.retrieval)

    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_execute_returns_response(self, mock_llm):
        mock_llm.side_effect = [
            '{"quality": "high", "confidence": 0.8, "explanation": "good"}',
            '{"answer": "test answer", "citations": [], "confidence": 0.8}',
        ]
        response = self.strategy.execute("What is Kafka?")
        assert response.strategy == "corrective_rag"
        assert "answer" in response.model_dump()


class TestAdaptiveRAG:
    def setup_method(self):
        self.retrieval = RetrievalEngine()
        self.llm = LLMClient()
        self.strategy = AdaptiveRAG(self.llm, self.retrieval)

    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_execute_simple(self, mock_llm):
        mock_llm.return_value = '{"complexity": "simple", "confidence": 0.9, "explanation": "simple query"}'
        response = self.strategy.execute("Say hello", top_k=10, complexity_threshold=0.7)
        assert response.strategy == "adaptive_rag"
        assert "answer" in response.model_dump()

    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_execute_moderate(self, mock_llm):
        mock_llm.return_value = '{"complexity": "moderate", "confidence": 0.8, "explanation": "moderate"}'
        response = self.strategy.execute("What is Kafka?")
        assert response.strategy == "adaptive_rag"
        assert "answer" in response.model_dump()


class TestMultiHop:
    def setup_method(self):
        self.retrieval = RetrievalEngine()
        self.llm = LLMClient()
        self.strategy = MultiHop(self.llm, self.retrieval)

    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_execute_returns_response(self, mock_llm):
        mock_llm.side_effect = [
            '{"sub_questions": ["What is Kafka?"], "synthesis_instruction": "answer"}',
            '{"answer": "sub answer", "citations": [], "confidence": 0.8}',
            '{"complete": true, "follow_up": null}',
            '{"answer": "synthesized answer", "confidence": 0.8}',
        ]
        response = self.strategy.execute("What is Kafka?", top_k=5, max_hops=2)
        assert response.strategy == "multi_hop"
        assert "answer" in response.model_dump()
