# Workflow Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how workflows are represented in the RAG Knowledge Model.

Workflows describe ordered, conditional or iterative execution structures that coordinate RAG components, models, tools, agents, retrieval steps, evaluation steps and human review.

The Workflow Model answers the question:

> **How is a RAG process organized from inputs to outputs, and which entities participate in each step?**

---

# Core Principle

A workflow is a first-class knowledge entity that models process structure.

It is not only prose about a system.

It captures the stages, steps, transitions, participants, inputs, outputs and control logic that make a RAG process reproducible, comparable and exportable as graph knowledge.

```text
Workflow CONTAINS Step
Workflow USES Component
Agent EXECUTES Workflow
Workflow EXECUTES Step
Workflow TRIGGERS Evaluation Step
```

---

# Workflow

A Workflow represents a repeatable process for performing part or all of a RAG system behavior.

A workflow may describe:

* ingestion
* parsing
* chunking
* embedding
* indexing
* query understanding
* retrieval
* reranking
* context assembly
* generation
* citation selection
* answer verification
* evaluation
* monitoring
* human review

Workflows may be conceptual, implementation-specific or operational.

---

# Workflow Boundary

Every workflow should define a clear boundary.

The boundary identifies:

* what starts the workflow
* what input artifacts the workflow consumes
* what output artifacts the workflow produces
* which responsibilities are inside the workflow
* which dependencies are outside the workflow

Preferred:

```text
Question answering workflow that starts with a user query and produces a grounded answer with citations.
```

Avoid:

```text
The full application does RAG.
```

The avoided statement does not define process scope, inputs, outputs or participants.

---

# Workflow Step

A Workflow Step is a unit of work inside a workflow.

A step may:

* transform data
* retrieve candidates
* call a model
* invoke a tool
* apply a filter
* route execution
* evaluate an intermediate artifact
* request human approval
* store or publish an output

Steps should be named with action-oriented language.

Examples:

```text
Parse Source Documents
Generate Embeddings
Retrieve Candidate Chunks
Rerank Candidates
Assemble Context
Generate Grounded Answer
Verify Citations
```

---

# Step Identity

Workflow steps should have stable local identifiers when they are referenced by transitions, evidence, claims or examples.

Example:

```json
{
  "id": "STEP-0001",
  "name": "Retrieve Candidate Chunks"
}
```

Step identifiers are local to the workflow unless promoted to first-class entities in a future model version.

---

# Participants

Workflow participants are entities that perform, support or govern steps.

Common participant entity types include:

* Component
* Agent
* Tool
* Framework
* Retriever
* Reranker
* Embedding Model
* Language Model
* Vector Database
* Graph Database
* Evaluation Metric
* Provider

Participants should be referenced by stable identifiers whenever possible.

---

# Inputs and Outputs

Workflows should model important inputs and outputs as structured artifacts.

Common workflow inputs include:

* user query
* source document
* parsed document
* chunk
* embedding vector
* metadata filter
* retrieval result
* conversation state
* policy constraint

Common workflow outputs include:

* indexed corpus
* ranked context
* assembled prompt
* generated answer
* citation set
* evaluation score
* trace record
* feedback signal

Inputs and outputs matter because they define interoperability between steps and components.

---

# Transitions

A transition describes how execution moves from one step to another.

Transitions may be:

* sequential
* conditional
* parallel
* iterative
* retry-based
* human-gated
* event-driven

Example:

```text
Retrieve Candidate Chunks THEN Rerank Candidates
```

Conditional example:

```text
If retrieval confidence is low, rewrite the query and retrieve again.
```

Transitions should be explicit when they affect correctness, latency, cost, safety or evaluation.

---

# Control Flow

Control flow describes the execution pattern of the workflow.

Canonical control flow types are:

```text
Linear
Branching
Parallel
Iterative
Event Driven
Human In The Loop
Agent Directed
Hybrid
```

The control flow type should describe the dominant execution structure, not every small implementation detail.

---

# Workflow Type

Workflow type describes the primary purpose of the workflow.

Canonical workflow types are:

```text
Ingestion Workflow
Indexing Workflow
Retrieval Workflow
Generation Workflow
Evaluation Workflow
Agent Workflow
Monitoring Workflow
Governance Workflow
End To End RAG Workflow
Other
```

Workflow type should be stable enough for search, filtering, graph export and documentation generation.

---

# Relationships

Workflows should use first-class relationships to connect process structure to the wider RKM graph.

Common workflow relationships include:

```text
Query Transformation PRECEDES Retrieval
Retrieval FOLLOWS Query Transformation
Agent EXECUTES Retrieval Workflow
Retrieval Workflow EXECUTES Retrieve Candidate Chunks
Low Retrieval Confidence TRIGGERS Corrective Retrieval
Query Router ROUTES_TO Hybrid Retriever
Evaluation Step BRANCHES_TO Retry Retrieval
Framework IMPLEMENTS Workflow
LangChain IMPLEMENTS Retrieval Workflow
```

Relationship direction should follow the canonical relationship model whenever a registered relationship type exists.

Predicates such as `INVOKES`, `COORDINATED_BY`, `IMPLEMENTED_BY` and `IS_IMPLEMENTED_BY` are noncanonical in the current relationship model. They may be considered future candidates or rejected examples, but current workflow examples should use canonical relationships such as `EXECUTES`, `TRIGGERS`, `ROUTES_TO`, `BRANCHES_TO` and `IMPLEMENTS`.

---

# Claims and Evidence

Workflow claims should be explicit when they describe behavior, performance, reliability, safety or tradeoffs.

Examples:

```text
This workflow reduces answer latency by skipping reranking when retrieval confidence is high.
```

```text
This workflow improves citation coverage by verifying generated citations against retrieved chunks.
```

Claims about workflow quality should link to evidence.

Evidence may come from:

* benchmark results
* experiment reports
* production traces
* official documentation
* papers
* implementation examples
* maintainer analysis

---

# Workflow vs Technique

A Technique describes a reusable method or approach.

A Workflow describes how steps are organized to execute a process.

Example:

```text
HyDE is a technique.
```

```text
A workflow may use HyDE during query transformation before retrieval.
```

The technique explains the method. The workflow explains the operational sequence.

---

# Workflow vs Component

A Component is a reusable building block.

A Workflow coordinates building blocks.

Example:

```text
A retriever is a component.
```

```text
A retrieval workflow may call a retriever, apply metadata filtering, rerank results and pass selected context to generation.
```

The component performs a role. The workflow defines how roles interact.

---

# Workflow vs Agent

An Agent can make decisions, select tools, plan steps or coordinate execution.

A Workflow can be static, agent-directed or partly agent-directed.

Example:

```text
An agent may coordinate a workflow by selecting retrieval tools and deciding whether to request another retrieval pass.
```

The agent is a participant. The workflow is the process structure in which the agent participates.

---

# Agentic RAG Workflows

An agentic RAG workflow is a workflow whose control flow depends on agent decisions about retrieval, tool use, evidence gathering, verification or stopping conditions.

Model an agentic RAG workflow when the process structure matters independently from the agent entity. The workflow should describe the ordered, conditional or iterative execution pattern; the agent should describe the bounded decision-making capability that participates in that pattern.

Agentic RAG workflow structure should make these responsibilities explicit when they affect behavior, cost, latency, governance or evaluation:

* planning step that decomposes the user query, task goal or evidence need
* tool or retriever selection step that chooses among available retrieval capabilities
* retrieval step that gathers candidate evidence or context
* verification step that checks grounding, citation candidates, source quality or policy compliance
* loop or branch that decides whether to retrieve again, revise the query, rerank candidates, escalate to a human or stop
* answer or artifact production step that consumes the verified context

Retrieval loops should include their termination conditions. A loop that continues until sufficient evidence is found is not reproducible unless the workflow records the confidence threshold, maximum retrieval attempts, human approval point, policy rule or evaluation signal that stops the loop.

Tool use inside an agentic workflow should identify the tool categories, side-effect boundaries and participant roles involved in each step. Tool-selection behavior belongs to the Agent Model when it describes autonomy or decision policy; step order, transition conditions and workflow outputs belong to the Workflow Model.

Evidence use should distinguish gathered context from evidence that supports a claim about the workflow. Retrieved documents, chunks or citations may be workflow inputs or outputs. Evidence records are required when RKM asserts that the workflow improves quality, reduces hallucination, changes latency, satisfies a policy or supports another reusable claim.

Use canonical relationships when connecting agentic workflows to the rest of RKM:

```text
Agent EXECUTES Workflow
Workflow USES Retriever
Workflow OPTIONALLY_USES Reranker
Workflow USES Tool
Workflow TRIGGERS Evaluation Step
Evaluation Step BRANCHES_TO Retrieval Step
Framework IMPLEMENTS Workflow
```

Do not create a separate architecture document for agentic RAG workflows unless the repository first establishes a distinct entity type or contract for them. Until then, agentic behavior is modeled through the existing Agent Model, Workflow Model, Tool Model, Retrieval Model, Claim Model and Evidence Model.

---

# Workflow Granularity

Workflows should be modeled at the smallest level that remains useful.

Use a workflow when the sequence, control flow or participant coordination has reusable semantic meaning.

Avoid creating separate workflows for trivial implementation details that do not affect knowledge representation, evaluation, interoperability or reasoning.

---

# Graph Export

Workflows should support graph export.

At minimum, a graph export should preserve:

* workflow identity
* workflow type
* workflow steps
* participant references
* step order or transition structure
* inputs and outputs
* relationships to techniques, components, agents, tools and evaluation entities
* claims and evidence attached to the workflow

This allows RKM consumers to query process-level knowledge, not only isolated entities.

---

# Modeling Guidance

Model a workflow when:

* a process has multiple meaningful steps
* step order affects behavior
* conditional or iterative control flow matters
* several entities must be coordinated
* the workflow is described by a paper, framework, benchmark or implementation
* claims about quality, cost, latency, safety or reliability depend on process structure

Do not model a workflow when a simple relationship is sufficient.

Example:

```text
Framework SUPPORTS Retriever
```

This relationship does not require a workflow unless the supported behavior involves meaningful process structure.

---

# Schema Implications

The reusable embedded workflow definition is `schema/definitions/workflow.schema.json`.

That definition represents workflow structure inside another entity, evaluation, evidence record or architecture record. It intentionally omits the full Knowledge Entity envelope: first-class identity, metadata, description and top-level entity relationships remain responsibilities of the containing document.

Use the embedded definition when workflow structure is needed as supporting knowledge but the workflow is not yet an independently managed entity.

A future first-class workflow schema should compose the common Knowledge Entity envelope and add workflow-specific structured knowledge.

Expected workflow-specific fields include:

* workflow type
* control flow type
* supported RAG stages
* inputs
* outputs
* steps
* transitions
* participants
* operational characteristics
* safety considerations
* limitations
* usage guidance

Before a specialized top-level workflow schema is introduced, the shared identity model and entity type registry must support `Workflow` as an allowed entity type. The specialized schema should then reuse or compose the embedded workflow definition for the workflow-specific structure instead of creating a parallel contract.
