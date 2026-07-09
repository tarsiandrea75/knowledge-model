# Entity Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines the Entity Model of the RAG Knowledge Model.

The Entity Model explains how all knowledge-bearing objects are represented conceptually before they are serialized into JSON, exported to graphs, transformed into schemas or generated into programming language types.

This document answers the question:

> **What is an entity in the RAG Knowledge Model, and what information must every entity contain?**

---

# Core Principle

Everything that can be identified, described, referenced or connected is an Entity.

Examples:

* HyDE
* Spring AI
* pgvector
* Self-RAG Paper
* BEIR Benchmark
* Low Recall
* Reranking
* Cosine Similarity
* Vector Database
* Query Transformation

If something can be the source or target of a relationship, it should be modeled as an Entity.

---

# Entity Hierarchy

The RAG Knowledge Model uses a layered entity hierarchy.

```text
Entity
  │
  └── Knowledge Entity
        │
        ├── Technique
        ├── Framework
        ├── Component
        ├── Paper
        ├── Dataset
        ├── Benchmark
        ├── Embedding Model
        ├── Language Model
        ├── Reranker
        ├── Retriever
        ├── Vector Database
        ├── Graph Database
        ├── Chunking Strategy
        ├── Prompt Technique
        ├── Evaluation Metric
        ├── Agent
        ├── Workflow
        ├── Tool
        ├── Provider
        ├── Problem
        ├── Advantage
        ├── Limitation
        ├── Tradeoff
        └── Use Case
```

---

# Entity

Entity is the base abstraction.

An Entity is something with stable identity.

An Entity does not necessarily need a long description.

An Entity may exist before the repository has complete knowledge about it.

---

# Entity Responsibilities

Every Entity is responsible for:

* stable identification
* canonical naming
* lifecycle status
* version tracking
* basic classification
* referenceability
* graph participation

---

# Entity Is Not a Document

An Entity is the concept being described.

A document is the file that stores the entity.

Example:

```text
Entity:
HyDE

Document:
techniques/hyde.json
```

The entity and the file are related but not identical.

---

# Entity Identity

Every Entity must have a stable identifier.

Example:

```text
TECHNIQUE-0007
```

The identifier is immutable.

It must not change when:

* the entity name changes
* the file path changes
* the slug changes
* the entity is deprecated
* the entity receives a new version
* the entity is moved to another collection

---

# Entity Slug

Every Entity should have a slug.

The slug is:

* human-readable
* URL-friendly
* file-friendly
* usually aligned with the file name

Example:

```text
hyde
```

Unlike identifiers, slugs may change when canonical naming changes.

Old slugs should be preserved as aliases.

---

# Entity Name

Every Entity has a canonical name.

The name may contain multiple representations:

* display name
* official name
* short name
* acronym
* pronunciation

Example:

```json
{
  "display": "HyDE",
  "official": "Hypothetical Document Embedding",
  "acronym": "HyDE"
}
```

Names are human-facing.

Identifiers are machine-facing.

---

# Entity Type

Every Entity has an entity type.

Examples:

```text
Technique
Framework
Paper
Component
Dataset
Benchmark
Problem
Advantage
Limitation
Tradeoff
```

The entity type determines which specialized schema applies.

---

# Entity Lifecycle

Every Entity has a lifecycle status.

Canonical values:

```text
Draft
Review
Published
Deprecated
Archived
```

---

# Draft Entity

An Entity is Draft when it has been created but not reviewed.

Draft entities may be incomplete.

---

# Review Entity

An Entity is in Review when maintainers are evaluating its correctness, completeness or classification.

---

# Published Entity

An Entity is Published when it is accepted as part of the official knowledge model.

---

# Deprecated Entity

An Entity is Deprecated when it should no longer be used as the preferred representation.

Deprecated entities remain available for compatibility and historical reasons.

---

# Archived Entity

An Entity is Archived when it is preserved only for historical reference.

Archived entities are not actively maintained.

---

# Knowledge Entity

A Knowledge Entity extends Entity.

A Knowledge Entity contains knowledge-bearing information.

It may include:

