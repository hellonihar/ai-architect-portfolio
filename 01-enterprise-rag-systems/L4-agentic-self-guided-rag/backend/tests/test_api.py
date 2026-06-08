from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


class TestHealth:
    def test_health_returns_ok(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "self_rag" in data["strategies"]
        assert data["corpus_size"] > 0


class TestSearch:
    def test_search_requires_query(self):
        resp = client.post("/agentic/search", json={})
        assert resp.status_code == 422

    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_search_returns_response(self, mock_llm):
        mock_llm.return_value = '{"answer": "test answer", "confidence": 0.8}'
        resp = client.post("/agentic/search", json={"query": "What is Kafka?"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["strategy"] == "self_rag"
        assert data["answer"] != ""
        assert "reflections" in data
        assert data["timing_ms"] > 0


class TestCorrect:
    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_correct_returns_response(self, mock_llm):
        mock_llm.side_effect = [
            '{"quality": "high", "confidence": 0.8, "explanation": "good"}',
            '{"answer": "test answer", "citations": [], "confidence": 0.8}',
        ]
        resp = client.post("/agentic/correct", json={"query": "What is Kafka?"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["strategy"] == "corrective_rag"
        assert data["answer"] != ""


class TestAdaptive:
    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_adaptive_returns_response(self, mock_llm):
        mock_llm.return_value = '{"complexity": "moderate", "confidence": 0.8, "explanation": "needs retrieval"}'
        resp = client.post("/agentic/adaptive", json={
            "query": "What is Kafka?", "complexity_threshold": 0.7
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["strategy"] == "adaptive_rag"
        assert data["answer"] != ""


class TestMultihop:
    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_multihop_returns_response(self, mock_llm):
        mock_llm.side_effect = [
            '{"sub_questions": ["What is Kafka?"], "synthesis_instruction": "answer", "explanation": ""}',
            '{"answer": "sub answer", "citations": [], "confidence": 0.8}',
            '{"complete": true, "confidence": 0.9, "follow_up": null}',
            '{"answer": "synthesized answer", "confidence": 0.8}',
        ]
        resp = client.post("/agentic/multihop", json={
            "query": "What is Kafka?", "top_k": 5, "max_hops": 3
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["strategy"] == "multi_hop"
        assert data["answer"] != ""


class TestAuto:
    @patch("agentic.llm_client.LLMClient._call_llm")
    def test_auto_returns_response(self, mock_llm):
        mock_llm.return_value = '{"strategy": "self_rag", "explanation": "best"}'
        resp = client.post("/agentic/auto", json={"query": "What is Kafka?"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["strategy"] == "auto"
        assert data["answer"] != ""
