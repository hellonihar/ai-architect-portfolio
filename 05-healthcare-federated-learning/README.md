# Healthcare Federated Learning

## Problem
Healthcare institutions cannot share patient data due to privacy regulations (HIPAA, GDPR), limiting the data available for robust ML models.

## Design
A federated learning framework where models train across hospital sites without raw data ever leaving each institution.

## Architecture
- **Client Nodes**: Each hospital trains locally on-premise
- **Aggregator Server**: Secure federated averaging of model weights
- **Privacy Layer**: Differential privacy + secure aggregation
- **Compliance**: Audit trail for each training round

## Best Practices
- Non-IID data handling strategies (FedProx, SCAFFOLD)
- Differential privacy budgeting across rounds
- Heterogeneous client support (different hardware/configs)
- Secure multi-party computation for weight aggregation

## Limitations
- Communication overhead for frequent aggregation rounds
- Model quality degradation with high privacy budgets
- Client drop-out resilience is complex
