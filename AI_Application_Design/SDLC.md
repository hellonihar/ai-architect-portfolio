# SDLC Phases Applicable for AI Projects

## Overview

The Software Development Life Cycle (SDLC) for AI projects extends the traditional SDLC with data-centric, model-centric, and ethical considerations unique to artificial intelligence. While the core phases — Plan, Define, Design, Build, Test, Deploy, Maintain — remain, each phase requires significant adaptation for AI workloads.

---
## Key Differences vs Traditional SDLC
**Data‑centric**: AI projects depend heavily on data quality and preparation.

**Iterative model training**: Unlike static code, models require retraining as data evolves.

**Governance**: Bias, fairness, and explainability are critical checkpoints.

**Continuous monitoring**: AI systems degrade over time due to data drift, requiring proactive maintenance.

---
## 1. Planning & Feasibility Assessment

**Goal:** Determine if AI is the right solution and scope the project.

| Activity | AI-Specific Considerations |
|---|---|
| Problem framing | Is this a classification, regression, generation, or reasoning problem? Can it be solved with a simpler heuristic or rule-based system? |
| Feasibility analysis | Assess data availability, quality, and accessibility. Evaluate model performance baselines (e.g., human-level baseline, simple heuristic). |
| ROI estimation | Account for data labeling costs, compute infrastructure, MLOps tooling, and ongoing monitoring. |
| Risk assessment | Identify fairness, bias, regulatory (e.g., GDPR, EU AI Act), and safety risks. |
| Build vs. buy vs. fine-tune | Evaluate using an API (e.g., GPT-4, Claude), fine-tuning an open-source model, or training from scratch. |

**Key artifacts:** AI Project Charter, Feasibility Report, Data Landscape Assessment.

---

## 2. Requirements Definition

**Goal:** Translate business needs into functional and non-functional requirements for the AI system.

| Requirement Type | Examples |
|---|---|
| Functional | Expected input/output formats, supported use cases, latency targets (P50/P95), accuracy/precision/recall thresholds. |
| Data | Volume, freshness, labeling schema, data source SLAs, privacy compliance (PII scrubbing, anonymization). |
| Model | Inference speed, explainability (SHAP, LIME), versioning, reproducibility. |
| Infrastructure | GPU/TPU requirements, deployment SKU (GlobalStandard, Provisioned Managed), autoscaling rules. |
| Governance | Content filtering (RAI policy), human-in-the-loop thresholds, audit logging, bias monitoring. |

**Key artifacts:** PRD (Product Requirements Document), Model Card template, RAI Impact Assessment.

---

## 3. Architecture & Design

