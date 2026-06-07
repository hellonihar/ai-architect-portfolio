from refinery.strategies.base import RefinementResult, BaseStrategy
from refinery.strategies.query_rewriter import QueryRewriter
from refinery.strategies.hyde import HyDE
from refinery.strategies.multi_query import MultiQuery
from refinery.strategies.query_decomposer import QueryDecomposer


class TestQueryRewriter:
    def test_refine_returns_refinement_result(self, mocker):
        mock_llm = mocker.patch("refinery.strategies.query_rewriter.GroqClient")
        mock_llm.return_value.generate.return_value = "What were the Q3 2025 financial results?"

        strategy = QueryRewriter()
        result = strategy.refine("what about the results", conversation_history=["How did Q3 go?"])

        assert isinstance(result, RefinementResult)
        assert len(result.refined_queries) == 1
        assert result.refined_queries[0] == "What were the Q3 2025 financial results?"
        assert result.strategy == "query_rewriter"
        assert result.explanation is not None

    def test_refine_no_history(self, mocker):
        mock_llm = mocker.patch("refinery.strategies.query_rewriter.GroqClient")
        mock_llm.return_value.generate.return_value = "Show me the monthly active users."

        strategy = QueryRewriter()
        result = strategy.refine("show me mau")

        assert len(result.refined_queries) == 1
        assert result.metadata["used_history"] is False


class TestHyDE:
    def test_refine_returns_hypothetical_doc_and_embedding(self, mocker):
        mock_llm = mocker.patch("refinery.strategies.hyde.GroqClient")
        mock_llm.return_value.generate.return_value = "A hypothetical document about machine learning."

        mock_embed = mocker.patch("refinery.strategies.hyde.Embedder")
        mock_embed.return_value.embed.return_value = [0.1, 0.2, 0.3]

        strategy = HyDE()
        result = strategy.refine("What is machine learning?")

        assert isinstance(result, RefinementResult)
        assert len(result.refined_queries) == 1
        assert "machine learning" in result.refined_queries[0].lower()
        assert result.strategy == "hyde"
        assert "embedding" in result.metadata
        assert result.metadata["embedding_dimension"] == 3

    def test_refine_embedding_dimensions(self, mocker):
        mock_llm = mocker.patch("refinery.strategies.hyde.GroqClient")
        mock_llm.return_value.generate.return_value = "Document about AI."

        mock_embed = mocker.patch("refinery.strategies.hyde.Embedder")
        mock_embed.return_value.embed.return_value = [0.5] * 384

        strategy = HyDE()
        result = strategy.refine("Tell me about AI")

        assert result.metadata["embedding_dimension"] == 384
        assert len(result.metadata["embedding"]) == 384


class TestMultiQuery:
    def test_refine_returns_multiple_variants(self, mocker):
        mock_llm = mocker.patch("refinery.strategies.multi_query.GroqClient")
        mock_llm.return_value.generate.return_value = (
            "RAG architecture best practices\n"
            "How to implement retrieval augmented generation\n"
            "RAG system design patterns"
        )

        strategy = MultiQuery()
        result = strategy.refine("RAG best practices")

        assert isinstance(result, RefinementResult)
        assert len(result.refined_queries) >= 3
        assert result.strategy == "multi_query"
        assert "num_variants" in result.metadata

    def test_refine_includes_original_query(self, mocker):
        mock_llm = mocker.patch("refinery.strategies.multi_query.GroqClient")
        mock_llm.return_value.generate.return_value = "Variant one\nVariant two"

        strategy = MultiQuery()
        result = strategy.refine("original query")

        assert result.refined_queries[0] == "original query"


class TestQueryDecomposer:
    def test_refine_splits_compound_query(self, mocker):
        mock_llm = mocker.patch("refinery.strategies.query_decomposer.GroqClient")
        mock_llm.return_value.generate.return_value = (
            "What were Q3 2025 sales?\n"
            "Who leads the engineering team?"
        )

        strategy = QueryDecomposer()
        result = strategy.refine("What are Q3 sales and who leads the engineering team?")

        assert isinstance(result, RefinementResult)
        assert len(result.refined_queries) == 2
        assert "sales" in result.refined_queries[0].lower()
        assert "engineering" in result.refined_queries[1].lower()
        assert result.strategy == "query_decomposer"

    def test_refine_atomic_query(self, mocker):
        mock_llm = mocker.patch("refinery.strategies.query_decomposer.GroqClient")
        mock_llm.return_value.generate.return_value = "What is the capital of France?"

        strategy = QueryDecomposer()
        result = strategy.refine("What is the capital of France?")

        assert len(result.refined_queries) == 1
        assert "capital" in result.refined_queries[0].lower()


class TestRefinementResult:
    def test_default_metadata_is_empty_dict(self):
        result = RefinementResult(refined_queries=["test"], strategy="test")
        assert result.metadata == {}

    def test_custom_metadata(self):
        result = RefinementResult(
            refined_queries=["test"],
            strategy="test",
            metadata={"key": "value"},
        )
        assert result.metadata["key"] == "value"
