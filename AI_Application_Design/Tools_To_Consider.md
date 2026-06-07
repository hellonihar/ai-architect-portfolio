# Tools & Frameworks for AI Project SDLC Phases

A curated reference of popular tools and frameworks mapped to each phase of the AI SDLC.

---

## 1. Planning & Feasibility Assessment

| Tool / Framework | Purpose | Type |
|---|---|---|
| **Azure AI Foundry** | Model catalog, benchmarking, capacity discovery | Managed platform |
| **Hugging Face Hub** | Explore pre-trained models, compare benchmarks, dataset search | Open-source platform |
| **LangSmith / Weights & Biases** | Evaluate model performance on representative tasks before committing | MLOps platform |
| **Google Colab / SageMaker Studio Lab** | Rapid prototyping to test feasibility with sample data | Notebook environment |
| **Airbyte / Fivetran** | Data source discovery and feasibility (connector availability) | Data integration |

---

## 2. Requirements Definition

| Tool / Framework | Purpose | Type |
|---|---|---|
| **Azure AI Foundry** | Define model card metadata, RAI policy requirements | Managed platform |
| **ModelCard Toolkit (Google)** | Programmatic model card generation | Open-source library |
| **Confluence / Notion** | Requirements documentation and stakeholder alignment | Collaboration |
| **Jira / Azure DevOps** | Epics, user stories, acceptance criteria for AI features | Project management |
| **Aporia / WhyLabs** | Define monitoring SLOs and drift thresholds | AI observability |

---

## 3. Architecture & Design

| Tool / Framework | Purpose | Type |
|---|---|---|
| **Azure Architecture Center** | Reference architectures for RAG, agents, fine-tuning | Documentation |
| **C4 Model (Structurizr)** | Architecture diagrams: Context, Container, Component, Code | Diagramming |
| **LangGraph / CrewAI / AutoGen** | Agent orchestration topologies (supervisor, DAG, swarm) | Framework |
| **Kafka / Event Hubs / RabbitMQ** | Event-driven data pipeline design | Message broker |
| **Feast / Tecton / Hopsworks** | Feature store design for ML | Feature store |
| **Qdrant / Pinecone / Cosmos DB (vCore)** | Vector database selection for RAG | Vector store |

---

## 4. Data Acquisition & Preparation

| Tool / Framework | Purpose | Type |
|---|---|---|
| **Apache Spark / Pandas / Polars** | Data transformation at scale | Compute engine |
| **dbt (data build tool)** | Data transformation with version control and testing | Data transformation |
| **DVC (Data Version Control)** | Dataset versioning, pipeline management | Open-source |
| **Label Studio / Scale AI / Snorkel** | Human annotation and weak supervision | Labeling platform |
| **Great Expectations / Deequ** | Data quality validation, profiling, expectation suites | Data quality |
| **LangChain Document Loaders / Unstructured.io** | Parse PDFs, HTML, markdown into clean text for RAG | Document parsing |
| **Faker / SDV (Synthetic Data Vault)** | Synthetic data generation for augmentation | Data generation |
| **Apache Atlas / Alation / Collibra** | Data catalog, lineage, and governance | Data governance |

---

## 5. Model Development & Experimentation

| Tool / Framework | Purpose | Type |
|---|---|---|
| **Azure OpenAI / Anthropic / Gemini** | API-based model access for prompting and fine-tuning | Model API |
| **Hugging Face Transformers / TRL** | Open-source model training, fine-tuning (SFT, DPO, LoRA) | Library |
| **Unsloth / Axolotl** | Optimized fine-tuning (2x faster, 50% less memory) | Library |
| **Ollama / llama.cpp / vLLM** | Local model serving and experimentation | Inference engine |
| **MLflow / Weights & Biases / Neptune** | Experiment tracking, hyperparameter logging, artifact storage | MLOps |
| **LangChain / LlamaIndex** | RAG pipelines, prompt chaining, tool-calling abstractions | Framework |
| **OpenAI Evals / LangSmith / DeepEval** | LLM evaluation pipelines, LLM-as-judge | Evaluation |
| **Ray / Tune / Optuna** | Distributed hyperparameter tuning | Compute / optimization |
| **Jupyter / VS Code (Jupyter extension)** | Interactive development and exploration | IDE |

---

## 6. Evaluation & Validation

