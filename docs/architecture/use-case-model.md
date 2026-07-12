# Use Case Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how use cases are represented in the RAG Knowledge Model.

Use cases describe recurring application contexts in which RAG entities are selected, combined, evaluated or constrained.

The Use Case Model answers the question:

> **Where is a RAG entity useful, and what contextual requirements make that usefulness meaningful?**

---

# Core Principle

A use case is first-class knowledge when it explains suitability.

It is not only a market label, domain tag or example scenario.

A use case connects techniques, workflows, tools, models, datasets, evaluation metrics, policies, claims and evidence to the real task context in which they matter.

```text
Technique HAS_USE_CASE Use Case
Workflow SUPPORTS Use Case
Tool SUPPORTS Use Case
Evaluation Metric MEASURES Use Case
Use Case GOVERNED_BY Policy
Claim REFERENCES Use Case
```

Use cases help RKM consumers compare alternatives by task context instead of by generic popularity.

---

# Use Case

A Use Case represents a recurring application context for a RAG system, technique, workflow, component, model, tool or evaluation method.

Examples include:

* customer support question answering
* enterprise document search
* compliance research
* codebase assistance
* literature review
* medical policy lookup
* legal document analysis
* internal knowledge assistant

A use case should describe a task, actor, information source or decision context clearly enough that relationships to entities are meaningful.

Preferred:

```text
Answering employee questions from versioned internal policy documents.
```

Avoid:

```text
Enterprise.
```

The avoided statement is a broad market category, not a reusable application context.

---

# Use Case Boundary

Every use case should have a clear boundary.

The boundary identifies:

* the user or actor
* the task being performed
* the source material or knowledge domain
* the expected output
* the quality requirements
* the operational or governance constraints

Boundaries matter because the same RAG entity may be suitable in one use case and unsuitable in another.

For example, a workflow that is acceptable for exploratory literature review may not satisfy citation, retention or audit requirements for regulated compliance guidance.

---

# Context Dimensions

Use cases should preserve the dimensions that affect entity selection and evaluation.

Important dimensions include:

* task type
* user role
* knowledge domain
* source freshness
* source trust requirements
* answer format
* citation requirements
* latency expectations
* cost constraints
* privacy constraints
* evaluation criteria
* failure tolerance

These dimensions should be represented structurally when they are reused across relationships, claims, policies or evaluation decisions.

---

# Suitability

Suitability describes why an entity fits a use case.

Suitability should be supported by relationships, claims and evidence when it affects adoption or comparison.

Examples:

```text
Hybrid retrieval HAS_USE_CASE customer support question answering over product documentation.
Citation verification SUPPORTS legal document analysis.
Freshness monitoring SUPPORTS policy lookup over frequently updated source material.
```

Suitability should avoid universal claims unless the evidence supports that scope.

Preferred:

```text
Dense retrieval can support semantic search over long-form policy documents when queries use paraphrased language.
```

Avoid:

```text
Dense retrieval is best for enterprise search.
```

The avoided statement is too broad to preserve task context, evidence scope or comparison criteria.

---

# Requirements

A use case may imply functional, quality, governance and operational requirements.

Common requirements include:

* retrieving relevant source material
* generating grounded answers
* preserving citations
* explaining uncertainty
* respecting access controls
* handling stale documents
* supporting multilingual queries
* recording evaluation traces
* enforcing human review
* limiting latency or cost

Requirements should be separated from solutions.

For example, a use case may require citation faithfulness. A particular workflow, tool or evaluation metric may support that requirement, but the use case itself should not assume one implementation.

---

# Relationship Use

Use cases should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Technique HAS_USE_CASE Use Case
Framework SUPPORTS Use Case
Workflow SUPPORTS Use Case
Tool SUPPORTS Use Case
Evaluation Metric MEASURES Use Case
Use Case GOVERNED_BY Policy
Use Case REQUIRES Component
Use Case DEPENDS_ON Dataset
Use Case HAS_LIMITATION Limitation
Use Case HAS_TRADEOFF Tradeoff
```

Relationship targets should use stable identifiers whenever the target concept is represented as an RKM entity.

Plain prose may describe examples, but reusable suitability, requirement, governance and evaluation knowledge should be represented structurally.

---

# Use Case vs Problem

A Problem describes a challenge, failure mode or requirement gap.

A Use Case describes the application context in which work is performed.

Example:

```text
Use Case: Answer customer questions from product documentation.
Problem: Retrieved passages miss exact product version constraints.
```

The use case explains where the system is applied.

The problem explains what can go wrong or what must be improved.

---

# Use Case vs Domain

A domain describes a subject area or industry.

A use case describes a task context inside a domain.

Example:

```text
Domain: Healthcare.
Use Case: Answer staff questions from hospital policy documents with source citations.
```

RKM should avoid treating domain labels as use cases unless the task context is also defined.

---

# Evidence and Claims

Claims about use case suitability should be evidence-backed when they affect selection, comparison or governance.

Examples of use case claims include:

* a technique improves retrieval quality for codebase assistance
* a workflow satisfies citation requirements for compliance research
* a tool supports source filtering for internal knowledge assistants
* a metric measures citation faithfulness for legal document analysis
* a provider supports the availability needs of a production support assistant

Evidence should identify the observed context, source material, evaluation method and relevant constraints when that information is available.

---

# Modeling Guidance

Use cases should be modeled with enough precision to support graph export, search and comparison.

Preferred use case names are concise task descriptions.

Preferred descriptions include actor, task, source material and expected outcome.

Use cases should not duplicate technique descriptions, provider marketing categories or dataset summaries.

When a scenario is unique, local or temporary, it may remain prose. When the scenario is reused across entities, claims, evidence, policies or evaluation, it should be promoted to a Use Case entity.
