# Ubiquitous Language
## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines the official vocabulary of the RAG Knowledge Model.

It establishes the terms that maintainers, contributors, schemas, documentation, JSON documents, diagrams and generated artifacts must use consistently.

The purpose of this file is to avoid ambiguity.

The RAG ecosystem contains many overlapping terms.

Different frameworks often use different names for similar concepts.

This document defines the canonical language used by this repository.

---

# Core Rule

Use the terms defined in this document.

Do not introduce synonyms unless they are explicitly registered as aliases.

Example:

Preferred:

```
Advantage
```

Avoid:

```
Benefit
Pro
Upside
Positive Aspect
```

Preferred:

```
Vector Database
```

Avoid:

```
Vector DB
Embedding Store
Vector Store Database
```

Preferred:

```
Embedding Model
```

Avoid:

```
Embedder
Embedding Engine
Embedding Generator Model
```

---

# Vocabulary Design Principles

## 1. One Concept, One Preferred Term

Every important concept has one canonical term.

Aliases may exist, but they must resolve to the preferred term.

---

## 2. Prefer Explicit Names

Avoid overly generic names.

Preferred:

```
Embedding Model
```

Avoid:

```
Model
```

Preferred:

```
Vector Database
```

Avoid:

```
Database
```

Preferred:

```
Retrieval Technique
```

Avoid:

```
Technique
```

when ambiguity is possible.

---

## 3. Avoid Framework-Specific Terminology

Framework-specific terms may be documented, but they should not become canonical unless they are domain-standard.

Example:

```
Document
```

is canonical.

```
LangChain Document
```

is framework-specific.

---

## 4. Distinguish Concept from Implementation

A concept describes what something is.

An implementation describes how a framework realizes it.

Example:

```
Retriever
```

is a concept.

```
Spring AI VectorStoreRetriever
```

is an implementation.

---

## 5. Distinguish Technique from Component

A technique is a method or strategy.

A component is a reusable architectural part.

Example:

```
HyDE
```

is a Technique.

```
Retriever
```

is a Component.

---

## 6. Distinguish Model Types

Do not use the term `Model` alone.

Use one of:

- Language Model
- Large Language Model
- Embedding Model
- Reranker Model
- Vision Language Model
- Multimodal Model
- Classification Model
- Generative Model

---

# Canonical Entity Terms

## Entity

The most generic identifiable object in the repository.

Every object that has a stable identifier is an Entity.

Examples:

- Technique
- Framework
- Paper
- Component
- Dataset
- Benchmark

---

## Knowledge Entity

An Entity that contains knowledge-bearing information.

A Knowledge Entity has descriptions, relationships, references, metadata and evidence.

Examples:

- Naive RAG
- HyDE
- Spring AI
- Self-RAG Paper
- BEIR Benchmark

---

## Technique

A method, strategy or algorithmic approach used to solve a problem in the RAG ecosystem.

Examples:

- Naive RAG
- Hybrid RAG
- HyDE
- Self-RAG
- CRAG
- GraphRAG
- RAPTOR

Avoid using Technique for concrete software classes, libraries or tools.

---

## Framework

A software framework that provides reusable abstractions or implementations for building AI, LLM or RAG applications.

Examples:

- Spring AI
- LangChain
- LlamaIndex
- Haystack
- Semantic Kernel

---

## Component

A reusable architectural building block.

Examples:

- Retriever
- Reranker
- Vector Store
- Document Loader
- Chunker
- Prompt Template
- Output Parser

---

## Paper

An academic or technical publication that introduces, evaluates, describes or formalizes a concept.

Examples:

- RAG Paper
- Self-RAG Paper
- CRAG Paper
- RAPTOR Paper

---

## Dataset

A collection of data used for training, evaluation, benchmarking or demonstration.

Examples:

- Natural Questions
- HotpotQA
- MS MARCO
- BEIR datasets

---

## Benchmark

A standardized evaluation setup used to compare systems, models or techniques.

Examples:

