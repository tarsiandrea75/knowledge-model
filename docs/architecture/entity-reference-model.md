# Entity Reference Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how entity references are represented in the RAG Knowledge Model.

An entity reference is a compact pointer from an embedded structure to an existing first-class RKM entity.

The Entity Reference Model answers the question:

> **How can embedded knowledge point to an entity without duplicating the full entity document or replacing a first-class relationship?**

---

# Core Principle

An entity reference identifies an existing entity by stable identifier.

It is not a relationship object, claim, evidence record, reference source or embedded copy of the target entity.

The stable identifier is authoritative for graph export and cross-file linking. Optional fields such as entity type, slug, name and role exist to improve readability, review and local context.

---

# Entity Reference

An entity reference may appear inside embedded structures that need to point to a known RKM entity.

Examples include:

* a tool contract that names a required provider
* a workflow step that points to an implementing component
* a policy fragment that names the governed entity
* a security control that identifies a protected artifact
* an evidence record that links an observation to a relevant entity

Entity references should be used when the surrounding structure already defines the local meaning of the pointer.

When the pointer itself is the reusable knowledge statement, model it as a relationship instead.

---

# Required Identifier

Every entity reference requires an `id`.

The `id` must be the globally unique immutable identifier of the referenced entity.

Examples:

```text
TECHNIQUE-0001
FRAMEWORK-0003
PAPER-0015
COMPONENT-0028
```

The identifier remains authoritative when the target entity changes display name, slug, file path, description, metadata or version.

---

# Optional Readability Fields

An entity reference may include optional fields that help contributors understand the target without resolving the full document.

Optional fields include:

* `entityType`
* `slug`
* `name`
* `role`

These fields must not override the stable identifier.

If `slug` or `name` becomes stale, the reference still points to the entity identified by `id`.

---

# Role

The `role` field describes how the referenced entity participates in the local embedded structure.

Examples:

```text
primary retriever
required provider
protected artifact
evaluation target
governing policy
```

Use `role` for local context only.

Do not encode reusable semantic predicates in `role`. Reusable graph meaning belongs in relationship objects with canonical relationship types.

---

# Entity Reference vs Relationship

An entity reference is a pointer.

A relationship is a semantic graph statement between two entities.

Use an entity reference when an embedded object needs to name a participant.

Use a relationship when RKM should preserve the association as reusable graph knowledge.

Preferred relationship example:

```text
Framework IMPLEMENTS Technique
```

Preferred embedded reference example:

```json
{
  "id": "FRAMEWORK-0003",
  "entityType": "Framework",
  "slug": "spring-ai",
  "name": "Spring AI",
  "role": "implementation framework"
}
```

The embedded reference helps interpret the local structure. The relationship expresses the reusable graph statement.

---

# Entity Reference vs Reference

An entity reference points to an RKM entity.

A Reference identifies an external or source-like item used for citation, provenance or evidence.

Use an entity reference for an existing RKM entity such as a technique, framework, paper, component, dataset, benchmark, model, retriever, reranker, agent or provider.

Use a Reference for a cited source such as official documentation, a repository, a paper, a standard, a benchmark report or a maintainer analysis source.

---

# Entity Reference vs Identity

Identity defines the entity itself.

An entity reference points to that entity from another structure.

The referenced entity owns its canonical name, aliases, taxonomy, lifecycle state, metadata, relationships, claims, evidence and references.

The entity reference should not duplicate those fields.

---

# Validation Expectations

Entity references must be stable, minimal and resolvable.

Validation should ensure that:

* `id` follows the shared identifier pattern
* `entityType` uses the shared identity entity-type vocabulary when present
* `slug` follows the shared slug pattern when present
* optional readability fields do not replace `id`
* embedded references do not duplicate complete entity documents

Repository-level validation may later verify that referenced identifiers resolve to known entity files when entity instances are available.

---

# Graph Export

Entity references support graph export by preserving stable links from embedded structures to first-class nodes.

During export, an entity reference may become an edge endpoint, an annotation target or a supporting pointer depending on the containing structure.

Exporters must treat `id` as the authoritative node key.

Fields such as `slug`, `name` and `role` may be exported as labels or context, but they must not create separate nodes for the same entity.
