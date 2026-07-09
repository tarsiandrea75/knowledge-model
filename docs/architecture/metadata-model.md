# Metadata Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how metadata is represented in the RAG Knowledge Model.

Metadata describes the repository artifact.

It does not describe the real-world concept represented by the artifact.

This distinction is fundamental.

---

# Core Principle

Metadata is information about the document.

Knowledge is information about the entity.

Example:

```text
updatedAt
```

describes when the entity document was updated.

Example:

```text
introducedYear
```

describes when the represented concept was introduced.

These two types of information must not be mixed.

---

# Metadata vs Knowledge

## Metadata

Metadata describes:

* the JSON document
* the schema version
* the lifecycle state
* maintainers
* review status
* creation time
* update time
* license
* repository version
* provenance of the document itself

## Knowledge

Knowledge describes:

* what the entity is
* how it works
* which problem it solves
* which paper introduced it
* which framework implements it
* which limitations it has
* which relationships it participates in

---

# Example

Correct separation:

```json
{
  "metadata": {
    "createdAt": "2026-07-08T00:00:00Z",
    "updatedAt": "2026-07-08T00:00:00Z",
    "schemaVersion": "1.0.0",
    "status": "Draft"
  },
  "knowledge": {
    "introducedYear": 2022,
    "summary": "HyDE generates a hypothetical document before retrieval."
  }
}
```

---

# Metadata Scope

Metadata applies to:

* entity documents
* relationship documents
* schema files
* ontology documents
* generated artifacts
* examples
* exports
* migrations

Every persisted artifact should have enough metadata to be traceable.

---

# Entity Metadata

Entity metadata describes the entity document.

It may include:

* version
* schema version
* status
* created date
* updated date
* maintainers
* reviewers
* license
* language
* repository version
* review state

---

# Relationship Metadata

Relationship metadata describes a relationship document or embedded relationship.

It may include:

* status
* confidence
* created date
* updated date
* introduced version
* deprecated version
* evidence status
* review state

---

# Schema Metadata

Schema metadata describes a schema file.

It may include:

* schema version
* schema identifier
* compatible repository versions
* stability level
* deprecation status
* maintainers

---

# Generated Artifact Metadata

Generated artifact metadata describes generated files.

It should include:

* generator name
* generator version
* repository version
* schema version
* generated date
* source files
* target language
* generation options

---

# Canonical Metadata Fields

The following fields are canonical.

```json
{
  "version": "1.0.0",
  "schemaVersion": "1.0.0",
  "status": "Draft",
  "createdAt": "2026-07-08T00:00:00Z",
  "updatedAt": "2026-07-08T00:00:00Z",
  "createdBy": [],
  "updatedBy": [],
  "maintainers": [],
  "reviewers": [],
  "license": "Apache-2.0",
  "language": "en"
}
```

---

# Version

The `version` field describes the version of the document or entity.

It follows Semantic Versioning.

Example:

```json
{
  "version": "1.0.0"
}
```

---

# Schema Version

The `schemaVersion` field describes the version of the schema used by the document.

Example:

```json
{
  "schemaVersion": "1.0.0"
}
```

The schema version is not the same as the entity version.

---

# Status

The `status` field describes the lifecycle state of the document.

Canonical values:

```text
Draft
Review
Published
Deprecated
Archived
```

---

# Draft

The document exists but is not yet reviewed.

Draft documents may be incomplete.

---

# Review

The document is being reviewed for correctness, consistency and completeness.

---

# Published

The document has been accepted as part of the official knowledge model.

---

# Deprecated

The document is still available but should not be used as the preferred representation.

Deprecated documents should include migration guidance when applicable.

---

# Archived

The document is preserved for historical reasons and is no longer actively maintained.

---

# Created At

The `createdAt` field records when the document was created.

Use ISO 8601 UTC timestamps.

Example:

```json
{
  "createdAt": "2026-07-08T00:00:00Z"
}
```

---

# Updated At

The `updatedAt` field records when the document was last modified.

Use ISO 8601 UTC timestamps.

Example:

```json
{
  "updatedAt": "2026-07-08T00:00:00Z"
}
```

---

# Created By

The `createdBy` field identifies who created the document.

It may reference:

* maintainer identifiers
* contributor identifiers
* organization identifiers
* automation identifiers

Example:

```json
{
  "createdBy": [
    {
      "type": "Maintainer",
      "name": "RKM Maintainers"
    }
  ]
}
```

---

# Updated By

The `updatedBy` field identifies who last updated the document.

Example:

```json
{
  "updatedBy": [
    {
      "type": "Maintainer",
      "name": "RKM Maintainers"
    }
  ]
}
```

---

# Maintainers

The `maintainers` field identifies the people or organizations responsible for ongoing maintenance.

Example:

```json
{
  "maintainers": [
    {
      "name": "RKM Maintainers",
      "role": "Maintainer"
    }
  ]
}
```

---

# Reviewers

The `reviewers` field identifies people or systems that reviewed the document.

Example:

```json
{
  "reviewers": [
    {
      "name": "Technical Review",
      "role": "Reviewer"
    }
  ]
}
```

---

# License

The `license` field declares the license applying to the document.

Use SPDX identifiers.

Preferred:

```json
{
  "license": "Apache-2.0"
}
```

Other examples:

```text
MIT
CC-BY-4.0
CC-BY-SA-4.0
```

---

# Language

The `language` field declares the primary language of the document.

Use BCP 47 language codes.

Examples:

```json
{
  "language": "en"
}
```

```json
{
  "language": "it"
}
```

```json
{
  "language": "es-AR"
}
```

---

# Repository Version

The `repositoryVersion` field may be used when a document is tied to a specific repository release.

Example:

```json
{
  "repositoryVersion": "1.0.0"
}
```

---

# Introduced In Version

The `introducedInVersion` field records when a document, field, relationship or feature was introduced.

Example:

```json
{
  "introducedInVersion": "1.0.0"
}
```

---

# Deprecated In Version

The `deprecatedInVersion` field records when a document, field, relationship or feature was deprecated.

Example:

```json
{
  "deprecatedInVersion": "2.0.0"
}
```

Use `null` when the item is not deprecated.

---

# Removed In Version

The `removedInVersion` field records when something was removed.

This should be used mainly in changelogs, migrations and generated compatibility artifacts.

Example:

```json
{
  "removedInVersion": "3.0.0"
}
```

---

# Stability

The `stability` field describes how stable an artifact is.

Canonical values:

```text
Experimental
Draft
Stable
Deprecated
Archived
```

---

# Review State

Review state may provide more detail than lifecycle status.

Example values:

```text
Not Reviewed
Needs Review
Reviewed
Approved
Rejected
Needs Evidence
Needs Revision
```

Review state is operational metadata.

Lifecycle status is canonical metadata.

---

# Completeness

Completeness describes how complete a document is.

Canonical values:

```text
Stub
Partial
Substantial
Complete
```

---

# Stub

The document exists only as a stub or minimal entry.

---

# Partial

The document contains useful information but is clearly incomplete.

---

# Substantial

The document is mostly complete but may still need improvements.

---

# Complete

The document is considered complete for the current repository version.

Complete does not mean permanently finished.

---

# Confidence

Metadata may include a general confidence level for the document.

Canonical values:

```text
Very Low
Low
Medium
High
Very High
```

This is a high-level editorial confidence.

It does not replace claim-level confidence or evidence-level confidence.

---

# Source Provenance

Source provenance describes how the document was created.

Examples:

* Manual
* Imported
* Generated
* Derived
* Migrated
* LLM-Assisted
* Mixed

Example:

```json
{
  "provenance": {
    "creationMethod": "Manual",
    "hasLLMAssistance": true,
    "notes": []
  }
}
```

---

# LLM Assistance Metadata

When LLMs assist in creating or editing content, metadata may record it.

Example:

```json
{
  "llmAssistance": {
    "used": true,
    "purpose": [
      "Drafting",
      "Editing",
      "Structuring"
    ],
    "humanReviewed": true
  }
}
```

LLM assistance metadata increases transparency.

It does not reduce the need for evidence or review.

---

# Generated Metadata

Generated artifacts should include generation metadata.

Example:

```json
{
  "generated": {
    "isGenerated": true,
    "generator": "rkm-schema-generator",
    "generatorVersion": "0.1.0",
    "generatedAt": "2026-07-08T00:00:00Z",
    "sourceFiles": [
      "schema/technique.schema.json"
    ]
  }
}
```

