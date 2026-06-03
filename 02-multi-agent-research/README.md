# Multi-Agent Research System

## Problem
Deep research on complex topics requires synthesizing information across multiple domains — a single LLM call is insufficient and lacks structured reasoning.

## Design
A multi-agent orchestration system where specialized agents (Planner, Searcher, Critic, Writer) collaborate via a supervisor agent using LangGraph.

## Architecture
- **Supervisor Agent**: Routes tasks, manages state, handles handoffs
- **Planner Agent**: Decomposes research questions into sub-tasks
- **Searcher Agent**: Retrieves information per sub-task
- **Critic Agent**: Evaluates quality, identifies gaps
- **Writer Agent**: Produces final synthesized output

## Best Practices
- Agent specialization with focused system prompts
- Human-in-the-loop checkpoints for critical decisions
- Shared memory across agent turns
- Structured output schemas for inter-agent communication

## Limitations
- High token cost from multi-turn agent loops
- Coordination overhead increases with agent count
- Error propagation if a single agent produces poor output
