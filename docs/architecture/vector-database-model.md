# Vector Database Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how vector databases are represented in the RAG Knowledge Model.

Vector databases are storage entities that store, index, filter and retrieve vector representations used by RAG retrievers, workflows, benchmarks and applications.

The Vector Database Model answers the question:

> **How should RKM describe vector storage systems whose indexing, query behavior, deployment model and operational constraints affect RAG retrieval quality?**

---

# Core Principle

A vector database is not only a backing store behind a retriever.

A vector database is a first-class knowledge entity when its index support, distance metrics, metadata filtering, deployment model, consistency behavior, scalability profile or integration surface materially affects RAG behavior.

```text
Retriever REQUIRES Vector Database
Framework SUPPORTS Vector Database
Provider PROVIDES Vector Database
Vector Database DEPENDS_ON Embedding Model
Benchmark EVALUATES Vector Database
Technique USES Vector Database
```

Representing vector databases explicitly allows RKM to separate storage capability from embedding model behavior, retriever behavior, provider availability and evidence-supported performance claims.

---

# Vector Database

A Vector Database is an entity specialized for storing vector representations and making them searchable through similarity, filtering or hybrid retrieval operations.

Vector database entities may represent:

* dedicated vector databases
* search engines with vector support
* relational databases with vector extensions
* NoSQL databases with vector support
* graph databases with vector support
* in-memory vector stores
* embedded vector stores
* managed vector search services

A vector database should be modeled when its capabilities are reusable across RAG systems or when its behavior affects retrieval quality, latency, cost, governance or reproducibility.

Preferred:

```text
Managed vector database that supports HNSW indexing, cosine similarity, metadata filtering and hybrid sparse-dense search for chunk-level retrieval.
```

Avoid:

```text
Vector search tool.
```

The avoided statement does not identify the storage boundary, index behavior, query capability or RAG role.

---

# Entity Boundary

Every vector database should have a clear boundary.

The boundary identifies:

* which vector representations the system stores
* which index types and distance metrics it supports
* which filtering, partitioning and hybrid search behaviors are available
* which deployment models and providers make it available
* which consistency, scalability and operational characteristics apply
* which retrievers, frameworks, embedding models, providers or benchmarks depend on it

A vector database should remain distinct from:

* an Embedding Model that creates vectors
* a Retriever that turns vector search into a RAG-facing retrieval capability
* a Provider that hosts, sells or maintains the database
* a Dataset or corpus stored inside the database
* a Benchmark that evaluates retrieval behavior using the database

These entities may be connected through canonical relationships when the relationship has reusable semantic value.

---

# Modality Semantics

Vector databases store and retrieve vector representations. The modality of the
artifact from which a vector was produced must not be confused with a native
capability of the database.

A vector generated from text, code, an image, audio, video, a table or another
artifact remains a numeric representation when it is stored in a vector
database. The database does not thereby acquire the ability to parse,
understand, transform or embed the original artifact.

RKM must distinguish three modality-related concepts.

## Embedding Source Modalities

Embedding source modalities identify the kinds of artifacts that may be
represented by vectors stored or searched through the database.

Examples include:

* text
* code
* image
* audio
* video
* table
* graph-derived data

This characteristic normally belongs to the embedding model, ingestion
pipeline, retriever or documented workload rather than to the vector database
itself.

A vector database record may mention an embedding source modality only when
the statement is scoped as workload compatibility or embedding provenance. It
must not be presented as native media processing by the database.

## Native Payload Modalities

Native payload modalities identify artifact or field types that the product
stores, indexes or queries as first-class data in addition to numeric vectors.

Examples may include:

* text fields with native lexical indexing
* JSON documents
* relational columns
* graph nodes and relationships
* binary or media columns
* collection-native data objects

Native payload support requires direct product evidence. Generic metadata
storage, opaque binary storage or the ability to attach an external URI does
not by itself prove native modality-specific retrieval or processing.

## Native Embedding Generation

Native embedding generation identifies whether the product or managed service
accepts source artifacts and generates embeddings through an integrated,
documented capability.

This knowledge must preserve:

* supported source modalities
* embedding model or provider
* capability origin
* product generation or API
* edition, plan and region
* configuration requirements
* preview or generally available status
* model-version, latency, quota and cost dependencies

An embedding model invoked by application code is external pipeline behavior.
A separately installed first-party package is not DBMS-core behavior. A managed
service feature must be scoped to the service generation and plan that provide
it.

