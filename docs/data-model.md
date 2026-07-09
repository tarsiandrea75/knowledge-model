# RAG Knowledge Model
## Data Model Specification
Version 1.0.0

---

# Purpose

The purpose of this document is to define the conceptual data model used throughout the RAG Knowledge Model (RKM).

Rather than describing JSON serialization details, this document defines the logical entities, their relationships, and the design principles governing the repository.

This specification should remain stable across future versions.

---

# Design Goals

The data model has been designed to satisfy the following requirements:

- Human-readable
- Machine-readable
- Framework-independent
- Extensible
- Backward compatible whenever possible
- Easily convertible to relational databases
- Easily convertible to graph databases
- Easily indexable by vector databases
- Suitable for Retrieval-Augmented Generation (RAG)
- Suitable for LLM consumption
- Suitable for semantic search
- Suitable for documentation generation

---

# Core Design Principles

## One Entity = One File

Every logical entity is represented by a single JSON document.

Examples:

```
techniques/hyde.json

frameworks/spring-ai.json

papers/self-rag.json

components/vector-store.json
```

This minimizes merge conflicts and allows independent evolution of entities.

---

## Stable Identity

Each entity owns a permanent identifier.

Identifiers MUST NEVER change.

Names may evolve.

Descriptions may evolve.

Identifiers remain immutable.

---

## Separation of Concerns

The repository separates different concepts into dedicated collections.

For example:

- techniques
- frameworks
- papers
- components
- chunking strategies
- embedding models
- vector databases
- rerankers

This avoids mixing unrelated concepts.

---

## Normalization

Information should not be duplicated whenever possible.

Relationships should be represented through references.

Example:

Technique

↓

Framework

↓

Paper

instead of copying the same information multiple times.

---

## Extensibility

Every entity should allow additional fields in future versions.

The schema should evolve without breaking existing documents.

---

## Explicit Relationships

Relationships between entities should always be represented explicitly.

Examples:

```
extends

requires

compatibleWith

alternativeTo

implementedBy

inspiredBy

introducedBy

references
```

---

# Repository Entity Types

The repository contains multiple categories of entities.

Each category has its own schema.

## Technique

Represents a Retrieval-Augmented Generation technique.

Examples:

- Naive RAG
- Hybrid RAG
- HyDE
- Self-RAG
- CRAG
- GraphRAG

---

## Framework

Represents a software framework supporting RAG.

Examples:

- Spring AI
- LangChain
- LlamaIndex
- Haystack

---

## Component

Represents reusable architectural components.

Examples:

- Embedding Model
- Vector Store
- Retriever
- Reranker
- Prompt Template
- Document Loader

---

## Paper

Represents an academic publication.

Examples:

- Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
- Self-RAG
- CRAG
- RAPTOR

---

## Pattern

Represents an architectural pattern.

Examples:

- Query Transformation
- Context Compression
- Parent Document Retrieval

---

## Glossary Term

Represents a technical concept.

Examples:

- Embedding
- Chunk
- Recall
- Precision
- Grounding

---

# Relationship Model

Entities are connected using logical references.

Example:

```
HyDE

requires

Embedding Model

implementedBy

Spring AI

describedIn

HyDE Paper
```

The repository should be convertible into a property graph without structural changes.

---

# Entity Identity

Every entity must contain a globally unique identifier.

Example:

```
RAG-TECH-0001

FRAMEWORK-0003

PAPER-0017

COMPONENT-0025
```

Identifiers are immutable.

Human-readable names are not.

---

# Versioning

Every entity is versioned independently.

Example:

```
HyDE

version 1.0.0

↓

version 1.1.0

↓

version 2.0.0
```

Entity versioning is independent from repository versioning.

---

# Human-Oriented Fields

Every entity should contain information intended for human readers.

Examples:

- summary
- description
- history
- motivation
- advantages
- disadvantages
- implementation notes

These fields prioritize clarity over compactness.

---

# Machine-Oriented Fields

Every entity should also expose structured fields.

Examples:

- identifiers
- enumerations
- relationships
- metrics
- capabilities
- dependencies

These fields should avoid ambiguous wording whenever possible.

---

# Entity References

Relationships should reference identifiers instead of names whenever practical.

Preferred:

```
RAG-TECH-0017
```

instead of

```
HyDE
```

Applications may resolve identifiers into names.

---

# Classification

Every entity belongs to at least one category.

Example:

Technique

↓

Family

↓

Subfamily

Classification is hierarchical whenever appropriate.

---

# Metadata

Every entity contains metadata describing itself.

Typical metadata includes:

- version
- creation date
- update date
- author
- status
- license

Metadata never describes the represented concept.

Metadata describes the JSON document itself.

---

# Separation Between Knowledge and Metadata

Example:

Knowledge

```
HyDE improves retrieval quality by embedding a hypothetical answer.
```

Metadata

```
Last Updated

2026-07-08
```

Knowledge and metadata should never be mixed.

---

# References

Every factual statement should be traceable whenever possible.

Preferred sources include:

- peer-reviewed papers
- official documentation
- standards
- RFCs
- books
- conference proceedings

---

# Future Compatibility

The model is intentionally designed to support future entity types.

Possible future additions include:

- Benchmarks
- Datasets
- LLM Providers
- Evaluation Metrics
- Prompt Patterns
- MCP Servers
- AI Agents
- Orchestrators
- Memory Strategies
- Tool Calling Strategies

without requiring structural redesign.

---

# Serialization

The canonical serialization format is JSON.

Future official serializations may include:

- YAML
- JSON-LD
- RDF
- GraphML

The conceptual model remains identical across all serializations.

---

# Long-Term Vision

The RAG Knowledge Model aims to become a structured representation of the Retrieval-Augmented Generation ecosystem.

Rather than documenting isolated algorithms, the repository models:

- concepts
- techniques
- architectures
- implementations
- relationships
- research
- production practices

This enables both humans and machines to reason about the RAG landscape using a common, extensible, and well-defined data model.

This document serves as the foundation for every schema contained in this repository.