- BEIR
- MTEB
- RAGAS evaluation suite

---

## Pattern

A reusable architectural solution to a recurring design problem.

Examples:

- Query Transformation
- Context Compression
- Parent Document Retrieval
- Multi-Step Retrieval

---

## Prompt Technique

A prompting strategy used to guide a language model.

Examples:

- Chain of Thought
- ReAct
- Step Back Prompting
- Few-Shot Prompting

---

## Agent

A system that uses reasoning, tools, memory or planning to perform tasks with some degree of autonomy.

Examples:

- ReAct Agent
- Tool-Using Agent
- Planning Agent
- Multi-Agent System

---

# Canonical RAG Terms

## Retrieval-Augmented Generation

A technique in which a generative model receives external information retrieved from a knowledge source before producing an answer.

Preferred abbreviation:

```
RAG
```

---

## Naive RAG

The simplest RAG pipeline.

It typically consists of:

1. User query
2. Query embedding
3. Vector search
4. Top-k retrieval
5. Prompt construction
6. LLM answer generation

---

## Advanced RAG

A RAG pipeline that improves over Naive RAG by adding techniques such as query rewriting, hybrid search, reranking, metadata filtering or contextual compression.

---

## Modular RAG

A RAG architecture where the pipeline is composed of interchangeable modules.

Examples:

- Query Transformer
- Retriever
- Reranker
- Compressor
- Generator
- Evaluator

---

## Agentic RAG

A RAG architecture in which an agent dynamically decides when, how and where to retrieve information.

Agentic RAG may involve planning, tool use, multiple retrieval steps and self-correction.

---

## Adaptive RAG

A RAG architecture that dynamically decides whether retrieval is needed and which retrieval strategy should be used.

---

## Corrective RAG

A RAG architecture that evaluates retrieval quality and performs corrective actions when retrieved context is insufficient or unreliable.

Preferred abbreviation:

```
CRAG
```

---

## Self-RAG

A RAG architecture in which the model reflects on retrieval necessity, evidence relevance and answer quality during generation.

---

## GraphRAG

A RAG technique that uses graph-structured knowledge to improve retrieval, reasoning or answer generation.

Preferred spelling:

```
GraphRAG
```

Avoid:

```
Graph RAG
Graph-RAG
Graph Rag
```

unless referring to a specific paper, product or framework that uses a different spelling.

---

## Hybrid RAG

A RAG technique that combines multiple retrieval methods, usually dense vector search and sparse lexical search.

---

## Multimodal RAG

A RAG architecture that retrieves and uses information from multiple modalities.

Examples:

- text
- images
- audio
- video
- tables
- diagrams

---

# Query Terms

## Query

The input request used to retrieve information.

A Query may originate from a user, an agent, a tool or another model.

---

## User Query

The original query provided by the user.

---

## Transformed Query

A query produced by modifying another query.

Examples:

- rewritten query
- expanded query
- decomposed query
- hypothetical query

---

## Query Transformation

A technique that modifies a query before retrieval.

Examples:

- Query Rewriting
- Query Expansion
- Query Decomposition
- Multi-Query Generation
- Step-Back Querying

---

## Query Rewriting

A query transformation that rewrites the user query into a clearer or more retrieval-friendly form.

---

## Query Expansion

A query transformation that adds related terms or concepts to improve recall.

---

## Query Decomposition

A query transformation that breaks a complex query into simpler subqueries.

---

## Multi-Query Generation

A technique where multiple alternative queries are generated from the original query.

---

## Step-Back Prompting

A technique where a more abstract or general question is generated before answering the specific question.

---

## HyDE

Hypothetical Document Embedding.

A technique where a language model generates a hypothetical answer or document, and that generated text is embedded for retrieval.

Preferred spelling:

```
HyDE
```

Official expansion:

```
Hypothetical Document Embedding
```

---

# Document Terms

## Document

A unit of source information before processing.

A Document may be a PDF, web page, Markdown file, DOCX file, HTML page, transcript or database record.

