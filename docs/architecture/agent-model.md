# Agent Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how agents are represented in the RAG Knowledge Model.

Agents are knowledge-bearing entities that can plan, select tools, coordinate retrieval, invoke models, evaluate intermediate results or execute workflows in a RAG system.

The Agent Model answers the question:

> **What decision-making capability participates in a RAG process, and how should its autonomy, roles, tool use, memory and control policy be represented?**

---

# Core Principle

An agent is a first-class knowledge entity when its decision-making behavior affects retrieval quality, grounding, workflow execution, cost, latency, safety or governance.

An agent is not only a prompt, a model, a workflow or a framework feature.

It represents a bounded capability that observes state, chooses actions and produces outputs under explicit constraints.

```text
Agent USES Language Model
Agent USES Retriever
Agent EXECUTES Workflow
Agent DEPENDS_ON Component
Agent GOVERNED_BY Policy
Benchmark EVALUATES Agent
```

Representing agents explicitly makes agentic RAG behavior easier to compare, evaluate, govern and export as graph knowledge.

---

# Agent

An Agent represents a bounded decision-making capability in a RAG system.

An agent may:

* rewrite or decompose a user query
* plan retrieval steps
* select a retriever, reranker, model or tool
* gather and verify context
* assemble evidence for generation
* generate or revise an answer
* evaluate grounding or citation quality
* coordinate multiple specialized agents
* execute a workflow with human supervision

The agent should be modeled when its decision process has reusable semantic meaning.

Preferred:

```text
Retriever-selection agent that chooses between dense, sparse and hybrid retrieval based on query type and available metadata.
```

Avoid:

```text
Smart RAG agent.
```

The avoided statement does not define the agent boundary, responsibility or decision behavior.

---

# Agent Boundary

Every agent should define a clear boundary.

The boundary identifies:

* what goals or inputs the agent receives
* what decisions the agent is allowed to make
* which tools, models, components or workflows it may use
* what memory or intermediate state it may read or write
* what outputs it may produce
* where human approval, policy or guardrails constrain behavior

Agent boundaries matter because the same language model can behave differently when embedded in different planning loops, tool-use policies or workflow contexts.

---

# Agent Type

Agent type describes the primary architectural form of the agent.

Canonical agent types include:

```text
Single Agent
Multi Agent System
Planner Agent
Executor Agent
Retriever Agent
Router Agent
Evaluator Agent
Critic Agent
Tool Using Agent
Workflow Agent
Conversational Agent
Other
```

The agent type should describe the dominant role. More detailed behavior should be represented through RAG roles, relationships, claims, evidence and structured agent fields.

---

# Autonomy Level

Autonomy level describes the degree of independent decision-making expected from the agent.

Canonical autonomy levels include:

```text
None
Low
Medium
High
Human Supervised
Variable
Unknown
```

Autonomy should not be inferred from marketing language alone.

Claims about autonomous planning, tool selection, self-correction or human supervision should cite evidence when those claims affect selection, safety or governance.

---

# RAG Roles

RAG roles describe the responsibilities an agent performs or coordinates in a RAG system.

Common RAG roles include:

* query understanding
* query planning
* retrieval planning
* retriever selection
* tool selection
* context gathering
* context verification
* context assembly
* answer generation
* grounding verification
* citation selection
* evaluation
* workflow orchestration
* user interaction
* monitoring

RAG roles should be precise enough to distinguish an agent that merely calls a retriever from an agent that plans retrieval strategy, evaluates retrieved context and revises the plan.

---

# Planning

Planning describes how an agent decomposes goals, sequences actions or revises decisions.

Important planning knowledge includes:

* planning mode
* planning horizon
* whether intermediate state is used
* whether human approval is required
* whether replanning is supported
* which workflow or policy constrains the plan

Planning should be represented when it affects correctness, cost, latency, reproducibility or safety.

For example, an iterative replanning agent that retrieves additional evidence after detecting weak grounding should be distinguishable from a static workflow agent that follows a fixed sequence.

---

# Tool Use

Tool use describes how an agent selects and invokes callable capabilities.

Important tool-use knowledge includes:

* tool selection mode
* tool invocation mode
* allowed tool categories
* forbidden tool categories
* side-effect permissions
* error handling behavior
* retry behavior

Tool use is especially important for agents that can mutate state, call external systems, retrieve private data, publish artifacts or trigger operational workflows.

Tool-related claims should identify whether the agent selects tools itself, follows a deterministic rule, receives human-selected tools or uses a hybrid control policy.

