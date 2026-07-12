# Component Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how components are represented in the RAG Knowledge Model.

Components are reusable architectural building blocks that perform bounded responsibilities inside RAG systems.

The Component Model answers the question:

> **What functional building block participates in a RAG system, and how should its role, boundaries, inputs, outputs and dependencies be represented?**

---

# Core Principle

A component is a first-class knowledge entity when it has reusable architectural meaning.

It is not only a class name, package name, service name or implementation detail.

A component may load documents, parse content, chunk text, generate embeddings, store vectors, retrieve candidates, rerank results, assemble context, build prompts, evaluate outputs, enforce guardrails or observe system behavior.

```text
Component CONSUMES Artifact
Component PRODUCES Artifact
Component TRANSFORMS Artifact
Component DEPENDS_ON Component
Component IMPLEMENTS Technique
Component SUPPORTS Workflow
```

Representing components explicitly makes RAG systems easier to compare, compose, evaluate and export as graph knowledge.

---

# Component

A Component represents a bounded functional unit in a RAG architecture.

A component may be:

* conceptual, such as a retriever or context assembler
* an interface, such as an embedding generator API
* an implementation, such as a vector store adapter
* a service, such as a managed retrieval endpoint
* infrastructure, such as a cache or telemetry collector
* a workflow-level unit, such as an ingestion stage coordinator

A component should have a clear responsibility and should be meaningful independently of one specific codebase.

Preferred:

```text
Context assembler that selects ranked retrieval results and formats them for prompt construction.
```

Avoid:

```text
Helper module.
```

The avoided statement does not define the responsibility, boundary or RAG role.

---

# Component Boundary

Every component should define what is inside and outside its responsibility.

The boundary should identify:

* inputs consumed by the component
* outputs produced by the component
* transformations performed by the component
* dependencies required by the component
* configuration that materially changes behavior
* quality attributes affected by the component
* operational risks introduced by the component

Clear boundaries prevent component entities from becoming vague containers for unrelated behavior.

---

# Component Type

Component type describes the primary architectural role of the component.

Canonical component types include:

```text
Document Loader
Parser
Chunker
Embedding Generator
Vector Store
Graph Store
Retriever
Reranker
Query Transformer
Prompt Builder
Context Assembler
Language Model
Router
Memory Store
Evaluator
Guardrail
Orchestrator
Cache
Telemetry
Tool
Other
```

The component type should describe the dominant role, not every entity it may interact with.

---

# RAG Stage Participation

Components should identify the RAG pipeline stages in which they participate.

Common stages include:

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
* evaluation
* orchestration
* monitoring

A component may participate in multiple stages when the same boundary has meaningful responsibilities across those stages.

For example, an orchestrator component may coordinate retrieval, generation and evaluation without replacing the specialized components that perform those steps.

---

# Inputs and Outputs

Components should model important inputs and outputs structurally when those values have reusable meaning.

Common component inputs include:

* source document
* parsed document
* chunk
* embedding vector
* user query
* rewritten query
* metadata filter
* retrieval candidate
* ranked result
* assembled context
* prompt
* generated answer
* evaluation criterion

Common component outputs include:

* extracted text
* chunk list
* embedding vector
* indexed record
* candidate result set
* reranked result list
* context package
* grounded prompt
* answer draft
* evaluation score
* validation finding
* trace event

Inputs and outputs should be precise enough that relationships to artifacts, workflows and tools can be interpreted without prose-only assumptions.

---

# Configuration

Important component configuration should be represented when it affects behavior, evaluation, cost or reproducibility.

Examples include:

* chunk size
* chunk overlap
* embedding model
* retrieval depth
* similarity threshold
* reranking limit
* context token budget
* prompt template
* cache policy
* retry policy
* timeout

Configuration should be modeled as structured knowledge when the value or parameter is important for comparing alternatives or reproducing results.

---

# Quality Attributes

Components often affect system quality attributes.

Relevant attributes include:

* retrieval quality
* latency
* throughput
* cost
* freshness
* scalability
* observability
* reliability
* reproducibility
* privacy
* security
* citation faithfulness

Quality attributes should be linked to claims and evidence when they influence selection or evaluation.

For example, a reranker component may improve ranking quality while increasing latency and cost.

---

# Relationship Use

Components should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Component CONSUMES Artifact
Component PRODUCES Artifact
Component TRANSFORMS Artifact
Component DEPENDS_ON Component
Component REQUIRES Provider
Component IMPLEMENTS Technique
Component SUPPORTS Workflow
Component USES Tool
Framework PROVIDES Component
Workflow USES Component
Evaluation Metric MEASURES Component
Component GOVERNED_BY Policy
```

Relationship targets should use stable identifiers whenever the target entity is represented in RKM.

Plain prose may explain a component, but reusable dependency, implementation, workflow participation and evaluation knowledge should be represented structurally.

---

# Evidence and Claims

Claims about components should be evidence-backed when they affect trust, selection or operational use.

Examples of claims that should usually cite evidence include:

* a component implements a specific technique
* a component supports a specific RAG pipeline stage
* a component improves retrieval quality
* a component increases latency or cost
* a component requires a provider dependency
* a component produces auditable traces
* a component enforces a policy or guardrail

Evidence may come from documentation, source code, papers, benchmark reports, evaluation runs, release notes or observed system behavior.

Implementation-specific claims should include version or observation context when available.

---

# Component vs Tool

A component is an architectural building block.

A tool is a callable capability with an invocation boundary.

The same implementation may be represented as both when both perspectives have reusable meaning.

Example:

```text
Component: Retrieval service adapter used inside a workflow.
Tool: Callable search endpoint invoked by an agent.
```

Use Component when modeling architectural responsibility, composition and pipeline participation.

Use Tool when modeling invocation, contract, side effects and callable behavior.

---

# Component vs Framework

A framework provides reusable abstractions, libraries or runtime conventions.

A component is a functional unit used within an architecture.

Example:

```text
Framework PROVIDES Component
Component IMPLEMENTS Technique
```

A framework may provide many components, and a component may be implemented independently of any one framework.

---

# Component vs Technique

A technique is a method or approach.

A component is the architectural unit that applies or implements behavior.

Example:

```text
Component IMPLEMENTS Technique
Technique HAS_USE_CASE Use Case
```

This separation keeps reusable methods distinct from concrete architectural roles.
