# Tool Shortlisting Workflow

A repeatable, stage-gated process for organizations to go from the broad tool landscape to a vetted shortlist, with iteration loops where needed.

---

## 1. Overview

**Purpose:** Systematically narrow the wide field of AI tools and platforms (`Tools_To_Consider.md`) to a justified shortlist using the evaluation criteria from `AI_Tool_Selection_Strategy.md`, accounting for organizational context, constraints, and real-world validation.

**When to use this workflow:**
- Selecting a model serving platform (e.g., vLLM vs. Triton vs. SageMaker)
- Choosing an LLM provider (e.g., Azure OpenAI vs. Anthropic vs. self-hosted)
- Evaluating MLOps / AI platforms (e.g., MLflow vs. Weights & Biases vs. Vertex AI)
- Procuring vector databases, observability tools, or AI gateways

**Audience:**
- **Engineering / ML teams** — hands-on evaluation, POC execution, technical scoring
- **Engineering Managers / Directors** — scoring oversight, decision gates
- **Procurement / Vendor Management** — RFx process, commercial negotiation, licensing
- **Legal / Compliance** — regulatory review, data privacy agreement, contract terms
- **CTO / VP Engineering** — final approval, strategic alignment

**Organizational Contexts:**

| Context | Characteristics |
|---|---|
| **Enterprise** | Formal procurement gates, vendor panel, legal review, MSA negotiation |
| **Startup / Speed-Run** | Lightweight criteria, founder/CTO decides, minimal bureaucracy |
| **Mid-Size / Growth** | Balance of rigor and speed, PM + engineering lead decide |
| **Regulated Industry** | Compliance sign-off (HIPAA, PCI-DSS, EU AI Act), data residency |
| **Government / Public Sector** | Security clearance, FedRAMP, on-prem requirement, procurement law |

---

## 2. Workflow Diagram

```
                         ┌─────────────────────────────────────────┐
                         │  1. Business Need & Requirements Defn   │
                         │  (Problem framing, constraints, budget) │
                         └─────────────────┬───────────────────────┘
                                           ▼
                         ┌─────────────────────────────────────────┐
                         │  2. Initial Scan & Filtering (Knockout) │
                         │  Longlist: 10–15 tools                  │
                         └─────────────────┬───────────────────────┘
                                           ▼
 ┌──────────────────────────┐  ┌─────────────────────────────────────────┐
 │ D) Market / version      │  │  3. Weighted Scoring (Evaluation Matrix)│
 │    change triggers re-   │  │  Shortlist: 3–5 tools                   │
 │    scan                  │  └─────────────────┬───────────────────────┘
 └──────────────────────────┘                    ▼
 ┌──────────────────────────┐  ┌─────────────────────────────────────────┐
 │ A) POC fails → re-score │  │  4. Proof of Concept                    │
 │ B) All fail → re-scan    │  │  (1–2 week hands-on eval)              │
 │ C) No tool → re-assess   │  │  Champions: 1–2 tools                  │
 │ E) Req change → redef    │  └─────────────────┬───────────────────────┘
 └──────────────────────────┘                    ▼
                         ┌─────────────────────────────────────────┐
                         │  5. Final Decision & Governance Sign-off│
                         │  (TCO, legal, stakeholder alignment)    │
                         │  Selected: 1 tool                       │
                         └─────────────────────────────────────────┘
```

### Iteration Paths

| Loop | Trigger | Action |
|---|---|---|
| **A** | POC fails for all shortlisted tools | Return to Stage 3 — pull next ranked tools from the longlist, re-score |
| **B** | No tools in Stage 3 score above threshold | Return to Stage 2 — broaden scan, relax non-critical knockout criteria |
| **C** | No tools pass Stage 2 knockout | Return to Stage 1 — revisit build vs. buy, adjust budget/compliance constraints |
| **D** | Major vendor change (pricing, deprecation, license update) | Trigger Stage 2 re-scan of the affected category |
| **E** | Requirements change mid-process | Return to Stage 1 — update requirements brief, adjust weights in Stage 3 |

---

## 3. Stage 1: Business Need & Requirements Definition

**Goal:** Define the problem, constraints, and must-have criteria before looking at any tools.

| Activity | Description |
|---|---|
| Problem framing | What SDLC phase(s) need tooling? (Model dev, deployment, monitoring, etc.) |
| Stakeholder mapping | Who evaluates, who decides, who signs off? |
| Must-have vs. nice-to-have | Categorize criteria into knock-out vs. weighted scoring |
| Constraint identification | Budget range, timeline, team size, compliance requirements |
| Context setup | Apply the relevant organizational context template |

