from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


class TestHealth:
    def test_health_returns_ok(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "query_rewriter" in data["strategies"]


class TestRefine:
    def test_refine_requires_query(self):
        resp = client.post("/refine", json={})
        assert resp.status_code == 422

    def test_refine_invalid_strategy(self):
        resp = client.post("/refine", json={"query": "hello", "strategy": "invalid"})
        assert resp.status_code == 500

    def test_refine_query_rewriter(self, mocker):
        mock = mocker.patch("refinery.engine.QueryRewriter.refine")
        mock.return_value.refined_queries = ["refined query"]
        mock.return_value.strategy = "query_rewriter"
        mock.return_value.explanation = "Rewritten"
        mock.return_value.metadata = {}

        resp = client.post("/refine", json={"query": "test", "strategy": "query_rewriter"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["refined_queries"] == ["refined query"]
        assert data["strategy"] == "query_rewriter"

    def test_refine_with_conversation_history(self, mocker):
        mock = mocker.patch("refinery.engine.QueryRewriter.refine")
        mock.return_value.refined_queries = ["refined with history"]
        mock.return_value.strategy = "query_rewriter"
        mock.return_value.explanation = "Used history"
        mock.return_value.metadata = {"used_history": True}

        resp = client.post(
            "/refine",
            json={"query": "test", "strategy": "query_rewriter", "conversation_history": ["previous"]},
        )
        assert resp.status_code == 200
        assert resp.json()["refined_queries"] == ["refined with history"]


class TestAutoRefine:
    def test_auto_refine_returns_refined_query(self, mocker):
        mock_engine = mocker.patch("refinery.engine.RefineryEngine.auto_refine")
        mock_engine.return_value = {
            "original_query": "test",
            "refined_queries": ["auto refined"],
            "strategy": "query_rewriter",
            "explanation": "Auto-selected: query_rewriter",
            "metadata": {"auto_classification": "query_rewriter"},
        }

        resp = client.post("/auto-refine", json={"query": "test"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["refined_queries"] == ["auto refined"]
        assert "auto_classification" in data["metadata"]


class TestEvaluate:
    def test_evaluate_returns_scores(self, mocker):
        mock_engine = mocker.patch("refinery.engine.RefineryEngine.evaluate")
        mock_engine.return_value = {
            "original_query": "test",
            "raw_queries": ["test"],
            "refined_queries": ["refined"],
            "strategy": "query_rewriter",
            "scores": [
                {"criterion": "Clarity", "raw_score": 5, "refined_score": 8, "explanation": "more specific"},
            ],
        }

        resp = client.post("/evaluate", json={"query": "test", "strategy": "query_rewriter"})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["scores"]) == 1
        assert data["scores"][0]["criterion"] == "Clarity"
        assert data["scores"][0]["refined_score"] == 8