---

## Source Document

The original document before chunking, cleaning or transformation.

---

## Parsed Document

A document after extraction and structural parsing.

---

## Cleaned Document

A document after removal of irrelevant or noisy content.

---

## Enriched Document

A document enhanced with metadata, summaries, entities or additional annotations.

---

## Chunk

A smaller unit of text derived from a document.

Chunks are commonly used for embedding and retrieval.

---

## Parent Document

A larger document segment associated with one or more child chunks.

In Parent Document Retrieval, small chunks are used for matching while larger parent documents are returned as context.

---

## Child Chunk

A smaller chunk linked to a parent document or parent segment.

---

## Context Window

The maximum amount of text or tokens that can be provided to a model in a single prompt.

---

## Retrieved Context

The information retrieved from external sources and inserted into the model prompt.

---

## Grounding Context

Retrieved context used to support answer generation and reduce hallucination.

---

# Chunking Terms

## Chunking

The process of splitting documents into smaller units.

---

## Chunking Strategy

A method used to split documents.

Examples:

- Fixed-Size Chunking
- Recursive Chunking
- Semantic Chunking
- Sentence-Based Chunking
- Paragraph-Based Chunking
- Markdown-Aware Chunking
- Code-Aware Chunking

---

## Fixed-Size Chunking

A chunking strategy that splits text into chunks of approximately equal size.

---

## Recursive Chunking

A chunking strategy that recursively splits text using a hierarchy of separators.

---

## Semantic Chunking

A chunking strategy that attempts to split text according to semantic coherence.

---

## Sentence Window Retrieval

A retrieval strategy that retrieves a matching sentence plus nearby surrounding sentences.

---

## Overlap

The repeated content shared between adjacent chunks.

Preferred term:

```
Chunk Overlap
```

---

# Embedding Terms

## Embedding

A numerical vector representation of content.

Embeddings are used to compare semantic similarity.

---

## Embedding Model

A model that converts text, images, audio or other inputs into embeddings.

---

## Dense Embedding

A continuous vector representation, typically used for semantic similarity search.

---

## Sparse Embedding

A sparse vector representation, often related to lexical or term-based matching.

---

## Multimodal Embedding

An embedding that represents more than one modality.

Examples:

- text and image
- image and audio
- video and text

---

## Embedding Dimension

The number of numeric values in an embedding vector.

---

## Embedding Space

The vector space in which embeddings are compared.

---

## Semantic Similarity

A measure of conceptual closeness between two embeddings.

---

# Retrieval Terms

## Retrieval

The process of finding relevant information from one or more knowledge sources.

---

## Retriever

A component responsible for retrieving information.

---

## Dense Retrieval

Retrieval based on dense vector embeddings.

---

## Sparse Retrieval

Retrieval based on sparse lexical or term-based representations.

---

## Lexical Retrieval

Retrieval based on exact or approximate term matching.

---

## Semantic Retrieval

Retrieval based on conceptual similarity rather than exact words.

---

## Hybrid Retrieval

Retrieval that combines dense and sparse retrieval.

---

## Keyword Search

Search based on explicit terms or keywords.

---

## Full-Text Search

Search over natural language documents using text indexing.

---

## BM25

A ranking function commonly used in lexical search.

BM25 should be treated as a lexical retrieval method, not as a vector retrieval method.

---

## Vector Search

Search based on vector similarity.

---

## Similarity Search

Search that returns items similar to a query representation.

---

## Top-K Retrieval

Retrieval that returns the top K most relevant results.

---

## Metadata Filtering

Filtering retrieval results using structured metadata.

Examples:

- date
- author
- document type
- tenant
- language
- access level

---

## Federated Retrieval

Retrieval performed across multiple independent sources.

Examples:

- vector database
- SQL database
- search engine
- knowledge graph
- file system
- API

---

## Recursive Retrieval

Retrieval performed repeatedly, where previous results influence subsequent retrieval steps.

---

