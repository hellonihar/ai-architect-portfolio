CATEGORIES = {
    "Distributed Systems": {
        "entities": [
            "Apache Kafka", "stream processing", "exactly-once semantics",
            "Kafka Streams", "event sourcing", "CQRS", "log compaction",
            "partitioning", "replication", "consensus", "Raft", "Paxos",
        ],
    },
    "Machine Learning": {
        "entities": [
            "feature engineering", "data leakage", "cross-validation",
            "hyperparameter tuning", "ensemble methods", "gradient boosting",
            "model drift", "concept drift", "online learning", "batch inference",
        ],
    },
    "LLMs & NLP": {
        "entities": [
            "attention mechanism", "transformer", "self-attention",
            "retrieval-augmented generation", "RAG", "prompt engineering",
            "chain-of-thought", "semantic search", "dense retrieval",
            "hybrid search", "embedding", "tokenization",
        ],
    },
    "Databases & Storage": {
        "entities": [
            "ACID", "BASE", "CAP theorem", "distributed transactions",
            "vector database", "LSM tree", "B-tree", "sharding",
            "consistent hashing", "read replicas", "write-ahead log",
        ],
    },
    "Cloud Architecture": {
        "entities": [
            "microservices", "service mesh", "sidecar pattern",
            "circuit breaker", "bulkhead", "event-driven architecture",
            "serverless", "cold start", "function-as-a-service",
            "observability", "distributed tracing",
        ],
    },
}

ENTITY_CHAINS = [
    ["chain-1", ["event sourcing", "CQRS", "log compaction"]],
    ["chain-2", ["data leakage", "cross-validation", "hyperparameter tuning"]],
    ["chain-3", ["RAG", "dense retrieval", "hybrid search"]],
    ["chain-4", ["attention mechanism", "transformer", "self-attention"]],
    ["chain-5", ["ACID", "distributed transactions", "consensus"]],
    ["chain-6", ["microservices", "circuit breaker", "observability"]],
    ["chain-7", ["model drift", "online learning", "batch inference"]],
    ["chain-8", ["vector database", "semantic search", "embedding"]],
    ["chain-9", ["Apache Kafka", "exactly-once semantics", "Kafka Streams"]],
    ["chain-10", ["CAP theorem", "consistent hashing", "sharding"]],
]

