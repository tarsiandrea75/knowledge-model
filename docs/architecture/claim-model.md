# Claim Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how claims are represented in the RAG Knowledge Model.

Claims make important statements explicit, identifiable, reviewable and traceable.

The Claim Model answers the question:

> **What does RKM assert about an entity, relationship, reference or evidence record, and how should that assertion be represented?**

---

# Core Principle

A claim is a structured statement that can be reviewed independently from the prose around it.

Claims are first-class knowledge objects.

They may be embedded in entity documents, linked to evidence, cited by relationships and exported to graph representations.

```text
Subject ── Claim ──► Object
              │
              └── SUPPORTED_BY ──► Evidence
```

---

# Claim

A Claim is a precise statement about something represented in RKM.

A claim may describe:

* what an entity is
* what an entity does
* which problem an entity addresses
* which limitation applies to an entity
* which tradeoff is introduced by a design choice
* how two entities compare
* how a relationship should be interpreted
* what a source reports

Claims should be used when the statement has reusable semantic value or requires evidence, confidence, review or lifecycle tracking.

---

# Claim Subject

Every claim has a subject.

The subject is the thing the claim is about.

A claim subject may be:

* Entity
* Relationship
* Reference
* Evidence

The subject should use a stable identifier whenever possible.

Example:

```json
{
  "id": "TECHNIQUE-0007",
  "type": "Entity",
  "name": "HyDE"
}
```

---

# Claim Statement

Every claim has a human-readable statement.

The statement should be:

* precise
* independently understandable
* scoped to one assertion
* free of hidden compound claims when possible
* consistent with repository terminology

Preferred:

```text
HyDE uses a language model to generate a hypothetical document before retrieval.
```

Avoid:

```text
HyDE is great and improves retrieval in many cases.
```

The avoided statement mixes evaluation, scope and evidence expectations into one vague assertion.

---

# Claim Type

Every claim has a claim type.

Canonical claim types are:

```text
Factual
Interpretive
Comparative
Evaluative
Historical
Implementation Specific
Version Specific
```

The claim type describes the nature of the assertion, not the source that supports it.

---

# Factual Claim

A Factual claim states something that can normally be verified directly.

Example:

```text
Hybrid retrieval combines dense retrieval and sparse retrieval.
```

---

# Interpretive Claim

An Interpretive claim explains meaning, role or significance.

Example:

```text
Self-RAG treats retrieval as a controllable generation-time decision rather than a fixed preprocessing step.
```

Interpretive claims require clear rationale and should usually cite evidence.

---

# Comparative Claim

A Comparative claim compares entities, approaches or configurations.

Example:

```text
Reranking can improve precision compared with using initial retriever scores alone.
```

Comparative claims should state the comparison baseline.

---

# Evaluative Claim

An Evaluative claim judges quality, usefulness, risk or suitability.

Example:

```text
Graph-based retrieval is useful when answer quality depends on explicit relationships between entities.
```

Evaluative claims should include qualifiers that define the conditions under which the evaluation applies.

---

# Historical Claim

A Historical claim describes origin, chronology or development.

Example:

```text
The Self-RAG paper introduced reflection tokens for retrieval and generation control.
```

Historical claims should cite primary sources when available.

---

# Implementation Specific Claim

An Implementation Specific claim applies to a concrete framework, product, repository, provider or versioned implementation.

Example:

```text
Spring AI provides abstractions for vector store interactions.
```

Implementation Specific claims should not be generalized into universal RAG claims unless separate evidence supports that generalization.

---

# Version Specific Claim

A Version Specific claim is valid only for a known version, release line, model version or dated source state.

Example:

```text
A framework version supports a specific retriever integration.
```

Version Specific claims should use qualifiers such as `version`, `releaseDate` or `observedAt` when those details are known.

---

# Predicate and Object

A claim may include a structured predicate and object when the statement can be represented as graph-like knowledge.

Example:

```json
{
  "predicate": "USES",
  "object": {
    "id": "COMPONENT-0004",
    "name": "Language Model"
  }
}
```

The predicate must use uppercase snake case when it represents a relationship-like assertion.

The object may be:

* a modeled entity
* another first-class concept
* a literal value
* a named concept that is not yet modeled as an entity

---

# Qualifiers

Qualifiers constrain when or how a claim is true.

Examples:

```json
[
  {
    "name": "baseline",
    "value": "initial retriever scores"
  },
  {
    "name": "condition",
    "value": "short or underspecified queries"
  }
]
```

Qualifiers are important for claims involving performance, cost, latency, quality, implementation support or benchmark results.

---

# Evidence Links

Claims should reference evidence when the assertion is important, contested, comparative or evaluative.

Evidence links use stable evidence identifiers.

Example:

