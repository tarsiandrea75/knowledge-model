# Anti Pattern Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how anti patterns are represented in the RAG Knowledge Model.

Anti patterns describe recurring RAG design, implementation, evaluation or operational practices that tend to produce poor outcomes.

The Anti Pattern Model answers the question:

> **Which recurring practice should be avoided, where does it cause harm, and how should RKM connect that harm to signals, evidence, problems, limitations and safer alternatives?**

---

# Core Principle

An anti pattern is first-class knowledge when it explains a repeatable harmful structure or behavior.

It is not only a negative opinion.

An anti pattern should identify the practice, the scope where it appears, the harmful outcome, the conditions that make it likely, observable signals, affected quality attributes and recommended alternatives when those links have reusable semantic meaning.

```text
Pattern HAS_ANTI_PATTERN Anti Pattern
Framework HAS_ANTI_PATTERN Anti Pattern
Workflow HAS_ANTI_PATTERN Anti Pattern
Technique MITIGATES Problem
Evidence SUPPORTS Claim
Evidence REFERENCES Reference
```

Anti patterns help RKM consumers avoid designs that appear plausible but repeatedly degrade retrieval quality, grounding, citation faithfulness, evaluation validity, security, governance or operational reliability.

---

# Anti Pattern

An Anti Pattern is a recurring practice that tends to produce harmful outcomes in a RAG context.

Anti patterns may apply to:

* techniques
* frameworks
* components
* patterns
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

An anti pattern should describe the harmful practice and the context in which it matters.

Preferred:

```text
Treating citation presence as citation faithfulness can hide unsupported answer claims when generated citations are not checked against cited passages.
```

Avoid:

```text
Citations are often bad.
```

The avoided statement names a concern but does not identify the recurring practice, scope, harmful outcome or evidence boundary.

---

# Anti Pattern Boundary

Every anti pattern should have a clear boundary.

The boundary identifies:

* the entity, entity class, workflow stage or use case where the practice appears
* the harmful practice or structure
* the condition that makes the practice harmful
* the primary harmful outcome
* the affected quality attributes
* the observable signals that indicate the anti pattern may be present
* the problems or limitations related to the anti pattern
* the recommended alternatives or mitigations
* the claims, evidence and references supporting the assessment

Boundaries prevent RKM from treating every local defect as a reusable anti pattern.

For example, a stale index is an operational problem. It becomes an anti pattern when a workflow repeatedly serves time-sensitive answers from an index with no freshness policy, freshness signal or source recency check.

---

# Anti Pattern Type

Anti pattern type describes the primary area where the harmful practice occurs.

Canonical anti pattern types include:

```text
Retrieval Anti Pattern
Ranking Anti Pattern
Chunking Anti Pattern
Indexing Anti Pattern
Context Assembly Anti Pattern
Prompting Anti Pattern
Generation Anti Pattern
Citation Anti Pattern
Evaluation Anti Pattern
Data Governance Anti Pattern
Security Anti Pattern
Observability Anti Pattern
Operational Anti Pattern
Other
```

The anti pattern type should describe the dominant source of harm, not every downstream consequence.

---

# Harmful Outcome

An anti pattern must identify a harmful outcome.

Common harmful outcomes include:

* lower recall
* lower precision
* poor grounding
* citation failure
* higher latency
* higher cost
* reduced scalability
* reduced freshness
* weaker explainability
* weaker observability
* governance risk
* security risk
* operational fragility

The outcome should be scoped to the conditions under which the harm appears.

Preferred:

```text
Retrieving too few candidates before reranking can lower recall when relevant evidence is distributed across semantically diverse passages.
```

Avoid:

```text
Small candidate sets are wrong.
```

The avoided statement turns a context-dependent design choice into an unconditional rule.

---

# Conditions and Signals

Anti patterns should preserve the conditions that make them likely or harmful.

Important condition dimensions include:

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

Signals are observable signs that the anti pattern may be present.

Useful signal types include:

* evaluation results
* trace events
* metric movement
* user feedback
* citation inspection
* retrieval inspection
* operational incidents
* code review findings

Signals should not be treated as proof by themselves. They should guide review and connect to claims, evidence or references when the anti pattern affects selection, governance or evaluation.

---

# Recommended Alternatives

A recommended alternative is a replacement, mitigation or design correction for an anti pattern.

Recommended alternatives may include:

* a technique
* a pattern
* a workflow
* an evaluation practice
* a governance control
* an operational practice

Alternatives should explain their expected effect without implying that the anti pattern is eliminated unless evidence supports that stronger claim.

Examples:

```text
Hybrid retrieval MITIGATES lexical mismatch.
Citation verification MITIGATES unsupported answer risk.
Workflow GOVERNED_BY Policy
Component SECURED_BY Policy
Provider MONITORED_BY Tool
```

Recommended alternatives should be represented structurally when they affect graph traversal, comparison or evidence-backed guidance.

---

# Relationship Use

Anti patterns should be connected through canonical relationships when those relationships have reusable graph meaning.

Common relationship patterns include:

```text
Pattern HAS_ANTI_PATTERN Anti Pattern
Framework HAS_ANTI_PATTERN Anti Pattern
Workflow HAS_ANTI_PATTERN Anti Pattern
Technique MITIGATES Problem
Pattern MITIGATES Problem
Evaluation Metric MEASURES Problem
Evidence SUPPORTS Claim
Evidence REFERENCES Reference
```

Relationship targets may initially be represented as structured anti pattern objects or named concepts when the target is not yet promoted to a specialized entity type.

Stable identifiers should be used whenever the target concept is modeled as an entity.

---

# Anti Pattern vs Problem

A problem is a recurring challenge, failure mode or requirement gap.

An anti pattern is a recurring practice that tends to cause, expose or intensify a problem.

For example, citation mismatch is a problem. Treating citation presence as proof of citation faithfulness is an anti pattern because it is a practice that can conceal the problem during evaluation or review.

Problems can be targets for `SOLVES`, `MITIGATES` or `MEASURES` relationships. Anti patterns explain why certain practices should be avoided or replaced.

---

# Anti Pattern vs Limitation

A limitation is a known boundary of usefulness.

An anti pattern is a harmful use, design or evaluation practice that may appear within or around that boundary.

For example, dense retrieval may have a limitation around rare exact identifiers. Ignoring identifier-heavy query evaluation while claiming broad retrieval quality is an evaluation anti pattern.

Limitations should not be rewritten as anti patterns unless there is a recurring avoidable practice associated with the limitation.

---

# Anti Pattern vs Common Mistake

A common mistake is a frequent error that may be narrow, local or easy to correct.

An anti pattern is broader and more structural. It tends to recur across systems or workflows and usually requires a design, evaluation, governance or operational correction.

For example, using the wrong embedding dimension for a vector index is a common mistake. Evaluating a retriever on one query style and generalizing the result to all query styles is an evaluation anti pattern.

Common mistakes may be documented as guidance. Anti patterns should be modeled when the harmful practice affects reusable RKM knowledge, comparison or governance.

---

# Claims and Evidence

Anti patterns should use claims and evidence when they assert harm, scope, prevalence, causal effect or recommended alternatives.

Evidence may include:

* benchmark results
* evaluation reports
* papers
* official documentation
* incident reports
* source code
* trace analysis
* reproducible experiments

Evidence should support the specific anti pattern boundary being modeled. Evidence for one corpus, benchmark, workflow or provider should not be generalized unless the claim explicitly states that broader scope and confidence.
