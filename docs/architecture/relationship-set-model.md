# Relationship Set Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how RKM groups declared relationship instances into relationship set documents.

A relationship set is a curated collection of graph statements between populated RKM data records. It records which source entity is connected to which target entity through a canonical relationship predicate.

The Relationship Set Model answers the question:

```text
Which relationships does this dataset assert as graph knowledge?
```

---

# Core Principle

A relationship set is authoritative for graph structure.

Each relationship instance in a relationship set declares a directed edge:

```text
Source Entity ── Predicate ──► Target Entity
```

The set groups relationship instances that belong together because they share a dataset boundary, curation purpose or export scope.

Relationship sets should remain structural. Claims, evidence and references that justify relationship instances belong in relationship support sets.

---

# Relationship Set

A Relationship Set is a document that contains:

* a stable local identifier
* a title
* a description
* one or more relationship instances

The set identifier names the collection. It does not replace the identifiers of relationship instances inside the collection.

Use one relationship set for a coherent group of graph statements, such as:

* relationships between RAG techniques and components
* specialization relationships between components
* relationships among seed RAG technique records
* relationships exported from a bounded data directory

Do not use a relationship set as a general notes file or as a substitute for entity documents.

---

# Relationship Instance

A relationship instance is one declared graph edge.

It should identify:

* a stable relationship identifier
* a canonical uppercase snake case predicate
* the source entity identifier
* the target entity identifier
* the source data file
* the target data file
* the relationship kind
* a concise description
* structured properties for relationship-specific data

The relationship identifier is the handle used by relationship support, review workflows and graph export.

---

# Predicate Use

The predicate must be a canonical relationship type from the relationship type registry.

Preferred:

```text
Technique USES Component
Component SPECIALIZES Component
Technique COMPLEMENTS Technique
```

Avoid introducing relationship names that are not registered. Relationship sets are data assertions, not a place to define new predicates.

---

# Source and Target References

Relationship instances should use stable identifiers for the source and target.

File paths are included to make the relationship resolvable in the repository layout. They are helpers for validation, review and export, but the entity identifiers remain the semantic references.

Preferred:

```json
{
  "id": "RELATIONSHIP-10102",
  "predicate": "OPTIONALLY_USES",
  "sourceId": "TECHNIQUE-10001",
  "targetId": "COMPONENT-10002",
  "sourceDataFile": "data/rag-techniques/hybrid-retrieval.json",
  "targetDataFile": "data/components/semantic-retriever.json",
  "relationshipKind": "Domain Relationship",
  "description": "Hybrid Retrieval can use a Semantic Retriever in some implementations when a pipeline includes embedding-based or other semantic retrieval signals.",
  "properties": {}
}
```

Avoid:

```json
{
  "predicate": "USES",
  "sourceId": "hybrid retrieval",
  "targetId": "semantic retriever"
}
```

The avoided example relies on names rather than stable identifiers and does not provide enough structure for graph export.

---

# Relationship Kind

Relationship kind describes the local grouping or modeling category for the instance.

It may be useful for:

* separating relationship files by curation workflow
* documenting why a set exists
* guiding validation reports
* organizing graph export inputs

Relationship kind is not the predicate. It should not be used to express semantic meaning that belongs in the canonical relationship type.

---

# Properties

The properties object carries relationship-specific structured data that does not belong in the core edge fields.

Examples include:

* modeling scope
* dataset scope
* derivation notes
* export hints
* review annotations

Properties should remain structured and bounded. If a property becomes reusable across relationship files, it should be promoted into a shared schema field or a reusable definition.

---

# Relationship Support

Relationship sets and relationship support sets have separate responsibilities.

```text
Relationship Set CONTAINS Relationship
Relationship Support Set SUPPORTS Relationship
Relationship Support Set CONTAINS Claim
Relationship Support Set CONTAINS Evidence
Relationship Support Set CONTAINS Reference
```

The relationship set says that an edge exists in the RKM graph. The support set explains why that edge was accepted.

Keep support objects out of relationship set instances unless a future schema version explicitly adds a structured support reference.

---

# Validation

Relationship set documents are validated by `schema/relationship-set.schema.json`.

Validation should ensure that:

* required relationship set fields are present
* every relationship instance has an identifier
* every predicate uses uppercase snake case
* every predicate resolves to a registered relationship type
* every source and target identifier resolves to a data record
* every source and target data file exists
* relationship support references, when present in companion files, resolve to declared relationship identifiers

Schema validation checks document shape. Semantic validation checks registry membership, file resolution and graph consistency.

---

# Modeling Rules

Relationship sets should follow these rules:

* Use one relationship instance for one directed graph edge.
* Use canonical relationship predicates from the relationship type registry.
* Use stable entity identifiers instead of names.
* Use file paths only as repository resolution helpers.
* Do not duplicate derived inverse relationships unless the relationship type explicitly requires stored inverses.
* Do not store claims, evidence or references inside the relationship set.
* Keep relationship descriptions concise and specific to the declared edge.
* Group only relationships that share a coherent curation or dataset boundary.

---

# Non-Goals

A relationship set is not:

* a first-class entity type
* a relationship type registry
* a relationship support set
* a replacement for evidence or claims
* a place to introduce noncanonical predicates
* a place to store prose-only relationship notes
* a complete graph export by itself

---

# Example

```json
{
  "id": "RELATIONSHIP-SET-0001",
  "title": "RAG Technique Component Relationships",
  "description": "Declared relationships connecting seed RAG techniques to architectural components.",
  "relationships": [
    {
      "id": "RELATIONSHIP-10102",
      "predicate": "OPTIONALLY_USES",
      "sourceId": "TECHNIQUE-10001",
      "targetId": "COMPONENT-10002",
      "sourceDataFile": "data/rag-techniques/hybrid-retrieval.json",
      "targetDataFile": "data/components/semantic-retriever.json",
      "relationshipKind": "Domain Relationship",
      "description": "Hybrid Retrieval can use a Semantic Retriever in some implementations when a pipeline includes embedding-based or other semantic retrieval signals.",
      "properties": {
        "confidence": "Conservative",
        "edgeKind": "Domain Relationship",
        "scope": "Seed Dataset",
        "status": "Draft"
      }
    }
  ]
}
```

Concrete files must follow the active relationship set schema and the repository validation rules.