---

# Memory and State

Memory describes state an agent uses across steps, turns or executions.

Memory may include:

* conversation history
* retrieved context
* intermediate plans
* tool outputs
* user preferences
* feedback signals
* evaluation traces

Memory should be modeled when it affects reproducibility, privacy, evaluation, grounding or user experience.

Short-lived workflow state should be distinguished from durable memory that persists across sessions or users.

---

# Retrieval Behavior

Retrieval behavior describes how an agent participates in retrieval-centered decisions.

An agent may:

* choose a retriever
* generate query variants
* decide when to rerank
* request additional evidence
* filter retrieved context
* verify citation candidates
* stop retrieval when confidence is sufficient

Retrieval behavior should be connected to Retriever, Reranker, Embedding Model, Vector Database, Graph Database, Dataset, Benchmark and Evaluation Metric entities through canonical relationships when those links carry reusable semantic value.

---

# Coordination

Coordination describes how an agent interacts with other agents, workflows and components.

Coordination may be:

* single-agent execution
* planner and executor separation
* multi-agent delegation
* critic or evaluator review
* human-supervised execution
* workflow-directed execution

Coordination should be explicit when it affects responsibility boundaries, observability, failure handling or evaluation.

For multi-agent systems, represent each agent as a separate entity when the roles, evidence, claims or relationships need independent tracking.

---

# Control Policy

Control policy describes constraints that govern agent behavior.

Control policies may define:

* allowed actions
* forbidden actions
* approval requirements
* retrieval limits
* tool-use limits
* grounding requirements
* citation requirements
* escalation conditions
* termination conditions

Control policy should be represented when it affects safety, compliance, operational reliability or evaluation.

Governance relationships should use canonical predicates when policies are modeled as separate entities.

Example:

```text
Agent GOVERNED_BY Policy
Agent REQUIRES Human Approval Component
Agent EXECUTES Workflow
```

---

# Inputs and Outputs

Agents should model important inputs and outputs structurally.

Common agent inputs include:

* user query
* task goal
* conversation state
* retrieved context
* candidate citations
* tool output
* policy constraint
* evaluation feedback

Common agent outputs include:

* retrieval plan
* selected retriever
* tool invocation request
* assembled context
* generated answer
* grounding judgment
* citation set
* evaluation finding
* workflow decision

Inputs and outputs should be specific enough that workflows and components can consume them without relying on prose-only interpretation.

---

# Evaluation

Agent evaluation should identify the behavior being evaluated and the context in which it was observed.

Useful evaluation targets include:

* retrieval planning quality
* answer faithfulness
* citation correctness
* tool-selection accuracy
* task completion
* cost and latency
* human approval rate
* failure recovery
* policy compliance

Agent evaluation should not collapse all behavior into a single success score when the agent performs multiple RAG roles.

Claims about agent quality should cite evidence and should be scoped to the workflow, dataset, benchmark, model version, tool set and control policy used during evaluation.

---

# Relationship Use

Agents should be connected through canonical relationships when those relationships have reusable semantic value.

Useful agent relationships include:

```text
Agent USES Language Model
Agent USES Retriever
Agent OPTIONALLY_USES Reranker
Agent EXECUTES Workflow
Agent DEPENDS_ON Component
Agent REQUIRES Provider
Framework SUPPORTS Agent
Framework PROVIDES Agent
Benchmark EVALUATES Agent
Evaluation Metric MEASURES Agent
Agent HAS_LIMITATION Limitation
Agent HAS_TRADEOFF Tradeoff
Agent HAS_USE_CASE Use Case
Agent GOVERNED_BY Policy
```

Relationship targets should use stable identifiers whenever those entities are represented in RKM.

Plain prose may explain an agent, but reusable dependencies, execution behavior, evaluation context and governance constraints should be represented structurally.

---

# Evidence and Claims

Claims about agents should be evidence-backed when they affect selection, trust, safety or operational use.

Examples of claims that should usually cite evidence include:

* an agent can select tools autonomously
* an agent improves retrieval quality
* an agent verifies grounding before answer generation
* an agent requires human approval for state-changing actions
* an agent can coordinate multiple retrievers or workflows
* an agent reduces hallucination in a defined evaluation setting
* an agent has a specific latency, cost or reliability profile

Evidence may come from documentation, papers, benchmark reports, evaluation runs, source code, release notes or observed behavior.

Implementation-specific claims should include version, configuration, tool set and workflow context when available.