## Multi-Hop Retrieval

Retrieval that requires multiple dependent steps to answer a question.

---

# Ranking Terms

## Ranking

Ordering retrieved items by relevance or utility.

---

## Reranking

Reordering retrieved results using a secondary model or scoring method.

---

## Reranker

A component or model that reranks retrieved candidates.

---

## Cross-Encoder Reranker

A reranker that jointly processes the query and candidate document to estimate relevance.

---

## Bi-Encoder

A model architecture where query and document are encoded separately.

---

## Reciprocal Rank Fusion

A method for combining ranked results from multiple retrieval systems.

Preferred abbreviation:

```
RRF
```

---

# Storage Terms

## Vector Database

A database optimized for storing and searching vectors.

Examples:

- pgvector
- Pinecone
- Weaviate
- Milvus
- Qdrant
- Chroma

---

## Vector Store

A component or abstraction used by frameworks to interact with vector storage.

Use Vector Store when referring to the abstraction.

Use Vector Database when referring to the database system.

---

## Graph Database

A database optimized for storing nodes and relationships.

Examples:

- Neo4j
- Amazon Neptune
- ArangoDB

---

## Search Engine

A system optimized for text search and ranking.

Examples:

- Elasticsearch
- OpenSearch
- Solr

---

## Index

A data structure used to accelerate search.

---

## Vector Index

An index used for approximate or exact vector search.

---

## Approximate Nearest Neighbor

A family of algorithms used for efficient similarity search in high-dimensional spaces.

Preferred abbreviation:

```
ANN
```

---

## Distance Metric

A function used to compare vectors.

Examples:

- cosine distance
- dot product
- Euclidean distance

---

## Similarity Metric

A function used to measure similarity.

Examples:

- cosine similarity
- dot product similarity

---

# Generation Terms

## Generation

The process by which a model produces an output.

---

## Generator

A component responsible for generating final answers.

---

## Language Model

A model that processes or generates natural language.

---

## Large Language Model

A large-scale language model used for text generation, reasoning, summarization or instruction following.

Preferred abbreviation:

```
LLM
```

---

## Vision Language Model

A model that processes both visual and textual inputs.

Preferred abbreviation:

```
VLM
```

---

## Multimodal Model

A model capable of processing or generating multiple modalities.

---

## Prompt

The input sent to a model.

---

## Prompt Template

A reusable template used to construct prompts.

---

## System Prompt

A prompt section that defines high-level behavior or rules.

---

## User Prompt

A prompt section containing the user's input.

---

## Context Prompt

A prompt section containing retrieved or externally supplied context.

---

## Answer

The final response generated for the user or consuming system.

---

## Citation

A reference linking an answer to supporting evidence.

---

## Grounded Answer

An answer supported by retrieved evidence.

---

## Hallucination

A generated statement that is unsupported, false or not grounded in the available evidence.

---

# Evaluation Terms

## Evaluation

The process of measuring system behavior or output quality.

---

## Evaluation Metric

A metric used to evaluate a model, technique, pipeline or answer.

---

## Recall

The ability of a retrieval system to find relevant information.

---

## Precision

The proportion of retrieved information that is relevant.

---

## Faithfulness

The degree to which an answer is supported by the provided context.

---

## Groundedness

The degree to which an answer is anchored in retrieved evidence.

---

## Relevance

The degree to which retrieved or generated content addresses the query.

---

## Answer Correctness

The degree to which the generated answer is factually correct.

---

## Context Relevance

The degree to which retrieved context is useful for answering the query.

---

## Citation Accuracy

The degree to which citations correctly support the claims they reference.

---

## Latency

The time required to complete an operation.

---

## Cost

The computational, monetary or operational expense of a technique or system.

---

## Token Usage

The number of tokens consumed by a model call.

---

## Benchmark Score

A measured result produced by a benchmark.

---

# Relationship Terms

## Relationship

A directional semantic connection between two entities.

---

## Source Entity

The entity where a relationship starts.

