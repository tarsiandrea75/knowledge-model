# Pattern Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how patterns are represented in the RAG Knowledge Model.

Patterns are recurring architectural arrangements that describe how multiple RAG entities collaborate to solve a repeatable design problem.

The Pattern Model answers the question:

> **What reusable architectural arrangement appears across RAG systems, and how should its context, participants, structure, tradeoffs and evidence be represented?**

---

# Core Principle

A pattern is a first-class knowledge entity when the arrangement has reusable architectural meaning across implementations.

It is not only a technique name, product feature, workflow step, diagram label or implementation recipe.

A pattern captures the recurring problem context, participating entities, collaboration structure, forces, consequences, variants, known uses and evidence-backed claims.

```text
Pattern REQUIRES Component
Pattern USES Technique
Pattern SUPPORTS Workflow
Pattern DEPENDS_ON Dataset
Framework IMPLEMENTS Pattern
Paper DESCRIBES Pattern
Benchmark EVALUATES Pattern
Evaluation Metric MEASURES Pattern
```

Representing patterns explicitly helps RKM distinguish reusable system structure from isolated methods, individual components and implementation-specific choices.

---

# Pattern

A Pattern represents a reusable architectural arrangement in a RAG system.

A pattern may describe:

* a retrieval structure
* an indexing arrangement
* a chunking and metadata strategy
* a context assembly structure
* a generation control structure
* an evaluation arrangement
* an orchestration structure
* an agent collaboration pattern
* a data management arrangement
* a deployment or governance structure

A pattern should be modeled when the arrangement can be named, compared, implemented, evaluated or observed independently of one product.

Preferred:

```text
Multi-stage retrieval pattern that combines candidate generation, reranking and context assembly before answer generation.
```

Avoid:

```text
Good RAG architecture.
```

The avoided statement does not identify the recurring structure, participating entities, applicability or consequences.

---

# Pattern Boundary

Every pattern should define what is inside and outside the recurring arrangement.

The boundary should identify:

* the recurring problem context
* the RAG stages affected by the pattern
* the participants and their responsibilities
* the collaboration structure between participants
* required and optional dependencies
* forces and tradeoffs that shape the pattern
* expected consequences of applying the pattern
* variants or specializations that should be modeled separately when needed

Clear boundaries prevent patterns from becoming broad labels for complete systems.

For example, Graph RAG can be discussed as a family of techniques, workflows and system designs. A pattern entity should state whether it represents graph-enhanced indexing, graph traversal retrieval, graph-grounded context assembly or an end-to-end arrangement that combines those parts.

---

# Pattern Type

Pattern type describes the primary architectural category represented by the pattern.

Canonical pattern types include:

```text
Retrieval Pattern
Indexing Pattern
Chunking Pattern
Context Assembly Pattern
Generation Pattern
Evaluation Pattern
Orchestration Pattern
Agent Pattern
Data Management Pattern
Deployment Pattern
Governance Pattern
Other
```

The pattern type should describe the dominant architectural concern.

More specific knowledge should be represented through participants, structure, relationships, claims, evidence, advantages, limitations and tradeoffs.

---

# Scope

Scope describes the level at which the pattern is normally applied.

Canonical scopes include:

```text
Component
Pipeline
Workflow
System
Platform
Organization
Variable
Unknown
```

Scope matters because the same idea can have different consequences at different levels.

For example, routing between retrievers inside one component has a narrower scope than a platform-level routing pattern that selects tools, workflows, indexes and model providers.

---

# RAG Stage Participation

Patterns should identify the RAG pipeline stages where they are commonly applied or have direct impact.

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
* governance

A pattern may affect multiple stages when the arrangement coordinates responsibilities across them.

Stage participation should be explicit rather than inferred from the pattern name.

---

# Problem Context and Applicability

Patterns should identify the recurring context that motivates their use.

Problem context may include:

* poor retrieval recall
* weak citation grounding
* stale indexed knowledge
* heterogeneous document structure
* multi-hop question answering
* high latency constraints
* strict governance requirements
* limited context window budget
* need for human approval
* need for auditable evaluation

Applicability conditions should be structured when they determine whether the pattern is appropriate.

For example, a query routing pattern may be applicable when multiple retrievers expose complementary evidence sources and the system can observe enough query intent to choose between them.

---

# Participants and Structure

Patterns should describe important participants and their responsibilities.

Participants may be:

* components
* techniques
* frameworks
* retrievers
* rerankers
* embedding models
* language models
* vector databases
* graph databases
* datasets
* benchmarks
* agents
* workflows
* tools
* providers

The structure should explain how participants are arranged.

Useful structural knowledge includes:

* ordered stages
* required participants
* optional participants
* data flow
* control flow
* feedback loops
* fallback paths
* approval points
* evaluation points

Structure should be precise enough that a reader can distinguish the pattern from adjacent patterns without relying on prose-only intuition.

---

# Collaboration

Collaboration describes how participants work together.

Collaboration steps should identify:

