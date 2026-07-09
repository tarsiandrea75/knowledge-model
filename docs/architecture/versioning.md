# Versioning

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines the versioning strategy used by the RAG Knowledge Model.

It applies to:

* repository releases
* schemas
* entity documents
* ontology versions
* generated artifacts
* deprecated entities
* breaking changes
* migration policies

Versioning exists to make the project stable, predictable and safe to evolve.

---

# Core Principle

The RAG Knowledge Model separates several kinds of versioning.

They must not be confused.

The repository has a version.

Each schema has a version.

Each entity document has a version.

The ontology has a version.

Generated artifacts may have their own versions.

---

# Version Types

## Repository Version

The version of the entire project.

Example:

```text
1.0.0
```

This version describes the state of the repository as a whole.

---

## Schema Version

The version of a JSON Schema file.

Example:

```json
{
  "schemaVersion": "1.0.0"
}
```

Schema versions change when validation rules change.

---

## Entity Version

The version of an individual entity document.

Example:

```json
{
  "version": "1.2.0"
}
```

Entity versions change when the knowledge contained in a single entity document changes.

---

## Ontology Version

The version of the conceptual relationship model.

Example:

```text
Ontology 1.0.0
```

Ontology versions change when entity types, relationship types or semantic constraints change.

---

## Generated Artifact Version

Generated artifacts may have their own versions.

Examples:

* Java records
* TypeScript interfaces
* GraphQL types
* SQL DDL
* Neo4j constraints
* RDF exports

Generated artifact versions should reference the repository, schema and generator version used to produce them.

---

# Semantic Versioning

The project follows Semantic Versioning.

Format:

```text
MAJOR.MINOR.PATCH
```

Example:

```text
1.4.2
```

---

# Major Version

The MAJOR version changes when a breaking change is introduced.

Examples:

* removing a required field
* renaming a canonical field
* changing identifier format
* changing relationship direction
* changing ontology semantics
* removing a relationship type
* changing enum values incompatibly
* changing directory layout incompatibly
* making previously valid documents invalid

Example:

```text
1.8.0 → 2.0.0
```

---

# Minor Version

The MINOR version changes when backward-compatible functionality is added.

Examples:

* adding a new optional field
* adding a new entity type
* adding a new relationship type
* adding a new schema
* adding a new directory
* adding a new export format
* adding new generated artifacts
* adding documentation
* adding new entities

Example:

```text
1.2.0 → 1.3.0
```

---

# Patch Version

The PATCH version changes when backward-compatible fixes are made.

Examples:

* typo corrections
* description improvements
* metadata corrections
* non-breaking schema clarifications
* reference updates
* formatting fixes
* documentation fixes
* correcting invalid examples without changing the model

Example:

```text
1.2.1 → 1.2.2
```

---

# Repository Versioning

The repository version is authoritative for releases.

It represents a coherent snapshot of:

* schemas
* ontology
* documentation
* entity files
* examples
* generated artifacts

A repository release should be internally consistent.

---

# Schema Versioning

Every schema must declare its own version.

A schema version changes when the schema definition changes.

Schema version changes do not always require repository major version changes.

Example:

Adding an optional field to `technique.schema.json` may increment the schema minor version but only increment the repository minor version.

---

# Entity Versioning

Every entity document must declare its own version.

Entity versions change independently from repository versions.

Example:

The HyDE entity may evolve from:

```text
1.0.0
```

to:

```text
1.1.0
```

without requiring all other entities to change.

---

# Entity Version Rules

## Patch Entity Change

Use PATCH when correcting or clarifying existing information.

Examples:

* fixing typos
* improving wording
* correcting metadata
* fixing broken references
* improving examples without changing meaning

---

## Minor Entity Change

Use MINOR when adding new non-breaking knowledge.

Examples:

* adding relationships
* adding references
* adding use cases
* adding implementation notes
* adding framework support
* adding evaluation notes

---

## Major Entity Change

Use MAJOR when the meaning of the entity changes substantially.

Examples:

* splitting one entity into multiple entities
* merging entities
* changing the canonical identity meaning
* redefining the represented concept
* changing canonical classification incompatibly

Major entity changes should be rare.

---

# Identifier Stability

Entity identifiers are immutable.

Identifiers must not change across versions.

Example:

```text
TECHNIQUE-0007
```

must remain the same even if:

* the display name changes
* the slug changes
* the file moves
* the entity becomes deprecated
* the entity receives a major version bump

---

# Slug Stability

Slugs should remain stable but are not immutable.

If a slug changes, the previous slug should be preserved as an alias.

Example:

```json
{
  "slug": "graph-rag",
  "aliases": [
    {
      "value": "graphrag",
      "type": "Previous Slug"
    }
  ]
}
```

The stable identifier remains authoritative.

---

# Name Changes

Names may change when canonical terminology changes.

Name changes do not require identifier changes.

Example:

```text
Graph RAG
```

may become:

```text
GraphRAG
```

while preserving the same identifier.

---

# Deprecation Policy

Entities should not be deleted when they become obsolete.

They should be deprecated.

Deprecated entities remain useful for:

* historical understanding
* backward compatibility
* literature mapping
* graph traversal
* migration support

---

# Deprecation Status

Use the canonical lifecycle status:

```text
Deprecated
```

A deprecated entity should include:

* reason for deprecation
* replacement entity when applicable
* deprecation version
* migration notes when applicable

---

# Archival Policy

Archived entities are preserved for historical reasons.

Use:

```text
Archived
```

when an entity is no longer maintained but should remain accessible.