---

# Human Authored Metadata

Human-authored documents may include authorship metadata.

Example:

```json
{
  "authorship": {
    "mode": "Human Authored",
    "contributors": []
  }
}
```

---

# Review Metadata

Review metadata tracks quality assurance.

Example:

```json
{
  "review": {
    "status": "Needs Review",
    "reviewers": [],
    "reviewedAt": null,
    "notes": []
  }
}
```

---

# Validation Metadata

Validation metadata records whether a document has passed automated checks.

Example:

```json
{
  "validation": {
    "status": "Passed",
    "validatedAt": "2026-07-08T00:00:00Z",
    "schemaId": "https://ragknowledge.org/schema/technique.schema.json",
    "errors": []
  }
}
```

---

# Validation Status

Canonical validation status values:

```text
Not Run
Passed
Failed
Warning
Skipped
```

---

# Access Metadata

Most repository content is public.

However, metadata may describe visibility.

Canonical visibility values:

```text
Public
Internal
Private
Restricted
```

For open source releases, most content should be:

```text
Public
```

---

# Temporal Metadata

Some documents or relationships are time-sensitive.

Temporal metadata may include:

* validFrom
* validUntil
* observedAt
* accessedAt
* publishedAt
* deprecatedAt
* archivedAt

---

# Accessed At

Use `accessedAt` for references to web-based sources.

Example:

```json
{
  "accessedAt": "2026-07-08T00:00:00Z"
}
```

This is especially important for documentation pages, pricing pages, repositories and provider APIs.

---

# Observed At

Use `observedAt` when recording an observation.

Example:

```json
{
  "observedAt": "2026-07-08T00:00:00Z"
}
```

---

# Valid From

Use `validFrom` when a statement is valid starting at a known time.

Example:

```json
{
  "validFrom": "2025-01-01"
}
```

---

# Valid Until

Use `validUntil` when a statement is valid until a known time.

Example:

```json
{
  "validUntil": null
}
```

Use `null` when no end date is known.

---

# Deprecation Metadata

Deprecated artifacts should include deprecation metadata.

Example:

```json
{
  "deprecation": {
    "isDeprecated": true,
    "deprecatedAt": "2026-07-08T00:00:00Z",
    "deprecatedInVersion": "2.0.0",
    "reason": "Replaced by a more specific entity.",
    "replacementId": "TECHNIQUE-0021",
    "migrationNotes": "Use the replacement entity for new relationships."
  }
}
```

---

# Archival Metadata

Archived artifacts should include archival metadata.

Example:

```json
{
  "archival": {
    "isArchived": true,
    "archivedAt": "2026-07-08T00:00:00Z",
    "reason": "Kept for historical reference."
  }
}
```

---

# Change Metadata

Documents may track recent changes.

Example:

```json
{
  "change": {
    "changeType": "Added",
    "summary": "Initial entity definition.",
    "changedAt": "2026-07-08T00:00:00Z"
  }
}
```

Canonical change types:

```text
Added
Changed
Deprecated
Removed
Fixed
Security
```

---

# Machine Processing Metadata

Artifacts may include machine processing metadata.

Example:

```json
{
  "processing": {
    "isIndexable": true,
    "isSearchable": true,
    "isExportable": true,
    "isGraphNode": true
  }
}
```

---

# Search Metadata

Search metadata may improve retrieval and indexing.

Example:

```json
{
  "search": {
    "boost": 1.0,
    "keywords": [],
    "synonyms": [],
    "excludeFromSearch": false
  }
}
```

Search metadata should not replace canonical names or aliases.

---

# Graph Metadata

Graph metadata may describe graph export behavior.

Example:

```json
{
  "graph": {
    "isNode": true,
    "nodeLabel": "Technique",
    "isRelationship": false,
    "relationshipType": null
  }
}
```

---

# Export Metadata

Export metadata describes whether and how an artifact should be exported.

Example:

```json
{
  "exports": {
    "json": true,
    "jsonLd": true,
    "rdf": true,
    "neo4j": true,
    "graphql": true,
    "sql": true
  }
}
```

---

# Metadata Placement

Metadata should be grouped in a dedicated `metadata` object whenever practical.

