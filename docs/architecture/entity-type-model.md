# Entity Type Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how entity types are represented in the RAG Knowledge Model.

An entity type is the canonical ontology category that determines what kind of first-class knowledge entity a document represents.

The Entity Type Model answers the question:

> **Which kinds of entities can RKM describe as identity-backed knowledge, and how is that vocabulary governed before it appears in schemas, registries and data?**

---

# Core Principle

An entity type is controlled ontology vocabulary.

It is not a tag, display label, directory name or implementation detail.

Every canonical entity type must have stable meaning, identity support, registry metadata, schema support and lifecycle metadata before it is used as a first-class entity.

Example:

```text
Technique USES Component
```

In this statement, `Technique` and `Component` are entity types.

The relationship type `USES` describes the predicate between instances of those types.

---

# Entity Type vs Entity

An entity type defines the reusable ontology category.

An entity is a concrete knowledge document with identity, metadata, description and domain-specific structure.

Entity type:

```json
{
  "type": "Retriever",
  "label": "Retriever",
  "description": "A component or system responsible for retrieving candidate information for a Retrieval-Augmented Generation workflow.",
  "identifierPrefix": "RETRIEVER",
  "schema": "schema/retriever.schema.json"
}
```

Entity:

```json
{
  "identity": {
    "id": "RETRIEVER-0001",
    "slug": "lexical-retriever",
    "name": {
      "official": "Lexical Retriever",
      "display": "Lexical Retriever"
    },
    "entityType": "Retriever"
  }
}
```

The entity type defines what category the entity belongs to.

The entity document records a specific item in that category.

---

# Canonical Name

Every entity type has one canonical `type` value.

Entity type names use PascalCase without spaces.

Examples:

```text
Technique
Framework
Paper
Component
VectorDatabase
EvaluationMetric
ChunkingStrategy
PromptTechnique
```

The canonical name is stable ontology vocabulary.

Changing it is a breaking semantic change unless the previous value is deprecated with an explicit replacement.

---

# Identity Support

A first-class entity type must be supported by `schema/definitions/identity.schema.json`.

Specialized schemas must only constrain `identity.entityType` to values already supported by the shared identity definition.

This rule prevents schemas from creating entity categories that cannot be validated consistently across the repository.

Preferred sequence:

```text
Add shared identity support.
Add registry entry.
Add specialized schema.
Add data instances.
```

Rejected sequence:

```text
Rejected example: Add a specialized Threat schema before Threat exists in shared identity support.
```

The rejected sequence creates a schema that cannot be safely used as an identity-backed RKM entity.

---

# Registry Authority

The Entity Type Registry is the authoritative source for canonical entity type entries.

Each registry entry should define:

* type
* label
* plural label
* description
* category
* identifier prefix
* canonical directory
* schema path
* lifecycle status
* stability level
* ontology version metadata
* required or recommended relationship expectations when applicable

The architecture defines the governance rules.

The registry lists the accepted entity types.

The schema validates the registry structure.

---

# Category

Entity type category groups related types for documentation, navigation and ontology review.

Canonical categories include:

```text
Core
RAG Concept
Implementation
Evaluation
Source
Evidence
Workflow
Infrastructure
Quality
Use Context
```

Category is not a substitute for entity type.

For example, `Retriever`, `Reranker` and `LanguageModel` may all belong to implementation knowledge, but they remain distinct entity types because they have different semantics, schemas and relationship expectations.

---

# Identifier Prefix

Every instantiable entity type should define an identifier prefix.

The prefix must match the stable identifier pattern used by entity identities.

Examples:

```text
TECHNIQUE-0001
FRAMEWORK-0001
VECTOR-DATABASE-0001
EVALUATION-METRIC-0001
```

Identifier prefixes should remain stable after publication because they are part of durable cross-document references.

---

# Schema Support

An instantiable entity type should have a schema for validating documents of that type.

Specialized schemas should compose shared definitions whenever possible:

* identity
* metadata
* description
* relationship
* claim
* evidence
* reference

Reusable concepts that are not identity-backed entity documents should usually live under `schema/definitions/`.

Examples include:

```text
Claim
Evidence
Reference
Advantage
Limitation
Risk
Policy
Workflow
Tool
Use Case
```

These concepts may be first-class in the domain model without being standalone identity-backed entity documents yet.

---

# Relationship Expectations

Entity types may define required or recommended relationships.

Relationship expectations describe graph completeness for entities of a type.

Examples:

```text
Paper INTRODUCES Technique
Technique USES Component
Benchmark EVALUATES Retriever
Component PART_OF Workflow
```

Required relationships should be used only when an entity is incomplete without the relationship.

Recommended relationships should be used when the relationship improves graph utility but is not always available.

Relationship expectations must use canonical relationship predicates from the relationship type registry.

---

# Lifecycle

Entity types follow the ontology lifecycle.

Canonical lifecycle values are:

```text
Draft
Review
Published
Deprecated
Archived
```

Draft entity types may be proposed but should not be used broadly in data.

Review entity types are being evaluated for canonical use.

Published entity types are available for normal repository use.

Deprecated entity types remain readable for historical compatibility but should not be used for new entities.

Archived entity types are retained only to interpret older data.

---

# Stability

Entity types should declare stability when the registry schema supports it.

Canonical stability values are:

```text
Experimental
Stable
Deprecated
```

Experimental entity types may change before publication.

Stable entity types may be used by schemas, entity data, relationship validation, generated exports and documentation.

Deprecated entity types should identify a replacement when one exists.

---

# Abstract Types

An entity type may be abstract when it describes a conceptual grouping rather than an instantiable document category.

Abstract types should not be used directly as `identity.entityType` values for entity documents unless the registry and identity schema explicitly allow that use.

For example, `Model` may be useful as a conceptual parent of `EmbeddingModel` and `LanguageModel`, while concrete entities should use the supported specialized type.

---

# Graph Export

Entity types are exported as graph node classifications.

Graph exporters should preserve:

* canonical entity type
* stable identifier prefix
* entity category
* schema path
* lifecycle status
* relationship expectations when available

Entity type metadata helps downstream consumers distinguish concepts, implementations, sources, evaluation assets and infrastructure without relying on directory names or display labels.

---

# Modeling Rules

Entity type modeling should follow these rules:

* Do not introduce a specialized schema for a new entity type before shared identity support exists.
* Do not use plural labels, directory names or tags as substitutes for canonical entity type names.
* Do not use relationship type names as entity type names.
* Do not model reusable embedded concepts as identity-backed entity types until the repository has identity, registry, schema and relationship guidance for them.
* Do not rename published entity types without deprecation and replacement metadata.
* Use PascalCase for entity type names.
* Use uppercase kebab-compatible identifier prefixes for stable IDs.
* Keep entity type descriptions semantic, not product-specific.
* Keep relationship expectations aligned with the relationship type registry.

---

# Validation

Entity type registry documents are validated by `schema/entity-type-registry.schema.json`.

Individual entity type entries are structured by `schema/definitions/entity-type.schema.json`.

Entity documents are validated by their specialized schemas, which constrain `identity.entityType` to the supported canonical value for that schema.

Semantic validation should ensure that:

* registry entity types are supported by shared identity when they are instantiable
* specialized schemas use only supported identity entity type values
* identifier prefixes match entity IDs
* canonical directories match repository data locations
* schema paths resolve
* relationship expectations use canonical relationship predicates
