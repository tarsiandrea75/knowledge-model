# Relationship Support Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how RKM represents support for declared relationship instances.

Relationship support explains why a relationship is included in the knowledge model. It packages the references, claims and evidence that justify a relationship without making those support objects part of the relationship instance itself.

The Relationship Support Model answers the question:

```text
Why does RKM assert that this relationship exists?
```

---

# Core Principle

A relationship instance is the authoritative graph statement.

A relationship support set is the structured justification for one or more relationship instances.

```text
Relationship Support Set ── SUPPORTS ── Relationship
Relationship Support Set ── CONTAINS ── Reference
Relationship Support Set ── CONTAINS ── Claim
Relationship Support Set ── CONTAINS ── Evidence
```

The relationship remains stored in a relationship set. The support set records the reviewable basis for accepting that relationship into RKM.

---

# Scope

Relationship support applies when a relationship needs explicit justification, traceability or review context.

It is useful for:

* seed data relationships
* relationship sets derived from maintainer analysis
* relationships supported by papers or documentation
* relationships that encode modeling decisions
* relationships that may be challenged or revised
* relationship evidence that should not be duplicated inside multiple entity files

Relationship support does not replace the relationship model, evidence model, claim model or reference model.

---

# Relationship Support Set

A Relationship Support Set is a document that groups support objects for declared relationship instances.

It contains:

* a stable local identifier
* a title
* a description
* structured references
* structured claims
* structured evidence

The support set may support one relationship or a coherent group of relationships when the same rationale, sources or evidence apply.

---

# Relationship Instance Authority

The relationship instance is authoritative for graph structure.

Relationship support is authoritative for justification.

For example, this relationship is a graph assertion:

```json
{
  "id": "RELATIONSHIP-0001",
  "type": "USES",
  "sourceId": "TECHNIQUE-0001",
  "targetId": "COMPONENT-0001"
}
```

The support set should not redefine the relationship type, source or target as prose. It should identify the supported relationship and explain the basis for accepting it.

---

# Support Claims

Claims in a relationship support set describe what RKM asserts about the supported relationship.

Support claims may state:

* a relationship is part of the seed dataset modeling rationale
* a source directly reports a relationship between two concepts
* a relationship follows from an implementation description
* a relationship represents a conservative architectural dependency
* a relationship is intentionally scoped to a specific dataset, framework, paper or version

Claims should be precise, scoped and independently reviewable.

Preferred:

```text
Hybrid retrieval uses both dense retrieval and lexical retrieval as candidate retrieval signals in the seed RKM model.
```

Avoid:

```text
Hybrid retrieval is related to retrievers.
```

The avoided statement is too vague to justify a specific relationship.

---

# Support Evidence

Evidence in a relationship support set explains how references support the claims.

Evidence should identify:

* the supported claim
* the relevant reference
* the evidence role
* the interpretation made by RKM maintainers
* confidence or review status when available

Maintainer analysis may be used when the relationship records a modeling decision rather than an external factual claim. When used, it must be labeled as maintainer analysis and should not be presented as benchmark evidence or external proof.

---

# Support References

References identify sources used by the support set.

References may include:

* papers
* official documentation
* repositories
* benchmark descriptions
* dataset documentation
* maintainer analysis records

A support set may include internal maintainer analysis references when the purpose is to justify seed data modeling choices. External claims should prefer primary sources when available.

---

# Granularity

Relationship support should use the smallest coherent unit of justification.

Use one support set for a single relationship when:

* the relationship has distinct evidence
* the relationship is likely to be reviewed independently
* the relationship has a unique source or claim

Use one support set for a group of relationships when:

* the relationships share the same modeling rationale
* the claims and evidence apply to the group as a unit
* splitting the support would duplicate identical references and evidence without adding clarity

Grouped support must still make clear which relationships are supported.

---

# Validation

Relationship support set documents are validated by `schema/relationship-support-set.schema.json`.

Data validation should ensure that:

* required support set fields are present
* references conform to the reference definition
* claims conform to the claim definition
* evidence conforms to the evidence definition
* supported relationship identifiers resolve in the declared dataset
* claim, evidence and reference identifiers resolve within the support set or dataset context

Schema validation checks structure. Semantic validation checks whether the support set actually resolves to declared relationship instances and support objects.

---

# Modeling Rules

Relationship support should follow these rules:

* Do not duplicate relationship instances as unsupported prose.
* Do not introduce noncanonical relationship predicates.
* Use uppercase snake case for relationship types when they appear in examples.
* Keep evidence tied to claims, not only to broad topics.
* Keep references structured and reusable.
* Distinguish external evidence from maintainer analysis.
* Scope support claims to the relationship being justified.
* Prefer stable identifiers over names when linking to relationships, claims, evidence or references.

---

# Non-Goals

Relationship support is not:

* a replacement for relationship sets
* a new first-class entity type
* a place to define relationship predicates
* a place to infer relationships from names or descriptions
* a general notes field for entity documentation
* a benchmark result unless the evidence explicitly represents benchmark data

---

# Example

```json
{
  "id": "RELATIONSHIP-SUPPORT-SET-0001",
  "title": "RAG Technique Component Relationship Support",
  "description": "Support for seed relationships connecting RAG techniques to architectural components.",
  "references": [
    {
      "id": "REFERENCE-0001",
      "sourceType": "Maintainer Analysis",
      "sourcePriority": "Tertiary",
      "title": "RKM Seed Relationship Modeling Analysis",
      "publisher": "RAG Knowledge Model maintainers",
      "updatedAt": "2026-07-13",
      "abstract": "Internal maintainer analysis describing why the seed relationship is modeled as a conservative component-use relationship rather than a mandatory architecture rule."
    }
  ],
  "claims": [
    {
      "id": "CLAIM-0001",
      "statement": "The seed RKM model represents hybrid retrieval as using both semantic and lexical retrieval components.",
      "claimType": "Interpretive",
      "subject": {
        "type": "Relationship",
        "id": "RELATIONSHIP-0001"
      },
      "confidence": "Low",
      "status": "Draft",
      "evidenceIds": [
        "EVIDENCE-0001"
      ],
      "referenceIds": [
        "REFERENCE-0001"
      ],
      "rationale": "The claim records seed dataset modeling rationale and does not assert that every hybrid retrieval implementation must use both components."
    }
  ],
  "evidence": [
    {
      "id": "EVIDENCE-0001",
      "role": "Motivates",
      "strength": "Weak",
      "summary": "Maintainer analysis records the modeling rationale for representing hybrid retrieval through both semantic and lexical retrieval components.",
      "interpretation": "This evidence supports inclusion of the relationship as seed dataset modeling rationale only and does not establish external factual proof.",
      "claimIds": [
        "CLAIM-0001"
      ],
      "referenceIds": [
        "REFERENCE-0001"
      ],
      "relationshipIds": [
        "RELATIONSHIP-0001"
      ],
      "confidence": "Low",
      "status": "Draft",
      "limitations": [
        "Internal maintainer rationale is weak support and should not be interpreted as a universal RAG architecture rule."
      ]
    }
  ]
}
```

This example is illustrative. Concrete files must follow the active relationship support schema and the validation rules for the dataset that declares them.
