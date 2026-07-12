# Citation Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how citations are represented in the RAG Knowledge Model.

Citations connect generated answers, claims, evidence, references and source artifacts so that grounded knowledge can be inspected, evaluated and reused.

The Citation Model answers the question:

> **Which source supports a statement, where is the supporting material located, and how should that support be interpreted?**

---

# Core Principle

A citation is a structured link between a statement and a source-bearing record.

It is not only a formatted bibliography entry.

In RKM, citations preserve traceability between the thing being asserted and the source used to justify, qualify, contextualize or challenge that assertion.

```text
Evidence SUPPORTS Claim
Evidence REFERENCES Reference
Reference REFERENCES Artifact
Evaluation Metric MEASURES Artifact
```

Citations make RAG outputs auditable because they identify both the source and the role that source plays in supporting a statement.

---

# Citation

A Citation identifies source material used to support or explain a statement.

A citation may point to:

* a paper section
* a documentation page
* a repository file
* a benchmark report
* a dataset record
* an evaluation result
* a generated answer artifact
* a retrieved passage
* maintainer analysis

The cited source should be represented as a Reference when it is reusable across files.

The citation should be represented as Evidence when it explains how the source supports a claim.

---

# Citation Boundary

Every citation should have a clear boundary.

The boundary identifies:

* the cited reference
* the cited location when known
* the statement or claim being supported
* the support role
* the confidence of the interpretation when available
* the retrieval or evaluation context when the citation comes from a RAG workflow

Boundaries matter because a source may support one statement while failing to support another statement in the same paragraph, page or paper.

---

# Citation vs Reference

A Reference identifies a source.

A Citation uses that source for a specific purpose.

Example reference:

```text
The Self-RAG paper.
```

Example citation:

```text
The Self-RAG paper is cited as evidence that Self-RAG introduces reflection tokens for deciding when retrieval is needed.
```

The reference is reusable.

The citation is contextual.

---

# Citation vs Evidence

Evidence explains how a source supports, weakens, contradicts or contextualizes a claim.

A citation is the source-facing part of that evidence.

Evidence may include:

* a citation to a reference
* a short rationale
* an evidence role
* confidence
* source priority
* observation context

When a citation only identifies a source, it belongs in Reference data.

When it explains support for a claim, it belongs in Evidence data.

---

# Citation Location

Citation location describes where the supporting material appears inside the source.

Common citation locations include:

* section
* page
* paragraph
* table
* figure
* appendix
* repository path
* commit
* URL fragment
* dataset row
* benchmark task
* trace span
* retrieved passage identifier

Locations should be as stable as the source allows.

For web sources, prefer stable URLs, versioned documentation, permalinks or archived references when available.

For repositories, prefer commit-pinned paths when the cited behavior may change.

---

# Support Role

Support role describes how the cited source relates to the statement.

Canonical support roles include:

```text
Supports
Contradicts
Qualifies
Contextualizes
Defines
Introduces
Evaluates
Reports
Implements
Explains
```

The support role should not be confused with relationship type.

Relationship types such as `SUPPORTS`, `REFERENCES`, `EVALUATES`, `MEASURES` and `VALIDATES` define graph predicates.

Support roles describe the evidentiary use of a citation inside evidence or claim interpretation.

---

# Grounding Use

Citations are especially important for RAG systems because generated answers often need to be grounded in retrieved context.

RKM should preserve citation knowledge when it helps answer questions such as:

* Which retrieved passage supports this generated answer?
* Does the cited source actually support the generated claim?
* Which citations were available to the generator?
* Which citations were included in the final answer?
* Which citations were used during evaluation?
* Which citation policy governed the workflow?

Citation modeling should separate retrieval availability from answer attribution.

A passage can be retrieved without being cited.

A generated answer can cite a source without the citation being faithful.

Evaluation can measure whether the cited source supports the generated statement.

---

# Citation Quality

Citation quality describes whether the citation is useful and faithful for its stated purpose.

Common citation quality dimensions include:

* source relevance
* source authority
* location precision
* attribution faithfulness
* claim coverage
* source freshness
* source accessibility
* context sufficiency

These dimensions may be measured by evaluation metrics or described as claims supported by evidence.

For example, a citation faithfulness metric may measure whether a generated answer is supported by the cited retrieved passage.

---

# Relationship Use

Citations should use canonical relationships when the source, evidence, claim or evaluated artifact is represented as an RKM entity.

Common relationship patterns include:

```text
Evidence SUPPORTS Claim
Evidence REFERENCES Reference
Reference REFERENCES Artifact
Evaluation Metric MEASURES Artifact
Benchmark EVALUATES Evaluation Metric
Benchmark VALIDATES Technique
Policy GOVERNED_BY Reference
```

Relationship targets should use stable identifiers whenever the target concept is represented in RKM.

Citation-specific fields may still record source locations, snippets, roles and confidence inside the evidence or reference structure.

---

# Modeling Guidance

Use references for reusable source identity.

Use evidence for the interpretation of how a source supports a claim.

Use claims for statements that need review, comparison, evidence or lifecycle tracking.

Use artifacts for retrieved passages, generated answers, traces and evaluation outputs when they have process significance.

Use evaluation metrics when citation behavior is being measured.

Do not encode important citation semantics only in prose if the information affects trust, evaluation, policy or graph export.

---

# Acceptance Criteria

A citation representation is coherent with RKM when:

* the source can be identified again
* the supported statement is explicit
* the evidence role is clear
* the citation location is recorded when known
* source identity is separated from evidentiary interpretation
* claims, evidence and references remain first-class concepts
* relationships use canonical uppercase snake case predicates
* metadata remains separate from domain knowledge