**Goal:** Design the system architecture including data pipelines, model serving, and application integration.

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Data Layer  │────▶│   AI Layer   │────▶│  App Layer   │
│ (Ingestion,  │     │ (Training,   │     │ (Inference,  │
│  Storage,    │     │  Evaluation, │     │  Orchestration,
│  Feature     │     │  Serving)    │     │  UX)         │
│  Store)      │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
```

| Component | AI-Specific Patterns |
|---|---|
| Data pipeline | Batch vs. streaming ingestion, feature store (Feast, Tecton), data versioning (DVC, lakeFS). |
| Model registry | MLflow, Weights & Biases, or custom registry for experiment tracking. |
| Inference serving | Real-time (REST/gRPC), batch inference, edge deployment. Caching (semantic cache). |
| RAG systems | Chunking strategy, embedding model, vector database (Pinecone, Qdrant, Cosmos DB), retrieval re-ranking. |
| Agent orchestration | Multi-agent topologies (supervisor, round-robin, DAG), tool execution, memory (short-term, persistent). |
| Monitoring | Model drift detection (data drift, concept drift), performance degradation alerts, cost tracking. |

**Key artifacts:** Architecture Decision Record (ADR), Data Flow Diagram, Model Architecture Spec, Deployment Topology.

---

## 4. Data Acquisition & Preparation

**Goal:** Collect, clean, label, and version the data required for model training and evaluation.

| Phase | Activities |
|---|---|
| Collection | Identify sources (internal DBs, APIs, web crawl, synthetic generation). Establish data SLAs. |
| Cleaning | Deduplication, outlier removal, missing value handling, format normalization. |
| Labeling | Human annotation (scale via labeling platforms), programmatic labeling (snorkel, weak supervision), synthetic data generation. |
| Augmentation | Data augmentation for robustness (rotation, noise injection, paraphrasing for NLP). |
| Splitting | Train/validation/test splits (stratified, temporal for time-series). |
| Versioning | DVC or similar for dataset versioning; hash-based data lineage. |

**Key artifacts:** Dataset Catalog, Labeling Guidelines, Data Splits Report, Data Version Manifest.

---

## 5. Model Development & Experimentation

**Goal:** Implement, train, and iterate on models in a reproducible manner.

| Step | Description |
|---|---|
| Baseline | Establish a simple baseline (rule-based, linear model) to beat. |
| Prototyping | Iterate on model architecture, hyperparameters, prompt engineering, retrieval strategies. |
| Experiment tracking | Log every run: hyperparameters, metrics, code version, dataset version, environment. |
| Prompt engineering | For LLMs: chain-of-thought, few-shot examples, system prompts, structured output parsing. |
| Fine-tuning | SFT (supervised fine-tuning), DPO (direct preference optimization), LoRA/QLoRA for efficient fine-tuning. |
| Evaluation | Hold-out validation, cross-validation, human eval, LLM-as-judge (e.g., GPT-4 eval). |

**Key artifacts:** Experiment Tracker (MLflow/W&B), Model Cards, Evaluation Reports.

---

## 6. Evaluation & Validation

**Goal:** Rigorously evaluate model performance, safety, and fairness before production deployment.

| Evaluation Type | Metrics / Methods |
|---|---|
| Task performance | Accuracy, F1, BLEU, ROUGE, METEOR (NLP); precision/recall (classification); RMSE/MAE (regression). |
| Safety & robustness | Adversarial testing, out-of-distribution detection, jailbreak attempts (red-teaming). |
| Fairness & bias | Demographic parity, equal opportunity, disparate impact analysis across sensitive attributes. |
| Explainability | SHAP/LIME values, attention visualization, feature importance. |
| RAG quality | Faithfulness, answer relevance, context precision/recall (RAGAS framework). |
| LLM-specific | Hallucination rate, refusal rate, instruction adherence, tone/style consistency. |

**Key artifacts:** Evaluation Report, Bias Audit, Red-Teaming Results, RAI Review Sign-off.

---

## 7. Deployment

**Goal:** Package and deploy the model into production with appropriate infrastructure.

| Deployment Pattern | Description |
|---|---|
| Real-time API | Model behind REST/gRPC endpoint with autoscaling (e.g., Azure OpenAI PTU, GlobalStandard). |
| Batch inference | Scheduled or event-triggered batch processing (e.g., Spark, Azure ML batch endpoints). |
| Edge deployment | ONNX, TensorRT, or quantized models on edge devices. |
| A/B testing | Deploy shadow (log-only) or canary (traffic split) variants for safe rollout. |
| Blue/Green | Maintain two environments; switch traffic after validation. |

**Key artifacts:** Deployment Manifest, Rollback Plan, Runbook, Infrastructure-as-Code (Terraform, Bicep).

---

## 8. Monitoring & Operations

**Goal:** Continuously monitor model health, data quality, and business impact in production.

| Monitoring Type | What to Track |
|---|---|
| Model performance | Accuracy, latency, throughput, error rates (by segment). |
| Data drift | Feature distribution shifts (PSI, KL divergence), missing values, new categories. |
| Concept drift | Degradation of prediction quality over time (ground-truth feedback loop). |
| Cost | Inference cost per request, compute utilization, API token consumption. |
| Safety | Content filter trigger rates, user flag/complaint rates, policy violation counts. |
| BI/Analytics | Business KPIs impacted by model (conversion, retention, revenue). |

**Key artifacts:** Monitoring Dashboard, Alert Rules & Thresholds, Incident Response Plan.

---

## 9. Maintenance & Iteration

**Goal:** Continually improve the system through retraining, fine-tuning, and architectural updates.

| Activity | Frequency |
|---|---|
| Model retraining | Scheduled (weekly/monthly) or trigger-based (drift detected). |
| Data refresh | Update training data with new production data (data flywheel). |
| Prompt tuning | Iterate on system prompts based on production feedback. |
| A/B test promotion | Promote winning variant to 100% traffic. |
| Dependency updates | Update SDKs, model versions, infrastructure patches. |
| Compliance reviews | Periodic RAI audits, regulatory filings (EU AI Act conformity). |

**Key artifacts:** Model Version Changelog, Retraining Pipeline, Post-Deployment Monitoring Report.

---

## 10. Governance & Compliance (Cross-Cutting)

**Goal:** Ensure responsible AI practices throughout the entire lifecycle.

| Governance Area | Practices |
|---|---|
| Model inventory | Centralized registry of all deployed models with metadata (owner, version, status). |
| Approval gates | Stage gates: Technical Review, RAI Review, Legal/Compliance Review before production. |
| Audit trail | Immutable logs of all model versions, training data, evaluation results, and deployment changes. |
| RAI policy | Content filters, jailbreak detection, protected material detection, groundedness checks. |
| Regulatory compliance | GDPR (right to explanation), EU AI Act (risk classification), HIPAA (PHI handling), SOC 2. |

**Key artifacts:** Model Governance Policy, RAI Policy Configuration, Audit Logs, Compliance Certifications.

---

## Comparison: Traditional SDLC vs. AI SDLC

| Aspect | Traditional SDLC | AI SDLC |
|---|---|---|
| Determinism | Code is deterministic; same input → same output | Models are probabilistic; same input may vary |
| Testing | Unit/integration tests cover logic paths | Evaluation requires statistical validation, hold-out datasets, and human judgment |
| Debugging | Breakpoints and stack traces | Requires experiment tracking, data lineage, and model interpretability tools |
| Requirements | Fixed and specifiable upfront | Often emergent; performance depends on data quality |
| Deployment | Single artifact (compiled binary) | Multiple artifacts: model weights, tokenizer, preprocessing pipeline, inference code |
| Maintenance | Bug fixes and feature updates | Data drift monitoring, retraining, prompt engineering, concept drift |
| Risk | Logic errors, security vulnerabilities | Bias, hallucinations, safety violations, regulatory non-compliance |

---

## Recommended AI SDLC Process Flow

```
1. Plan & Feasibility ───────────────► 2. Requirements ─────────────────► 3. Architecture & Design
                                         │                                         │
                                         ▼                                         ▼
                                 4. Data Acquisition ─────────────────► 5. Model Development
                                         │                                         │
                                         ▼                                         ▼
                                 6. Evaluation & Validation ──────────► 7. Deployment
                                         │                                         │
                                         ▼                                         ▼
                                 8. Monitoring & Operations ◄───────── 9. Maintenance & Iteration
                                                                                │
                                                                                ▼
                                                         10. Governance & Compliance (Cross-Cutting)
```

Each phase feeds back into earlier ones — AI SDLC is inherently iterative, especially between Data Preparation, Model Development, and Evaluation.

---

## References

- Microsoft Responsible AI Standard (v2)
- EU AI Act Risk Categories
- NIST AI Risk Management Framework
- Google MLOps: Continuous Delivery and Automation Pipelines in Machine Learning
- Amazon Well-Architected Framework — Machine Learning Lens