Preferred:

```json
{
  "metadata": {
    "version": "1.0.0",
    "schemaVersion": "1.0.0",
    "createdAt": "2026-07-08T00:00:00Z"
  }
}
```

Avoid scattering metadata across the root unless schema simplicity requires it.

---

# Root-Level Metadata Exception

Some fields may appear at the root for convenience and validation.

Examples:

```json
{
  "id": "TECHNIQUE-0001",
  "slug": "naive-rag",
  "entityType": "Technique",
  "version": "1.0.0",
  "schemaVersion": "1.0.0"
}
```

Even when root-level fields exist, the model should clearly distinguish identity, metadata and knowledge.

---

# Metadata Anti-Patterns

Avoid the following anti-patterns.

---

## Mixing Metadata and Knowledge

Bad:

```json
{
  "updatedAt": "2026-07-08T00:00:00Z",
  "introducedAt": "2022"
}
```

Better:

```json
{
  "metadata": {
    "updatedAt": "2026-07-08T00:00:00Z"
  },
  "knowledge": {
    "introducedYear": 2022
  }
}
```

---

## Unstructured Maintainer Notes

Bad:

```json
{
  "notes": "Andrea updated this maybe in July."
}
```

Better:

```json
{
  "metadata": {
    "updatedAt": "2026-07-08T00:00:00Z",
    "updatedBy": [
      {
        "name": "Andrea Tarsi",
        "role": "Maintainer"
      }
    ]
  }
}
```

---

## Missing Schema Version

Bad:

```json
{
  "id": "TECHNIQUE-0001"
}
```

Better:

```json
{
  "id": "TECHNIQUE-0001",
  "schemaVersion": "1.0.0"
}
```

---

## Metadata Used as Evidence

Bad:

```json
{
  "metadata": {
    "source": "Self-RAG paper"
  }
}
```

Better:

```json
{
  "references": [
    {
      "id": "REFERENCE-0001",
      "sourceType": "Paper",
      "title": "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection"
    }
  ],
  "evidence": [
    {
      "referenceId": "REFERENCE-0001",
      "role": "Supports"
    }
  ]
}
```

---

# Metadata Review Checklist

Before publishing a document, maintainers should verify:

* Does it declare a version?
* Does it declare a schema version?
* Does it have a lifecycle status?
* Does it have creation metadata?
* Does it have update metadata?
* Is metadata separated from knowledge?
* Are dates ISO 8601?
* Are licenses SPDX identifiers?
* Are review states clear?
* Is generated content marked as generated?
* Is LLM-assisted content marked when applicable?
* Are deprecated artifacts clearly marked?
* Are archived artifacts clearly marked?

---

# Minimal Metadata Contract

Every entity document should contain at least:

```json
{
  "metadata": {
    "version": "1.0.0",
    "schemaVersion": "1.0.0",
    "status": "Draft",
    "createdAt": "2026-07-08T00:00:00Z",
    "updatedAt": "2026-07-08T00:00:00Z",
    "language": "en",
    "license": "Apache-2.0"
  }
}
```

---

# Recommended Metadata Contract

A mature document should contain:

```json
{
  "metadata": {
    "version": "1.0.0",
    "schemaVersion": "1.0.0",
    "repositoryVersion": "1.0.0",
    "status": "Published",
    "stability": "Stable",
    "completeness": "Substantial",
    "confidence": "High",
    "createdAt": "2026-07-08T00:00:00Z",
    "updatedAt": "2026-07-08T00:00:00Z",
    "createdBy": [],
    "updatedBy": [],
    "maintainers": [],
    "reviewers": [],
    "language": "en",
    "license": "Apache-2.0",
    "provenance": {
      "creationMethod": "Manual",
      "hasLLMAssistance": true,
      "humanReviewed": true
    },
    "review": {
      "status": "Needs Review",
      "reviewedAt": null,
      "notes": []
    },
    "validation": {
      "status": "Not Run",
      "validatedAt": null,
      "errors": []
    }
  }
}
```

---

# Summary

Metadata makes the repository maintainable.

Knowledge explains the world.

Metadata explains the artifact.

Keeping them separate allows the RAG Knowledge Model to remain trustworthy, versionable, auditable and automatable.