Archived is stronger than Deprecated.

Deprecated means "avoid using this going forward."

Archived means "kept only for historical reference."

---

# Deletion Policy

Deleting entities should be avoided.

Deletion is allowed only when:

* the entity was added by mistake
* the entity duplicates another entity
* the entity contains invalid or unsafe content
* legal or licensing reasons require removal

If deletion occurs after publication, the changelog must mention it.

---

# Breaking Changes

A breaking change is any change that may invalidate existing consumers.

Examples:

* removing fields
* renaming fields
* changing field types
* changing enum values
* changing required fields
* changing relationship semantics
* changing identifier rules
* changing directory structure
* changing canonical relationship direction

Breaking changes require a major repository version bump.

---

# Non-Breaking Changes

Examples of non-breaking changes:

* adding optional fields
* adding new entities
* adding new relationships
* adding aliases
* adding references
* adding documentation
* adding examples
* adding generated artifacts

Non-breaking changes require a minor or patch version bump.

---

# Ontology Versioning

The ontology has its own version because relationship semantics are foundational.

Ontology version changes are required when:

* new entity types are introduced
* new relationship types are introduced
* relationship meanings change
* relationship constraints change
* cardinality rules change
* graph export semantics change

---

# Ontology Breaking Changes

The following ontology changes are breaking:

* removing an entity type
* removing a relationship type
* changing relationship direction
* changing relationship meaning
* changing cardinality incompatibly
* changing semantic constraints incompatibly

These require a major repository version bump.

---

# Relationship Versioning

Relationships may include their own lifecycle metadata.

Example:

```json
{
  "type": "IMPLEMENTS",
  "introducedInVersion": "1.2.0",
  "deprecatedInVersion": null
}
```

Relationship versioning is useful when exports need to track historical graph evolution.

---

# Schema Compatibility

Schemas should preserve backward compatibility whenever possible.

Preferred evolution:

```text
Add optional field
```

Avoid:

```text
Rename required field
```

Preferred:

```text
Deprecate old field, add new field
```

Avoid:

```text
Remove old field immediately
```

---

# Field Deprecation

Fields may be deprecated before removal.

A deprecated field should include:

* deprecation notice in schema description
* replacement field if applicable
* version of deprecation
* expected removal version if known

Removal should happen only in a major version.

---

# Enum Evolution

Adding enum values is usually a minor change.

Removing enum values is a breaking change.

Renaming enum values is a breaking change.

Preferred approach:

1. add the new enum value;
2. deprecate the old enum value;
3. migrate data;
4. remove the old value only in a future major version.

---

# Directory Versioning

Directory layout should remain stable within a major version.

Changing the meaning of a directory is a breaking change.

Adding a new directory is non-breaking.

Moving files across directories may be breaking if consumers depend on paths.

---

# Generated Artifact Versioning

Generated artifacts must declare:

* repository version
* schema version
* generator version
* generation date

Example:

```json
{
  "repositoryVersion": "1.0.0",
  "schemaVersion": "1.0.0",
  "generatorVersion": "0.1.0",
  "generatedAt": "2026-07-08T00:00:00Z"
}
```

---

# Migration Policy

Breaking changes should include migration notes.

Migration notes should explain:

* what changed
* why it changed
* how to update existing data
* whether automated migration is possible
* examples before and after

---

# Changelog

Every release should update a changelog.

The changelog should group changes by type:

* Added
* Changed
* Deprecated
* Removed
* Fixed
* Security

This follows the Keep a Changelog convention.

---

# Release Tags

Repository releases should be tagged using:

```text
vMAJOR.MINOR.PATCH
```

Examples:

```text
v1.0.0
v1.1.0
v2.0.0
```

---

# Pre-Releases

Pre-release versions may be used before stable releases.

Examples:

```text
1.0.0-alpha.1
1.0.0-beta.1
1.0.0-rc.1
```

Use pre-releases when schemas or ontology may still change incompatibly.

---

# Stability Levels

The repository may classify artifacts by stability.

Canonical stability values:

```text
Experimental
Draft
Stable
Deprecated
Archived
```

---

# Version Fields

Canonical version-related JSON fields:

```json
{
  "version": "1.0.0",
  "schemaVersion": "1.0.0",
  "introducedInVersion": "1.0.0",
  "deprecatedInVersion": null
}
```

---

# Date Fields

Version-related dates should use ISO 8601.

Timestamps should use UTC.

Example:

```json
{
  "createdAt": "2026-07-08T00:00:00Z",
  "updatedAt": "2026-07-08T00:00:00Z"
}
```

Date-only values may be used for publications.

Example:

```json
{
  "publicationDate": "2023-10-01"
}
```

---

# Version Comparison

Versions must be compared according to Semantic Versioning rules.

String comparison is not sufficient.

Example:

```text
1.10.0
```

is greater than:

```text
1.2.0
```

---

# Compatibility Declaration

Schemas and generated artifacts may declare compatibility.

Example:

```json
{
  "compatibleRepositoryVersions": [
    ">=1.0.0 <2.0.0"
  ]
}
```

---

# Long-Term Compatibility

The project should optimize for long-term compatibility.

When in doubt:

* add instead of replace
* deprecate instead of remove
* alias instead of rename
* migrate gradually
* document every breaking change

---

# Summary

Versioning is part of the architecture of the RAG Knowledge Model.

The repository must remain stable enough for tools, users, generated artifacts and external systems to depend on it.

Every change should make clear whether it affects:

* the repository
* the ontology
* a schema
* an entity
* a generated artifact

Clear versioning makes the model trustworthy.