**Output:** Requirements Brief (1–2 pages)

**Timeline by context:**
| Context | Duration |
|---|---|
| Enterprise | 1–2 weeks |
| Startup | 1–2 days |
| Mid-Size | 3–5 days |
| Regulated | 2–3 weeks |
| Government | 3–4 weeks |

### Template: Requirements Brief

```
Project / Initiative: ________________________________________
SDLC Phase(s) Covered: ______________________________________
Key Stakeholders: ___________________________________________
Budget Range: $_______________
Timeline: ____________________
Compliance Requirements: ____________________________________

Must-Have Criteria:
1. __________________________________________________________
2. __________________________________________________________
3. __________________________________________________________

Nice-to-Have Criteria:
1. __________________________________________________________
2. __________________________________________________________
3. __________________________________________________________
```

---

## 4. Stage 2: Initial Scan & Filtering (Pass/Fail Knockout)

**Goal:** Rapidly filter the broad tool landscape to a manageable longlist (10–15) using objective knockout gates.

| Step | Description |
|---|---|
| Catalog lookup | Reference `Tools_To_Consider.md`; filter by SDLC phase and problem type |
| Knockout gates | Apply pass/fail against must-have criteria |
| Market scan supplement | Add newer or niche tools not in the catalog (optional) |
| Longlist compilation | Document 10–15 surviving tools with a one-line rationale per tool |

### Common Knockout Criteria

| Criterion | Description |
|---|---|
| Compliance | No SOC 2 / HIPAA / FedRAMP cert (when required) |
| Deployment model | No on-prem / VPC option (when required) |
| Budget ceiling | Exceeds per-unit or annual budget threshold |
| Integration | No SDK or REST API for target language |
| Team capacity | Requires rare skill the team lacks |
| Vendor viability | Startup risk, no clear roadmap, history of churn |

**Output:** Longlist (10–15 tools) with knockout rationale

**Timeline by context:**
| Context | Duration |
|---|---|
| Enterprise | 1 week |
| Startup | 4–6 hours |
| Mid-Size | 2–3 days |
| Regulated | 1–2 weeks |
| Government | 2–3 weeks |

### Template: Longlist Tracker

```
| # | Tool Name       | SDLC Phase   | Pass/Fail | Knockout Reason (if Fail)           | Notes                             |
|---|-----------------|--------------|-----------|-------------------------------------|-----------------------------------|
| 1 | Tool A          | Model Dev    | PASS      | —                                   | Strong eval framework, good docs  |
| 2 | Tool B          | Monitoring   | FAIL      | No SOC 2 cert                       | Revisit if cert obtained          |
| 3 | Tool C          | Deployment   | PASS      | —                                   | Budget borderline, check pricing  |
| 4 | Tool D          | Model Dev    | FAIL      | No Python SDK                       |                                   |
| 5 | Tool E          | Monitoring   | PASS      | —                                   | Open-source, active community     |
```

---

## 5. Stage 3: Weighted Scoring (Shortlist)

**Goal:** Score longlist tools using the Evaluation Matrix from `AI_Tool_Selection_Strategy.md` and select top 3–5 for POC.

| Step | Description |
|---|---|
| Define weights | Assign 1–5 weight to each criterion based on project priority |
| Score each tool | Score 1–5 per criterion; compute weighted totals |
| Gap analysis | Identify deal-breakers per tool |
| Rank & cut | Select top 3–5 tools for hands-on evaluation |

### Evaluation Criteria & Weight Guidance

| Criterion | Description | Enterprise | Startup | Mid-Size | Regulated | Gov |
|---|---|---|---|---|---|---|
| Performance / Accuracy | Task-specific eval results | 4 | 5 | 5 | 5 | 5 |
| Pricing Model | Predictability, scalability | 4 | 5 | 4 | 3 | 3 |
| Latency & Throughput | P50/P95, autoscaling | 3 | 4 | 4 | 4 | 4 |
| Security & Compliance | SOC 2, HIPAA, GDPR, FedRAMP | 5 | 2 | 4 | 5 | 5 |
| Data Privacy | No training on customer data, on-prem option | 4 | 2 | 3 | 5 | 5 |
| Portability | Open formats (ONNX, GGUF), no lock-in | 3 | 3 | 3 | 4 | 5 |
| Ecosystem | Native integrations (vector DBs, monitoring, CI/CD) | 3 | 4 | 3 | 3 | 3 |
| Integration Readiness | SDK quality, API completeness, auth setup effort | 4 | 5 | 4 | 4 | 4 |
| Business Alignment | Strategic fit, roadmap alignment, contract flexibility | 5 | 3 | 4 | 4 | 4 |
| Support & Community | SLA, documentation, community, MSA terms | 5 | 3 | 4 | 4 | 5 |
| RAI & Safety Tooling | Content filters, jailbreak detection, bias auditing | 3 | 2 | 3 | 5 | 4 |

