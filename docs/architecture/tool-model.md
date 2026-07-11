# Tool Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how tools are represented in the RAG Knowledge Model.

Tools are executable or callable capabilities that can be used by agents, workflows, frameworks, components or humans to perform bounded work in a RAG system.

The Tool Model answers the question:

> **What external or internal capability is invoked during a RAG process, and how should its boundary, inputs, outputs and governance be represented?**

---

# Core Principle

A tool is a first-class knowledge entity when its callable capability has reusable semantic meaning.

It is not only an implementation detail.

A tool may retrieve information, transform artifacts, call an external service, query a database, evaluate an answer, inspect a repository, trigger an action or expose operational state.

```text
Agent USES Tool
Workflow EXECUTES Tool
Tool EXPOSES Capability
Tool CONSUMES Artifact
Tool PRODUCES Artifact
Tool GOVERNED_BY Policy
```

Representing tools explicitly makes agent behavior, workflow dependencies, operational risk and evidence-backed capability claims easier to compare and export as graph knowledge.

---

# Tool

A Tool represents a bounded callable capability.

A tool may be:

* a function
* an API endpoint
* a command line utility
* a database query interface
* a search connector
* a retrieval service
* an evaluation harness
* an indexing job
* an observability query
* a human approval interface

A tool should have a clear invocation boundary.

Preferred:

```text
Search tool that accepts a query and returns ranked source snippets with references.
```

Avoid:

```text
Search.
```

The avoided statement does not identify the callable boundary, input or output.

---

# Tool Boundary

Every tool should define what is inside and outside the callable capability.

The boundary should identify:

* who or what may invoke the tool
* what inputs the tool accepts
* what outputs the tool returns
* what external systems the tool depends on
* what side effects the tool may produce
* what authorization or policy constraints apply

Tools with unclear boundaries are difficult to evaluate, govern and compose into workflows.

---

# Tool Type

Tool type describes the primary capability exposed by the tool.

Canonical tool types include:

```text
Search Tool
Retrieval Tool
Database Tool
Transformation Tool
Evaluation Tool
Indexing Tool
Monitoring Tool
Validation Tool
Generation Tool
Routing Tool
Connector Tool
Human Approval Tool
Operational Tool
Other
```

The tool type should describe the dominant capability, not every possible use.

---

# Invocation Mode

Invocation mode describes how the tool is called.

Canonical invocation modes include:

```text
Synchronous
Asynchronous
Streaming
Batch
Scheduled
Event Driven
Human Initiated
Agent Initiated
Workflow Initiated
Hybrid
```

Invocation mode matters because it affects latency, observability, retry behavior and workflow design.

---

# Inputs and Outputs

Tools should model important inputs and outputs structurally.

Common tool inputs include:

* user query
* rewritten query
* document identifier
* chunk identifier
* embedding vector
* metadata filter
* retrieval result
* prompt
* generated answer
* evaluation criterion
* approval request

Common tool outputs include:

* ranked results
* source references
* transformed document
* extracted metadata
* evaluation score
* validation finding
* generated artifact
* trace event
* approval decision

Inputs and outputs should be named precisely enough that a workflow step can consume or produce them without relying on prose-only interpretation.

---

# Side Effects

Some tools only return data.

Other tools change state.

State-changing effects may include:

* writing to an index
* updating a database
* sending a notification
* creating an audit record
* publishing generated content
* triggering a downstream workflow
* changing access controls

Side effects should be modeled explicitly when they affect safety, reproducibility, governance, cost or operational risk.

---

# Tool Contract

A tool contract describes the expected invocation surface.

A contract may include:

* input schema
* output schema
* required parameters
* optional parameters
* error modes
* timeout behavior
* retry behavior
* idempotency expectations
* authentication requirements

The contract should be represented when the tool participates in automated workflows or agentic behavior.

---

# Relationship Use

Tools should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Agent USES Tool
Workflow EXECUTES Tool
Framework PROVIDES Tool
Component EXPOSES Tool
Tool REQUIRES Provider
Tool DEPENDS_ON Component
Tool CONSUMES Dataset
Tool PRODUCES Evidence
Tool SUPPORTS Evaluation Metric
Tool GOVERNED_BY Policy
```

Relationship targets should use stable identifiers whenever those entities are represented in RKM.

Plain prose may explain a tool, but reusable dependency, execution, governance and output relationships should be represented structurally.

---

# Evidence and Claims

Claims about tools should be evidence-backed when they affect selection, trust or operational use.

Examples of claims that should usually cite evidence include:

* a tool supports a specific retrieval mode
* a tool integrates with a particular framework
* a tool requires a provider account
* a tool produces auditable traces
* a tool has a specific latency or cost profile
* a tool can mutate external state

Evidence may come from documentation, source code, papers, benchmark reports, release notes or observed behavior.

Implementation-specific claims should include version or observation context when available.

---

# Governance

Tools often cross system boundaries.

Governance information should be represented when a tool can access sensitive data, call external services, change state or trigger high-impact actions.

Important governance dimensions include:

* authorization
* authentication
* data access scope
* network access
* write access
* audit logging
* rate limits
* approval requirements
* policy constraints

Governance details should not be hidden in descriptions when they determine whether an agent or workflow may safely use the tool.

---

# Distinction From Component

A Component is an architectural building block.

A Tool is a callable capability.

The same real-world object may be represented as both when both meanings are useful.

Example:

```text
Vector Store Component
Vector Search Tool
```

The component represents the architectural role.

The tool represents the callable search capability exposed to an agent, workflow or framework.

---

# Distinction From Framework

A Framework provides abstractions, integrations or runtime structure.

A Tool is a bounded capability that can be invoked.

Example:

```text
Framework PROVIDES Tool
Agent USES Tool
```

Framework documentation may describe tool support, but the tool itself should be modeled separately when its inputs, outputs, side effects or governance need independent representation.

---

# Distinction From Workflow

A Workflow organizes ordered, conditional or iterative process structure.

A Tool performs a bounded callable action within that structure.

Example:

```text
Workflow EXECUTES Tool
Tool PRODUCES Evidence
```

A workflow may execute many tools.

A tool should not be used as a substitute for the workflow that coordinates it.

---

# Modeling Guidance

Model a tool as a first-class entity when:

* it is invoked by an agent or workflow
* it exposes a reusable capability
* it has meaningful inputs, outputs or side effects
* it introduces dependencies or governance constraints
* it is compared, evaluated or selected independently
* it has evidence-backed claims
* it participates in graph relationships

Do not model a tool as a first-class entity when it is only an internal helper with no reusable semantic value.

When uncertain, prefer modeling the capability only when it can be named, invoked, related and evidenced independently.
