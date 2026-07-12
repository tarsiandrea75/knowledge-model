# Limitation Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how limitations are represented in the RAG Knowledge Model.

Limitations describe known constraints, weaknesses, boundary conditions and failure-prone contexts for RAG entities.

The Limitation Model answers the question:

> **Where does a RAG entity stop being reliable, suitable or cost-effective, and how should that constraint be represented?**

---

# Core Principle

A limitation is first-class knowledge when it affects selection, evaluation, operation or governance.

It is not only a warning note.

A limitation explains the boundary of an entity's usefulness and should be linked to claims, evidence, affected quality attributes, mitigations and use cases when those links have reusable semantic meaning.

```text
Technique HAS_LIMITATION Limitation
Retriever HAS_LIMITATION Limitation
Workflow HAS_LIMITATION Limitation
Use Case HAS_LIMITATION Limitation
Evaluation Metric MEASURES Limitation
Evidence SUPPORTS Claim
```

Limitations make RKM useful for comparison because they preserve the conditions under which an entity should be constrained, evaluated differently or paired with a mitigation.

---

# Limitation

A Limitation is a known boundary, weakness or constraint that reduces the suitability of an entity in a defined context.

Limitations may apply to:

* techniques
* frameworks
* components
* retrievers
* rerankers
* models
* databases
* datasets
* benchmarks
* evaluation metrics
* agents
* workflows
* tools
* providers
* use cases

A limitation should identify the affected entity, the constrained behavior and the context in which the limitation matters.

Preferred:

```text
Dense retrieval may miss rare exact identifiers when the embedding model does not preserve lexical specificity.
```

Avoid:

```text
Dense retrieval is bad with IDs.
```

The avoided statement is too broad to support evidence, comparison or mitigation guidance.

---

# Limitation Boundary

Every limitation should have a clear boundary.

The boundary identifies:

* the affected entity or entity class
* the behavior being constrained
* the condition that exposes the limitation
* the likely impact
* the affected quality attributes
* the use cases or workflows where the limitation matters
* the evidence or observation supporting the limitation

Boundaries prevent local implementation issues from being incorrectly modeled as universal properties.

For example, a retriever may have low recall in one benchmark because of corpus preprocessing, while the underlying retrieval technique may remain appropriate in other corpus conditions.

---

# Limitation Type

Limitation type describes the primary cause or nature of the constraint.

Canonical limitation types include:

```text
Data Quality Limitation
Retrieval Limitation
Ranking Limitation
Generation Limitation
Evaluation Limitation
Context Window Limitation
Latency Limitation
Cost Limitation
Scalability Limitation
Freshness Limitation
Observability Limitation
Governance Limitation
Provider Limitation
Operational Limitation
Other
```

The limitation type should describe the dominant constraint, not every secondary effect.

---

# Scope and Conditions

Limitations should preserve scope.

Important scope dimensions include:

* corpus type
* query style
* language
* modality
* document freshness
* source trust level
* benchmark or dataset
* model version
* provider behavior
* latency budget
* cost budget
* governance requirement
* deployment environment

Scope is required when a limitation would otherwise sound universal.

Preferred:

```text
Small chunks can reduce answer completeness when the workflow does not retrieve enough neighboring context.
```

Avoid:

```text
Small chunks reduce answer quality.
```

The avoided statement drops the condition that makes the limitation meaningful.

---

# Impact

A limitation should identify its impact when the impact is known.

Common impacts include:

* lower retrieval recall
* lower precision
* weaker citation faithfulness
* incomplete answers
* higher latency
* higher cost
* reduced reproducibility
* weaker evaluation coverage
* greater operational complexity
* increased governance risk

Impact should not be exaggerated beyond the available evidence.

When impact is uncertain, the limitation should be represented as a claim with confidence and evidence rather than as an unconditional fact.

---

# Mitigation

A mitigation is a technique, workflow, component, policy, evaluation method or operational control that reduces the effect of a limitation.

Mitigations should be modeled separately from the limitation so that RKM can compare alternatives.

In the current relationship registry, `MITIGATES` targets the problem, risk or failure mode associated with a limitation, not the limitation entity itself.

Examples:

```text
Hybrid retrieval MITIGATES lexical mismatch.
Citation verification MITIGATES unsupported answer risk.
Freshness monitoring MITIGATES stale index risk.
```

A mitigation should not imply that the limitation is eliminated unless evidence supports that stronger claim.

---

# Relationship Use

Limitations should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Technique HAS_LIMITATION Limitation
Framework HAS_LIMITATION Limitation
Retriever HAS_LIMITATION Limitation
Reranker HAS_LIMITATION Limitation
Embedding Model HAS_LIMITATION Limitation
Language Model HAS_LIMITATION Limitation
Dataset HAS_LIMITATION Limitation
Benchmark HAS_LIMITATION Limitation
Evaluation Metric MEASURES Limitation
Workflow HAS_LIMITATION Limitation
Agent HAS_LIMITATION Limitation
Use Case HAS_LIMITATION Limitation
Technique MITIGATES Problem
Workflow MITIGATES Problem
Evidence SUPPORTS Claim
```

Relationship targets should use stable identifiers whenever the target concept is represented as an RKM entity.

Plain prose may describe local caveats, but reusable limitations should be represented structurally so they can support graph export and comparison.

---

# Limitations vs Tradeoffs

A Limitation states a constraint or boundary.

A Tradeoff states an exchange between properties.

Example:

```text
Limitation: Dense retrieval may miss exact identifiers that are rare in the embedding model's training distribution.
Tradeoff: Increasing top-k retrieval can improve recall but may increase latency and context noise.
```

The limitation identifies where an entity is weak.

The tradeoff identifies a decision where improving one property can worsen another.

---

# Limitations vs Problems

A Problem describes a challenge that exists in a RAG context.

A Limitation describes a boundary of a specific entity, approach or use case.

Example:

```text
Problem: Retrieved context does not include the answer-bearing passage.
Limitation: A sparse retriever may miss paraphrased queries that do not share important terms with relevant passages.
```

The problem explains what goes wrong.

The limitation explains why a modeled entity may contribute to that problem under specific conditions.

---

# Claims and Evidence

Limitations often need claims because they express contextual assertions.

Examples of limitation claims include:

* a benchmark does not measure citation faithfulness
* a retriever underperforms on queries with rare identifiers
* a provider has deployment-region constraints
* a workflow is unsuitable when source freshness is required within minutes
* an evaluation metric misses answer completeness failures

Evidence should identify the source, evaluation context, observed behavior and scope of the limitation.

Evidence may come from:

* papers
* benchmarks
* datasets
* framework documentation
* provider documentation
* experiment reports
* production traces
* maintainer analysis

Evidence should support the specific limitation claim, not only the general entity being described.

---

# Modeling Guidance

Limitations should be specific enough to support comparison, but stable enough to avoid temporary implementation noise.

Use limitations when a constraint affects architecture choice, evaluation design, operational risk, governance or use case suitability.

Do not model every minor inconvenience as a limitation.

When a limitation is reusable across multiple entities, it may be represented as a named concept or promoted to a first-class entity in a future ontology version. Until then, it should be represented through structured claims, relationships, evidence and precise prose.
