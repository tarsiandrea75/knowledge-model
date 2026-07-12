# Model Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how machine learning models are represented in the RAG Knowledge Model.

Models are first-class knowledge entities when their capabilities, access conditions, evaluation results, limitations or operational characteristics affect RAG system behavior.

The Model Model answers the question:

> **How should RKM describe models that encode, rank, reason over or generate knowledge in a RAG system?**

---

# Core Principle

A model is not only a provider product name or an implementation detail.

A model represents a reusable capability with observable behavior, constraints and evidence.

RKM currently represents model capabilities through specialized entity types such as Language Model, Embedding Model and Reranker.

```text
Technique REQUIRES Embedding Model
Retriever USES Embedding Model
Reranker USES Language Model
Benchmark EVALUATES Language Model
Provider PROVIDES Embedding Model
```

Model entities help RKM compare retrieval quality, generation behavior, latency, cost, deployment constraints, provenance and suitability for use cases.

---

# Model Boundary

Every model entity should define a clear boundary.

The boundary identifies:

* what capability the model provides
* which modalities it consumes and produces
* which RAG stages it supports
* which provider or release makes it available
* which version, checkpoint or access channel is being described
* which evaluation context supports claims about the model

Preferred:

```text
Embedding model that encodes text queries and passages into dense vectors for semantic retrieval.
```

Avoid:

```text
AI model.
```

The avoided statement does not identify the model capability, inputs, outputs or RAG role.

---

# Language Model

A Language Model is a model entity used for generation, reasoning, synthesis, tool use, query rewriting, relevance judging or other language-centered behavior.

Language models may be used to:

* generate grounded answers
* rewrite or expand queries
* compress retrieved context
* judge candidate relevance
* synthesize citations
* plan agent steps
* call tools
* produce structured outputs

Important language model knowledge includes context window limits, input and output modalities, tool-use support, structured-output support, deployment model, safety constraints and evaluation results.

Language model claims should be scoped to the task and context in which the behavior was observed.

---

# Embedding Model

An Embedding Model is a model entity that encodes text, code, images or other artifacts into vectors used for retrieval, clustering, classification or similarity comparison.

Embedding models may be used to:

* encode queries
* encode passages or documents
* support dense retrieval
* support hybrid retrieval
* support semantic clustering
* produce features for reranking
* align multimodal artifacts in a shared vector space

Important embedding model knowledge includes embedding dimensionality, supported modalities, context limits, distance metrics, normalization expectations, language coverage, training objective and retrieval evaluation results.

Embedding model entities should distinguish the model from the vector database, index configuration and retriever that use its vectors.

---

# Reranker

A Reranker is a model or scoring capability that reorders retrieved candidates by relevance, grounding value, diversity or task-specific utility.

Rerankers may be implemented as cross encoders, bi-encoder rerankers, learning-to-rank models, LLM-based judges, rule-based scorers or rank-fusion methods.

Rerankers may be used to:

* improve precision after candidate retrieval
* prioritize passages for context assembly
* select citation candidates
* combine dense and sparse retrieval results
* filter low-value candidates before generation
* support evaluation of retrieval outputs

Important reranker knowledge includes candidate input shape, scoring approach, output structure, latency impact, cost impact, quality impact and benchmark evidence.

---

# Model Identity

Model identity should be stable and specific enough to avoid confusing related releases.

Identity should distinguish:

* model family
* concrete model or checkpoint
* versioned release
* provider-hosted variant
* open-weight release
* fine-tuned derivative
* deployment-specific wrapper

When a provider changes the served behavior behind a stable product label, RKM should preserve evidence context and avoid treating historical evaluation claims as universally valid.

---

# Capability

A model capability is a reusable behavior that affects RAG design.

Examples include:

* grounded answer generation
* citation generation
* query rewriting
* semantic search
* asymmetric retrieval
* relevance scoring
* context compression
* structured output
* tool use
* multilingual retrieval

Capabilities should be represented structurally when they affect entity selection, relationships, claims or evaluation.

Capabilities should not be inferred from marketing language alone when a claim requires evidence.

---

# Access and Deployment

Model access describes how the model can be used.

Common access modes include:

* hosted API
* managed service
* open weights
* local deployment
* fine-tuning endpoint
* research release
* private preview

Deployment characteristics matter because the same model capability may have different latency, cost, privacy, governance and reproducibility properties under different access modes.

Provider-hosted models should be connected to Provider entities when the provider affects availability, policy, pricing, region support or evidence interpretation.

---

# Evaluation

Model evaluation should identify the task, dataset, benchmark, metric and configuration used to support a claim.

Examples of model evaluation contexts include:

* retrieval quality for an embedding model on a named dataset
* answer faithfulness for a language model in a grounded generation workflow
* precision improvement from a reranker after a specific retriever
* latency impact for a hosted model under a specific batch size
* citation quality for a model under a defined prompt technique

Evaluation claims should not be generalized beyond the observed task, corpus, model version or workflow configuration unless evidence supports that scope.

---

# Relationship Use

Models should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Technique REQUIRES Embedding Model
Technique OPTIONALLY_USES Reranker
Retriever USES Embedding Model
Reranker USES Language Model
Framework SUPPORTS Language Model
Provider PROVIDES Language Model
Benchmark EVALUATES Embedding Model
Benchmark EVALUATES Reranker
Language Model COMPATIBLE_WITH Prompt Technique
Embedding Model HAS_LIMITATION Limitation
Reranker MITIGATES Problem
```

Relationship targets should use stable identifiers whenever the target is represented as an RKM entity.

Plain text may explain local context, but reusable dependencies, support claims, compatibility statements and evaluation results should be represented structurally.

---

# Claims and Evidence

Model claims often become stale as providers update hosted models, release new checkpoints, change pricing or modify access conditions.

Claims about model quality, context length, supported modalities, benchmark scores, safety behavior, latency, cost, availability or provider policy should cite evidence and references when they affect adoption or comparison.

Evidence should record the model version, evaluation date, dataset version, benchmark configuration and provider context whenever those details are available.

---

# Model vs Related Entities

Model is distinct from the entities that use, host or evaluate it.

## Model vs Provider

A Provider makes a model available.

The model is the capability being used. The provider is the source, host, maintainer or distributor.

## Model vs Framework

A Framework integrates or orchestrates models.

The framework is not the model unless the framework itself exposes a model capability that should be represented separately.

## Model vs Retriever

A Retriever performs retrieval behavior.

An embedding model may support a retriever by producing vectors, but the retriever also includes retrieval strategy, index interaction and filtering behavior.

## Model vs Benchmark

A Benchmark evaluates model behavior under a defined protocol.

A benchmark result is evidence for a claim, not a replacement for the model entity.
