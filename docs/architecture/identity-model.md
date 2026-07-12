# Identity Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how identity is represented in the RAG Knowledge Model.

Identity is the stable, machine-readable description of what an entity is, how it is named, how it is typed and how it can be referenced across documents, schemas, registries and graph exports.

The Identity Model answers the question:

> **How does RKM identify an entity independently of its file path, display name, metadata or descriptive knowledge?**

---

# Core Principle

Identity is the durable reference boundary of an entity.

An entity identity must remain stable enough that relationships, claims, evidence, references, examples, registries and downstream graph exports can point to the same concept over time.

Identity is not the full entity description.

Identity identifies the entity. Description explains the entity. Metadata describes the document that stores the entity.

---

# Identity Scope

The identity object applies to first-class knowledge entities.

It captures:

* stable identifier
* entity type
* slug
* canonical names
* aliases
* abbreviations
* keywords
* tags
* taxonomy
* lifecycle status
* visibility
* language
* entity version

Identity fields should support lookup, linking, validation and graph export without requiring prose interpretation.

---

# Stable Identifier

The stable identifier is the primary machine-facing identity field.

It is globally unique within RKM and immutable after publication.

Examples:

```text
TECHNIQUE-0001
FRAMEWORK-0003
PAPER-0015
COMPONENT-0028
```

A stable identifier must not change when:

* the entity display name changes
* the slug changes
* the file path changes
* the entity document version changes
* the entity receives additional evidence
* the entity is deprecated
* the entity moves to a different directory

Identifier prefixes should align with registered entity types and their registry definitions.

---

# Entity Type

The entity type classifies the entity at the schema and ontology level.

The entity type determines which specialized schema may validate the entity document.

Examples:

```text
Technique
Framework
Paper
Component
Dataset
Benchmark
EmbeddingModel
LanguageModel
Retriever
Reranker
Agent
Provider
```

Specialized schemas must only use entity type values already supported by the shared identity definition.

New entity types require shared identity support and registry support before a specialized top-level schema can safely depend on them.

---

# Slug

The slug is the preferred filesystem-safe and URL-safe human-readable identifier.

Examples:

```text
hyde
self-rag
graph-rag
spring-ai
```

Slugs should be lowercase kebab-case.

A slug may change when canonical naming changes, but changes should be managed carefully because slugs are often visible in file paths, URLs and generated documentation.

The stable identifier remains the authoritative reference when the slug changes.

---

# Names

The name object stores canonical human-facing names.

It may include:

* official name
* display name
* short name
* acronym
* pronunciation

The official name should be the most formal or source-backed name for the entity.

The display name should be the preferred label for readers and generated documentation.

Short names and acronyms should be included when they are widely used or needed for disambiguation.

---

# Aliases And Abbreviations

Aliases represent alternative names used in literature, implementations, products or community discussion.

Abbreviations represent shortened textual forms.

Aliases and abbreviations are useful for search and source matching, but they must not replace the canonical name or stable identifier.

When an old slug or name remains important after a rename, it should be preserved as an alias when appropriate.

---

# Keywords And Tags

Keywords support search and discovery.

Tags support lightweight grouping.

These fields are identity-adjacent classification aids, not substitutes for structured relationships, entity types or registry-controlled concepts.

Important semantic relationships should be modeled as relationship objects instead of being encoded only as tags.

---

# Taxonomy

Taxonomy fields provide optional coarse classification within an entity type.

They may describe:

* family
* subfamily
* category
* domain

Taxonomy should be used for stable classification that helps organize entities within RKM.

It should not be used to store claims, evidence, implementation details or relationship targets.

---

# Lifecycle Identity Fields

Identity includes selected lifecycle fields that affect how the entity can be discovered and referenced.

Canonical lifecycle fields include:

* status
* visibility
* language
* version

Status describes the lifecycle state of the entity identity and document.

Visibility describes whether the entity is public or internal.

Language identifies the primary language of the entity document.

Version describes the version of the entity document and should follow Semantic Versioning.

---

# Identity vs Metadata

Identity describes the entity reference.

Metadata describes the repository artifact that stores the entity.

Example identity concerns:

* what the entity identifier is
* what entity type the document represents
* what canonical name should be displayed
* what slug should be used for lookup

Example metadata concerns:

* when the document was created
* when the document was updated
* which schema version was used
* who authored or reviewed the document
* what license applies to the document

These concerns must remain separate so repository operations do not pollute domain identity.

---

# Identity vs Description

Identity identifies the entity.

Description explains the entity.

The identity object should not contain summaries, definitions, implementation notes, advantages, limitations or evidence-backed claims.

Those belong in the description field, specialized entity details, claims, evidence or relationships.

---

# Graph Export

Graph exports should preserve identity fields needed for stable node creation and human-readable labels.

At minimum, graph export should preserve:

* stable identifier
* entity type
* slug
* display name
* official name
* aliases when useful for search
* lifecycle status
* version

Graph nodes should use stable identifiers as durable keys.

Names and slugs may be exported as labels or lookup properties, but they should not replace stable identifiers as graph keys.

---

# Modeling Guidance

Use identity fields when the information helps identify, classify, find or reference the entity.

Use relationships when the information connects one entity to another.

Use metadata when the information describes the repository artifact.

Use claims and evidence when the information asserts behavior, quality, provenance, performance, reliability or tradeoffs.

Use specialized entity details when the information describes domain-specific structure for a supported entity type.