| Tool / Framework | Purpose | Type |
|---|---|---|
| **RAGAS / TruLens / Arize Phoenix** | RAG-specific evaluation: faithfulness, relevance, context precision | Evaluation framework |
| **OpenAI Evals** | Custom eval templates for classification, Q&A, safety | Evaluation framework |
| **DeepEval / LangSmith** | Unit-test-style evaluation with CI/CD integration | Testing framework |
| **Azure AI Safety Evaluation** | Jailbreak detection, content filter testing, protected material | Safety evaluation |
| **Fairlearn / AIF360 (IBM)** | Bias detection and fairness metrics | Fairness toolkit |
| **SHAP / LIME / Captum** | Model interpretability and feature attribution | Explainability |
| **Giskard / Robust Intelligence** | Adversarial testing, robustness scanning, vulnerability detection | Security / robustness |
| **Red Team Toolkit (Microsoft)** | Manual and automated red-teaming for LLMs | Red-teaming |

---

## 7. Deployment

| Tool / Framework | Purpose | Type |
|---|---|---|
| **Azure AI Foundry / Azure ML** | Model deployment, endpoint management, SKU selection | Managed platform |
| **Docker / Kubernetes / AKS** | Containerization and orchestration for model serving | Infrastructure |
| **Terraform / Bicep / Pulumi** | Infrastructure as Code for repeatable deployments | IaC |
| **BentoML / MLflow Serving / Ray Serve** | Model packaging and serving framework | Serving |
| **NVIDIA Triton Inference Server** | High-performance inference serving with GPU optimization | Inference server |
| **ONNX Runtime / TensorRT / OpenVINO** | Model optimization and cross-platform inference | Optimization |
| **Istio / Envoy / Azure API Management** | Traffic splitting, canary releases, A/B testing | Service mesh / gateway |
| **Azure Container Registry / Docker Hub** | Model image registry | Registry |

---

## 8. Monitoring & Operations

| Tool / Framework | Purpose | Type |
|---|---|---|
| **Azure Monitor / Application Insights** | Infrastructure and application performance monitoring | Cloud monitoring |
| **Prometheus + Grafana** | Metrics collection and dashboarding (drift, latency, throughput) | Open-source monitoring |
| **WhyLabs / Aporia / Arize AI** | Model-specific monitoring: data drift, concept drift, performance decay | AI observability |
| **Evidently AI / NannyML** | Open-source drift detection and model performance monitoring | Open-source monitoring |
| **LangFuse / Helicone / Lunary** | LLM observability: token usage, latency, cost per request, trace logging | LLM observability |
| **PagerDuty / Opsgenie** | Incident alerting and on-call management | Incident response |

---

## 9. Maintenance & Iteration

| Tool / Framework | Purpose | Type |
|---|---|---|
| **Azure ML Pipelines / Airflow / Prefect** | Scheduled retraining pipelines and workflow orchestration | Pipeline orchestration |
| **DVC / LakeFS / Delta Lake** | Data and model lineage for reproducible updates | Version control |
| **Weights & Biases / MLflow** | Model registry for version promotion and rollback | Model registry |
| **GitHub Actions / Azure DevOps Pipelines** | CI/CD for model training, evaluation, and deployment | CI/CD |
| **LangSmith Hub / PromptLayer** | Prompt version management, prompt registry | Prompt management |

---

## 10. Governance & Compliance (Cross-Cutting)

| Tool / Framework | Purpose | Type |
|---|---|---|
| **Azure AI Foundry (Content Safety)** | RAI policy enforcement: content filters, jailbreak detection, groundedness | Managed safety |
| **Microsoft Purview** | Data governance, classification, lineage, and compliance reporting | Data governance |
| **ModelOp / Seldon Core / KServe** | Model governance: approval gates, compliance dashboards, audit trails | Model governance |
| **Open Policy Agent (OPA) / Styra** | Policy-as-code for deployment approvals and access control | Policy engine |
| **Vault / Azure Key Vault** | Secrets management for API keys, model credentials | Secrets management |
| **SOC 2 / HIPAA / GDPR tooling** | Compliance automation (e.g., Drata, Vanta, OneTrust) | Compliance |

---

## End-to-End Platforms (Cover Multiple Phases)

| Platform | Phases Covered |
|---|---|
| **Azure AI Foundry** | 1–10 (full lifecycle: model catalog, fine-tuning, deployment, monitoring, RAI) |
| **MLflow** | 5–9 (experiment tracking, model registry, serving, monitoring) |
| **Weights & Biases** | 5–9 (experiments, hyperparameter tuning, model registry, monitoring) |
| **LangSmith** | 2–9 (prompt engineering, tracing, evaluation, monitoring, hub) |
| **Hugging Face Hub + Spaces** | 1, 5, 6 (model discovery, training, inference, evaluation demos) |
| **Kubeflow** | 3–9 (pipeline orchestration, training, serving, monitoring on K8s) |
| **Google Vertex AI** | 1–10 (full lifecycle on GCP) |
| **Amazon SageMaker** | 1–10 (full lifecycle on AWS) |

---

*This list is representative and evolves rapidly. Evaluate tools against your team's cloud provider, MLOps maturity, scale, and compliance requirements.*