DOCUMENTS = [
    # ── Distributed Systems ──
    {
        "id": "ds-01",
        "content": "Apache Kafka is a distributed event streaming platform capable of handling trillions of events a day. It provides a high-throughput, low-latency platform for handling real-time data feeds. Kafka uses a partitioned log model where messages are stored in topics and divided into partitions for parallelism. Each partition is an ordered, immutable sequence of records.",
        "category": "Distributed Systems",
        "entities": ["Apache Kafka", "partitioning"],
    },
    {
        "id": "ds-02",
        "content": "Stream processing is a programming paradigm that treats data streams as the core abstraction. Unlike batch processing, stream processing operates on data continuously as it arrives. Stream processing engines like Kafka Streams and Apache Flink enable real-time analytics, anomaly detection, and event-driven applications. The key challenge is maintaining state across potentially unbounded streams.",
        "category": "Distributed Systems",
        "entities": ["stream processing", "Kafka Streams"],
    },
    {
        "id": "ds-03",
        "content": "Exactly-once semantics ensure that each message is processed precisely one time, even in the face of failures. This is the strongest delivery guarantee in distributed messaging systems. Implementing exactly-once requires idempotent producers, transactional writes, and coordinated commit protocols. Kafka achieves exactly-once through a combination of idempotent delivery and transactional APIs.",
        "category": "Distributed Systems",
        "entities": ["exactly-once semantics", "Apache Kafka"],
    },
    {
        "id": "ds-04",
        "content": "Kafka Streams is a client library for building applications and microservices where the input and output are stored in Kafka topics. It combines the simplicity of writing standard Java applications with the scalability of Kafka clusters. Kafka Streams supports exactly-once processing semantics, stateful operations like windowed joins and aggregations, and one-record-at-a-time processing with sub-millisecond latency.",
        "category": "Distributed Systems",
        "entities": ["Kafka Streams", "exactly-once semantics", "stream processing"],
    },
    {
        "id": "ds-05",
        "content": "Event sourcing is an architectural pattern where state changes are captured as a sequence of events. Instead of storing the current state, the system stores every state-changing event. The current state can be reconstructed by replaying all events. This provides a complete audit trail and enables temporal queries. Event sourcing works naturally with CQRS and stream processing systems.",
        "category": "Distributed Systems",
        "entities": ["event sourcing", "CQRS", "stream processing"],
    },
    {
        "id": "ds-06",
        "content": "CQRS (Command Query Responsibility Segregation) separates read and write operations into different models. Commands handle writes (inserts, updates, deletes) using a write-optimized model, while queries use a separate read-optimized model. This allows independent scaling of read and write workloads. CQRS is often combined with event sourcing for event-driven architectures.",
        "category": "Distributed Systems",
        "entities": ["CQRS", "event sourcing"],
    },
    {
        "id": "ds-07",
        "content": "Log compaction is a mechanism in Kafka that retains the latest value for each key within a partition. This ensures that the log does not grow unboundedly while still providing a complete record of changes. Log compaction is essential for restoring state after failures and for implementing the database-like semantics in event sourcing. It allows consumers to bootstrap their state from a compacted topic.",
        "category": "Distributed Systems",
        "entities": ["log compaction", "Apache Kafka", "event sourcing"],
    },
    {
        "id": "ds-08",
        "content": "The Raft consensus algorithm is designed to be more understandable than Paxos. It works by electing a leader who manages log replication across a cluster. Consensus is achieved when a majority of nodes have committed an entry. Raft is used by etcd, Consul, and many distributed databases for coordination and leader election.",
        "category": "Distributed Systems",
        "entities": ["consensus", "Raft"],
    },
    {
        "id": "ds-09",
        "content": "Partitioning, or sharding, divides a large dataset into smaller, independent partitions. Each partition is stored on a separate node, enabling horizontal scaling. The key distribution strategy (range-based, hash-based, or consistent hashing) determines how evenly data is distributed. Good partitioning minimizes data movement during rebalancing and reduces hotspotting.",
        "category": "Distributed Systems",
        "entities": ["partitioning", "consistent hashing"],
    },
    # ── Machine Learning ──
    {
        "id": "ml-01",
        "content": "Feature engineering is the process of transforming raw data into features that better represent the underlying problem structure. Good feature engineering can significantly improve model performance even with simple algorithms. Techniques include encoding categorical variables, creating interaction terms, scaling numeric features, and extracting date/time components.",
        "category": "Machine Learning",
        "entities": ["feature engineering"],
    },
    {
        "id": "ml-02",
        "content": "Data leakage occurs when information from outside the training set is used to create features, leading to overly optimistic performance estimates. Common sources include scaling before train-test split, using future data in time series, and leakage from target encoding. Cross-validation helps detect leakage by exposing inconsistencies in performance across folds.",
        "category": "Machine Learning",
        "entities": ["data leakage", "cross-validation"],
    },
    {
        "id": "ml-03",
        "content": "Cross-validation is a resampling procedure used to evaluate machine learning models on limited data. The most common variant is k-fold cross-validation, where the data is split into k folds, and the model is trained on k-1 folds and validated on the remaining fold. This is repeated k times. Cross-validation provides a more robust estimate of model performance than a single train-test split.",
        "category": "Machine Learning",
        "entities": ["cross-validation"],
    },
    {
        "id": "ml-04",
        "content": "Hyperparameter tuning searches for the optimal set of hyperparameters that maximize model performance. Common methods include grid search, random search, and Bayesian optimization. Proper tuning requires cross-validation to avoid overfitting to the validation set. The results of tuning are sensitive to the chosen evaluation metric and search space.",
        "category": "Machine Learning",
        "entities": ["hyperparameter tuning", "cross-validation"],
    },
    {
        "id": "ml-05",
        "content": "Ensemble methods combine multiple machine learning models to produce better predictive performance than any single model. Techniques include bagging (training models in parallel), boosting (training models sequentially to correct errors), and stacking (training a meta-model on base model outputs). Gradient boosting is one of the most popular ensemble methods.",
        "category": "Machine Learning",
        "entities": ["ensemble methods", "gradient boosting"],
    },
    {
        "id": "ml-06",
        "content": "Gradient boosting builds an ensemble of weak learners, typically decision trees, in a sequential manner. Each new tree corrects the errors of the previous ensemble by fitting to the negative gradient of the loss function. Popular implementations include XGBoost, LightGBM, and CatBoost. Gradient boosting is known for its high performance on tabular data.",
        "category": "Machine Learning",
        "entities": ["gradient boosting", "ensemble methods"],
    },
    {
        "id": "ml-07",
        "content": "Model drift refers to the degradation of model performance over time due to changes in the underlying data distribution. It can be caused by changes in consumer behavior, seasonal patterns, or external factors. Monitoring model drift requires tracking prediction distributions, performance metrics, and data schemas over time.",
        "category": "Machine Learning",
        "entities": ["model drift"],
    },
    {
        "id": "ml-08",
        "content": "Concept drift occurs when the statistical properties of the target variable change over time. Unlike model drift which focuses on input distributions, concept drift specifically addresses changes in the relationship between features and the target. Online learning algorithms are designed to adapt to concept drift by updating the model incrementally as new data arrives.",
        "category": "Machine Learning",
        "entities": ["concept drift", "online learning"],
    },
    {
        "id": "ml-09",
        "content": "Online learning trains machine learning models incrementally as data arrives, rather than in a single batch. This is useful when data arrives continuously and concept drift is present. Online algorithms update their parameters after each data point or mini-batch, making them memory-efficient and capable of adapting to changing patterns.",
        "category": "Machine Learning",
        "entities": ["online learning", "concept drift"],
    },
    {
        "id": "ml-10",
        "content": "Batch inference processes large volumes of data in pre-defined batches, typically on a schedule. It is suitable for use cases where real-time predictions are not required, such as nightly recommendation updates or periodic fraud scoring. Batch inference is more cost-efficient than real-time for high-throughput workloads.",
        "category": "Machine Learning",
        "entities": ["batch inference"],
    },
    # ── LLMs & NLP ──
    {
        "id": "llm-01",
        "content": "The attention mechanism allows a model to focus on relevant parts of the input when producing each part of the output. It computes a weighted sum of values, where weights are determined by the compatibility between a query and a set of keys. This enables the model to capture long-range dependencies without the limitations of fixed-length context windows.",
        "category": "LLMs & NLP",
        "entities": ["attention mechanism"],
    },
    {
        "id": "llm-02",
        "content": "The Transformer architecture is based entirely on the attention mechanism, dispensing with recurrence and convolutions. It uses multi-head self-attention, positional encodings, and feed-forward layers. The Transformer achieved state-of-the-art results on machine translation and became the foundation for models like BERT and GPT. Its parallelizable architecture enables efficient training on large datasets.",
        "category": "LLMs & NLP",
        "entities": ["transformer", "attention mechanism", "self-attention"],
    },
    {
        "id": "llm-03",
        "content": "Self-attention, also called intra-attention, relates different positions within a single sequence. Each position attends to all positions in the same sequence, computing a context-aware representation. This is the core innovation of the Transformer architecture, enabling it to capture both local and global dependencies in a single layer.",
        "category": "LLMs & NLP",
        "entities": ["self-attention", "transformer", "attention mechanism"],
    },
    {
        "id": "llm-04",
        "content": "Retrieval-Augmented Generation (RAG) is a technique that combines retrieval from a knowledge base with text generation from an LLM. The model retrieves relevant documents from a corpus and conditions its generation on both the query and the retrieved context. RAG reduces hallucination by grounding responses in external knowledge and enables updating knowledge without retraining.",
        "category": "LLMs & NLP",
        "entities": ["retrieval-augmented generation", "RAG"],
    },
    {
        "id": "llm-05",
        "content": "Dense retrieval represents queries and documents as dense vectors in a continuous embedding space and finds relevant documents by nearest neighbor search. Unlike sparse methods (BM25) that rely on exact keyword overlap, dense retrieval captures semantic similarity. It is the backbone of modern RAG systems and semantic search applications.",
        "category": "LLMs & NLP",
        "entities": ["dense retrieval", "embedding", "semantic search", "RAG"],
    },
    {
        "id": "llm-06",
        "content": "Hybrid search combines dense (semantic) and sparse (keyword) retrieval to get the best of both worlds. Dense retrieval captures meaning and synonyms, while sparse retrieval excels at exact matches on names, IDs, and rare terms. The results are typically fused using techniques like Reciprocal Rank Fusion (RRF) or weighted score normalization.",
        "category": "LLMs & NLP",
        "entities": ["hybrid search", "dense retrieval", "RAG"],
    },
    {
        "id": "llm-07",
        "content": "Prompt engineering is the practice of designing input prompts to elicit desired outputs from LLMs. Techniques include few-shot prompting, chain-of-thought reasoning, and role prompting. Effective prompt engineering can dramatically improve output quality without modifying model weights.",
        "category": "LLMs & NLP",
        "entities": ["prompt engineering", "chain-of-thought"],
    },
    {
        "id": "llm-08",
        "content": "Chain-of-thought prompting encourages LLMs to reason step-by-step before producing a final answer. By adding 'think step by step' or providing few-shot examples of reasoning chains, the model's accuracy on complex reasoning tasks improves substantially. This technique has been shown to boost performance on arithmetic, symbolic, and commonsense reasoning benchmarks.",
        "category": "LLMs & NLP",
        "entities": ["chain-of-thought", "prompt engineering"],
    },
    {
        "id": "llm-09",
        "content": "Tokenization is the process of converting text into subword units that an LLM can process. Modern tokenizers like Byte-Pair Encoding (BPE) and WordPiece balance vocabulary size and sequence length. The choice of tokenizer affects model performance, inference speed, and the ability to handle rare words and multiple languages.",
        "category": "LLMs & NLP",
        "entities": ["tokenization"],
    },
    {
        "id": "llm-10",
        "content": "Semantic search goes beyond keyword matching to understand the intent and contextual meaning of a search query. It uses dense embeddings to represent both queries and documents in a semantic vector space. When a user searches, the system finds documents whose semantic meaning is closest to the query, even if they share no exact keywords.",
        "category": "LLMs & NLP",
        "entities": ["semantic search", "dense retrieval", "embedding"],
    },
    # ── Databases & Storage ──
    {
        "id": "db-01",
        "content": "ACID stands for Atomicity, Consistency, Isolation, and Durability. These properties ensure that database transactions are processed reliably. Atomicity means transactions are all-or-nothing. Consistency ensures transitions between valid states. Isolation prevents concurrent transactions from interfering. Durability guarantees committed transactions persist.",
        "category": "Databases & Storage",
        "entities": ["ACID"],
    },
    {
        "id": "db-02",
        "content": "The CAP theorem states that a distributed data store can only provide two of three guarantees: Consistency, Availability, and Partition Tolerance. Partition tolerance is non-negotiable in distributed systems, so the practical choice is between CP (consistency) and AP (availability). This theorem guides architectural decisions for distributed databases.",
        "category": "Databases & Storage",
        "entities": ["CAP theorem"],
    },
    {
        "id": "db-03",
        "content": "Distributed transactions span multiple databases or services and require coordination to ensure ACID properties across all participants. The two-phase commit (2PC) protocol is the standard approach, with a coordinator that votes then commits. Distributed transactions are complex and often trade availability for consistency, aligning with the CAP theorem.",
        "category": "Databases & Storage",
        "entities": ["distributed transactions", "ACID", "CAP theorem"],
    },
    {
        "id": "db-04",
        "content": "Vector databases are purpose-built for storing and searching high-dimensional vector embeddings. They use approximate nearest neighbor (ANN) algorithms like HNSW, IVF, or PQ to enable fast similarity search at scale. Vector databases are essential for RAG applications, semantic search, and recommender systems.",
        "category": "Databases & Storage",
        "entities": ["vector database", "embedding"],
    },
    {
        "id": "db-05",
        "content": "LSM trees (Log-Structured Merge-Trees) are a data structure designed for write-heavy workloads. They batch writes in memory, flush them to immutable SSTables on disk, and periodically merge them in the background. LSM trees are used by LevelDB, RocksDB, Cassandra, and many other NoSQL databases. They offer excellent write throughput at the cost of read amplification.",
        "category": "Databases & Storage",
        "entities": ["LSM tree"],
    },
    {
        "id": "db-06",
        "content": "B-trees are the most common indexing data structure in relational databases. They maintain sorted data for efficient insertions, deletions, and lookups. B-trees keep data balanced with O(log n) complexity for operations and are optimized for disk-based storage with large block sizes. PostgreSQL and MySQL use B-tree indexes as their primary index type.",
        "category": "Databases & Storage",
        "entities": ["B-tree"],
    },
    {
        "id": "db-07",
        "content": "Consistent hashing is a distributed hashing scheme that minimizes key remapping when the number of hash buckets changes. Each key is mapped to a position on a hash ring, and servers are also placed on the ring. Keys are assigned to the nearest server clockwise. This is used by DynamoDB, Cassandra, and distributed caching systems for load balancing.",
        "category": "Databases & Storage",
        "entities": ["consistent hashing", "sharding"],
    },
    {
        "id": "db-08",
        "content": "Write-ahead logging (WAL) ensures data durability by recording changes to a log before applying them to the data store. In the event of a crash, the system can recover by replaying the WAL. This technique is used by PostgreSQL, SQLite, and many distributed systems to guarantee that committed transactions are not lost.",
        "category": "Databases & Storage",
        "entities": ["write-ahead log"],
    },
    # ── Cloud Architecture ──
    {
        "id": "cloud-01",
        "content": "Microservices is an architectural style that structures an application as a collection of small, independently deployable services. Each service is focused on a specific business capability and can be developed, deployed, and scaled independently. Microservices communicate via lightweight protocols like HTTP/REST or message queues.",
        "category": "Cloud Architecture",
        "entities": ["microservices"],
    },
    {
        "id": "cloud-02",
        "content": "A service mesh adds observability, security, and traffic management capabilities to microservice deployments without changing application code. It uses sidecar proxies deployed alongside each service to handle inter-service communication. Service meshes like Istio and Linkerd provide features like load balancing, circuit breaking, and distributed tracing.",
        "category": "Cloud Architecture",
        "entities": ["service mesh", "sidecar pattern", "microservices"],
    },
    {
        "id": "cloud-03",
        "content": "The sidecar pattern deploys helper components as separate containers in the same pod as the main application. These sidecars provide supporting functionality such as logging, monitoring, or proxying. This pattern allows these cross-cutting concerns to be managed independently from the application code and is the foundation of service mesh architectures.",
        "category": "Cloud Architecture",
        "entities": ["sidecar pattern", "service mesh"],
    },
    {
        "id": "cloud-04",
        "content": "The circuit breaker pattern prevents cascading failures in distributed systems by detecting failures and preventing calls to an unhealthy service. When the failure threshold is exceeded, the circuit trips to open state and subsequent calls fail immediately. After a timeout, the circuit transitions to half-open to test if the service has recovered. This is a critical resilience pattern in microservice architectures.",
        "category": "Cloud Architecture",
        "entities": ["circuit breaker", "microservices"],
    },
    {
        "id": "cloud-05",
        "content": "Event-driven architecture (EDA) uses events to trigger and communicate between decoupled services. Producers emit events without knowing which consumers will process them. Consumers subscribe to relevant event streams. This pattern enables loose coupling, scalability, and asynchronous processing. Event sourcing and CQRS are commonly used together with EDA.",
        "category": "Cloud Architecture",
        "entities": ["event-driven architecture"],
    },
    {
        "id": "cloud-06",
        "content": "Serverless computing allows developers to build and run applications without managing servers. The cloud provider automatically provisions and scales infrastructure. Function-as-a-Service (FaaS) platforms like AWS Lambda execute code in response to events. Serverless reduces operational overhead but introduces challenges like cold starts and statelessness constraints.",
        "category": "Cloud Architecture",
        "entities": ["serverless", "cold start", "function-as-a-service"],
    },
    {
        "id": "cloud-07",
        "content": "Cold start is a delay experienced when a serverless function is invoked after being idle. The platform must provision a new execution environment, load the runtime, and initialize the code. Cold starts can add hundreds of milliseconds to response times. Strategies to mitigate include keeping functions warm, using provisioned concurrency, and minimizing deployment package size.",
        "category": "Cloud Architecture",
        "entities": ["cold start", "serverless", "function-as-a-service"],
    },
    {
        "id": "cloud-08",
        "content": "Observability is the ability to understand a system's internal state from its external outputs. The three pillars are logs (discrete events), metrics (aggregated measurements), and traces (request flows across services). Distributed tracing follows a request across service boundaries, identifying bottlenecks and failures. Observability is essential for debugging microservice architectures.",
        "category": "Cloud Architecture",
        "entities": ["observability", "distributed tracing", "microservices"],
    },
    # ── Noise documents (intentionally off-topic or irrelevant) ──
    {
        "id": "noise-01",
        "content": "The Great Barrier Reef is the world's largest coral reef system, stretching over 2,300 kilometers off the coast of Australia. It is home to thousands of marine species and is visible from space. Climate change poses the greatest threat to its survival, with rising ocean temperatures causing coral bleaching events.",
        "category": "Uncategorized",
        "entities": [],
    },
    {
        "id": "noise-02",
        "content": "The history of the Roman Empire spans over a thousand years, from 27 BC to 1453 AD. At its peak, it controlled territory across Europe, North Africa, and the Middle East. The Roman legal system, engineering achievements, and Latin language have profoundly influenced Western civilization.",
        "category": "Uncategorized",
        "entities": [],
    },
    {
        "id": "noise-03",
        "content": "The Mediterranean diet is based on the traditional foods of countries bordering the Mediterranean Sea. It emphasizes plant-based foods, whole grains, fish, and healthy fats like olive oil. Studies have shown it reduces the risk of heart disease, diabetes, and cognitive decline.",
        "category": "Uncategorized",
        "entities": [],
    },
    {
        "id": "noise-04",
        "content": "The sport of competitive programming involves solving algorithmic problems under time constraints. Participants write code to solve problems ranging from basic data structures to advanced graph theory. Major competitions include ICPC, Codeforces, and Google Code Jam.",
        "category": "Uncategorized",
        "entities": [],
    },
    {
        "id": "noise-05",
        "content": "The Baroque period in music lasted from approximately 1600 to 1750. Composers like Bach, Handel, and Vivaldi created works characterized by ornate melodies, contrast, and basso continuo. The period saw the development of many musical forms still used today, including the concerto, sonata, and fugue.",
        "category": "Uncategorized",
        "entities": [],
    },
    {
        "id": "noise-06",
        "content": "The Python programming language was created by Guido van Rossum and first released in 1991. It emphasizes code readability with its use of significant indentation. Python supports multiple programming paradigms and has a large standard library. It is one of the most popular languages for data science and web development.",
        "category": "Uncategorized",
        "entities": [],
    },
    {
        "id": "noise-07",
        "content": "The sport of Formula 1 racing involves open-wheel, single-seater cars competing on purpose-built circuits and public roads. The championship season consists of races called Grands Prix held worldwide. Teams like Ferrari, Mercedes, and Red Bull invest heavily in aerodynamics, power units, and driver talent.",
        "category": "Uncategorized",
        "entities": [],
    },
    {
        "id": "noise-08",
        "content": "The Moon is Earth's only natural satellite and the fifth largest moon in the Solar System. It is in synchronous rotation with Earth, always showing the same face. The Moon's surface is covered in craters from impacts, and its lack of atmosphere means extreme temperature variations between day and night.",
        "category": "Uncategorized",
        "entities": [],
    },
]