---

## Target Entity

The entity where a relationship ends.

---

## Relationship Type

The canonical predicate used to describe a relationship.

Examples:

- REQUIRES
- USES
- IMPLEMENTS
- INTRODUCES
- EVALUATES

---

## Relationship Property

Metadata attached to a relationship.

Examples:

- confidence
- evidence
- version
- rationale
- mandatory

---

## Cardinality

The number of allowed relationship targets.

Examples:

- 0..1
- 1..1
- 0..N
- 1..N

---

# Canonical Relationship Verbs

## EXTENDS

Indicates that one entity builds upon another.

Example:

```
Advanced RAG EXTENDS Naive RAG
```

---

## SPECIALIZES

Indicates that one entity is a more specific form of another.

Example:

```
Hybrid RAG SPECIALIZES Retrieval Technique
```

---

## GENERALIZES

Indicates that one entity abstracts over another.

Example:

```
Retrieval Technique GENERALIZES Hybrid RAG
```

---

## BELONGS_TO

Indicates membership in a family, category or taxonomy.

Example:

```
HyDE BELONGS_TO Query Transformation
```

---

## REQUIRES

Indicates a mandatory dependency.

Example:

```
Naive RAG REQUIRES Retriever
```

---

## OPTIONALLY_USES

Indicates an optional dependency.

Example:

```
Naive RAG OPTIONALLY_USES Reranker
```

---

## USES

Indicates usage without specifying whether it is mandatory.

Example:

```
Hybrid RAG USES Sparse Retrieval
```

---

## IMPLEMENTS

Indicates that a concrete framework or component realizes a concept.

Example:

```
Spring AI IMPLEMENTS Vector Store Abstraction
```

---

## SUPPORTS

Indicates compatibility or supported capability.

Example:

```
pgvector SUPPORTS Vector Search
```

---

## INTRODUCES

Indicates that a paper, author or organization introduced a concept.

Example:

```
Self-RAG Paper INTRODUCES Self-RAG
```

---

## DESCRIBES

Indicates that a source explains a concept.

Example:

```
Paper DESCRIBES Technique
```

---

## EVALUATES

Indicates that a benchmark, paper or experiment evaluates something.

Example:

```
Benchmark EVALUATES Technique
```

---

## MEASURES

Indicates that a metric measures an aspect of quality.

Example:

```
Faithfulness MEASURES Grounded Answer Quality
```

---

## COMPATIBLE_WITH

Indicates that two entities can be used together.

Example:

```
HyDE COMPATIBLE_WITH Reranking
```

---

## INCOMPATIBLE_WITH

Indicates that two entities should not be used together or are technically incompatible.

---

## ALTERNATIVE_TO

Indicates that one entity may replace another in some contexts.

Example:

```
Multi-Query Retrieval ALTERNATIVE_TO HyDE
```

---

## COMPLEMENTS

Indicates that two entities work well together.

Example:

```
Hybrid Retrieval COMPLEMENTS Reranking
```

---

## SUPERSEDES

Indicates that one entity replaces or improves upon another.

---

## PRODUCES

Indicates that an entity creates an output.

Example:

```
Embedding Model PRODUCES Embedding
```

---

## CONSUMES

Indicates that an entity receives an input.

Example:

```
Language Model CONSUMES Prompt
```

---

## TRANSFORMS

Indicates that an entity changes one artifact into another.

Example:

```
Chunking Strategy TRANSFORMS Document INTO Chunk
```

---

# Quality Attribute Terms

## Accuracy

The degree to which outputs are correct.

---

## Robustness

The ability of a system to handle unexpected, noisy or adversarial inputs.

---

## Scalability

The ability of a system to handle growth in data, traffic or complexity.

---

## Maintainability

The ease with which a system can be modified or extended.

---

## Observability

The ability to inspect and understand system behavior.

---

## Explainability

The ability to explain why a system produced a result.

---

## Traceability

The ability to trace an answer, decision or output back to supporting evidence.

---