**Output:** Shortlist (3–5 tools) with weighted scores and gap analysis

**Timeline by context:**
| Context | Duration |
|---|---|
| Enterprise | 1–2 weeks |
| Startup | 1 day |
| Mid-Size | 3–5 days |
| Regulated | 2 weeks |
| Government | 2–3 weeks |

### Template: Weighted Scoring Matrix

```
| Criterion                    | Weight | Tool A | A-Wtd | Tool B | B-Wtd | Tool C | C-Wtd |
|------------------------------|--------|--------|-------|--------|-------|--------|-------|
| Performance / Accuracy       | 5      | 4      | 20    | 5      | 25    | 3      | 15    |
| Pricing Model                | 3      | 5      | 15    | 2      | 6     | 4      | 12    |
| Latency & Throughput         | 4      | 3      | 12    | 4      | 16    | 4      | 16    |
| Security & Compliance        | 4      | 3      | 12    | 5      | 20    | 4      | 16    |
| Data Privacy                 | 3      | 4      | 12    | 4      | 12    | 3      | 9     |
| Portability                  | 2      | 3      | 6     | 3      | 6     | 5      | 10    |
| Ecosystem                    | 3      | 4      | 12    | 4      | 12    | 3      | 9     |
| Integration Readiness        | 4      | 4      | 16    | 4      | 16    | 3      | 12    |
| Business Alignment           | 4      | 5      | 20    | 3      | 12    | 4      | 16    |
| Support & Community          | 3      | 4      | 12    | 4      | 12    | 3      | 9     |
| RAI & Safety Tooling         | 2      | 3      | 6     | 4      | 8     | 2      | 4     |
|------------------------------|--------|--------|-------|--------|-------|--------|-------|
| **Total**                    | **37** |        | **143**|      | **145**|      | **128**|
| **Normalized (%)**           |        |        | **77%**|      | **78%**|      | **69%**|
```

---

## 6. Stage 4: Proof of Concept

**Goal:** Hands-on evaluation of shortlisted tools against a representative use case to validate real-world fit.

| Step | Description |
|---|---|
| Define POC scope | Specific task, dataset, success criteria, evaluation period |
| Set up environment | Sandbox / trial account; allocate compute and data |
| Run evaluation | Hands-on testing; measure against success criteria (1–2 weeks) |
| Document findings | Per-tool report: strengths, weaknesses, surprises, effort required |
| Rank & recommend | Pass / Fail per tool; recommend champion (1 tool) and alternate (1 tool) |

### POC Success Criteria Examples

| Criterion | Target Example |
|---|---|
| Accuracy | ≥ 90% on held-out eval set |
| Latency P95 | ≤ 500ms at expected load |
| Cost | ≤ $X per 1K inferences |
| Integration effort | ≤ 2 engineering-weeks to MVP integration |
| Developer experience | Team satisfaction rating ≥ 4/5 |
| Reliability | Zero hard failures during 1-week evaluation |

**Output:** POC Report per tool; Champion + Alternate recommendation

**Timeline by context:**
| Context | Duration |
|---|---|
| Enterprise | 2–4 weeks |
| Startup | 3–5 days |
| Mid-Size | 1–2 weeks |
| Regulated | 3–4 weeks |
| Government | 4–6 weeks |

### Template: POC Report

```
Tool Name: ___________________________________________________
Version Evaluated: ___________________________________________
Evaluation Period: ___________________________________________
Evaluator(s): ________________________________________________

Success Criteria & Results:
  Criterion 1 (Target → Actual): _________ → _________
  Criterion 2 (Target → Actual): _________ → _________
  Criterion 3 (Target → Actual): _________ → _________
  Criterion 4 (Target → Actual): _________ → _________

Strengths Observed:
  • __________________________________________________________
  • __________________________________________________________

Weaknesses / Risks:
  • __________________________________________________________
  • __________________________________________________________

Unexpected Findings:
  • __________________________________________________________

Integration Complexity:
  Estimated engineering effort: _________ weeks
  Identified blockers:
  • __________________________________________________________

Recommendation: [ Champion / Alternate / Pass / Fail ]
```

---

## 7. Stage 5: Final Decision & Governance Sign-off

**Goal:** Validate TCO, secure approvals, and document the final decision with rationale.

