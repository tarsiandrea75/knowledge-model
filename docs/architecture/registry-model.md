# Registry Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how registries are represented in the RAG Knowledge Model.

Registries are controlled vocabulary documents that make ontology terms explicit, reviewable and machine-validatable.

The Registry Model answers the question:

> **Which vocabulary terms are canonical in RKM, and how are those terms governed over time?**

---

# Core Principle

A registry is the authoritative source for a controlled vocabulary.

Schemas define shape.

Architecture documents define meaning.

Registries define the accepted terms that contributors and tools may use.

Examples:

```text
Entity Type Registry defines Technique, Framework and Retriever.
Relationship Type Registry defines REQUIRES, IMPLEMENTS and EVALUATES.
```

---

# Registry Responsibilities

Every registry is responsible for:

* declaring canonical vocabulary terms
* defining the meaning of each term
* preserving stable term names
* recording lifecycle status
* supporting validation
* supporting graph export
* documenting deprecation and replacement paths

A registry is not a free-form glossary.

It is a governed vocabulary used by schemas, entity documents, relationship documents, ontology exports and generated documentation.

---

# Registry Scope

RKM uses registries when a value has reusable semantic meaning across the repository.

Registry-backed vocabulary should be used for:

* entity types
* relationship types
* relationship direction rules
* required and recommended relationship expectations
* ontology lifecycle status
* stable schema-to-ontology mappings

Registry-backed vocabulary should not be used for:

* one-off prose examples
* local implementation notes
* transient labels
* source-specific names that are not RKM concepts

---

# Entity Type Registry

The Entity Type Registry defines canonical entity types in the ontology.

Each entity type definition should include:

* type
* label
* description
* category
* identifier prefix
* canonical directory
* schema path
* lifecycle status
* stability level
* relationship expectations

Example:

```json
{
  "type": "Retriever",
  "label": "Retriever",
  "description": "A component or system responsible for retrieving candidate information for a RAG workflow.",
  "category": "Implementation",
  "identifierPrefix": "RETRIEVER",
  "directory": "retrievers/",
  "schema": "schema/retriever.schema.json",
  "status": "Published",
  "stability": "Stable"
}
```

The registry entry defines the ontology term.

The specialized schema defines the document structure for instances of that type.

---

# Relationship Type Registry

The Relationship Type Registry defines canonical relationship predicates.

Each relationship type definition should include:

* type
* label
* description
* category
* canonical source entity types
* canonical target entity types
* inverse relationship behavior
* cardinality expectations
* lifecycle status
* stability level
* examples

Example:

```json
{
  "type": "IMPLEMENTS",
  "label": "implements",
  "description": "Indicates that the source entity implements the target entity.",
  "category": "Implementation",
  "status": "Published",
  "stability": "Stable"
}
```

Relationship type names must use uppercase snake case.

---

# Registry Entries

A registry entry is a structured definition of one vocabulary term.

Every registry entry must have a stable canonical name.

Renaming a canonical term is a breaking ontology change unless the old term is deprecated with an explicit replacement.

Preferred:

```json
{
  "type": "EVALUATES",
  "status": "Published",
  "replacementRelationshipType": null
}
```

Avoid:

```json
{
  "type": "checks",
  "status": "Published"
}
```

The avoided example is not uppercase snake case and does not match the canonical relationship naming convention.

---

# Lifecycle

Registry terms follow the same lifecycle vocabulary used by entity and relationship documents.

Canonical lifecycle values are:

```text
Draft
Review
Published
Deprecated
Archived
```

Draft terms may be used for proposed vocabulary.

Review terms are being evaluated for canonical use.

Published terms are canonical.

Deprecated terms remain readable for compatibility but should not be used in new content.

Archived terms are retained for historical interpretation.

---

# Stability

Registry entries should declare stability when the registry schema supports it.

Canonical stability values are:

```text
Experimental
Stable
Deprecated
```

Experimental terms may change before publication.

Stable terms may be used by schemas, generated exports and entity documents.

Deprecated terms must identify a replacement when one exists.

---

# Versioning

Every registry belongs to an ontology version.

Registry documents should record:

* ontology version represented by the registry
* version where each term was introduced
* version where each term was deprecated
* replacement term when a deprecated term has one

Adding a new Published term is usually a backward-compatible ontology change.

Changing the meaning, identifier prefix, allowed direction or required structure of an existing Published term may be a breaking change.

---

# Relationship to Schemas

Schemas and registries have different responsibilities.

Schemas validate document structure.

Registries validate vocabulary meaning.

For example, a schema may require an entity type string, while the Entity Type Registry defines whether that entity type is canonical, deprecated or experimental.

When a specialized schema constrains `identity.entityType`, that const value must already be supported by the shared identity definition.

---

# Relationship to the Ontology

The ontology defines the conceptual model.

Registries operationalize the ontology as machine-readable vocabulary.

The ontology may describe that relationships are directional.

The Relationship Type Registry records the canonical direction for each relationship type.

The ontology may describe entity types.

The Entity Type Registry records the canonical names, directories and schemas for those entity types.

---

# Validation

Registry validation should check that:

* registry documents conform to their schemas
* registered relationship types use uppercase snake case
* registered entity types use canonical type names
* schema paths are repository-relative
* identifier prefixes match RKM identifier rules
* deprecated terms identify replacements when appropriate
* examples use valid identifiers, slugs and relationship names

Validation should not silently normalize registry terms.

Invalid vocabulary should be rejected so that ontology drift is visible.

---

# Contributor Guidance

Contributors should add or change registry terms only when the term has reusable semantic value.

Before adding a term, check whether an existing term already represents the intended meaning.

If a new term is needed, define it in the registry before using it broadly in entity documents, relationship documents or architecture examples.

When a proposed entity type needs a specialized schema, shared identity support must be added before creating that specialized schema.

---

# Non-Goals

The Registry Model does not define every ontology term directly.

It defines how registry-backed vocabulary is governed.

The actual controlled vocabularies live in registry documents and registry schemas.