## Reliability

The ability of a system to behave consistently over time.

---

## Determinism

The degree to which the same input produces the same output.

---

# Problem Terms

## Problem

A recurring challenge addressed by one or more techniques.

Examples:

- Low Recall
- Low Precision
- Hallucination
- Context Window Limit
- Stale Knowledge
- Query Ambiguity
- Semantic Gap
- High Latency
- High Cost

---

## Low Recall

A retrieval problem where relevant information is not retrieved.

---

## Low Precision

A retrieval problem where retrieved information contains too much irrelevant content.

---

## Semantic Gap

The mismatch between how a user asks a question and how relevant information is expressed in documents.

---

## Query Ambiguity

A problem where the user's query has multiple possible interpretations.

---

## Context Window Limit

The limitation caused by the finite amount of text a model can process at once.

---

## Stale Knowledge

A problem where the model or knowledge source lacks up-to-date information.

---

## Noise

Irrelevant or harmful information included in retrieved context.

---

# Benefit and Limitation Terms

## Advantage

A positive effect introduced by an entity.

Preferred term:

```
Advantage
```

Avoid:

```
Benefit
Pro
Upside
Positive
```

---

## Limitation

A known boundary or weakness.

Preferred term:

```
Limitation
```

Avoid:

```
Con
Downside
Weakness
Problem
```

unless the entity is explicitly a Problem.

---

## Tradeoff

A compromise introduced by a design decision.

Example:

```
Reranking improves precision but increases latency.
```

---

## Use Case

A scenario where an entity is useful.

---

## Anti-Pattern

A scenario where a technique is commonly misused or should be avoided.

---

## Common Mistake

A frequent implementation error.

---

## Misconception

A commonly held but incorrect belief.

---

# Implementation Terms

## Implementation

A concrete realization of a concept in software.

---

## Native Support

Support provided directly by a framework without custom code.

---

## Custom Implementation

An implementation that requires user-defined code.

---

## Integration

A connection between two systems or components.

---

## Adapter

A component that translates one interface into another.

---

## Provider

A service or platform that supplies models, APIs or infrastructure.

Examples:

- OpenAI
- Anthropic
- Google
- Azure
- AWS
- Cohere
- Mistral

---

## Orchestrator

A component that coordinates multiple steps, tools or agents.

---

## Pipeline

A sequence of processing steps.

---

## Workflow

A structured process that may include branching, loops or conditional execution.

Use Pipeline for mostly linear processing.

Use Workflow for broader orchestration.

---

# Agent Terms

## Tool

An external function, API or capability callable by an agent or model.

---

## Tool Calling

The ability of a model or agent to invoke tools.

---

## Planning

The process of decomposing a task into steps.

---

## Memory

Stored information used by an agent across turns or tasks.

---

## Short-Term Memory

Memory used within a session or task.

---

## Long-Term Memory

Memory persisted across sessions or tasks.

---

## Reflection

A process where a model evaluates or critiques its own reasoning or output.

---

## Self-Correction

A process where a system detects and corrects its own errors.

---

# Evidence Terms

## Evidence

Information supporting a claim.

---

## Reference

A pointer to an external or internal source.

---

## Source

The origin of information.

Examples:

- paper
- documentation
- benchmark
- experiment
- repository
- production report

---

## Claim

A statement that may require evidence.

---

## Confidence

The estimated reliability of a statement, relationship or classification.

Allowed conceptual values:

- Very Low
- Low
- Medium
- High
- Very High

---

## Rationale

The reason behind a decision, classification or relationship.

---

# Metadata Terms

## Metadata

Information about a document, not about the represented concept.

---

## Version

The version of an entity document.

---

## Schema Version

The version of the schema used by a document.

---

## Status

The lifecycle state of a document.

Preferred values:

- Draft
- Review
- Published
- Deprecated
- Archived

---

## Maintainer

A person or organization responsible for maintaining a document.

---

## Created At

The date when a document was created.

---

## Updated At

