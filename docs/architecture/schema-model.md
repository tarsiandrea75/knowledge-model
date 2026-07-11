# Schema Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how JSON Schemas are used in the RAG Knowledge Model.

The Schema Model explains how conceptual architecture, controlled vocabularies and machine validation fit together before entity instance files are added to the repository.

This document answers the question:

> **How does RKM turn the architecture model into valid, reusable and graph-ready JSON documents?**

---

# Core Principle

Schemas validate document structure.

Architecture documents define conceptual meaning.

Registries define canonical vocabulary.

No schema is the sole source of truth for a domain concept. A schema is valid only when it remains coherent with the domain model, entity model, relationship model, evidence model, metadata model, ontology, naming conventions and versioning rules.

---

# Schema Layers

RKM schemas are organized into reusable layers.

```text
Shared Definitions
  |
  +-- Registry Schemas
  |
  +-- Ontology Schema
  |
  +-- Specialized Entity Schemas
```

Each layer has a different responsibility.

---

# Shared Definitions

Shared definitions live under `schema/definitions/`.

They define reusable structures used across many schemas.

Current shared definitions include:

* identity
* metadata
* description
* relationship
* relationship type
* entity type
* claim
* evidence
* reference
* knowledge entity

Shared definitions should be introduced when a concept is reused across multiple schema families or has stable semantic meaning across the ontology.

They should not contain specialized entity details that apply only to one entity type.

---

# Identity Definition

The identity definition is the shared gatekeeper for entity type support.

Every specialized entity schema that constrains `identity.entityType` must use a value already supported by `schema/definitions/identity.schema.json`.

This rule keeps the schema graph internally consistent.

The correct order for adding a new specialized entity type is:

1. Establish that the entity type is part of the architecture.
2. Add shared identity support for the entity type.
3. Add or update registry support for the entity type.
4. Add the specialized schema.
5. Add instance documents only after the schema is valid.

A specialized schema must not introduce a new `identity.entityType` value by itself.

---

# Specialized Entity Schemas

Specialized entity schemas live directly under `schema/`.

Each specialized entity schema represents one concrete entity type from the architecture.

Examples include:

* `schema/rag-technique.schema.json`
* `schema/framework.schema.json`
* `schema/paper.schema.json`
* `schema/dataset.schema.json`
* `schema/benchmark.schema.json`
* `schema/embedding-model.schema.json`
* `schema/language-model.schema.json`
* `schema/vector-database.schema.json`
* `schema/graph-database.schema.json`
* `schema/retriever.schema.json`
* `schema/reranker.schema.json`
* `schema/chunking-strategy.schema.json`
* `schema/prompt-technique.schema.json`
* `schema/evaluation-metric.schema.json`
* `schema/agent.schema.json`
* `schema/provider.schema.json`
* `schema/pattern.schema.json`
* `schema/glossary.schema.json`

A specialized schema should compose shared definitions for identity, metadata, descriptions, relationships, claims, evidence, references and external links unless there is a strong architectural reason to do otherwise.

The specialized section of the schema should contain only domain-specific structured knowledge for that entity type.

---

# Registry Schemas

Registry schemas validate controlled vocabulary documents.

They are not substitutes for the registries themselves.

For example:

* `schema/entity-type-registry.schema.json` validates entity type registry documents.
* `schema/relationship-type-registry.schema.json` validates relationship type registry documents.

The registry document is the authoritative vocabulary artifact.

The registry schema validates the shape of that artifact.

---

# Ontology Schema

The ontology schema validates ontology export documents.

Ontology exports should be generated from the same canonical concepts represented in architecture documents, registries and schemas.

The ontology schema should not introduce vocabulary that is absent from the relevant registry or architecture model.

---

# Relationship Fields

Entity schemas should expose relationships as first-class structured arrays.

Relationship values must use the shared relationship definition so that source entities, target entities, predicates, evidence, confidence and lifecycle metadata remain exportable to graph representations.

Relationship predicates must use canonical uppercase snake case terms from the relationship type registry.

Relationship examples in documentation should use canonical predicates such as `REQUIRES`, `IMPLEMENTS`, `EVALUATES`, `INTRODUCES`, `EXTENDS`, `SPECIALIZES`, `PART_OF` and `CONTAINS`.

---

# Claims, Evidence and References

Claims, evidence and references are separate concepts.

A schema should not collapse them into plain prose fields when the information has reusable semantic meaning.

Claims represent asserted knowledge.

Evidence supports or challenges claims.

References identify source materials.

Specialized entity schemas should reuse the shared definitions for these structures so that provenance and confidence can be preserved across generated documentation, validation, search indexes and graph exports.

---

# External Links

External links are resources associated with an entity but not necessarily cited as evidence.

They should be modeled separately from references.

Examples include:

* project home pages
* documentation pages
* package repositories
* hosted demos
* dashboards

When an external resource is used to support a claim, it should be represented as a reference and connected through evidence.

---

# Required Fields

Required fields must express minimum useful structure, not editorial preference.

Every specialized entity schema should require:

* identity
* metadata
* description
* the specialized detail object for that entity type

Optional fields should remain optional when knowledge may be unknown, evolving or source-dependent.

Arrays that represent controlled, meaningful collections should use `uniqueItems` when duplicate values would be semantically invalid.

---

# Compatibility

Schemas should remain compatible with graph export, generated documentation and downstream typed models.

To support that compatibility:

* identifiers should remain stable
* references should be structured
* reusable concepts should be shared definitions
* domain-specific fields should be scoped to specialized detail objects
* lifecycle and version fields should follow the metadata and versioning models
* controlled values should align with registries when a registry exists

---

# Change Order

Schema work should follow the smallest coherent change order.

For a new reusable structure, add or update a shared definition before using it in specialized schemas.

For a new entity type, add identity and registry support before adding a specialized schema.

For a new relationship predicate, add registry support before using it as canonical documentation or structured data.

For a new specialized field, keep the change local to the specialized schema unless the concept is reusable across entity types.

---

# Current Coverage Boundary

The current schema set covers many primary RAG entity types, including techniques, frameworks, components, papers, datasets, benchmarks, patterns, models, retrievers, rerankers, databases, chunking strategies, prompt techniques, evaluation metrics, agents, providers and glossary entries.

Some architecture-level entity types may be defined conceptually before they have identity support, registry entries or specialized schemas.

That state is allowed as long as later schema additions follow the required change order and do not introduce unsupported `identity.entityType` constants.

---

# Acceptance Criteria

A schema change is coherent when:

* it validates as JSON Schema Draft 2020-12
* all `$ref` values resolve
* specialized `identity.entityType` constants are supported by the shared identity definition
* controlled values align with registries when registries exist
* relationship predicates are canonical
* shared concepts are not duplicated as incompatible local structures
* required fields match the minimum useful structure for the entity type
* examples, if present, are complete and valid

---

# Non-Goals

The Schema Model does not define the full ontology.

It does not define every entity type.

It does not replace the registry model.

It does not decide which entity instance files should be created.

It defines how schema artifacts must be structured so that RKM remains coherent as the knowledge model grows.
