from unittest.mock import patch

from agentic.engine import AgenticEngine
from retrieval.engine import RetrievalEngine


class TestAgenticEngine:
    def setup_method(self):
        self.retrieval = RetrievalEngine()
        self.engine = AgenticEngine(self.retrieval)

    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_search_returns_agentic_response(self, mock_llm):
        mock_llm.return_value = '{"answer": "test answer", "confidence": 0.8}'
        response = self.engine.search("What is Kafka?")
        assert response.strategy == "self_rag"
        assert "answer" in response.model_dump()
        assert response.timing_ms > 0

    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_correct_returns_agentic_response(self, mock_llm):
        mock_llm.side_effect = [
            '{"quality": "high", "confidence": 0.8, "explanation": "good"}',
            '{"answer": "test answer", "citations": [], "confidence": 0.8}',
        ]
        response = self.engine.correct("What is Kafka?")
        assert response.strategy == "corrective_rag"
        assert "answer" in response.model_dump()

    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_adaptive_returns_agentic_response(self, mock_llm):
        mock_llm.return_value = '{"complexity": "moderate", "confidence": 0.8}'
        response = self.engine.adaptive("What is Kafka?")
        assert response.strategy == "adaptive_rag"
        assert "answer" in response.model_dump()

    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_multihop_returns_agentic_response(self, mock_llm):
        mock_llm.side_effect = [
            '{"sub_questions": ["What is Kafka?"], "synthesis_instruction": "answer"}',
            '{"answer": "sub answer", "citations": [], "confidence": 0.8}',
            '{"complete": true, "follow_up": null}',
            '{"answer": "synthesized answer", "confidence": 0.8}',
        ]
        response = self.engine.multihop("What is Kafka?", top_k=5, max_hops=2)
        assert response.strategy == "multi_hop"
        assert "answer" in response.model_dump()

    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_auto_returns_agentic_response(self, mock_llm):
        mock_llm.return_value = '{"strategy": "self_rag", "explanation": "best"}'
        response = self.engine.auto("What is Kafka?")
        assert response.strategy == "auto"
        assert "answer" in response.model_dump()

    def test_available_strategies(self):
        strategies = self.engine.available_strategies
        assert "self_rag" in strategies
        assert "corrective_rag" in strategies
        assert "adaptive_rag" in strategies
        assert "multi_hop" in strategies
