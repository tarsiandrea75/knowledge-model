# Reranker Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how rerankers are represented in the RAG Knowledge Model.

Rerankers are entities that reorder, filter or score retrieved candidates after an initial retrieval step and before candidates are used for context assembly, citation selection, answer generation or evaluation.

The Reranker Model answers the question:

> **How should RKM describe reranking capabilities that change the order, relevance or usefulness of retrieved candidates in a RAG system?**

---

# Core Principle

A reranker is not only a model name or an implementation detail inside a retriever.

A reranker is a reusable capability with a defined candidate input shape, scoring approach, output structure, model profile, deployment profile, operational impact and evaluation context.

```text
Retriever OPTIONALLY_USES Reranker
Reranker USES Language Model
Reranker REQUIRES Retrieved Candidates
Benchmark EVALUATES Reranker
Evaluation Metric MEASURES Reranker
Provider PROVIDES Reranker
```

Representing rerankers explicitly allows RKM to describe ranking quality, latency, cost, citation utility, context selection behavior and evidence-supported tradeoffs separately from first-stage retrieval.

---

# Reranker

A Reranker is an entity that receives candidate artifacts and returns an ordered, scored or filtered candidate set.

Candidate artifacts may include:

* passages
* documents
* chunks
* graph nodes
* search results
* citation candidates
* generated answers

Reranker entities should identify what they accept, how they score candidates, what they return, which RAG stages they affect and which evaluation evidence supports claims about their behavior.

Preferred:

```text
Cross encoder reranker that scores query and passage pairs, reorders the top retrieved passages and improves precision before context assembly.
```

Avoid:

```text
Better ranking layer.
```

The avoided statement does not identify the reranking method, input candidates, scoring behavior or downstream effect.

---

# Reranker Boundary

Every reranker should have a clear boundary.

The boundary identifies:

* whether the entity represents a standalone reranking model, a rank-fusion method, an LLM-based judge or a rule-based scorer
* which candidate artifacts it consumes
* whether a query, metadata, retrieved scores or full candidate content are required
* whether the output is a score, rank, filtered set, explanation or structured judgment
* which retriever or retrieval stage supplies the candidates when known
* which workflow step consumes the reranked output

A reranker should not be collapsed into the retriever that produces its input candidates unless the documented capability is intentionally modeled as a combined retrieval capability.

---

# Reranker Type

Reranker type describes the primary ranking method.

Canonical reranker types include:

```text
Cross Encoder
Bi Encoder Reranker
Sparse Reranker
LLM Based Reranker
Learning To Rank
Hybrid Reranker
Rule Based Reranker
Reciprocal Rank Fusion
Domain Specific Reranker
Other
```

The type should describe the dominant reranking approach. More specific knowledge should be represented through scoring approach, candidate inputs, outputs, model profile, relationships, claims and evidence.

---

# Scoring Approach

Scoring approach describes how a reranker assigns relevance, utility or priority to candidates.

Common scoring approaches include:

* pairwise query and candidate scoring
* listwise candidate scoring
* pointwise candidate scoring
* rank fusion
* heuristic scoring
* generative relevance judging

Scoring details matter because rerankers can optimize for different objectives, including semantic relevance, lexical relevance, answer support, citation quality, diversity, freshness or domain-specific utility.

When a reranker combines first-stage retrieval scores with new scores, the combination method should be described when it affects reproducibility or evaluation interpretation.

---

# Candidate Inputs

Candidate inputs describe the artifacts a reranker can reorder or filter.

Important candidate input knowledge includes:

* artifact type
* input modality
* whether the original query is required
* whether candidate text, metadata, embeddings or prior scores are required
* candidate depth supplied by the first-stage retriever
* maximum candidate length or context requirements

Candidate inputs should be structured when they affect portability across retrievers, vector databases, graph databases, frameworks or workflows.

---

# Output

Reranker output describes what the downstream RAG system receives.

Common outputs include:

* ordered candidates
* relevance scores
* normalized scores
* filtered candidate sets
* relevance labels
* ranking explanations
* selected citation candidates

Output structure should be explicit when another component, workflow step, evaluation metric or citation process depends on it.

For example, a context assembler may require ordered passages, while a citation workflow may require candidate-level evidence labels.

---

# Model Profile

Some rerankers are model-backed.

Important model profile knowledge includes:

* whether the reranker uses a language model, embedding model or specialized ranking model
* supported modalities
* context length limits
* instruction-following requirements
* open-weight or hosted access mode
* provider-managed versioning
* deterministic or stochastic scoring behavior

Model-backed rerankers should be connected to relevant model or provider entities when those relationships affect availability, reproducibility, governance or evaluation interpretation.

---

# Operational Characteristics

Rerankers often improve ranking quality by adding latency, cost or deployment complexity.

Operational characteristics may include:

* latency impact
* cost impact
* quality impact
* throughput sensitivity
* context length sensitivity
* batching behavior
* deployment requirements

These characteristics should be represented when they affect system design, framework compatibility, production use, benchmark interpretation or use-case suitability.

---

# Evaluation

Reranker evaluation should distinguish reranking behavior from first-stage retrieval behavior.

An evaluation should identify:

* first-stage retriever or candidate source
* candidate depth before reranking
* reranked depth after reranking
* dataset or benchmark
* evaluation metric
* protocol
* result
* configuration
* evidence

Example:

```text
Benchmark EVALUATES Reranker
Evaluation Metric MEASURES Reranker
Evidence SUPPORTS Claim
```

Claims about reranker quality should not be generalized beyond the retrieval setup, candidate depth, dataset, metric, model version, prompt configuration or evaluation date supported by evidence.

---

# Relationship Use

Rerankers should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Retriever OPTIONALLY_USES Reranker
Technique USES Reranker
Framework SUPPORTS Reranker
Provider PROVIDES Reranker
Reranker USES Language Model
Reranker DEPENDS_ON Embedding Model
Benchmark EVALUATES Reranker
Evaluation Metric MEASURES Reranker
Paper INTRODUCES Reranker
```

Relationships should describe graph-ready knowledge rather than restating prose. When a relationship depends on a specific configuration or benchmark result, the relationship should be supported by claims, evidence and references.

---

# Reranker Records

A complete reranker record should include:

* identity
* metadata
* description
* reranker type
* scoring approach
* input modalities
* candidate inputs
* output structure
* RAG stages
* capabilities
* model profile when applicable
* deployment profile when known
* evaluation profile when available
* operational characteristics
* limitations
* usage guidance
* relationships
* claims
* evidence
* references

The reranker-specific section should contain structured reranker knowledge. Provenance, lifecycle, authorship and review state belong in metadata. Source materials belong in references. Assertions about behavior belong in claims and should be connected to evidence.