The date when a document was last updated.

---

# Naming Rules

## Entity Names

Use singular nouns.

Preferred:

```
Technique
Framework
Component
Paper
Dataset
Benchmark
```

Avoid:

```
Techniques
Frameworks
Components
```

unless naming a collection.

---

## Relationship Names

Use uppercase verb phrases.

Preferred:

```
REQUIRES
IMPLEMENTS
INTRODUCES
EVALUATES
COMPATIBLE_WITH
```

Avoid:

```
requires
implements
introducedBy
is compatible with
```

---

## File Names

Use lowercase kebab-case.

Preferred:

```
self-rag.json
graph-rag.json
hybrid-rag.json
```

Avoid:

```
SelfRAG.json
graph_rag.json
Graph RAG.json
```

---

## Slugs

Use lowercase kebab-case.

Preferred:

```
parent-document-rag
multi-query-retrieval
contextual-compression
```

---

## Identifiers

Use uppercase stable identifiers.

Examples:

```
TECHNIQUE-0001
FRAMEWORK-0001
PAPER-0001
COMPONENT-0001
```

---

# Preferred Terms and Avoided Terms

| Preferred Term | Avoid |
|---|---|
| Advantage | Benefit, Pro, Upside |
| Limitation | Con, Downside |
| Tradeoff | Compromise, Cost unless referring to monetary/computational cost |
| Vector Database | Vector DB, Embedding DB |
| Vector Store | Vector Database when referring to a framework abstraction |
| Embedding Model | Embedder |
| Language Model | Text Model |
| Large Language Model | AI Model when referring specifically to LLMs |
| Retriever | Retrieval Engine |
| Reranker | Re-ranker unless used by a specific project |
| Chunk | Segment, Piece |
| Document | File unless specifically referring to filesystem files |
| Query Transformation | Query Manipulation |
| Hybrid Retrieval | Hybrid Search when retrieval is the intended concept |
| Grounded Answer | Verified Answer unless verification is actually performed |
| Hallucination | Fabrication, Made-up Answer |
| Evaluation Metric | Score unless referring to a concrete measured value |
| Framework | Library when the project provides architectural abstractions |
| Component | Module unless referring to a specific module system |
| Relationship | Link, Edge, Association |
| Entity | Node unless specifically discussing graph export |

---

# Alias Policy

Aliases are allowed.

Aliases must be explicitly declared.

Aliases must resolve to exactly one preferred term whenever possible.

Example:

```
Vector DB
```

is an alias for:

```
Vector Database
```

Example:

```
Re-ranker
```

is an alias for:

```
Reranker
```

Example:

```
Graph RAG
```

may be an alias for:

```
GraphRAG
```

unless referring to a source that uses a specific spelling.

---

# Ambiguous Terms

The following terms are ambiguous and should be avoided unless qualified.

## Model

Use one of:

- Language Model
- Large Language Model
- Embedding Model
- Reranker Model
- Multimodal Model

---

## Database

Use one of:

- Vector Database
- Graph Database
- Relational Database
- Document Database
- Search Engine

---

## Search

Use one of:

- Vector Search
- Keyword Search
- Full-Text Search
- Semantic Search
- Hybrid Retrieval

---

## Context

Use one of:

- Retrieved Context
- Prompt Context
- Grounding Context
- Conversation Context
- Execution Context

---

## Agent

Clarify whether the meaning is:

- Tool-Using Agent
- Planning Agent
- RAG Agent
- Multi-Agent System
- Autonomous Agent

---

# Enforcement

Schemas, documentation and JSON instances should follow this vocabulary.

Pull requests introducing new terms should either:

1. use an existing canonical term;
2. add the new term to this document;
3. justify why the new term is not an alias of an existing term.

---

# Summary

The Ubiquitous Language is the shared vocabulary of the RAG Knowledge Model.

It exists to ensure that humans, schemas, JSON documents, generated code and AI agents all use the same conceptual language.

Consistency of language is consistency of knowledge.