# Relationship Type Registry Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines the Relationship Type Registry model in the RAG Knowledge Model.

The Relationship Type Registry is the governed registry document that records the canonical relationship predicates RKM recognizes as ontology vocabulary.

The Relationship Type Registry Model answers the question:

> **How does RKM publish, validate and govern the canonical predicates that may connect knowledge entities?**

---

# Core Principle

The Relationship Type Registry is the authoritative published list of canonical relationship predicates.

The Relationship Type Model defines what a relationship type means.

The Registry Model defines how controlled vocabulary documents are governed.

The Relationship Type Registry Model defines how those rules apply to the registry document validated by `schema/relationship-type-registry.schema.json`.

A predicate should not be treated as canonical because it appears in prose, an example, a relationship file or a graph export. It becomes canonical when the registry entry, endpoint rules, lifecycle metadata and ontology meaning are coherent.

---

# Registry Document

A Relationship Type Registry document contains metadata for the registry itself and a collection of relationship type entries.

The registry document should identify:

* the metadata for the registry artifact
* the ontology version represented by the registry
* the set of registered relationship type definitions
* registry-level notes when they clarify vocabulary governance

The registry is a vocabulary authority, not a collection of relationship instances. It defines the predicates that concrete RKM relationships may use.

---

# Relationship Type Entries

Each relationship type entry defines one canonical predicate.

An entry should provide enough information for humans and tools to understand:

* the canonical predicate name
* the display label
* the relationship type description
* the relationship category
* the canonical source-to-target direction
* allowed source entity types
* allowed target entity types
* inverse behavior when an inverse exists
* transitivity, symmetry or other reasoning expectations when applicable
* lifecycle status
* stability level
* version metadata

The registry entry is the durable contract for the predicate. Supporting architecture documents may explain relationship modeling in more detail, and schemas may validate registry structure, but the registry entry remains the controlled vocabulary record.

---

# Canonical Predicate Names

Relationship type names use uppercase snake case.

Examples include:

```text
REQUIRES
DEPENDS_ON
IMPLEMENTS
EVALUATES
INTRODUCES
PART_OF
CONTAINS
```

The canonical predicate name is stable ontology vocabulary. Renaming a published relationship type is a breaking ontology change unless the previous value is deprecated with an explicit replacement.

Labels may be optimized for human display, but they must not replace the canonical predicate value used by relationship instances, schemas, graph export and documentation.

---

# Direction and Endpoint Alignment

A relationship type entry must define the semantic direction of the predicate.

The canonical direction should identify:

* the role of the source entity
* the role of the target entity
* the source-to-target meaning of the predicate

Endpoint rules should identify which entity types may appear as sources and targets. These rules make invalid graph statements detectable before they become repository knowledge.

For example:

```text
Framework IMPLEMENTS Workflow
Benchmark EVALUATES Reranker
Technique REQUIRES Retriever
```

The predicate controls how the relationship is read. The relationship instance supplies the concrete source and target identifiers.

---

# Inverse and Reasoning Rules

Some predicates have useful inverse views or reasoning behavior.

The registry should record whether an inverse is:

* derived for query, documentation or export views
* stored as authored knowledge
* absent because a reverse statement would be ambiguous or misleading

Reasoning behavior should be explicit when it affects validation or graph traversal. For example, `SPECIALIZES` may be transitive, while `ALTERNATIVE_TO` may be symmetric only when the registry defines that behavior.

Derived inverse views must not create duplicate authored relationships unless the registry explicitly allows stored inverse relationships.

---

# Lifecycle and Stability

Relationship type entries follow the ontology lifecycle used across RKM.

Lifecycle status indicates whether the predicate is draft, under review, published, deprecated or archived.

Stability indicates how safe the predicate is for schemas, data records, relationship sets, graph export and downstream tools.

Published and stable relationship types may be used as durable ontology vocabulary. Deprecated relationship types should remain readable for compatibility and should identify a replacement when one exists.

---

# Relationship to Relationship Instances

The Relationship Type Registry defines predicates.

Relationship sets declare concrete relationship instances.

Relationship support sets justify why those instances are accepted into RKM.

```text
Relationship Type Registry DEFINES Predicate
Relationship Set CONTAINS Relationship
Relationship Support Set SUPPORTS Relationship
```

The registry should not contain relationship instances. Relationship files should not define new canonical predicates. This separation keeps ontology vocabulary, graph structure and evidence support independently reviewable.

---

# Governance Rules

Changes to the Relationship Type Registry affect the ontology surface of RKM.

Adding a new relationship type should be coordinated with:

* the Relationship Type Model
* relationship instance validation
* endpoint rules for registered entity types
* relationship set authoring guidance
* relationship support expectations
* graph export behavior
* migration notes when existing relationships are affected

Removing or renaming a published relationship type should be avoided. Deprecation with explicit replacement is preferred because it preserves existing references, graph history and downstream compatibility.

---

# Modeling Guidance

Use the Relationship Type Registry when a predicate must have reusable semantic value across schemas, data records, relationship sets, documentation and graph exports.

Do not use the registry for:

* one-off prose labels
* local relationship descriptions
* temporary planning categories
* source-specific phrasing that is not RKM ontology vocabulary
* inferred inverse names that are not governed vocabulary

The registry should stay small enough to govern carefully and complete enough to make relationship validation deterministic.
