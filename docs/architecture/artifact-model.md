# Artifact Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how artifacts are represented in the RAG Knowledge Model.

Artifacts are the inputs, outputs, intermediate products, traces and durable records that move through RAG systems.

The Artifact Model answers the question:

> **What is produced, consumed, transformed, stored or evaluated during a RAG process?**

---

# Core Principle

Artifacts are first-class knowledge when they explain how entities interact.

They are not only implementation payloads.

Artifacts connect workflows, tools, components, models, datasets, retrievers, rerankers, evaluation metrics, claims and evidence into reproducible process knowledge.

```text
Tool PRODUCES Artifact
Workflow CONSUMES Artifact
Component TRANSFORMS Artifact
Evaluation Metric MEASURES Artifact
Evidence SUPPORTS Claim
Evidence REFERENCES Reference
```

Representing artifacts explicitly makes RAG behavior easier to inspect, evaluate, compare and export as graph knowledge.

---

# Artifact

An Artifact is a discrete item or record that exists because a RAG process consumes, produces, transforms, evaluates or stores it.

Artifacts may be physical, digital, conceptual or operational.

Common artifacts include:

* source document
* parsed document
* chunk
* embedding vector
* metadata record
* query
* rewritten query
* retrieval result
* ranked result list
* assembled context
* prompt
* generated answer
* citation set
* evaluation score
* trace event
* feedback signal
* policy decision

An artifact should be modeled when it has reusable semantic meaning across entities, workflows, tools, evaluation, evidence or graph export.

Preferred:

```text
Ranked retrieval result containing chunk identifiers, relevance scores and source references.
```

Avoid:

```text
Output.
```

The avoided statement does not identify the artifact boundary, structure or role in the RAG process.

---

# Artifact Boundary

Every artifact should have a clear boundary.

The boundary identifies:

* what the artifact represents
* when it is created
* which entity produced it
* which entities consume it
* whether it is transient or stored
* whether it carries provenance
* whether it can be used as evidence

Artifacts with unclear boundaries make workflows difficult to validate and claims difficult to support.

---

# Artifact Type

Artifact type describes the primary semantic role of an artifact.

Canonical artifact types include:

```text
Source Document
Parsed Document
Chunk
Embedding Vector
Metadata Record
Query
Transformed Query
Retrieval Result
Ranked Result
Context Package
Prompt
Generated Answer
Citation Set
Evaluation Result
Execution Trace
Feedback Signal
Policy Decision
Configuration Snapshot
Other
```

The type should describe what the artifact is, not only where it appears in a pipeline.

---

# Lifecycle Role

Artifacts may have different lifecycle roles.

Common lifecycle roles include:

* input
* output
* intermediate
* persisted record
* derived record
* evaluation target
* evidence source
* audit record

Lifecycle role matters because an artifact used as an intermediate workflow value may require less governance than an artifact stored as evidence or audit history.

---

# Structure

Artifacts should be structured when their fields have reusable meaning.

Important structural fields may include:

* stable identifier
* local workflow identifier
* artifact type
* content format
* source entity reference
* producer entity reference
* consumer entity references
* creation time
* provenance
* confidence
* score
* evaluation result
* references
* retention policy

The structure should be detailed enough to support validation, search, evaluation and graph export.

---

# Provenance

Artifact provenance records where an artifact came from and how it was produced.

Provenance may include:

* source document reference
* generating component
* generating model
* executing workflow step
* tool invocation
* dataset version
* transformation parameters
* timestamp
* evidence links

Provenance should be represented when it affects trust, reproducibility, evaluation, compliance or debugging.

---

# Persistence

Artifacts may be transient or persistent.

Transient artifacts exist only during a workflow execution.

Persistent artifacts are stored, indexed, cited, evaluated or reused.

Persistence should be explicit when it affects:

* reproducibility
* auditability
* privacy
* cost
* freshness
* deletion
* versioning

For example, an assembled context package may be transient during answer generation, while an execution trace may be retained for evaluation and incident review.

---

# Relationship Use

Artifacts should be connected through canonical relationships when those relationships have reusable semantic value.

Useful artifact relationships include:

```text
Tool PRODUCES Artifact
Tool CONSUMES Artifact
Component PRODUCES Artifact
Component CONSUMES Artifact
Component TRANSFORMS Artifact
Workflow CONTAINS Artifact
Workflow PRODUCES Artifact
Workflow CONSUMES Artifact
Artifact PRECEDES Artifact
Artifact FOLLOWS Artifact
Evaluation Metric MEASURES Artifact
Evidence REFERENCES Reference
```

Artifact relationships should not duplicate prose-only pipeline descriptions. They should express graph-ready knowledge about flow, derivation, evaluation, evidence or operational state.

---

# Artifact vs Entity

An Artifact is an item produced, consumed or transformed by a process.

A Knowledge Entity is a stable repository concept with identity, metadata, description, relationships, claims, evidence and references.

Some artifacts may later become knowledge entities when they have stable reusable meaning.

For example, a specific benchmark dataset should be modeled as a Dataset entity. A retrieval result produced during one workflow run should usually remain an artifact.

---

# Artifact vs Evidence

Evidence supports or challenges a claim.

An artifact may become evidence when it is used to support or challenge a claim.

For example, an evaluation result is an artifact produced by an evaluation workflow. When that result supports a claim about retrieval quality, it should be connected through evidence and references.

---

# Artifact vs Reference

A Reference identifies a source material.

An Artifact is produced, consumed, transformed, stored or evaluated inside a RAG process.

A source document may be both a referenced material and an artifact in an ingestion workflow, but the two roles should remain distinct when provenance, citation or evidence semantics matter.

---

# Modeling Guidance

Model an artifact explicitly when:

* it crosses a workflow, tool or component boundary
* it is evaluated by a metric
* it supports or challenges a claim
* it is stored, indexed or reused
* it affects governance, privacy, cost or reproducibility
* it is needed to explain a relationship between entities

Do not model an artifact explicitly when it is only a low-level implementation variable with no reusable semantic meaning.

---

# Schema Implications

The current schema set uses artifacts in relationships and specialized entity fields, but does not yet define a specialized `artifact.schema.json`.

A future artifact schema should be introduced only after shared identity support and registry support for `Artifact` are aligned.

Until then, artifact knowledge should appear through structured fields in existing schemas, relationship targets, workflow descriptions, tool descriptions, claims, evidence and references.
