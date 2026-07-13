# Problem Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how problems are represented in the RAG Knowledge Model.

Problems describe recurring challenges, failure modes, requirement gaps and quality issues in RAG systems.

The Problem Model answers the question:

> **What can go wrong, what requirement is not yet satisfied, and how should that challenge be represented so RKM can connect it to solutions, mitigations, evidence and evaluation?**

---

# Core Principle

A problem is first-class knowledge when it motivates selection, design, evaluation, operation or governance.

It is not only a negative note.

A problem explains why a RAG entity matters and should be linked to techniques, components, workflows, quality attributes, limitations, claims, evidence and references when those links have reusable semantic meaning.

```text
Technique SOLVES Problem
Technique MITIGATES Problem
Workflow MITIGATES Problem
Evaluation Metric MEASURES Problem
Benchmark EVALUATES Technique
Evidence SUPPORTS Claim
```

Problems make RKM useful for reasoning because they preserve the conditions under which a technique, workflow or control is needed.

---

# Problem

A Problem is a recurring challenge, failure mode, requirement gap or quality issue in a RAG system context.

Problems may apply to:

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

A problem should identify the affected context, the unsatisfied requirement or failure mode and the conditions under which the problem matters.

Preferred:

```text
Dense retrieval may miss rare exact identifiers when the embedding model does not preserve lexical specificity.
```

Avoid:

```text
Retrieval is bad.
```

The avoided statement is too broad to support evidence, comparison or mitigation guidance.

---

# Problem Boundary

Every problem should have a clear boundary.

The boundary identifies:

* the affected entity or entity class
* the RAG pipeline stage or workflow context
* the triggering condition
* the observed or expected effect
* the affected quality attributes
* the use cases where the problem matters
* the evidence or observation supporting the problem

Boundaries prevent local implementation defects from being modeled as universal RAG properties.

For example, low recall in one benchmark may be caused by corpus preprocessing, query style or embedding model choice. The problem should preserve those conditions instead of asserting that a retrieval technique is generally unreliable.

---

# Problem Type

Problem type describes the primary nature of the challenge.

Canonical problem types include:

```text
Retrieval Problem
Ranking Problem
Generation Problem
Grounding Problem
Citation Problem
Evaluation Problem
Data Quality Problem
Freshness Problem
Context Assembly Problem
Latency Problem
Cost Problem
Scalability Problem
Observability Problem
Governance Problem
Operational Problem
Other
```

The problem type should describe the dominant challenge, not every downstream effect.

---

# Scope and Conditions

Problems should preserve scope.

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

Scope is required when a problem would otherwise sound universal.

Preferred:

```text
Citation faithfulness can be difficult to evaluate when generated answers synthesize multiple retrieved passages into one statement.
```

Avoid:

```text
Citations are hard to evaluate.
```

The avoided statement drops the condition that makes the problem useful for modeling, evaluation and mitigation.

---

# Effects

A problem should identify its effects when the effects are known.

Common effects include:

* lower retrieval recall
* lower precision
* unsupported generated answers
* incomplete answers
* stale answers
* weak citation faithfulness
* higher latency
* higher cost
* reduced reproducibility
* weaker observability
* increased governance risk

Effects should not be exaggerated beyond the available evidence.

When an effect is uncertain, the problem should be expressed through a claim with confidence and evidence rather than as an unconditional fact.

---

# Solutions and Mitigations

A solution directly addresses a problem in the stated scope.

A mitigation reduces the impact, likelihood or severity of a problem without necessarily eliminating it.

Examples:

```text
Hybrid retrieval SOLVES exact and semantic matching gaps in some mixed-query settings.
Hybrid retrieval MITIGATES lexical mismatch in corpora with important exact terms.
Freshness monitoring MITIGATES stale index risk.
Citation verification MITIGATES unsupported answer risk.
```

`SOLVES` should be used carefully because it is a stronger relationship and should have evidence or explicit rationale.

`MITIGATES` is appropriate when the source entity partially addresses a problem, addresses it only under stated conditions or reduces only one effect of the problem.

---

# Relationship Use

Problems should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Technique SOLVES Problem
Technique MITIGATES Problem
Framework MITIGATES Problem
Component MITIGATES Problem
Retriever MITIGATES Problem
Reranker MITIGATES Problem
Workflow MITIGATES Problem
Agent MITIGATES Problem
Evaluation Metric MEASURES Problem
Benchmark EVALUATES Technique
Evidence SUPPORTS Claim
```

Relationship targets should use stable identifiers whenever the target concept is represented as an RKM entity.

Plain prose may explain local issues, but recurring problems should be represented structurally so they can support graph export, comparison and evidence-backed selection.

---

# Problems vs Limitations

A Problem describes a challenge, failure mode or unmet requirement.

A Limitation describes a boundary or weakness of an entity.

Example:

```text
Problem: Retrieved passages miss exact product version constraints.
Limitation: Dense retrieval may underweight rare product version identifiers.
```

The problem explains what must be addressed.

The limitation explains where an entity may fail or become unsuitable.

---

# Problems vs Tradeoffs

A Problem describes an issue that motivates action.

A Tradeoff describes a decision tension where improving one property may degrade, constrain or complicate another property.

Example:

```text
Problem: Low recall for multi-hop questions over distributed evidence.
Tradeoff: Increasing retrieval depth may improve recall but increase latency and context noise.
```

The problem identifies the challenge.

The tradeoff explains the consequence of one possible response.

---

# Evidence and Claims

Claims are required when a problem expresses an assertion that needs review, confidence or evidence.

Examples of problem claims include:

* a retrieval approach has low recall for a query class
* a workflow produces unsupported answers under a source condition
* a benchmark exposes a citation faithfulness issue
* a provider behavior increases reproducibility risk
* a mitigation reduces the observed severity of a problem

Evidence should identify the observed context, dataset, benchmark, workflow, model version or source material when that information is available.

Problem statements without evidence may remain useful as hypotheses, but they should not be presented as established facts.

---

# Modeling Guidance

Problems should be modeled with enough precision to support search, comparison, evaluation and graph export.

Preferred problem names are concise failure modes or requirement gaps.

Preferred descriptions include the affected context, triggering condition and observed or expected effect.

Problems should not duplicate limitations, generic quality attributes or vague implementation complaints.

When a problem is unique to one implementation note, it may remain prose. When the problem recurs across entities, claims, evidence, evaluations or mitigations, it should be represented structurally.
