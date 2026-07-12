# Embedding Model Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how embedding models are represented in the RAG Knowledge Model.

Embedding models are model entities that encode queries, passages, documents, code, images or other artifacts into vector representations used for retrieval, clustering, comparison, reranking support or evaluation.

The Embedding Model Model answers the question:

> **How should RKM describe models that transform RAG-relevant inputs into embeddings used by retrieval and similarity workflows?**

---

# Core Principle

An embedding model is not only a vector size, provider endpoint or implementation detail inside a retriever.

An embedding model is a reusable model capability with defined inputs, vector output characteristics, retrieval behavior, access conditions, operational constraints and evaluation evidence.

```text
Retriever USES Embedding Model
Technique REQUIRES Embedding Model
Provider PROVIDES Embedding Model
Vector Database SUPPORTS Embedding Model
Benchmark EVALUATES Embedding Model
Embedding Model HAS_LIMITATION Limitation
```

Representing embedding models explicitly allows RKM to describe retrieval quality, dimensionality, supported modalities, distance metrics, normalization expectations, multilingual behavior, deployment options and evidence-supported tradeoffs separately from retrievers and vector databases.

---

# Embedding Model

An Embedding Model is an entity that converts an input artifact into an embedding suitable for comparison or indexing.

Input artifacts may include:

* queries
* passages
* documents
* code blocks
* images
* tables
* multimodal records

Embedding model entities should identify what they encode, what vector output they produce, how the output is commonly compared, which RAG stages they support and which evidence supports claims about their behavior.

Preferred:

```text
Dense text embedding model that encodes queries and passages into normalized vectors for semantic retrieval over paragraph-sized chunks.
```

Avoid:

```text
Embedding API.
```

The avoided statement does not identify the model capability, input shape, output behavior or RAG role.

---

# Embedding Model Boundary

Every embedding model should have a clear boundary.

The boundary identifies:

* whether the entity represents a concrete model, checkpoint, provider-hosted variant or fine-tuned derivative
* which input modalities the model accepts
* which embedding dimensionality or supported dimensionalities it produces
* whether the output is dense, sparse, hybrid, multimodal or domain-specific
* which context limits and truncation behavior affect encoding
* which provider, license, repository or access channel makes the model available
* which retrievers, vector databases, benchmarks or workflows depend on the model

An embedding model should not be collapsed into the retriever that uses it or the vector database that stores its output. Those entities have separate responsibilities and may change independently.

---

# Model Type

Model type describes the dominant embedding approach.

Canonical model types include:

```text
Dense Text Embedding
Sparse Text Embedding
Hybrid Embedding
Sentence Embedding
Document Embedding
Code Embedding
Image Embedding
Multimodal Embedding
Instruction Tuned Embedding
Domain Specific Embedding
Other
```

The model type should describe the embedding capability, not the hosting provider or storage backend.

More detailed knowledge should be represented through input modalities, training profile, capabilities, relationships, claims and evidence.

---

# Vector Output

Vector output describes the representation produced by the embedding model.

Important output knowledge includes:

* embedding dimensionality
* supported alternative dimensionalities
* sparse, dense or hybrid representation shape
* expected normalization behavior
* compatible distance or similarity metrics
* whether query and document embeddings use the same encoder
* whether vector truncation or dimensionality reduction is supported

Vector output characteristics matter because they affect index design, storage cost, retrieval latency, metric selection and compatibility with vector databases.

When a provider allows configurable dimensions, the entity should distinguish the default output from supported alternatives.

---

# Input Modalities and Context

Input modalities describe what the model can encode.

Common modalities include:

* text
* code
* image
* audio
* video
* table
* graph
* multimodal input

Context limits should be recorded when they affect chunking strategy, query encoding, document preprocessing or evaluation interpretation.

Important context knowledge includes maximum tokens, maximum characters, tokenizer, oversized input handling and truncation behavior.

---

# Retrieval Capabilities

Embedding capabilities describe reusable behavior that affects RAG design.

Common capabilities include:

* semantic search
* asymmetric retrieval
* symmetric similarity
* query embedding
* document embedding
* passage embedding
* code search
* cross-lingual retrieval
* multilingual retrieval
* multimodal retrieval
* clustering
* classification
* reranking feature generation

Capabilities should be represented structurally when they affect entity selection, relationship modeling, benchmark interpretation or workflow design.

Capability claims should not be inferred from broad marketing language when a precise retrieval behavior requires evidence.

---

# Training Profile

Training profile describes known information about how the embedding model was trained or adapted.

Important training knowledge includes:

* training approach
* training data summary
* domain adaptation
* instruction tuning
* distillation
* cutoff date when available

Training knowledge helps explain why an embedding model may perform differently across domains, languages, modalities or query styles.

Training claims should remain scoped to the evidence available. Unknown training details should not be replaced with unsupported assumptions.

---

# Access and Deployment

Embedding model access describes how the model can be used.

Common access modes include:

* open weights
* hosted API
* managed service
* local runtime
* commercial license
* research license

Deployment characteristics may include batching support, quantization support, latency class, cost class, resource requirement and deployment target.

Provider-hosted embedding models should be connected to Provider entities when provider behavior affects availability, pricing, data handling, region support, versioning or reproducibility.

---

# Evaluation

Embedding model evaluation should identify the retrieval task, dataset, benchmark, metric, corpus, query set and indexing configuration used to support a claim.

Important evaluation context includes:

* benchmark or dataset identifier
* retrieval task
* metric values
* rank or comparison baseline
* evaluation date
* chunking strategy
* similarity metric
* vector index configuration
* candidate depth

Claims about embedding quality should not be generalized beyond the evaluated language, domain, corpus, query style, chunking approach, distance metric, model version or evaluation protocol.

---

# Relationship Use

Embedding models should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Retriever USES Embedding Model
Technique REQUIRES Embedding Model
Framework SUPPORTS Embedding Model
Provider PROVIDES Embedding Model
Vector Database SUPPORTS Embedding Model
Benchmark EVALUATES Embedding Model
Evaluation Metric MEASURES Embedding Model
Paper DESCRIBES Embedding Model
Embedding Model COMPATIBLE_WITH Vector Database
Embedding Model HAS_LIMITATION Limitation
```

Relationships should express graph-ready knowledge rather than restating prose. When a relationship depends on a specific configuration, version, benchmark result or provider setting, it should be supported by claims, evidence and references.

---

# Embedding Model Records

A complete embedding model record should include:

* identity
* metadata
* description
* embedding model details
* relationships
* claims
* evidence
* references

The embedding model details should include model type, input modalities and embedding dimensionality. Additional fields should be included when they materially affect retrieval design, reproducibility, comparison or operational adoption.

---

# Embedding Model vs Related Entities

Embedding Model is distinct from the entities that use, store, host or evaluate embeddings.

## Embedding Model vs Retriever

A Retriever selects candidate information for a RAG workflow.

An Embedding Model may provide vectors used by a retriever, but the retriever also includes retrieval strategy, candidate selection behavior, filtering, query handling and result formatting.

## Embedding Model vs Vector Database

A Vector Database stores, indexes and queries embeddings.

An Embedding Model produces the embeddings. The vector database controls storage, indexing, filtering and search execution.

## Embedding Model vs Provider

A Provider makes an embedding model available, hosts it, maintains it or distributes it.

The provider is not the model capability itself. Provider facts should be modeled separately when access, governance, cost or availability matters.

## Embedding Model vs Chunking Strategy

A Chunking Strategy defines how source content is divided into retrieval units.

An Embedding Model encodes those units. Chunk size and structure may affect embedding quality, but they remain separate modeling concerns.

---

# Quality Bar

An embedding model entry is ready for use when it:

* identifies the model boundary clearly
* uses `identity.entityType` value `EmbeddingModel`
* records required embedding model details
* separates model capability from provider, retriever and vector database behavior
* links reusable dependencies and compatibility through relationships
* scopes evaluation claims to the observed task and protocol
* cites evidence for quality, availability, limitation and operational claims that affect adoption