## Current `supportedModalities` Field

The current `vectorDatabase.supportedModalities` field is transitional.

Until the schema is migrated, it must be interpreted only as:

> Embedding source modalities commonly represented by vectors in documented
> workloads using the database.

It must not be interpreted as proof that the database:

* accepts raw artifacts of those modalities
* parses or chunks those artifacts
* generates embeddings for them
* provides modality-specific indexing
* understands their semantic content
* offers equivalent native support across all listed modalities

The field is therefore unsuitable by itself for ranking or capability
comparison.

`Multimodal` is not an atomic source modality. It describes a model, record or
workflow that combines multiple modalities. A future schema should represent
the contributing modalities explicitly rather than mixing `Multimodal` into
the same enumeration as text, image or audio.

A future schema migration should replace or supersede
`supportedModalities` with separate structures equivalent to:

~~~text
embeddingSourceModalities
nativePayloadModalities
nativeEmbeddingGeneration
~~~

The migration must be performed separately from this semantic decision.
Existing records must not be rewritten mechanically. Each future value must be
re-established from product-specific evidence and capability-origin
qualifiers.

---

# Index Support

Index support describes the retrieval structures or search approaches available in the database.

Important index knowledge includes:

* flat exact search
* HNSW indexes
* inverted file indexes
* product quantization
* scalar quantization
* disk-based approximate nearest neighbor indexes
* graph-based approximate nearest neighbor indexes
* hybrid sparse and dense indexes

Index details should be represented when they affect retrieval quality, latency, cost, memory use, update behavior or reproducibility.

Claims about index performance should identify the corpus, vector dimensionality, distance metric, hardware, deployment model, query workload, index configuration and evaluation date when those details affect interpretation.

---

# Distance Metrics and Vector Compatibility

Distance metrics describe how stored vectors are compared at query time.

Common vector comparison methods include:

* cosine similarity
* dot product
* Euclidean distance
* Manhattan distance
* Hamming distance
* Jaccard similarity

Vector compatibility matters because embedding models may expect specific normalization behavior, dimensionality, distance metrics or sparse-dense representation shapes.

Compatibility should be modeled through structured fields and canonical relationships instead of prose-only claims when it affects entity selection or graph export.

---

# Filtering, Hybrid Retrieval and Graph Augmentation

Filtering, hybrid retrieval and graph augmentation are distinct retrieval
concepts. They must not be collapsed into one product-level boolean.

## Filtering

Filtering defines which stored objects are eligible for retrieval.

A filter constrains a candidate population through metadata, document fields,
labels, tenant identifiers, access-control predicates, dates, regions or other
structured conditions.

Filtering does not become hybrid retrieval merely because it is used together
with vector search. A filter normally changes candidate eligibility rather
than contributing an independent ranked retrieval signal.

RKM should distinguish:

* pre-filtering applied before or during candidate selection
* post-filtering applied after candidate selection
* static index scope established when an index is created
* dynamic query-time filtering
* database-side filtering
* application-side filtering
* over-fetch behavior required to preserve the requested result count

## Hybrid Retrieval

Hybrid Retrieval combines two or more independently meaningful retrieval
channels whose candidates, ranks or scores are merged, fused or reranked.

In the canonical RKM usage, the primary hybrid pattern combines:

* dense vector or semantic retrieval
* sparse, lexical, keyword or full-text retrieval

Examples include:

* dense-vector plus sparse-vector retrieval
* vector similarity plus BM25 or BM25F retrieval
* lexical and vector candidate lists merged through Reciprocal Rank Fusion
* score-bearing retrieval channels combined through weighted linear fusion
* multiple independently executed retrievers followed by a documented fusion
  or reranking stage

A capability must not be classified as Hybrid Retrieval merely because a
single query also contains:

* metadata filters
* graph predicates
* access-control conditions
* rule-based eligibility constraints
* traversal after candidate retrieval
* application logic that does not combine independent retrieval channels

Hybrid support must preserve:

* retrieval channels
* candidate-generation stage
* fusion or reranking method
* score or rank semantics
* capability origin
* execution boundary
* version, edition, plan and configuration
* whether the operation is automatic, configurable or application-defined

## Vector-Graph Composition

Vector-Graph Composition starts with vector candidates, graph candidates or
both and uses graph structure to expand, constrain, connect, explain or
contextualize retrieved entities.

Examples include:

* vector retrieval followed by neighborhood expansion
* vector candidates constrained by graph labels or relationships
* path traversal from semantically matched entities
* graph algorithms applied before or after vector retrieval
* connected-context assembly for GraphRAG
* graph-derived reranking or heuristic scoring

Vector-Graph Composition is valuable retrieval behavior, but it is not
synonymous with canonical dense-sparse Hybrid Retrieval.

A product may support Vector-Graph Composition without providing:

* BM25 or lexical retrieval
* sparse-vector retrieval
* ranked-list fusion
* score normalization
* a built-in hybrid ranker

RKM should eventually represent this capability through a separate structure
equivalent to:

~~~text
graphAugmentedRetrieval
vectorGraphComposition
~~~

## Capability Origin

Every material vector-database capability must identify where it is
implemented and under which product boundary it is available.

Capability origin applies not only to hybrid or graph-augmented retrieval but
also to:

* vector data types
* index families
* distance metrics
* filtering
* lexical or sparse retrieval
* fusion and reranking
* embedding generation
* graph traversal
* transactions and consistency
* replication and scaling
* backup and recovery
* security and access control
* observability
* multi-tenancy
* deployment automation

RKM must distinguish the following capability origins.

### Product Core

The capability is implemented by the database engine or managed service being
described and is available through its documented primary interface.

Examples include:

* a DBMS-native vector data type
* a built-in vector index
* a service-native filtering API
* a core query-language operator
* a built-in replication mechanism

Product-core classification still requires version and deployment qualifiers.
A feature in one major release must not be projected onto earlier releases.

### Edition-Specific Product Feature

The capability is implemented by the product but is available only in a named
edition, license tier or commercial distribution.

Examples include:

* Enterprise-only clustering
* edition-specific native vector storage
* commercial backup tooling
* advanced security or monitoring
* edition-specific sharding

The record must identify the edition boundary instead of assigning the
capability to every deployment of the product.

### Managed-Service Capability

The capability is supplied by a hosted service rather than by every
self-managed deployment of the underlying engine.

The record should preserve:

* service name
* resource generation or API family
* plan or pricing tier
* region
* preview or generally available status
* provider-managed dependencies
* quotas and lifecycle constraints

A managed backup, autoscaling or security feature must not be projected onto
the open-source or self-hosted engine.

### Host-Platform Capability

The capability is inherited from a host database, runtime or platform on which
the represented vector extension or subsystem depends.

Examples include:

* PostgreSQL transactions used by pgvector
* host-database replication
* host-database backup and recovery
* Kubernetes scheduling
* cloud identity and network controls

The capability belongs to the host boundary and must not be presented as an
independent implementation by the vector extension.

### First-Party Optional Package

The capability is delivered by the same vendor or project through a separately
installed library, package, SDK, plugin, module or toolkit.

Examples include:

* a GraphRAG retriever package
* an optional search plugin
* a vendor-maintained integration library
* a separately installed algorithm module

First-party ownership does not make an optional package part of the DBMS core.
The package name, version, installation requirement and supported product
versions should be retained.

### Third-Party Extension or Integration

The capability depends on software maintained outside the represented product
boundary.

Examples include:

* third-party plugins
* community adapters
* external rerankers
* external embedding services
* separately operated lexical-search systems
* external orchestration frameworks

The record must not imply that the primary product provides operational
support, lifecycle management or compatibility guarantees for the external
component unless evidence explicitly says so.

### Embedded External Component

The product ships with or invokes another search, indexing or model component
inside its supported distribution.

Examples include:

* an embedded search engine
* an ANN library used by the vector subsystem
* a bundled model runtime
* an internal indexing service

RKM should preserve both the product-facing capability and the implementation
dependency when that dependency affects licensing, compatibility, performance,
failure behavior or upgrade risk.

### Query-Language Composition

The capability can be expressed through the product query language by
combining lower-level primitives, but it is not a single automatic product
operation.

Examples include:

* SQL combining full-text and vector candidates
* Cypher combining vector retrieval and graph traversal
* user-authored score expressions
* query-defined normalization
* explicit candidate unions

Query-language composability is stronger than purely external orchestration,
but it must not be reported as a built-in automatic ranker, fusion pipeline or
workflow.

### Application-Side Orchestration

The capability exists only because application code coordinates multiple
queries, components or systems.

Examples include:

* application-side reciprocal-rank fusion
* client-side score normalization
* over-fetch and post-filter loops
* cross-database retrieval
* external graph expansion
* workflow-managed retries or failover

The product may enable the workflow, but the application owns its correctness,
latency, availability, security and reproducibility.

