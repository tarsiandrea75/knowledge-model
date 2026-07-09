# Domain Model
## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines the conceptual domain model of the RAG Knowledge Model (RKM).

It intentionally ignores implementation details such as JSON serialization, databases, programming languages or APIs.

Its purpose is to answer one question:

> **What are the concepts that exist in the RAG ecosystem, and how do they relate to each other?**

This document is the single source of truth for every schema contained in this repository.

---

# Philosophy

The RAG ecosystem is not a collection of isolated techniques.

It is a network of interconnected concepts.

A technique depends on models.

Models require embeddings.

Embeddings produce vectors.

Vectors are indexed by databases.

Retrievers search those databases.

Rerankers reorder retrieved documents.

LLMs consume retrieved context.

Evaluation metrics measure the quality of the final answer.

Therefore, the repository models **concepts first**, not files.

---

# Design Layers

The conceptual model is organized into four abstraction layers.

```
Knowledge Domain

        │

        ▼

Entity

        │

        ▼

Knowledge Entity

        │

        ▼

Specialized Entity
```

Each layer adds semantic capabilities.

---

# Layer 1 — Entity

Entity is the most generic object in the entire repository.

Every entity possesses an identity.

An entity may exist even if no descriptive information is available.

Examples:

- Technique
- Paper
- Framework
- Benchmark
- Dataset
- Company
- Author

Every entity is uniquely identifiable.

---

# Layer 2 — Knowledge Entity

Knowledge Entity extends Entity.

It represents something that conveys knowledge.

Every Knowledge Entity contains:

- descriptions
- references
- relationships
- metadata
- evidence

Knowledge Entities are searchable.

Knowledge Entities are indexable.

Knowledge Entities can participate in semantic relationships.

---

# Layer 3 — Specialized Entities

Specialized entities extend Knowledge Entity.

Examples include:

- Technique
- Framework
- Component
- Paper
- Benchmark
- Dataset
- Vector Database
- Embedding Model
- Retriever
- Reranker
- Prompt Technique
- Agent
- Evaluation Metric

Each specialized entity introduces domain-specific attributes.

---

# Fundamental Principle

Inheritance only adds information.

It never replaces inherited concepts.

Example:

Technique

inherits

Knowledge Entity

inherits

Entity

---

# Core Entity Categories

The current model defines the following primary categories.

## Technique

Represents a Retrieval-Augmented Generation technique.

Examples:

- Naive RAG
- HyDE
- Self-RAG
- CRAG
- GraphRAG

---

## Framework

Represents an implementation framework.

Examples:

- Spring AI
- LangChain
- LlamaIndex
- Haystack

---

## Component

Represents reusable architectural building blocks.

Examples:

- Retriever
- Loader
- Chunker
- Vector Store
- Embedding Generator
- Prompt Builder

---

## Paper

Represents academic publications.

A Paper introduces, validates or describes knowledge.

---

## Benchmark

Represents an evaluation benchmark.

Examples:

- BEIR
- MTEB

---

## Dataset

Represents datasets used for:

- evaluation
- training
- benchmarking

---

## Pattern

Represents reusable architectural patterns.

Examples:

- Query Transformation
- Context Compression
- Parent Retrieval

---

## Prompt Technique

Represents prompting methodologies.

Examples:

- Chain of Thought
- ReAct
- Step Back Prompting

---

## Agent

Represents autonomous reasoning systems.

Examples:

- ReAct Agent
- Planning Agent
- Multi-Agent Workflow

---

# Relationships

Knowledge is represented through relationships.

Relationships are first-class citizens.

Examples:

Technique

USES

Retriever

Technique

REQUIRES

Embedding Model

Retriever

SEARCHES

Vector Database

Paper

INTRODUCES

Technique

Framework

IMPLEMENTS

Technique

Benchmark

EVALUATES

Technique

Dataset

IS_USED_BY

Benchmark

---

# Relationship Characteristics

Every relationship may contain metadata.

Example:

```
Technique

USES

Retriever
```

may include:

- mandatory
- optional
- version
- confidence
- notes

Relationships are not simple strings.

Relationships are knowledge.

---

# Knowledge Graph

The conceptual model intentionally mirrors a Property Graph.

Nodes represent entities.

Edges represent relationships.

Both nodes and edges may possess properties.

This enables future export to:

- Neo4j
- RDF
- OWL
- GraphQL
- JSON-LD

without redesign.

---

# Evidence

Every important statement should be supported by evidence.

Evidence may originate from:

- academic papers
- official documentation
- benchmarks
- experiments
- production experience

Evidence itself is represented as structured data.

---

# Metadata

Metadata describes the document.

It never describes the represented concept.

Examples:

- version
- creation date
- update date
- maintainer
- review status
- schema version

---

# Identity

Identity is immutable.

Names may change.

Descriptions may evolve.

Identifiers never change.

---

# Extensibility

New entity categories may be introduced without modifying existing entities.

Examples:

Future additions:

- MCP Server
- Tool
- Memory Strategy
- Orchestrator
- Workflow
- Vector Index
- Tokenizer
- Compression Algorithm

---

# Repository Principle

One entity equals one document.

One document conforms to one schema.

One schema describes one entity type.

---

# Future Evolution

The current domain model intentionally remains technology-neutral.

Future repository versions may generate:

- JSON Schema
- Java Records
- Kotlin Data Classes
- TypeScript Interfaces
- SQL DDL
- Neo4j Constraints
- GraphQL Types
- RDF Ontologies

from the same conceptual model.

---

# Summary

The RAG Knowledge Model is not a documentation repository.

It is a structured semantic representation of the Retrieval-Augmented Generation ecosystem.

Every future schema, document and implementation must remain consistent with this domain model.