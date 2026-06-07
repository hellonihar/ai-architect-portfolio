import pytest

from refinery.strategies.query_rewriter import QueryRewriter
from refinery.strategies.hyde import HyDE
from refinery.strategies.multi_query import MultiQuery
from refinery.strategies.query_decomposer import QueryDecomposer


class TestRefineryEngine:
    def test_strategies_registered(self):
        from refinery.engine import RefineryEngine

        engine = RefineryEngine()
        assert "query_rewriter" in engine.strategies
        assert "hyde" in engine.strategies
        assert "multi_query" in engine.strategies
        assert "query_decomposer" in engine.strategies
        assert isinstance(engine.strategies["query_rewriter"], QueryRewriter)
        assert isinstance(engine.strategies["hyde"], HyDE)
        assert isinstance(engine.strategies["multi_query"], MultiQuery)
        assert isinstance(engine.strategies["query_decomposer"], QueryDecomposer)

    def test_refine_routes_to_correct_strategy(self, mocker):
        from refinery.engine import RefineryEngine

        mock = mocker.patch("refinery.strategies.query_rewriter.GroqClient")
        mock.return_value.generate.return_value = "rewritten query"

        engine = RefineryEngine()
        result = engine.refine("test", strategy="query_rewriter")

        assert result["strategy"] == "query_rewriter"
        assert result["refined_queries"] == ["rewritten query"]
        assert result["original_query"] == "test"

    def test_auto_refine_classifies_and_runs(self, mocker):
        from refinery.engine import RefineryEngine

        mock_llm = mocker.patch("refinery.engine.GroqClient")
        mock_llm.return_value.generate.return_value = "query_rewriter"

        mock = mocker.patch("refinery.strategies.query_rewriter.GroqClient")
        mock.return_value.generate.return_value = "auto rewritten query"

        engine = RefineryEngine()
        result = engine.auto_refine("some ambiguous query")

        assert result["strategy"] == "query_rewriter"
        assert result["refined_queries"] == ["auto rewritten query"]
        assert "auto_classification" in result["metadata"]

    def test_auto_refine_falls_back_on_bad_classification(self, mocker):
        from refinery.engine import RefineryEngine

        mock_llm = mocker.patch("refinery.engine.GroqClient")
        mock_llm.return_value.generate.return_value = "nonexistent_strategy"

        mock = mocker.patch("refinery.strategies.query_rewriter.GroqClient")
        mock.return_value.generate.return_value = "fallback rewritten"

        engine = RefineryEngine()
        result = engine.auto_refine("test")

        assert result["strategy"] == "query_rewriter"

    def test_parse_evaluation(self):
        from refinery.engine import RefineryEngine

        engine = RefineryEngine()
        text = (
            "Clarity: raw=5 refined=8 — more specific\n"
            "Specificity: raw=4 refined=9 — adds details\n"
            "Search-readiness: raw=6 refined=8 — better keywords"
        )
        scores = engine._parse_evaluation(text)

        assert len(scores) == 3
        assert scores[0].criterion == "Clarity"
        assert scores[0].raw_score == 5
        assert scores[0].refined_score == 8
        assert scores[1].criterion == "Specificity"
        assert scores[2].criterion == "Search-readiness"

    def test_parse_evaluation_handles_malformed_lines(self):
        from refinery.engine import RefineryEngine

        engine = RefineryEngine()
        text = "Clarity: raw=X refined=Y — broken\nSpecificity: raw=4 refined=9 — good"
        scores = engine._parse_evaluation(text)

        assert len(scores) == 1
        assert scores[0].criterion == "Specificity"