### Unknown or Unverified Origin

Use an unknown or unverified classification when available evidence proves
that a capability exists but does not establish its implementation boundary.

Unknown origin must not be silently interpreted as product core.

## Origin Is Independent From Support Strength

Capability origin and support strength are separate dimensions.

For example:

* an application-side workflow may be well documented and strongly supported
* a product-core feature may be preview, constrained or poorly documented
* a first-party package may be production-ready but independently versioned
* a managed-service feature may be generally available in only some regions

RKM must therefore avoid deriving confidence, maturity or quality directly
from origin.

## Required Origin Qualifiers

When origin affects comparison or adoption, claims and evidence should preserve:

* origin category
* product or component name
* version
* edition
* plan or tier
* deployment model
* API or resource generation
* region
* installation requirement
* configuration requirement
* release status
* supporting reference

These qualifiers may initially remain in claims and evidence until the schema
provides a dedicated capability-origin structure.

## Structured Capability Contract

The vector-database schema provides the optional
`vectorDatabase.capabilities` collection for material product, service,
package, integration, query-language and application-orchestrated
capabilities.

Each structured capability can preserve:

* the bounded behavior being described
* the implementation boundary
* the capability origin
* versions, editions, plans and deployment availability
* maturity or lifecycle status
* constraints and exclusions
* supporting claims, evidence and references

The structured capability contract supplements transitional aggregate fields
such as `supportedModalities`, `hybridSearch`, `scalability` and
`consistency`. It does not automatically make those legacy fields precise.

Existing records must not be migrated through blanket defaults. Each material
capability must be re-established from product-specific evidence.

During migration:

* absence of structured capabilities must not be interpreted as proof that the
  product lacks the behavior
* a first-party package must not be reported as DBMS-core behavior solely
  because it is published by the same vendor
* a managed-service capability must not be generalized to self-hosted
  deployments
* a host-platform capability must not be attributed solely to an extension
* query-language composition must not be described as an automatic built-in
  workflow
* application-side orchestration must not be described as native product
  behavior
* edition, plan, version and deployment boundaries must remain explicit

Capability origin and support strength remain independent dimensions. A
product-core capability may be preview or constrained, while an external or
application-side capability may be mature and strongly documented.

## Score Normalization

Score normalization is meaningful only when multiple score-bearing retrieval
channels are combined.

RKM must distinguish:

* no score combination
* rank-based fusion that does not require raw-score normalization
* built-in score normalization
* configurable score normalization
* first-party library normalization
* explicit query-expression normalization
* application-side normalization
* unknown or undocumented behavior

`scoreNormalizationSupported` must not be interpreted as proof that all hybrid
methods use normalization. Reciprocal Rank Fusion, weighted score fusion and
graph traversal have different score requirements.

## Current `hybridSearch` Field

The current `vectorDatabase.hybridSearch` field is transitional.

Until the schema is migrated:

* `supported: true` should mean that a documented multi-channel retrieval
  workflow exists, not that every method is DBMS-core
* each method must be interpreted together with claims, evidence and capability
  origin
* `Graph Plus Vector` must be treated as a legacy classification for
  Vector-Graph Composition, not as canonical dense-sparse Hybrid Retrieval
* metadata filtering must not be treated as a hybrid method
* `scoreNormalizationSupported` must be scoped to a concrete fusion method and
  implementation boundary

The current field is unsuitable by itself for capability ranking.

A future schema migration should separate structures equivalent to:

~~~text
hybridRetrieval
graphAugmentedRetrieval
capabilityOrigin
fusionMethods
scoreHandling
~~~

Existing records must not be rewritten mechanically. Hybrid, graph-augmented
and score-handling values must be re-established from product-specific
evidence.

Filtering, fusion and graph augmentation should remain structured whenever
they affect tenant isolation, access control, freshness, source selection,
candidate completeness, ranking, explainability or retrieval reproducibility.

---

# Product Licensing

Product licensing must be modeled separately from the license of the RKM
artifact.

`metadata.license` declares the SPDX license applying to the canonical RKM
record or document. It must not be reused to describe the software license,
commercial agreement or service terms of the vector database being modeled.

`vectorDatabase.productLicensing` describes edition-, offering-, plan-,
version- or deployment-scoped licensing profiles for the product or managed
service.

Each product-licensing profile requires:

* an explicit `scope`
* a `licenseModel`
* one or more supporting `referenceIds`
* at least one of `spdxExpression`, `licenseName` or `termsDescription`

