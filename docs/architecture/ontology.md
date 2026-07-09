# Ontology
## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

The ontology defines the semantic vocabulary of the RAG Knowledge Model.

It specifies:

- which entities exist
- which relationships are allowed
- what every relationship means
- how knowledge is connected

Unlike a database schema, the ontology models meaning rather than storage.

It is the semantic foundation of the repository.

---

# Philosophy

Knowledge is represented as a graph.

Everything is either:

- an Entity
- a Relationship

Both may contain properties.

Relationships are first-class citizens.

---

# Ontology Layers

The ontology is organized into four conceptual layers.

```
Concept

↓

Entity Type

↓

Relationship Type

↓

Knowledge Instance
```

Example:

```
Technique

↓

REQUIRES

↓

Embedding Model

↓

OpenAI text-embedding-3-large
```

---

# Entity Types

Current ontology defines the following top-level entity types.

- Technique
- Framework
- Component
- Paper
- Author
- Organization
- Dataset
- Benchmark
- Embedding Model
- LLM
- Retriever
- Reranker
- Chunking Strategy
- Prompt Technique
- Vector Database
- Graph Database
- Evaluation Metric
- Agent
- Workflow
- Memory Strategy
- Tool
- MCP Server

Future versions may introduce additional entity types without breaking compatibility.

---

# Relationship Philosophy

Relationships express knowledge.

Relationships are directional.

Relationships possess semantics.

Relationships may contain metadata.

Relationships may evolve independently from entities.

---

# Relationship Categories

The ontology groups relationships into semantic families.

## Structural

Describes hierarchy.

Examples:

```
EXTENDS

IMPLEMENTS

SPECIALIZES

GENERALIZES

BELONGS_TO
```

---

## Dependency

Describes mandatory or optional requirements.

Examples:

```
REQUIRES

DEPENDS_ON

USES

OPTIONALLY_USES

SUPPORTED_BY
```

---

## Implementation

Describes implementation capabilities.

Examples:

```
IMPLEMENTS

PROVIDES

SUPPORTS

GENERATES

EXECUTES
```

---

## Knowledge

Describes scientific or conceptual origin.

Examples:

```
INTRODUCED_BY

DESCRIBED_BY

DEFINED_IN

REFERENCES

INSPIRED_BY
```

---

## Evaluation

Describes evaluation relationships.

Examples:

```
EVALUATED_BY

BENCHMARKED_BY

MEASURED_WITH

VALIDATED_BY
```

---

## Compatibility

Examples:

```
COMPATIBLE_WITH

INCOMPATIBLE_WITH

ALTERNATIVE_TO

COMPLEMENTS

SUPERSEDES
```

---

## Workflow

Examples:

```
PRECEDES

FOLLOWS

PRODUCES

CONSUMES

TRANSFORMS
```

---

# Canonical Relationships

The following relationships are considered canonical.

## Technique

Technique

USES

Component

---

Technique

REQUIRES

Embedding Model

---

Technique

REQUIRES

Retriever

---

Technique

OPTIONALLY_USES

Reranker

---

Technique

IS_IMPLEMENTED_BY

Framework

---

Technique

IS_INTRODUCED_BY

Paper

---

Technique

IS_EVALUATED_BY

Benchmark

---

Technique

SOLVES

Problem

---

Technique

HAS_ADVANTAGE

Advantage

---

Technique

HAS_LIMITATION

Limitation

---

Technique

HAS_USE_CASE

Use Case

---

Technique

HAS_TRADEOFF

Tradeoff

---

# Framework

Framework

IMPLEMENTS

Technique

---

Framework

SUPPORTS

Component

---

Framework

SUPPORTS

Vector Database

---

Framework

SUPPORTS

Embedding Model

---

# Paper

Paper

INTRODUCES

Technique

---

Paper

DESCRIBES

Technique

---

Paper

AUTHORED_BY

Author

---

Paper

PUBLISHED_IN

Venue

---

Paper

CITES

Paper

---

# Retriever

Retriever

SEARCHES

Vector Database

---

Retriever

USES

Similarity Metric

---

Retriever

RETURNS

Document

---

# Chunking Strategy

Chunking Strategy

PRODUCES

Chunk

---

Chunk

IS_INDEXED_IN

Vector Database

---

# Embedding Model

Embedding Model

GENERATES

Embedding

---

Embedding

REPRESENTS

Chunk

---

# Vector Database

Vector Database

STORES

Embedding

---

Vector Database

SUPPORTS

Index Type

---

Vector Database

USES

Distance Metric

---

# Benchmark

Benchmark

USES

Dataset

---

Benchmark

MEASURES

Evaluation Metric

---

Benchmark

EVALUATES

Technique

---

# Agent

Agent

EXECUTES

Workflow

---

Agent

USES

Tool

---

Agent

USES

LLM

---

# Workflow

Workflow

CONTAINS

Step

---

Step

PRODUCES

Artifact

---

Artifact

CONSUMED_BY

Step

---

# Relationship Properties

Every relationship may contain additional information.

Typical properties include:

- id
- version
- confidence
- source
- evidence
- rationale
- notes
- introducedInVersion
- deprecatedInVersion

Relationships are entities in their own right.

---

# Cardinality

Relationships may define cardinality.

Examples:

```
Technique

REQUIRES

1..N

Retriever
```

```
Paper

AUTHORED_BY

1..N

Author
```

```
Framework

IMPLEMENTS

0..N

Technique
```

Cardinality belongs to the relationship.

Not to the entities.

---

# Semantic Constraints

Examples of ontology rules.

A Paper cannot IMPLEMENT a Technique.

A Framework cannot AUTHOR a Paper.

An Embedding Model cannot EVALUATE a Benchmark.

A Dataset cannot REQUIRE an LLM.

The ontology defines which relationships are valid.

---

# Future RDF Mapping

Every relationship is intentionally compatible with RDF triples.

Example:

```
Subject

Predicate

Object
```

Technique

REQUIRES

Retriever

The repository may therefore be exported to RDF without semantic loss.

---

# Knowledge Graph Vision

The complete repository forms a connected graph.

Every node represents knowledge.

Every edge represents meaning.

Queries should be answerable through graph traversal rather than document inspection.

Example questions:

- Which techniques require rerankers?
- Which frameworks implement GraphRAG?
- Which papers introduced recursive retrieval?
- Which benchmarks evaluate long-context retrieval?
- Which embedding models are compatible with Hybrid Search?

The ontology exists to make those questions computable.

---

# Guiding Principle

Knowledge is not stored.

Knowledge is connected.

Connections are the primary asset of the RAG Knowledge Model.

Every future entity, schema and document must strengthen the graph rather than duplicate information.