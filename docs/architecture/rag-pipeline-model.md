# RAG Pipeline Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how RAG pipelines are represented in the RAG Knowledge Model.

A RAG pipeline is the ordered processing structure that moves information from source material and user intent toward grounded generation, evaluation and operational feedback.

The RAG Pipeline Model answers the question:

> **Which stages make up a RAG process, what artifacts move between them and which entities perform each stage?**

---

# Core Principle

A pipeline is a structured view of RAG execution.

It is not a replacement for workflows, components, artifacts, claims or evidence. It connects them by defining the major stages that make a RAG system inspectable and comparable.

```text
Pipeline CONTAINS Stage
Stage USES Component
Stage CONSUMES Artifact
Stage PRODUCES Artifact
Stage TRIGGERS Evaluation
```

RKM models pipelines so that different techniques, frameworks and implementations can be compared against a shared process vocabulary.

---

# Pipeline

A Pipeline represents a repeatable end-to-end or partial RAG process.

Common pipeline scopes include:

* ingestion pipeline
* indexing pipeline
* retrieval pipeline
* answer generation pipeline
* evaluation pipeline
* monitoring pipeline
* full question answering pipeline

A pipeline may be conceptual, implementation-specific or operational.

Conceptual pipelines explain architecture.

Implementation-specific pipelines describe how a framework, technique or system realizes the process.

Operational pipelines describe deployed execution, monitoring, governance and feedback behavior.

---

# Pipeline Boundary

Every pipeline should define a clear boundary.

The boundary identifies:

* the triggering input or event
* the first stage inside the pipeline
* the final output or terminal state
* the artifacts that cross the boundary
* the entities responsible for execution
* the assumptions that are outside the pipeline

Preferred:

```text
Question answering pipeline that starts with a user query and ends with a generated answer, citation set and evaluation trace.
```

Avoid:

```text
RAG pipeline.
```

The avoided statement does not identify scope, inputs, outputs or responsibilities.

---

# Pipeline Stage

A Pipeline Stage is a named processing phase inside a pipeline.

Stages group related workflow steps and component responsibilities at a level useful for comparison across systems.

Canonical stage families include:

* ingestion
* parsing
* chunking
* enrichment
* embedding
* indexing
* query understanding
* retrieval
* reranking
* context assembly
* prompt construction
* generation
* citation selection
* verification
* evaluation
* monitoring
* feedback
* governance

A stage should be narrow enough to describe meaningful inputs, outputs and participating entities.

---

# Stage Ordering

Pipeline stages usually have an order, but the order may be conditional, iterative or parallel.

Sequential ordering is appropriate when one stage must complete before the next stage can run.

Conditional ordering is appropriate when routing, confidence thresholds, policy decisions or user actions determine the next stage.

Iterative ordering is appropriate when a stage may repeat, such as query rewriting followed by another retrieval attempt.

Parallel ordering is appropriate when independent retrievers, evaluators or enrichment steps run concurrently before a merge or selection stage.

The ordering should be represented explicitly when it affects reproducibility, evaluation, cost, latency or system behavior.

---

# Artifacts Between Stages

Artifacts define the observable handoff points between stages.

Common stage artifacts include:

* source document
* parsed document
* chunk
* embedding vector
* index record
* user query
* rewritten query
* retrieval result
* ranked result list
* context package
* prompt
* generated answer
* citation set
* evaluation result
* execution trace
* feedback signal
* policy decision

Artifacts should be named and structured when downstream stages, claims, evidence or evaluation depend on them.

For example, a ranked result list should preserve candidate identifiers, ranks, scores and source references when those values support retrieval evaluation or citation grounding.

---

# Participants

Pipeline participants are entities that execute, support, evaluate or govern stages.

Common participant entity types include:

* Component
* Framework
* Technique
* Pattern
* Retriever
* Reranker
* Embedding Model
* Language Model
* Vector Database
* Graph Database
* Evaluation Metric
* Agent
* Provider

Participants should be linked through first-class relationships when they have reusable semantic meaning.

Examples:

```text
Pipeline USES Retriever
Stage USES Reranker
Stage CONSUMES Retrieval Result
Stage PRODUCES Ranked Result
Evaluation Metric MEASURES Generated Answer
```

---

# Pipeline Variants

RAG pipelines vary by architecture and objective.

Important variants include:

* naive RAG pipeline
* query transformation pipeline
* multi-stage retrieval pipeline
* hybrid retrieval pipeline
* graph-enhanced RAG pipeline
* agentic RAG pipeline
* evaluation-driven pipeline
* human-in-the-loop pipeline
* policy-gated pipeline

Variants should identify which stages are added, removed, repeated or specialized.

A variant should not be represented only as a name when its structural difference is important to understanding behavior.

---

# Evaluation Role

Evaluation may appear as a stage, a sidecar process or an offline workflow.

Pipeline evaluation should identify:

* the stage or artifact being evaluated
* the metric or benchmark used
* the evaluation protocol
* the observed result
* the claim supported or challenged by the result

Evaluation is especially important at retrieval, reranking, context assembly, generation, citation and end-to-end answer quality boundaries.

---

# Relationship Guidance

Pipeline documentation should use canonical relationships from the relationship model and relationship type registry.

Recommended relationship patterns include:

```text
Pipeline CONTAINS Stage
Stage PART_OF Pipeline
Stage USES Component
Stage CONSUMES Artifact
Stage PRODUCES Artifact
Stage TRANSFORMS Artifact
Workflow IMPLEMENTS Pipeline
Framework IMPLEMENTS Pipeline
Benchmark EVALUATES Pipeline
Evaluation Metric MEASURES Artifact
```

Relationships should be stored at the entity or artifact level where they can be supported by evidence and exported to graph representations.

---

# Modeling Guidance

Use a pipeline model when the main concern is stage structure across a RAG process.

Use a workflow model when the main concern is step-level execution, branching, retries or orchestration.

Use a component model when the main concern is reusable architectural responsibility.

Use an artifact model when the main concern is the structure, lifecycle or provenance of a produced or consumed object.

Use an evaluation model when the main concern is measurement, protocol, result interpretation or benchmark comparison.

The same RAG system may need all of these views, but each view should preserve its own modeling boundary.

---

# Completion Criteria

A pipeline representation is complete enough for RKM when it identifies:

* pipeline scope
* triggering input
* terminal output
* ordered or conditional stages
* important artifacts between stages
* participating entities
* evaluation points
* relevant relationships
* evidence or references for non-obvious claims

Pipelines that omit artifacts, participants or evaluation points are incomplete when those omissions prevent comparison, reproducibility or graph export.