```json
{
  "evidenceIds": [
    "EVIDENCE-0001"
  ]
}
```

Evidence explains how sources support, weaken, contradict or contextualize the claim.

References identify the sources used by the claim.

---

# Confidence

Confidence expresses maintainer confidence in the claim.

Canonical confidence values are:

```text
Very Low
Low
Medium
High
Very High
```

Confidence is not the same as evidence strength.

Confidence reflects the maintainer interpretation after considering evidence quality, source authority, agreement between sources and specificity of the claim.

---

# Claim Status

Claims have lifecycle status.

Canonical claim status values are:

```text
Draft
Review
Published
Deprecated
Archived
```

A claim may be deprecated when it is no longer accurate, no longer relevant or replaced by a more precise claim.

Deprecated claims should remain traceable when they have been used by relationships, generated documentation or downstream graph exports.

---

# Rationale

A claim may include a rationale.

The rationale explains why the claim is represented and how maintainers interpret it.

Use rationale when:

* the claim is interpretive
* the claim is evaluative
* the claim aggregates multiple sources
* the claim affects important relationships
* the claim may be misunderstood without context

---

# Minimal Claim

A minimal claim contains:

```json
{
  "id": "CLAIM-0001",
  "statement": "HyDE uses a language model to generate a hypothetical document before retrieval.",
  "claimType": "Factual",
  "subject": {
    "id": "TECHNIQUE-0007",
    "type": "Entity",
    "name": "HyDE"
  },
  "status": "Draft"
}
```

---

# Full Claim

A full claim may contain:

```json
{
  "id": "CLAIM-0002",
  "statement": "Reranking can improve precision compared with using initial retriever scores alone.",
  "claimType": "Comparative",
  "subject": {
    "id": "COMPONENT-0012",
    "type": "Entity",
    "name": "Reranker"
  },
  "predicate": "IMPROVES",
  "object": {
    "value": "precision"
  },
  "qualifiers": [
    {
      "name": "baseline",
      "value": "initial retriever scores"
    }
  ],
  "confidence": "High",
  "status": "Review",
  "evidenceIds": [
    "EVIDENCE-0002"
  ],
  "referenceIds": [
    "REFERENCE-0003"
  ],
  "rationale": "The claim captures a reusable retrieval-quality tradeoff that should be available to generated documentation and graph queries."
}
```

---

# Relationship to Evidence

Claims and evidence have different responsibilities.

A claim states what RKM asserts.

Evidence explains why the assertion is supported, weakened, contradicted or contextualized.

Example:

```text
Claim:
Hybrid retrieval combines dense retrieval and sparse retrieval.

Evidence:
An official framework guide describes hybrid retrieval as using dense and sparse retrieval signals together.
```

Claims should not hide source interpretation inside evidence text.

Evidence should not introduce important assertions that are missing as claims when those assertions need reuse.

---

# Relationship to Relationships

Relationships are structured links between entities.

Claims can describe or qualify relationships.

Example relationship:

```text
Technique USES Component
```

Example claim about that relationship:

```text
HyDE uses a language model to generate a hypothetical document before retrieval.
```

When a relationship is important, contested or inferential, a claim should capture the assertion and evidence should support it.

---

# Relationship to References

References identify sources.

Claims may cite references directly, but evidence is preferred when the claim requires interpretation.

A reference answers:

```text
Which source is involved?
```

A claim answers:

```text
What does RKM assert?
```

Evidence answers:

```text
How does the source support or contextualize the assertion?
```

---

# Modeling Rules

Use a claim when:

* the statement may need evidence
* the statement may be reused across documentation, graph export or search
* the statement explains a relationship
* the statement involves performance, cost, quality, risk or suitability
* the statement has qualifiers or confidence
* the statement may change over time

Do not create a claim when:

* the text is purely descriptive and has no reusable semantic value
* the statement is already represented completely by a simple field
* the assertion is too vague to review
* the assertion combines multiple independent ideas that should be split

---

# Granularity

Claims should be narrow enough to verify.

Preferred:

```text
Reranking adds an additional scoring step after initial retrieval.
```

```text
Reranking can increase retrieval latency because it evaluates candidate documents after retrieval.
```

Avoid combining both into one claim.

---

# Graph Export

Claims may become graph nodes or graph properties.

Claims are useful as graph nodes when they have:

* independent identity
* evidence links
* confidence
* lifecycle status
* qualifiers
* review history

Claims are useful as graph properties when they are simple annotations on an entity or relationship.

The stable claim identifier is authoritative in either representation.

---

# Quality Bar

A good claim is:

* precise
* scoped
* typed
* traceable
* reviewable
* supported when necessary
* consistent with RKM terminology
* usable in documentation and graph export

A claim should make repository knowledge easier to inspect, not harder to maintain.