* descriptions
* summaries
* explanations
* relationships
* evidence
* references
* advantages
* limitations
* use cases
* tradeoffs
* implementation notes
* evaluation notes

Most entities in the repository are Knowledge Entities.

---

# Knowledge Entity Responsibilities

A Knowledge Entity is responsible for:

* explaining what the entity is
* explaining why it matters
* connecting to related entities
* exposing evidence
* enabling semantic search
* enabling graph traversal
* supporting generated documentation

---

# Knowledge Entity Structure

Conceptually, every Knowledge Entity contains these sections:

```text
Identity
Metadata
Description
Classification
Relationships
Evidence
References
Lifecycle
```

Specialized entities add domain-specific sections.

---

# Specialized Entity

A Specialized Entity is a Knowledge Entity with additional domain-specific fields.

Example:

Technique adds:

* workflow
* pipeline stage
* retrieval strategy
* cost impact
* latency impact
* framework support
* implementation complexity

Paper adds:

* authors
* publication date
* venue
* DOI
* arXiv identifier
* citation count

Framework adds:

* programming languages
* supported components
* official documentation
* license
* repository URL

---

# Entity vs Relationship

Entities represent things.

Relationships represent semantic connections between things.

Example:

```text
HyDE
```

is an Entity.

```text
HyDE REQUIRES Embedding Model
```

is a Relationship.

Do not encode relationships only as prose when they can be represented structurally.

---

# Entity vs Attribute

An Attribute describes an entity.

An Entity can stand alone and participate in relationships.

Example:

```text
Embedding Dimension
```

may be an attribute of an Embedding Model.

But:

```text
Cosine Similarity
```

should be an Entity because it can be used by many retrievers, vector databases and evaluation processes.

---

# Entity Promotion Rule

A value should be promoted to Entity when at least one of the following is true:

* it can be referenced by multiple other entities
* it can be the source or target of a relationship
* it has its own properties
* it has its own lifecycle
* it has aliases
* it has evidence
* it has external references
* it is useful for graph queries
* it is likely to be reused

---

# Examples of Promoted Entities

The following should be modeled as Entities:

* Low Recall
* Hallucination
* Semantic Gap
* Cosine Similarity
* BM25
* Hybrid Retrieval
* Cross-Encoder Reranker
* Vector Database
* Context Window Limit
* Query Transformation
* Reranking
* Chunking Strategy

---

# Examples of Attributes

The following are usually attributes:

* version number
* created date
* updated date
* programming language list
* token limit
* embedding dimension
* license identifier
* repository URL

However, attributes may later become entities if the model requires richer semantics.

---

# Entity Boundaries

Entity boundaries should be stable and meaningful.

Avoid creating entities that are too broad.

Avoid creating entities that are too narrow.

---

# Too Broad

Bad example:

```text
AI
```

This is too broad for useful modeling.

Preferred:

```text
Retrieval-Augmented Generation
Embedding Model
Large Language Model
Vector Database
```

---

# Too Narrow

Bad example:

```text
The fact that HyDE improves recall in some cases
```

This is better represented as a Claim or Evidence, not as a primary Entity.

---

# Correct Granularity

Good examples:

```text
HyDE
Low Recall
Query Transformation
Embedding Model
Reranker
Spring AI
Self-RAG Paper
```

These concepts are reusable, nameable and relational.

---

# Entity Classification

Every Knowledge Entity may be classified.

Classification may include:

* domain
* family
* subfamily
* category
* maturity
* difficulty
* production readiness
* research stage

Classification helps with filtering, navigation and graph queries.

---

# Classification Is Not Identity

Classification may change.

Identity does not.

Example:

HyDE may be classified as:

```text
Query Transformation
```

or:

```text
Retrieval Optimization
```

depending on taxonomy evolution.

But its identifier remains stable.

---

# Entity Metadata

Metadata describes the entity document.

Metadata does not describe the real-world concept.

Metadata may include:

* version
* schema version
* created date
* updated date
* maintainer
* status
* license
* review state

---

# Entity Knowledge

Entity knowledge describes the concept itself.

Examples:

* summary
* description
* motivation
* history
* advantages
* limitations
* use cases
* relationships
* references
* evidence

---