| Step | Description |
|---|---|
| TCO validation | Refine cost projection from Stage 1 with real POC data |
| Legal & compliance review | Contract terms, DPA, SLA review, data residency check |
| Stakeholder alignment | Present findings to engineering, product, procurement, leadership |
| Sign-off | Obtain formal approval per organizational delegation matrix |
| Decision record | Document rationale, rejected alternatives, lessons learned |

### Context-Specific Sign-off Requirements

| Context | Required Approvals |
|---|---|
| **Enterprise** | VP Engineering, Procurement, Legal, Finance |
| **Startup** | CTO / CEO (informal sign-off) |
| **Mid-Size** | Engineering Director + Product Manager |
| **Regulated** | Engineering Lead + Compliance Officer + CISO + Legal |
| **Government** | Procurement Officer + Security Officer + Legal + Agency Head |

**Output:** Final Tool Selection Document

**Timeline by context:**
| Context | Duration |
|---|---|
| Enterprise | 2–3 weeks |
| Startup | 1–2 days |
| Mid-Size | 1 week |
| Regulated | 3–4 weeks |
| Government | 4–6 weeks |

### Template: Final Decision Record

```
Decision Title: ______________________________________________
Date: ____________________
Decision Maker(s): __________________________________________

Selected Tool: ______________________________________________
Alternate(s): ________________________________________________
Rejected Tools (with reason):
  1. _________________________________________________________
  2. _________________________________________________________
  3. _________________________________________________________

TCO Summary (Year 1):
  Licensing / API:     $_______________
  Infrastructure:      $_______________
  Personnel:           $_______________
  Total Year 1:        $_______________

Approvals:
  [ ] Engineering Lead
  [ ] Product Owner
  [ ] Procurement
  [ ] Legal / Compliance
  [ ] CISO / Security
  [ ] Executive Sponsor

Lessons Learned / Notes for Next Evaluation:
  • __________________________________________________________
  • __________________________________________________________
```

---

## 8. Total Timeline by Context

| Context | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Stage 5 | **Total** |
|---|---|---|---|---|---|---|
| **Enterprise** | 1–2 wks | 1 wk | 1–2 wks | 2–4 wks | 2–3 wks | **7–12 wks** |
| **Startup** | 1–2 days | 4–6 hrs | 1 day | 3–5 days | 1–2 days | **1–2 wks** |
| **Mid-Size** | 3–5 days | 2–3 days | 3–5 days | 1–2 wks | 1 wk | **4–6 wks** |
| **Regulated** | 2–3 wks | 1–2 wks | 2 wks | 3–4 wks | 3–4 wks | **11–15 wks** |
| **Government** | 3–4 wks | 2–3 wks | 2–3 wks | 4–6 wks | 4–6 wks | **15–22 wks** |

---

## 9. Context Adaptation Reference

| Aspect | Enterprise | Startup | Mid-Size | Regulated | Government |
|---|---|---|---|---|---|
| **Decision velocity** | Slow (committees, procurement panels) | Fast (founder / CTO-led) | Moderate | Slow | Very slow |
| **Primary gate** | Procurement panel approval | Cost + time-to-market | Eng + PM alignment | Compliance sign-off | Security clearance + procurement law |
| **Top-weighted criteria** | Support/SLA, Business Alignment, Security | Ease of use, Speed of integration, Pricing | Balanced across dimensions | Compliance, Data Privacy, RAI | On-prem, FedRAMP, Data Sovereignty |
| **Documentation rigor** | Heavy (RFI, RFP, vendor presentations) | Lightweight (spreadsheet + decision memo) | Moderate (scoring matrix + POC report) | Heavy + auditable | Extremely heavy (legal + security docket) |
| **Vendor negotiation** | Formal RFP, MSA negotiation, enterprise agreement | Self-serve sign-up / credit card | Term sheet + email negotiation | DPA + BAA + data residency addendum | FedRAMP ATO, TAA compliance |
| **POC depth** | 2–4 weeks, formal success criteria | 3–5 days, targeted | 1–2 weeks | 3–4 weeks + security review | 4–6 weeks + security audit |
| **Team involved** | DS, MLE, Eng, Procurement, Legal, Finance | Founder / CTO + 1–2 engineers | Eng Lead + PM + 1–2 engineers | DS, MLE, Compliance, Legal, CISO | Multi-agency, procurement, legal, security |

---

## References

- **`SDLC.md`** — SDLC phases for AI projects (the phases you are tooling for)
- **`Tools_To_Consider.md`** — Broad catalog of tools per SDLC phase (input to Stage 2)
- **`AI_Tool_Selection_Strategy.md`** — Evaluation criteria, build vs. buy framework, vendor categories (input to Stage 3)