MULTI_HOP_QUERIES = [
    {
        "query": "How do Kafka transactions achieve exactly-once semantics in stream processing?",
        "hops": ["ds-01", "ds-03", "ds-02"],
        "chain": ["Apache Kafka", "exactly-once semantics", "stream processing"],
    },
    {
        "query": "How does CQRS combine with event sourcing and log compaction in event-driven systems?",
        "hops": ["ds-06", "ds-05", "ds-07"],
        "chain": ["CQRS", "event sourcing", "log compaction"],
    },
    {
        "query": "Why is cross-validation important for detecting data leakage during hyperparameter tuning?",
        "hops": ["ml-02", "ml-03", "ml-04"],
        "chain": ["data leakage", "cross-validation", "hyperparameter tuning"],
    },
    {
        "query": "How do dense retrieval and hybrid search improve RAG systems?",
        "hops": ["llm-05", "llm-06", "llm-04"],
        "chain": ["dense retrieval", "hybrid search", "RAG"],
    },
    {
        "query": "What is the relationship between attention mechanisms, self-attention, and the Transformer architecture?",
        "hops": ["llm-01", "llm-03", "llm-02"],
        "chain": ["attention mechanism", "self-attention", "transformer"],
    },
    {
        "query": "How do ACID properties and the CAP theorem influence distributed transaction design?",
        "hops": ["db-01", "db-02", "db-03"],
        "chain": ["ACID", "CAP theorem", "distributed transactions"],
    },
    {
        "query": "How do microservices use circuit breakers to improve observability through distributed tracing?",
        "hops": ["cloud-01", "cloud-04", "cloud-08"],
        "chain": ["microservices", "circuit breaker", "observability"],
    },
    {
        "query": "How does consistent hashing enable effective sharding in distributed databases?",
        "hops": ["db-07", "ds-09"],
        "chain": ["consistent hashing", "sharding"],
    },
    {
        "query": "How does the sidecar pattern relate to service mesh in microservice architectures?",
        "hops": ["cloud-03", "cloud-02", "cloud-01"],
        "chain": ["sidecar pattern", "service mesh", "microservices"],
    },
    {
        "query": "What is the connection between online learning, concept drift, and batch inference?",
        "hops": ["ml-09", "ml-08", "ml-10"],
        "chain": ["online learning", "concept drift", "batch inference"],
    },
    {
        "query": "How do gradient boosting and ensemble methods compare as machine learning techniques?",
        "hops": ["ml-06", "ml-05"],
        "chain": ["gradient boosting", "ensemble methods"],
    },
    {
        "query": "How does vector database embedding enable semantic search?",
        "hops": ["db-04", "llm-10"],
        "chain": ["vector database", "embedding", "semantic search"],
    },
    {
        "query": "How does Kafka Streams relate to stream processing and exactly-once semantics?",
        "hops": ["ds-04", "ds-02", "ds-03"],
        "chain": ["Kafka Streams", "stream processing", "exactly-once semantics"],
    },
    {
        "query": "What is the relationship between chain-of-thought and prompt engineering techniques?",
        "hops": ["llm-08", "llm-07"],
        "chain": ["chain-of-thought", "prompt engineering"],
    },
    {
        "query": "How do cold starts affect serverless FaaS architectures?",
        "hops": ["cloud-07", "cloud-06"],
        "chain": ["cold start", "serverless", "function-as-a-service"],
    },
]

E2E_QUERIES = [
    "What is Apache Kafka and how does it use partitioning?",
    "How does gradient boosting work as an ensemble method?",
    "What is dense retrieval in the context of RAG?",
    "How does the CAP theorem apply to distributed databases?",
    "What is a service mesh and how does it use sidecars?",
    "Explain the attention mechanism in the Transformer architecture.",
    "How does cross-validation help prevent data leakage?",
    "What is consistent hashing and how is it used in sharding?",
    "How does event sourcing work with CQRS?",
    "What are ACID properties in database transactions?",
    "Explain how Kafka Streams achieves stream processing.",
    "What is the difference between model drift and concept drift?",
    "How do vector databases support semantic search?",
    "What is the circuit breaker pattern in microservices?",
    "Explain how chain-of-thought prompting improves LLM reasoning.",
]


def get_documents():
    return DOCUMENTS


def get_categories():
    return CATEGORIES


def get_entity_chains():
    return ENTITY_CHAINS


def get_multi_hop_queries():
    return MULTI_HOP_QUERIES


def get_e2e_queries():
    return E2E_QUERIES


def get_document_by_id(doc_id: str) -> dict | None:
    for doc in DOCUMENTS:
        if doc["id"] == doc_id:
            return doc
    return None
