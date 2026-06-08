WEB_DOCUMENTS = [
    {
        "id": "web-01",
        "content": "Retrieval-Augmented Generation (RAG) is a popular technique that combines retrieval from external knowledge sources with LLM generation. The latest research has focused on agentic RAG where the LLM actively controls the retrieval process, including deciding when to retrieve, evaluating retrieved content quality, and performing multiple retrieval steps.",
        "source": "web",
        "url": "https://arxiv.org/abs/2501.00001",
    },
    {
        "id": "web-02",
        "content": "Self-RAG introduces reflection tokens that allow the LLM to explicitly reason about whether retrieval is needed and whether retrieved passages are relevant. The model is trained to output special tokens indicating retrieval decisions, relevance judgments, and citation support. This approach significantly reduces hallucination compared to standard RAG.",
        "source": "web",
        "url": "https://arxiv.org/abs/2310.11511",
    },
    {
        "id": "web-03",
        "content": "Corrective RAG (CRAG) adds a retrieval evaluator that scores the quality of retrieved documents. If quality is low, the system triggers a query rewriting step to re-retrieve. If quality is very low, it falls back to the LLM's parametric knowledge. CRAG has been shown to improve answer accuracy by 10-15% on knowledge-intensive tasks.",
        "source": "web",
        "url": "https://arxiv.org/abs/2401.15884",
    },
    {
        "id": "web-04",
        "content": "Adaptive RAG dynamically selects the retrieval strategy based on query complexity. Simple queries are answered directly by the LLM without retrieval, moderate queries use standard single-step RAG, and complex queries use multi-step reasoning with iterative retrieval. This reduces latency on simple queries while maintaining accuracy on complex ones.",
        "source": "web",
        "url": "https://arxiv.org/abs/2403.14403",
    },
    {
        "id": "web-05",
        "content": "Multi-hop RAG decomposes complex questions into simpler sub-questions and retrieves relevant information for each sub-question iteratively. The answers to sub-questions are then synthesized into a final comprehensive answer. This approach is particularly effective for questions that require connecting information across multiple documents.",
        "source": "web",
        "url": "https://arxiv.org/abs/2401.05861",
    },
    {
        "id": "web-06",
        "content": "Recent benchmarks show that agentic RAG approaches outperform standard RAG by 15-25% on multi-hop reasoning tasks. However, they introduce additional latency due to multiple LLM calls. Optimizations like parallel sub-question answering and caching reflection decisions are active areas of research.",
        "source": "web",
        "url": "https://arxiv.org/abs/2404.12345",
    },
    {
        "id": "web-07",
        "content": "Mixture of Agents (MoA) is a technique that leverages multiple LLMs in concert, where each agent specializes in a different aspect of the reasoning process. Applied to RAG, this can mean separate agents for retrieval decision, relevance checking, citation verification, and final generation.",
        "source": "web",
        "url": "https://arxiv.org/abs/2406.04692",
    },
    {
        "id": "web-08",
        "content": "Knowledge graphs combined with RAG (GraphRAG) use entity extraction and community detection to create structured knowledge representations from unstructured text. This enables multi-hop reasoning through graph traversal alongside traditional vector search for comprehensive question answering.",
        "source": "web",
        "url": "https://arxiv.org/abs/2404.16130",
    },
]


def get_web_documents():
    return WEB_DOCUMENTS
