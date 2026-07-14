# Repository Surface Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines the architectural boundaries between the major repository surfaces in RKM.

RKM contains architecture documents, schemas, shared definitions, registries, examples, fixtures, populated data, graph exports, and maintenance guidance. These surfaces work together, but they do not have the same authority.

This document answers the question:

> **Which repository surface is authoritative for which kind of RKM knowledge?**

---

# Core Principle

Each repository surface has one primary responsibility.

Architecture documents define conceptual meaning.

Schemas define machine-validatable structure.

Registries define canonical vocabulary.

Data records state populated knowledge.

Graph exports project existing knowledge for downstream use.

No surface should silently replace another surface's responsibility.

---

# Architecture Documents

Architecture documents define the meaning, scope, boundary, and modeling intent of RKM concepts.

They are authoritative for:

* concept definitions
* modeling boundaries
* semantic distinctions
* relationship interpretation
* evidence and metadata expectations
* compatibility principles

Architecture documents should not be treated as instance data.

They may describe how a concept should be represented, but the actual populated knowledge belongs in data records or fixtures.

---

# Schemas

Schemas define structural contracts for JSON documents.

They are authoritative for:

* required fields
* allowed value shapes
* identifier patterns
* reusable object composition
* machine validation expectations

Schemas are not the sole source of truth for domain meaning.

A schema field is valid only when it remains coherent with the architecture model, registry vocabulary, relationship model, evidence model, metadata model, ontology, naming conventions, and versioning rules.

---

# Shared Definitions

Shared definitions are reusable schema fragments under `schema/definitions/`.

They are authoritative for repeated structures that must remain consistent across multiple schemas.

Examples of shared definition responsibilities include:

* identity
* metadata
* relationships
* claims
* evidence
* references
* entity references
* descriptions

Shared definitions should not become hidden first-class entity models.

When a shared definition needs stable standalone identity, relationships, claims, evidence, lifecycle state, or independent graph export, the concept should be reviewed as a first-class entity or relationship structure instead of growing only as an embedded object.

---

# Registries

Registries define canonical vocabulary.

They are authoritative for:

* entity type names
* relationship predicate names
* accepted labels and descriptions for governed terms
* lifecycle and stability state for governed terms
* expected schema and directory mappings where applicable

Schemas validate registry shape, but the registry document is the vocabulary authority.

Architecture documents may explain the meaning of registry-backed concepts, but a term becomes canonical only when it is represented through the relevant registry and governance process.

---

# Fixtures

Fixtures are minimal examples used to prove schema shape, validation wiring, and graph export mechanics.

They are authoritative only for example validity.

Fixtures are not the populated RKM dataset and should not be interpreted as complete ecosystem knowledge.

A fixture may intentionally be small, abstract, or pedagogical when that makes validation behavior clear.

---

# Populated Data

Populated data records under `data/` represent RKM's current structured knowledge content.

They are authoritative for:

* declared seed entities
* declared relationship instances
* declared relationship support
* populated claims, evidence, and references
* manifest-declared validation scope

Populated data should remain conservative.

A data record should not imply undocumented relationships, evidence, or ontology commitments merely because prose fields mention related concepts.

Relationships that matter for graph export, search, evidence, or downstream reasoning should be represented as explicit relationship records or structured fields according to the relevant model.

---

# Examples

Examples demonstrate how repository contracts can be consumed.

They are authoritative only for the example package or generated artifact they represent.

Examples may be derived from fixtures, populated data, or exporters. When an example is generated, the source generator and source data remain authoritative.

Generated examples should not be edited as independent semantic sources unless the generation contract explicitly allows that workflow.

---

# Graph Exports

Graph exports are projections of canonical RKM knowledge.

They are authoritative for the committed exported view, not for new domain semantics.

An exported graph must preserve:

* stable identifiers
* canonical relationship predicates
* canonical relationship direction
* provenance back to source records
* evidence, claim, reference, and metadata distinctions when exported

Graph exporters must not invent domain relationships, support metadata, entity types, relationship predicates, lifecycle states, or source authority that are absent from canonical repository sources.

---

# Maintenance Guidance

Maintenance documents, task guides, rule files, and governance reports define operating rules for changing the repository.

They are authoritative for:

* contributor workflow
* validation expectations
* rule routing
* governance backlog items
* known maturity gaps
* release and automation guardrails

Maintenance guidance should not introduce new domain concepts that bypass architecture review, schema contracts, or registry governance.

When a maintenance document identifies a modeling gap, the resulting change should still land in the appropriate architecture, schema, registry, data, or validation surface.

---

# Boundary Rules

Use the architecture surface when the question is conceptual.

Use the schema surface when the question is structural.

Use the registry surface when the question is canonical vocabulary.

Use the fixture surface when the question is minimal validity.

Use the populated data surface when the question is current RKM knowledge content.

Use the graph export surface when the question is downstream projection.

Use the maintenance surface when the question is how to change, validate, release, or operate the repository.

---

# Summary

RKM is a structured knowledge model, not a single flat document collection.

Its repository surfaces are intentionally separated so conceptual meaning, validation contracts, canonical vocabulary, populated knowledge, examples, generated exports, and operational governance can evolve without overwriting each other.

This separation keeps RKM readable for humans, validatable by tools, and usable by downstream consumers.
