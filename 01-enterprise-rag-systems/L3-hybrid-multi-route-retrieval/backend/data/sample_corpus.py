CATEGORIES = {
    "architecture": {
        "label": "Software Architecture",
        "entities": ["Microservices", "Event-Driven Architecture", "CQRS", "Event Sourcing", "Hexagonal Architecture", "Clean Architecture", "Domain-Driven Design", "REST", "gRPC", "Message Queue"],
    },
    "machine_learning": {
        "label": "Machine Learning",
        "entities": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Random Forest", "XGBoost", "Neural Networks", "CNN", "RNN", "Transformer", "Gradient Descent", "Backpropagation", "Overfitting", "Regularization", "Cross-Validation"],
    },
    "llm": {
        "label": "Large Language Models",
        "entities": ["GPT", "BERT", "T5", "Llama", "Qwen", "Attention Mechanism", "Self-Attention", "Fine-Tuning", "RLHF", "Prompt Engineering", "RAG", "Chain-of-Thought", "Tokenization", "Embedding", "Vector Database"],
    },
    "databases": {
        "label": "Databases & Storage",
        "entities": ["PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "Pinecone", "ChromaDB", "Neo4j", "Cassandra", "ACID", "BASE", "Indexing", "Sharding", "Replication", "CAP Theorem"],
    },
}

DOCUMENTS = [
    # === Architecture (13 chunks) ===
    {
        "id": "arch-01", "category": "architecture",
        "content": "Microservices decompose applications into small independently deployable services. Each service owns its data and communicates via well-defined APIs, typically REST or gRPC. This improves scalability, fault isolation, and team autonomy but introduces complexity in distributed systems coordination.",
        "entities": {"Microservices", "REST", "gRPC"},
    },
    {
        "id": "arch-02", "category": "architecture",
        "content": "Event-Driven Architecture enables services to communicate asynchronously through events. Producers emit events without knowledge of consumers. Message queues like Kafka or RabbitMQ decouple services, improving resilience and allowing independent scaling of producers and consumers.",
        "entities": {"Event-Driven Architecture", "Message Queue"},
    },
    {
        "id": "arch-03", "category": "architecture",
        "content": "CQRS separates read and write operations into distinct models. Commands handle writes with validation and business logic, while queries read data through optimized projections. This allows each side to scale independently and use storage formats suited to its needs.",
        "entities": {"CQRS"},
    },
    {
        "id": "arch-04", "category": "architecture",
        "content": "Event Sourcing stores state changes as an ordered sequence of events rather than current state. The current state is derived by replaying events. This provides a complete audit trail, enables temporal queries, and supports rebuilding state from scratch.",
        "entities": {"Event Sourcing"},
    },
    {
        "id": "arch-05", "category": "architecture",
        "content": "Hexagonal Architecture structures applications around a core domain with ports and adapters. The domain is isolated from external concerns like databases, UI, or APIs. Adapters translate between the domain and external systems, making the core testable and framework-independent.",
        "entities": {"Hexagonal Architecture"},
    },
    {
        "id": "arch-06", "category": "architecture",
        "content": "Clean Architecture enforces dependency inversion where inner layers (entities, use cases) have no dependency on outer layers (frameworks, databases, UI). This creates a system that is independent of frameworks, testable, and adaptable to changing infrastructure.",
        "entities": {"Clean Architecture"},
    },
    {
        "id": "arch-07", "category": "architecture",
        "content": "Domain-Driven Design focuses on modeling software around business domains. It introduces concepts like bounded contexts, entities, value objects, aggregates, and domain events. DDD helps align software design with business strategy and evolves with domain understanding.",
        "entities": {"Domain-Driven Design"},
    },
    {
        "id": "arch-08", "category": "architecture",
        "content": "REST APIs use HTTP methods (GET, POST, PUT, DELETE) to operate on resources identified by URLs. Statelessness, uniform interface, and HATEOAS are key constraints. REST is widely adopted for its simplicity and compatibility with web infrastructure.",
        "entities": {"REST"},
    },
    {
        "id": "arch-09", "category": "architecture",
        "content": "gRPC is a high-performance RPC framework using Protocol Buffers for serialization and HTTP/2 for transport. It supports bi-directional streaming, strong typing through .proto files, and auto-generated client/server stubs. Used heavily in microservice environments.",
        "entities": {"gRPC"},
    },
    {
        "id": "arch-10", "category": "architecture",
        "content": "Message queues provide asynchronous communication between services. Producers send messages to a queue, consumers process them independently. This decouples services, buffers spikes in load, and provides reliability through message persistence and retry mechanisms.",
        "entities": {"Message Queue"},
    },
    {
        "id": "arch-11", "category": "architecture",
        "content": "API Gateway is a single entry point for microservices that handles request routing, authentication, rate limiting, and protocol translation. It simplifies client interactions by aggregating multiple service calls into one and enforces cross-cutting security policies.",
        "entities": {"Microservices", "REST"},
    },
    {
        "id": "arch-12", "category": "architecture",
        "content": "Service mesh abstracts inter-service communication into a dedicated infrastructure layer. Sidecar proxies handle service discovery, load balancing, encryption, and observability. Istio and Linkerd are popular implementations. Teams manage communication policies centrally.",
        "entities": {"Microservices"},
    },
    {
        "id": "arch-13", "category": "architecture",
        "content": "Saga pattern manages distributed transactions in microservices by breaking them into a sequence of local transactions. Each step publishes an event triggering the next step. Compensating transactions undo changes if a step fails, ensuring eventual consistency.",
        "entities": {"Microservices", "Event-Driven Architecture"},
    },

    # === Machine Learning (13 chunks) ===
    {
        "id": "ml-01", "category": "machine_learning",
        "content": "Supervised Learning trains models on labeled data where each input has a known output. Common tasks include classification and regression. Algorithms like linear regression, random forests, and neural networks learn patterns from training data and generalize to unseen examples.",
        "entities": {"Supervised Learning", "Random Forest", "Neural Networks"},
    },
    {
        "id": "ml-02", "category": "machine_learning",
        "content": "Unsupervised Learning finds patterns in unlabeled data. Clustering groups similar instances, dimensionality reduction compresses features, and association rules discover relationships. K-means, DBSCAN, PCA, and t-SNE are widely used unsupervised techniques.",
        "entities": {"Unsupervised Learning"},
    },
    {
        "id": "ml-03", "category": "machine_learning",
        "content": "Reinforcement Learning trains agents to make sequential decisions by maximizing cumulative reward. The agent explores an environment, takes actions, and receives feedback. Q-learning, Deep Q-Networks, and policy gradients are foundational RL algorithms.",
        "entities": {"Reinforcement Learning"},
    },
    {
        "id": "ml-04", "category": "machine_learning",
        "content": "Random Forest is an ensemble method combining many decision trees. Each tree trains on a bootstrap sample and considers random feature subsets. Predictions aggregate via voting or averaging. It handles non-linearity, resists overfitting, and provides feature importance.",
        "entities": {"Random Forest"},
    },
    {
        "id": "ml-05", "category": "machine_learning",
        "content": "XGBoost is a gradient-boosted tree framework optimized for speed and performance. It uses regularization, parallel processing, and tree pruning. XGBoost dominates tabular data competitions and is widely deployed in production for classification and regression tasks.",
        "entities": {"XGBoost"},
    },
    {
        "id": "ml-06", "category": "machine_learning",
        "content": "Neural Networks consist of layers of interconnected neurons that learn hierarchical representations. Deep networks with many hidden layers can model complex functions. Activation functions like ReLU, sigmoid, and tanh introduce non-linearity into the network.",
        "entities": {"Neural Networks"},
    },
    {
        "id": "ml-07", "category": "machine_learning",
        "content": "Convolutional Neural Networks use convolution operations to process grid-structured data like images. Filters slide over inputs detecting local patterns. Pooling reduces dimensionality. CNNs achieved breakthroughs in computer vision for classification, detection, and segmentation.",
        "entities": {"CNN", "Neural Networks"},
    },
    {
        "id": "ml-08", "category": "machine_learning",
        "content": "Recurrent Neural Networks process sequential data by maintaining a hidden state that captures information from previous steps. They are used for time series, natural language, and speech. LSTMs and GRUs address the vanishing gradient problem in long sequences.",
        "entities": {"RNN", "Neural Networks"},
    },
    {
        "id": "ml-09", "category": "machine_learning",
        "content": "Gradient Descent iteratively minimizes a loss function by moving parameters in the direction of steepest descent. Variants include stochastic, mini-batch, and Adam. Learning rate scheduling and momentum help convergence. It is the backbone of neural network training.",
        "entities": {"Gradient Descent", "Neural Networks"},
    },
    {
        "id": "ml-10", "category": "machine_learning",
        "content": "Backpropagation computes gradients of the loss with respect to network weights using the chain rule. It propagates error backward from output to input, updating weights to reduce error. It enables training of multi-layer neural networks effectively.",
        "entities": {"Backpropagation", "Neural Networks"},
    },
    {
        "id": "ml-11", "category": "machine_learning",
        "content": "Overfitting occurs when a model learns training data noise instead of underlying patterns. Symptoms include high training accuracy but poor test performance. Regularization, dropout, early stopping, and cross-validation are common countermeasures.",
        "entities": {"Overfitting", "Regularization", "Cross-Validation"},
    },
    {
        "id": "ml-12", "category": "machine_learning",
        "content": "Regularization techniques prevent overfitting by adding constraints to the model. L1 regularization (Lasso) drives weights to zero performing feature selection. L2 regularization (Ridge) shrinks weights uniformly. Dropout randomly deactivates neurons during training.",
        "entities": {"Regularization", "Overfitting"},
    },
    {
        "id": "ml-13", "category": "machine_learning",
        "content": "Cross-Validation assesses model generalization by partitioning data into folds. K-fold CV trains on k-1 folds and validates on the held-out fold, rotating k times. Stratified folds preserve class proportions. It provides robust performance estimates with lower variance.",
        "entities": {"Cross-Validation"},
    },

    # === LLM (14 chunks) ===
    {
        "id": "llm-01", "category": "llm",
        "content": "GPT (Generative Pre-trained Transformer) is an autoregressive language model using the Transformer decoder architecture. It predicts the next token given previous tokens. GPT-4 and GPT-4o demonstrate strong few-shot reasoning, code generation, and instruction following.",
        "entities": {"GPT", "Transformer", "Attention Mechanism"},
    },
    {
        "id": "llm-02", "category": "llm",
        "content": "BERT (Bidirectional Encoder Representations from Transformers) uses masked language modeling to pre-train deep bidirectional representations. It captures context from both directions making it excellent for understanding tasks like classification, NER, and QA.",
        "entities": {"BERT", "Transformer", "Attention Mechanism"},
    },
    {
        "id": "llm-03", "category": "llm",
        "content": "T5 (Text-to-Text Transfer Transformer) casts every NLP task into a text-to-text format. Using encoder-decoder architecture, it unifies tasks like translation, summarization, QA, and classification into a single framework with task-specific prefixes.",
        "entities": {"T5", "Transformer"},
    },
    {
        "id": "llm-04", "category": "llm",
        "content": "Llama is Meta's open-source LLM family. Llama 3 and 3.1 offer models from 8B to 405B parameters with strong performance rivaling proprietary models. The open weights allow fine-tuning and deployment in custom environments without API dependencies.",
        "entities": {"Llama", "Fine-Tuning"},
    },
    {
        "id": "llm-05", "category": "llm",
        "content": "Qwen is Alibaba's large language model family with variants from 0.5B to 110B parameters. Qwen3-32b balances performance and efficiency. It supports long context windows and performs well on reasoning, coding, and multilingual tasks.",
        "entities": {"Qwen"},
    },
    {
        "id": "llm-06", "category": "llm",
        "content": "Attention Mechanism allows models to focus on relevant input parts when producing output. It computes weighted sums of values based on query-key compatibility. Self-attention relates different positions of the same sequence, enabling rich contextual representations.",
        "entities": {"Attention Mechanism", "Transformer", "Self-Attention"},
    },
    {
        "id": "llm-07", "category": "llm",
        "content": "Self-Attention computes attention within a single sequence where queries, keys, and values all come from the same source. Multi-head attention runs multiple attention operations in parallel, capturing different relationship types. It is the core of Transformer models.",
        "entities": {"Self-Attention", "Attention Mechanism", "Transformer"},
    },
    {
        "id": "llm-08", "category": "llm",
        "content": "Fine-Tuning adapts a pre-trained LLM to a specific domain or task by continued training on labeled data. Full fine-tuning updates all parameters while parameter-efficient methods like LoRA and QLoRA train small adapter matrices, reducing memory and compute cost.",
        "entities": {"Fine-Tuning"},
    },
    {
        "id": "llm-09", "category": "llm",
        "content": "RLHF (Reinforcement Learning from Human Feedback) aligns LLM outputs with human preferences. A reward model is trained on human comparisons, then the LLM is fine-tuned via PPO to maximize the reward score. This improves helpfulness, honesty, and safety.",
        "entities": {"RLHF", "Fine-Tuning"},
    },
    {
        "id": "llm-10", "category": "llm",
        "content": "Prompt Engineering crafts input prompts to elicit desired LLM outputs. Techniques include few-shot prompting with examples, chain-of-thought prompting for reasoning, instruction prompting for task specification, and role prompting for persona-based responses.",
        "entities": {"Prompt Engineering", "Chain-of-Thought"},
    },
    {
        "id": "llm-11", "category": "llm",
        "content": "RAG (Retrieval-Augmented Generation) combines retrieval from a knowledge base with LLM generation. Documents are retrieved based on query embedding similarity, then fed as context to the LLM. This reduces hallucination and enables knowledge-grounded responses.",
        "entities": {"RAG", "Embedding", "Vector Database"},
    },
    {
        "id": "llm-12", "category": "llm",
        "content": "Chain-of-Thought prompting encourages LLMs to produce intermediate reasoning steps before answering. By showing step-by-step examples, the model learns to decompose complex problems. This dramatically improves performance on math, logic, and multi-step reasoning tasks.",
        "entities": {"Chain-of-Thought", "Prompt Engineering"},
    },
    {
        "id": "llm-13", "category": "llm",
        "content": "Tokenization splits text into tokens the model can process. Subword tokenizers like BPE and WordPiece balance vocabulary size and coverage. Special tokens mark boundaries. Tokenization choices affect model behavior, especially for code, non-English languages, and numbers.",
        "entities": {"Tokenization", "GPT", "BERT"},
    },
    {
        "id": "llm-14", "category": "llm",
        "content": "Embeddings are dense vector representations of text capturing semantic meaning. Models like BGE, text-embedding-ada, and Instructor produce embeddings where similar texts have nearby vectors. They power semantic search, clustering, and classification applications.",
        "entities": {"Embedding", "Vector Database", "BERT"},
    },

    # === Databases (12 chunks) ===
    {
        "id": "db-01", "category": "databases",
        "content": "PostgreSQL is a feature-rich relational database supporting ACID transactions, JSONB, full-text search, and extensions like PostGIS. Its extensibility, strong consistency, and mature ecosystem make it a default choice for operational workloads.",
        "entities": {"PostgreSQL", "ACID", "Indexing"},
    },
    {
        "id": "db-02", "category": "databases",
        "content": "MongoDB is a document-oriented NoSQL database storing JSON-like documents. It supports flexible schemas, horizontal scaling through sharding, and rich query capabilities including aggregation pipelines. Well-suited for rapidly evolving data models.",
        "entities": {"MongoDB", "Sharding", "BASE"},
    },
    {
        "id": "db-03", "category": "databases",
        "content": "Redis is an in-memory data store supporting strings, hashes, lists, sets, and streams. It provides sub-millisecond latency for caching, session management, and real-time analytics. Redis Cluster enables horizontal scaling with automatic partitioning.",
        "entities": {"Redis"},
    },
    {
        "id": "db-04", "category": "databases",
        "content": "Elasticsearch is a distributed search and analytics engine built on Apache Lucene. It provides full-text search, structured queries, aggregations, and near real-time indexing. The inverted index data structure enables fast keyword lookups across large datasets.",
        "entities": {"Elasticsearch", "Indexing"},
    },
    {
        "id": "db-05", "category": "databases",
        "content": "Pinecone is a managed vector database designed for production embedding search. It handles indexing, scalability, and performance automatically. Supports cosine similarity, dot product, and Euclidean distance. Used in RAG pipelines for semantic document retrieval.",
        "entities": {"Pinecone", "Vector Database", "Embedding", "RAG"},
    },
    {
        "id": "db-06", "category": "databases",
        "content": "ChromaDB is an open-source embedding database focused on developer experience. It offers simple APIs for adding, deleting, and searching embeddings. Supports metadata filtering and multiple distance functions. Lightweight enough for prototyping and small-scale RAG.",
        "entities": {"ChromaDB", "Vector Database", "Embedding"},
    },
    {
        "id": "db-07", "category": "databases",
        "content": "Neo4j is a leading graph database using property graph model with nodes, relationships, and properties. Cypher query language expresses graph patterns naturally. Excels at relationship-heavy queries like recommendation, fraud detection, and knowledge graphs.",
        "entities": {"Neo4j"},
    },
    {
        "id": "db-08", "category": "databases",
        "content": "Cassandra is a distributed wide-column NoSQL database offering high availability and partition tolerance. It uses a peer-to-peer architecture with no single point of failure. Optimized for write-heavy workloads with tunable consistency levels across data centers.",
        "entities": {"Cassandra", "BASE", "CAP Theorem"},
    },
    {
        "id": "db-09", "category": "databases",
        "content": "ACID properties guarantee reliable transactions: Atomicity ensures all-or-nothing execution, Consistency maintains database invariants, Isolation prevents concurrent transaction interference, and Durability persists committed changes. Essential for financial and critical systems.",
        "entities": {"ACID", "PostgreSQL"},
    },
    {
        "id": "db-10", "category": "databases",
        "content": "BASE (Basically Available, Soft state, Eventual consistency) describes properties of NoSQL systems. Availability and partition tolerance are prioritized over immediate consistency. Data converges to consistency over time, suitable for systems where availability is critical.",
        "entities": {"BASE", "CAP Theorem"},
    },
    {
        "id": "db-11", "category": "databases",
        "content": "Database indexing accelerates query performance by creating data structures optimized for search. B-tree indexes support range queries, hash indexes support equality lookups, and inverted indexes enable full-text search. Indexes trade write performance for read speed.",
        "entities": {"Indexing", "PostgreSQL"},
    },
    {
        "id": "db-12", "category": "databases",
        "content": "Sharding horizontally partitions data across multiple database instances. Each shard holds a subset of data based on a shard key. It distributes load, improves write throughput, and enables scaling beyond single-node limits. Consistent hashing simplifies rebalancing.",
        "entities": {"Sharding", "MongoDB", "Cassandra"},
    },
    {
        "id": "db-13", "category": "databases",
        "content": "CAP Theorem states distributed systems can guarantee at most two of Consistency, Availability, and Partition Tolerance. CA systems sacrifice partition tolerance, CP systems sacrifice availability, and AP systems sacrifice consistency. Trade-off guides database selection.",
        "entities": {"CAP Theorem"},
    },
]


def get_documents() -> list[dict]:
    return DOCUMENTS


def get_documents_by_category() -> dict[str, list[dict]]:
    by_cat: dict[str, list[dict]] = {}
    for doc in DOCUMENTS:
        by_cat.setdefault(doc["category"], []).append(doc)
    return by_cat