* the actor or participant role
* the action performed
* the artifact consumed
* the artifact produced
* the next participant or stage when that handoff has reusable meaning

Example collaboration:

```text
Retriever PRODUCES Artifact
Reranker TRANSFORMS Artifact
Workflow USES Component
Evaluation Metric MEASURES Workflow
```

Collaboration should focus on the recurring arrangement, not implementation-specific call stacks.

---

# Forces and Consequences

Patterns exist because design forces compete.

Common forces include:

* recall versus latency
* faithfulness versus answer coverage
* freshness versus index stability
* autonomy versus governance
* context breadth versus context precision
* retrieval diversity versus ranking confidence
* observability versus implementation complexity
* provider capability versus portability

Consequences should describe expected outcomes of applying the pattern.

Consequences may be positive, negative or conditional. They should not be treated as universal claims unless supported by evidence.

Examples:

* improves answer grounding when retrieved context is relevant
* increases latency because multiple retrieval or evaluation steps are added
* improves auditability when intermediate artifacts are persisted
* increases operational complexity because more components must be configured and monitored

---

# Variants

Variants represent meaningful specializations of a pattern.

A variant should be represented when it changes applicability, structure, participants, evaluation or consequences.

Examples of variant distinctions include:

* single-index routing versus multi-index routing
* pre-generation evaluation versus post-generation evaluation
* static fallback versus adaptive fallback
* human approval before retrieval versus human approval before publication
* graph expansion before retrieval versus graph expansion after dense retrieval

Variants may become separate Pattern entities when they have independent claims, evidence, known uses or relationships.

---

# Relationship Use

Patterns should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Pattern SPECIALIZES Pattern
Pattern REQUIRES Component
Pattern DEPENDS_ON Dataset
Pattern USES Technique
Pattern USES Embedding Model
Pattern USES Language Model
Pattern USES Vector Database
Pattern USES Graph Database
Pattern OPTIONALLY_USES Reranker
Pattern SUPPORTS Workflow
Framework IMPLEMENTS Pattern
Component IMPLEMENTS Pattern
Agent USES Pattern
Workflow USES Pattern
Paper DESCRIBES Pattern
Benchmark EVALUATES Pattern
Evaluation Metric MEASURES Pattern
Pattern HAS_ADVANTAGE Advantage
Pattern HAS_LIMITATION Limitation
Pattern HAS_TRADEOFF Tradeoff
Pattern HAS_USE_CASE Use Case
```

Relationship targets should use stable identifiers whenever those entities are represented in RKM.

Plain prose may explain a pattern, but reusable dependencies, implementations, evaluation targets and tradeoffs should be represented structurally.

---

# Evidence and Claims

Claims about patterns should be evidence-backed when they affect selection, trust or evaluation.

Common pattern claims include:

* improves retrieval recall
* improves answer faithfulness
* improves citation quality
* reduces context noise
* supports multi-hop reasoning
* improves observability
* increases latency
* increases cost
* increases operational complexity
* requires high-quality metadata

Claims should identify the task, dataset, benchmark, metric, configuration and observation context when available.

Evidence may come from papers, benchmarks, documentation, source code, reference architectures, implementation reports or structured observations.

```text
Paper DESCRIBES Pattern
Benchmark EVALUATES Pattern
Evaluation Metric MEASURES Pattern
Evidence SUPPORTS Claim
```

Unsupported architectural preferences should not be treated as established pattern knowledge.

---

# Distinction From Technique

A Technique describes a reusable method or algorithmic approach.

A Pattern describes a recurring arrangement of participants and responsibilities.

The same concept may be related to both when both meanings are useful.

Example:

```text
Pattern USES Technique
Framework IMPLEMENTS Pattern
```

The technique explains the method. The pattern explains the arrangement in which that method collaborates with other RAG entities.

---

# Distinction From Component

A Component is a bounded functional unit.

A Pattern is a reusable arrangement that may involve multiple components.

Example:

```text
Pattern REQUIRES Component
Workflow USES Component
```

The component represents the functional building block. The pattern represents how one or more building blocks are organized to address a recurring problem context.

---

# Distinction From Workflow

A Workflow defines ordered, conditional or iterative execution.

A Pattern describes a reusable architectural arrangement that a workflow may apply.

Example:

```text
Workflow USES Pattern
Workflow EXECUTES Tool
```

The workflow represents execution structure. The pattern represents the reusable design shape that may appear across many workflows.

---

# Modeling Guidance

Model a pattern as a first-class entity when:

* it has a recurring architectural structure
* it involves multiple participants or responsibilities
* it has meaningful applicability conditions
* it has identifiable forces and consequences
* it has variants or known uses
* it can be compared against alternative patterns
* it has evidence-backed claims
* it participates in graph relationships

Do not model a pattern as a first-class entity when it is only a synonym for a technique, a single component, a one-off implementation detail or a vague architecture preference.

When uncertain, prefer modeling the entity as a pattern only when its structure, participants and consequences can be described independently.
