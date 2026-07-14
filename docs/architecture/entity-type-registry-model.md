# Entity Type Registry Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines the Entity Type Registry model in the RAG Knowledge Model.

The Entity Type Registry is the governed registry document that records the canonical entity types RKM recognizes as ontology vocabulary.

The Entity Type Registry Model answers the question:

> **How does RKM publish, validate and govern the set of canonical entity types that may appear in identity-backed knowledge?**

---

# Core Principle

The Entity Type Registry is the authoritative published list of canonical entity type terms.

The Entity Type Model defines what an entity type means.

The Registry Model defines how controlled vocabulary documents are governed.

The Entity Type Registry Model defines how those rules apply to the registry document validated by `schema/entity-type-registry.schema.json`.

An entity type should not be treated as canonical because it appears in prose, a directory name, a draft schema or a local example. It becomes canonical when the registry entry, identity support, schema support and lifecycle metadata are coherent.

---

# Registry Document

An Entity Type Registry document contains metadata for the registry itself and a collection of entity type entries.

The registry document should identify:

* the metadata for the registry artifact
* the ontology version represented by the registry
* the set of registered entity type definitions
* registry-level notes when they clarify vocabulary governance

The registry is a vocabulary authority, not a catalog of entity instances. It defines the allowed entity type terms that concrete RKM entity documents may use.

---

# Entity Type Entries

Each entity type entry defines one canonical ontology term.

An entry should provide enough information for humans and tools to understand:

* the canonical type name
* the display label and plural label
* the entity type description
* the ontology category
* the identifier prefix used by entity identities
* the canonical directory for data records when applicable
* the schema path for validating instances when applicable
* lifecycle status
* stability level
* version metadata
* relationship expectations when applicable

The registry entry is the durable contract for the term. Supporting architecture documents may explain the concept in more detail, and schemas may validate instances of the concept, but the registry entry remains the controlled vocabulary record.

---

# Canonical Type Names

Entity type names use PascalCase without spaces.

Examples include:

```text
Technique
Framework
Component
VectorDatabase
EvaluationMetric
ChunkingStrategy
PromptTechnique
```

The canonical type name is stable ontology vocabulary. Renaming a published entity type is a breaking ontology change unless the previous value is deprecated with an explicit replacement.

Labels may be optimized for human display, but they must not replace the canonical type value used by identity, schemas, relationships and graph export.

---

# Identity Alignment

An instantiable entity type must align with the shared identity model before entity records use it.

The registry entry and shared identity support should agree on:

* the canonical entity type value
* the identifier prefix pattern, when identity validation constrains it

This alignment allows validators, graph exporters and generated documentation to interpret entity records consistently.

A registry entry without identity support may be useful during early ontology design, but it should not be used for identity-backed entity records until shared identity validation supports it.

---

# Schema Alignment

The Entity Type Registry schema validates the registry document shape.

Specialized entity schemas validate concrete entity records.

The registry should not use schema paths as informal labels. A schema path in an entity type entry should point to the contract that validates entity records of that type or be omitted when the type is not yet represented by a standalone specialized schema.

Reusable embedded concepts may have schema definitions without becoming registry-backed entity types. The registry should distinguish first-class entity types from supporting definitions so RKM does not accidentally promote embedded structures into identity-backed ontology categories.

---

# Lifecycle and Stability

Entity type entries follow the ontology lifecycle used across RKM.

Lifecycle status indicates whether the term is draft, under review, published, deprecated or archived.

Stability indicates how safe the term is for schemas, data records, graph export and downstream tools.

Published and stable entity types may be used as durable ontology vocabulary. Deprecated entity types should remain readable for compatibility and should identify a replacement when one exists.

---

# Relationship Expectations

The Entity Type Registry may record required or recommended relationship expectations for an entity type.

Relationship expectations help contributors and tools understand which semantic links are normally needed for complete records of that type.

These expectations should reference canonical relationship vocabulary and should remain consistent with the Relationship Type Registry. They are not a substitute for relationship instances in data records.

---

# Governance Rules

Changes to the Entity Type Registry affect the ontology surface of RKM.

Adding a new entity type should be coordinated with:

* the Entity Type Model
* shared identity support
* specialized schema support when the type is instantiable
* data directory conventions when records will be stored
* relationship type endpoint rules
* graph export behavior
* migration notes when existing records are affected

Removing or renaming a published entity type should be avoided. Deprecation with explicit replacement is preferred because it preserves existing references, graph history and downstream compatibility.

---

# Modeling Guidance

Use the Entity Type Registry when a term must be reusable ontology vocabulary across schemas, data records, relationships, documentation and graph exports.

Do not use the registry for:

* local prose labels
* temporary planning categories
* one-off documentation groupings
* implementation-specific classes that are not RKM ontology types
* embedded structures that do not need identity-backed records

The registry should stay small enough to govern carefully and complete enough to make entity type validation deterministic.
