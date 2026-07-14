# Confidence Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how confidence is represented in the RAG Knowledge Model.

Confidence expresses maintainer certainty about an assertion, interpretation, relationship, citation or evidence judgment after considering the available sources.

The Confidence Model answers the question:

> **How certain is RKM that this modeled statement is correct, given the available evidence and review state?**

---

# Core Principle

Confidence is an interpretation about knowledge quality.

It is not a source type, source priority, evidence strength, lifecycle status or popularity measure.

Confidence should remain explicit whenever a modeled statement may be uncertain, source-dependent, version-dependent or based on maintainer analysis.

```text
Evidence SUPPORTS Claim
Evidence REFERENCES Reference
Claim SUPPORTS Relationship
```

Confidence can be attached to the claim, evidence, citation or relationship that carries the interpretation.

---

# Confidence

Confidence is a controlled value that describes maintainer certainty.

Canonical confidence values are:

```text
Very Low
Low
Medium
High
Very High
```

The value should be chosen from the point of view of RKM maintainers, not from the point of view of a cited source.

A source may make a strong statement while RKM assigns Medium confidence because the source is old, ambiguous, contradicted by other sources or scoped to a narrow implementation.

---

# Confidence Levels

## Very Low

Use Very Low when the statement is speculative, weakly sourced or preserved mainly for review.

Very Low confidence is appropriate when:

* the statement is based on indirect evidence
* sources are unclear or incomplete
* the modeled interpretation is likely to change
* the statement is retained to document uncertainty

## Low

Use Low when the statement has some support but still has material uncertainty.

Low confidence is appropriate when:

* evidence exists but is thin
* sources use ambiguous terminology
* the statement depends on an implementation detail that may vary
* maintainers have not completed review

## Medium

Use Medium when the statement is plausible and supported, but not settled enough to treat as highly certain.

Medium confidence is appropriate when:

* sources support the statement but leave scope unclear
* there is agreement among secondary sources but no primary source
* the statement is generally correct with known exceptions
* the modeled relationship is useful but may need refinement

## High

Use High when the statement is well supported and unlikely to change without new evidence.

High confidence is appropriate when:

* primary sources directly support the statement
* sources agree on the key facts
* terminology is stable
* scope and version assumptions are clear

## Very High

Use Very High when the statement is directly established by authoritative sources and has little meaningful ambiguity.

Very High confidence is appropriate when:

* the statement is definitional
* the original source explicitly states the modeled fact
* the source is stable, versioned or canonical
* the interpretation requires little maintainer inference

---

# Confidence vs Evidence Strength

Evidence strength describes how strongly a piece of evidence supports, weakens, motivates, defines or evaluates a claim.

Confidence describes maintainer certainty in the modeled statement after evaluating all relevant context.

The two values may differ.

For example, a benchmark result may be strong evidence for a narrow experimental setting but only Medium confidence for a broad ecosystem claim.

Likewise, multiple moderate sources may collectively justify High confidence when they agree and describe the same concept consistently.

---

# Confidence vs Source Priority

Source priority describes how direct or authoritative a reference is for a specific knowledge question.

Canonical source priorities are Primary, Secondary and Tertiary.

Confidence describes how certain RKM is after interpreting the source.

A Primary source does not automatically produce Very High confidence.

Primary documentation may be outdated, underspecified, marketing-oriented or version-specific. A Secondary source may also improve confidence when it clarifies terminology or compares multiple primary sources.

---

# Confidence vs Lifecycle Status

Lifecycle status describes publication state.

Canonical lifecycle values include Draft, Review, Published, Deprecated and Archived.

Confidence describes certainty.

A Published claim can have Low confidence when RKM intentionally publishes a weakly supported but useful statement with clear evidence and limitations.

A Draft claim can have High confidence when the fact is clear but the record has not completed repository review.

---

# Scope

Confidence may appear on:

* claims
* evidence
* relationships
* citations
* entity-specific assertions
* relationship support sets
* evaluation interpretations

Confidence should be attached to the smallest structure that carries the uncertain interpretation.

If only one claim is uncertain, put confidence on that claim.

If a relationship is uncertain even though its supporting claim is clear, put confidence on the relationship.

If the cited source is clear but the source-to-claim interpretation is uncertain, put confidence on the evidence or citation.

---

# Selection Guidance

When assigning confidence, consider:

* source authority
* source freshness
* source agreement
* source specificity
* version scope
* implementation scope
* evidence strength
* maintainer inference
* known limitations
* unresolved contradictions

Confidence should be lowered when the modeled statement relies on broad generalization from narrow examples.

Confidence should be raised when independent sources agree, the statement is directly stated, and the modeled scope is precise.

---

# Examples

## High Confidence Claim

```json
{
  "id": "CLAIM-0001",
  "statement": "Hybrid retrieval combines dense and sparse retrieval signals.",
  "claimType": "Factual",
  "confidence": "High",
  "evidenceIds": [
    "EVIDENCE-0001"
  ],
  "status": "Published"
}
```

This claim can be High confidence when sources directly describe both dense and sparse retrieval signals and the claim remains scoped to the general technique.

## Medium Confidence Relationship

```json
{
  "id": "RELATIONSHIP-0001",
  "sourceId": "TECHNIQUE-0001",
  "type": "SUPPORTS",
  "targetId": "QUALITY-ATTRIBUTE-0001",
  "confidence": "Medium"
}
```

This relationship may be Medium confidence when the technique can support a quality attribute in common configurations but the effect depends on corpus, retriever, model and evaluation setup.

## Low Confidence Evidence Interpretation

```json
{
  "id": "EVIDENCE-0001",
  "role": "Supports",
  "strength": "Weak",
  "summary": "A secondary source describes the technique as useful for underspecified queries.",
  "claimIds": [
    "CLAIM-0002"
  ],
  "referenceIds": [
    "REFERENCE-0001"
  ],
  "confidence": "Low",
  "status": "Review"
}
```

This evidence interpretation may be Low confidence when the source is useful but indirect, lacks evaluation detail or uses informal terminology.

---

# Anti-Patterns

Do not use confidence to encode source type.

Do not use confidence to encode review status.

Do not assign Very High confidence to broad comparative claims without precise scope.

Do not hide uncertainty in prose when a structured confidence field exists.

Do not raise confidence only because a technique, framework or model is popular.

---

# Validation Expectations

Schemas that expose confidence should use the canonical confidence values defined by this model.

Specialized schemas may place confidence on the structure that carries the interpreted statement, but they should not introduce incompatible confidence vocabularies.

Validation should preserve confidence as structured data so graph exports, search indexes, generated documentation and review workflows can filter or inspect uncertain knowledge.

---

# Relationship to Other Models

The Confidence Model works with the Claim Model, Evidence Model, Citation Model, Relationship Model and Relationship Support Model.

Claims define what is being asserted.

Evidence explains how sources support or qualify the assertion.

References identify the sources.

Relationships connect entities through canonical predicates.

Confidence records maintainer certainty about those modeled interpretations.