# Metadata vs Knowledge

Correct:

```text
updatedAt
```

describes the JSON document.

```text
introducedYear
```

describes the concept.

These should not be confused.

---

# Entity References

Entities should reference other entities using stable identifiers.

Preferred:

```json
{
  "targetId": "TECHNIQUE-0007"
}
```

Avoid:

```json
{
  "target": "HyDE"
}
```

Names and slugs may be included for readability, but identifiers remain authoritative.

---

# Entity Aliases

Entities may have aliases.

Aliases are useful for:

* spelling variants
* previous names
* acronyms
* framework-specific names
* historical names
* common informal names

Example:

```json
{
  "aliases": [
    {
      "value": "Graph RAG",
      "type": "Spelling Variant"
    },
    {
      "value": "Graph-RAG",
      "type": "Spelling Variant"
    }
  ]
}
```

---

# Entity Description

A Knowledge Entity should contain multiple levels of explanation.

Recommended description levels:

* summary
* abstract
* full description
* intuition
* technical explanation
* implementation notes

Different consumers need different depths of explanation.

---

# Entity Evidence

Important claims should be supported by evidence.

Evidence may come from:

* papers
* official documentation
* source code
* benchmark results
* experiments
* production reports
* maintainer analysis

Evidence should be structured whenever possible.

---

# Entity References

References point to external or internal sources.

A reference is not the same as evidence.

A reference is a source.

Evidence is the use of that source to support a claim.

---

# Entity Claims

A Claim is a statement about an Entity.

Example:

```text
HyDE can improve recall for short or underspecified queries.
```

A Claim may require evidence.

Claims may later become first-class entities if the repository needs fine-grained traceability.

---

# Entity Collections

Entities are stored in collections by entity type.

Examples:

```text
techniques/
frameworks/
papers/
components/
datasets/
benchmarks/
problems/
advantages/
limitations/
tradeoffs/
use-cases/
```

The directory is an organizational convenience.

The entity type remains authoritative.

---

# Entity Document

An entity document is the serialized representation of an entity.

In JSON, an entity document should contain:

* id
* slug
* entityType
* name
* version
* schemaVersion
* status
* metadata
* description
* relationships

Specialized entities add more fields.

---

# Minimal Entity Contract

Every Entity must provide at least:

```json
{
  "id": "TECHNIQUE-0001",
  "slug": "naive-rag",
  "entityType": "Technique",
  "name": {
    "display": "Naive RAG",
    "official": "Naive Retrieval-Augmented Generation"
  },
  "version": "1.0.0",
  "schemaVersion": "1.0.0",
  "status": "Draft"
}
```

---

# Minimal Knowledge Entity Contract

Every Knowledge Entity should additionally provide:

```json
{
  "summary": "A concise explanation of the entity.",
  "description": "A complete explanation of the entity.",
  "relationships": [],
  "references": [],
  "evidence": []
}
```

---

# Rich Knowledge Entity Contract

A mature Knowledge Entity may include:

```json
{
  "motivation": "Explain why the entity exists and which RAG problem it addresses.",
  "history": "Describe the origin and evolution of the entity within the RAG ecosystem.",
  "technicalExplanation": "Explain how the entity works using implementation-oriented terminology.",
  "advantages": [],
  "limitations": [],
  "tradeoffs": [],
  "useCases": [],
  "antiPatterns": [],
  "commonMistakes": [],
  "relationships": [],
  "claims": [],
  "evidence": [],
  "references": []
}
```

---

# Entity Normalization

The repository should avoid unnecessary duplication.

If a concept is reused across many entities, it should become its own entity.

Example:

Avoid repeating:

```text
Improves Recall
```

inside many techniques as a free-form string.

Prefer creating:

```text
ADVANTAGE-0001 Improved Recall
```

and referencing it.

---

# Embedded vs Referenced Entities

Some small pieces of information may be embedded.

Other concepts should be referenced.

---

# Embedded Information

Embed information when it is:

* unique to the entity
* unlikely to be reused
* not useful as a graph node
* simple metadata
* purely descriptive

---

# Referenced Information

Reference information when it is:

* reusable
* relational
* evidence-backed
* independently meaningful
* part of the ontology
* useful in graph queries

---

# Entity Duplication Policy

Duplicate entities should be avoided.

Before creating a new entity, contributors should check:

* existing identifiers
* aliases
* previous slugs
* related terms
* deprecated entities

If two entities are found to represent the same concept, they should be merged or one should be deprecated.

---

# Entity Merge Policy

When two entities are merged:

* one identifier should remain canonical
* the other should be deprecated
* aliases should be preserved
* relationships should be migrated
* references should be updated
* migration notes should be added

Identifiers should not be reused.

---

# Entity Split Policy

When one entity is split into multiple entities:

* the original entity may become deprecated or generalized
* new identifiers must be created
* relationships must be redistributed
* migration notes must explain the split

Example:

A generic entity called:

```text
Model
```

may be split into:

```text
Embedding Model
Language Model
Reranker Model
Multimodal Model
```

---

# Entity Deprecation

Deprecation is preferred over deletion.

A deprecated entity should include:

* deprecation reason
* replacement entity when applicable
* migration guidance
* deprecated version
* deprecated date

---

# Entity Deletion

Deletion should be rare.

Deletion is allowed only when:

* the entity was created by mistake
* the entity is unsafe
* the entity is legally problematic
* the entity contains no meaningful knowledge
* the entity duplicates another unpublished entity

Published identifiers should not be reused.

---

# Entity Quality Criteria

A high-quality entity should be:

* clearly identified
* correctly classified
* described at multiple levels
* connected to related entities
* supported by references
* consistent with the ubiquitous language
* free of avoidable duplication
* useful for both humans and machines

---

# Entity Anti-Patterns

Avoid the following anti-patterns.

---

## Stringly-Typed Knowledge

Avoid important knowledge represented only as strings.

Bad:

```json
{
  "advantages": [
    "Improves recall"
  ]
}
```

Better:

```json
{
  "relationships": [
    {
      "type": "HAS_ADVANTAGE",
      "targetId": "ADVANTAGE-0001"
    }
  ]
}
```

---

## Ambiguous Entity Names

Avoid names like:

```text
Model
Search
Database
Context
```

Prefer explicit names:

```text
Embedding Model
Vector Search
Vector Database
Retrieved Context
```

---

## Framework Leakage

Avoid using framework-specific terminology as canonical domain terminology unless it is widely accepted.

Example:

A framework may call something a `VectorStore`.

The canonical concept may still be:

```text
Vector Store
```

or:

```text
Vector Database
```

depending on meaning.

---

## Overloaded Entities

Avoid using one entity to represent multiple concepts.

Example:

```text
RAG
```

should not simultaneously represent:

* the original RAG paper
* the general paradigm
* a pipeline implementation
* a software feature

Each should be modeled separately when needed.

---

## Relationship Hidden in Description

Avoid burying relationships in prose.

Bad:

```text
This technique was introduced by the Self-RAG paper.
```

Better:

```text
Paper INTRODUCES Technique
```

with a structured relationship.

---

# Entity Review Checklist

Before publishing an entity, maintainers should verify:

* Does it have a stable identifier?
* Does it use canonical vocabulary?
* Is the entity type correct?
* Is the slug valid?
* Are aliases captured?
* Is the description clear?
* Are relationships structured?
* Are important claims supported?
* Is metadata separated from knowledge?
* Are duplicated concepts avoided?
* Is the entity useful as a graph node?

---

# Future Schema Mapping

The Entity Model will later map to reusable schema definitions.

Expected schema layers:

```text
entity.schema.json
knowledge-entity.schema.json
relationship.schema.json
evidence.schema.json
reference.schema.json
metadata.schema.json
```

Specialized schemas will extend these base schemas.

Examples:

```text
technique.schema.json
framework.schema.json
paper.schema.json
component.schema.json
```

---

# Summary

The Entity Model defines the basic unit of knowledge in the RAG Knowledge Model.

Entities are stable, identifiable and connected.

Knowledge Entities add descriptions, evidence and relationships.

Specialized Entities add domain-specific structure.

The quality of the entire repository depends on modeling entities at the right level of abstraction.