The scope may identify:

* product versions
* software editions
* managed-service offerings
* plans or license tiers
* deployment models
* additional exclusions or boundaries

Separate profiles should be used when materially different terms apply to
different editions or offerings. For example, an open-source Community
Edition, a commercially licensed Enterprise Edition and a hosted managed
service should not be collapsed into one aggregate license value.

Use `spdxExpression` only when the applicable software license can be
represented accurately with SPDX syntax. Commercial agreements, evaluation
terms, provider contracts and managed-service terms must not be converted into
invented SPDX identifiers.

`licenseName` should preserve the documented name of a license, agreement or
service-terms document when one exists.

`termsDescription` should summarize material access or usage conditions that
cannot be represented by SPDX alone. It must remain concise and supported by
the referenced sources.

Boolean fields such as `commercialUseAllowed`, `redistributionAllowed` and
`sourceCodeAvailable` should be omitted when the answer depends on additional
conditions or has not been directly verified.

Product licensing must not be inferred solely from:

* source-code availability
* vendor ownership
* deployment model
* the existence of a free plan
* the license of a client library or driver
* the license of the RKM record

Claims and evidence should preserve additional qualifications when licensing
varies by version, edition, plan, region, contract or component.

---

# Deployment and Operations

Vector database deployment affects cost, latency, governance and reliability.

Common deployment models include:

* self-hosted
* managed cloud
* serverless
* embedded
* local
* hybrid
* edge

Operational knowledge should describe the characteristics that matter for RAG design, including scalability, durability, consistency, backup support, monitoring, indexing latency, query latency, update behavior, multi-tenancy and failure modes.

When a managed service and self-hosted deployment have materially different behavior, RKM should preserve that distinction through provider, deployment, claims, evidence and relationships.

---

# Relationship Use

Vector databases should be connected to other entities through canonical relationships when those relationships have reusable semantic value.

Useful vector database relationship patterns include:

```text
Retriever REQUIRES Vector Database
Framework SUPPORTS Vector Database
Provider PROVIDES Vector Database
Vector Database DEPENDS_ON Embedding Model
Vector Database SUPPORTS Retriever
Benchmark EVALUATES Vector Database
Technique USES Vector Database
Component IMPLEMENTS Vector Database
Vector Database HAS_LIMITATION Limitation
```

Relationships should express graph-ready knowledge about dependency, compatibility, support, implementation, evaluation and operational constraints.

---

# Evidence and Claims

Vector database claims require evidence when they describe behavior such as retrieval quality, latency, scalability, reliability, cost, consistency, filtering correctness, compliance support or production suitability.

Examples of evidence-scoped vector database claims include:

* a database supports a specific index type or distance metric
* a metadata filter changes retrieval precision for a documented workload
* a hybrid search configuration improves recall under a named benchmark
* a managed deployment provides documented region availability
* an index configuration reduces latency for a specified vector dimensionality and corpus size

Claims should not generalize beyond the database version, deployment model, index configuration, embedding model, corpus, query workload, metric, benchmark or evaluation date supported by evidence.

---

# Schema Alignment

Vector database entity documents are validated by `schema/vector-database.schema.json`.

The schema requires:

* `identity`
* `metadata`
* `description`
* `vectorDatabase`

The `identity.entityType` value must be `VectorDatabase`.

The specialized `vectorDatabase` object captures domain-specific structure such as database type, deployment models, supported index types, distance metrics, transitional modality information, metadata filtering, hybrid search, scalability, consistency, integration, operations, RAG usage, limitations and usage guidance.

Until the modality schema migration is completed, `supportedModalities` must be interpreted according to the transitional semantics defined in this document and must not be treated as native modality processing.

Shared concepts such as relationships, claims, evidence, references and external links remain outside the specialized object so they can be reused consistently across RKM entities and graph exports.

---

# Integration With Other Models

The Vector Database Model works with the Storage Model, Retrieval Model, Embedding Model Model, Provider Model, Benchmark Model, Evidence Model and Relationship Model.

The Storage Model defines the broader storage boundary for vector and graph storage systems.

The Retrieval Model defines the RAG-facing retrieval capability that queries a vector database.

The Embedding Model Model defines the models that produce vectors stored by the database.

The Provider Model identifies organizations or platforms that provide, host or support vector database capabilities.

The Benchmark Model and Evidence Model preserve the evaluation context behind claims about retrieval quality, performance and operational suitability.
