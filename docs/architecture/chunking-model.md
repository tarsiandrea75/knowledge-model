# Chunking Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how chunking strategies are represented in the RAG Knowledge Model.

Chunking strategies describe how source content is segmented into retrieval units before indexing, retrieval, context assembly and grounded generation.

The Chunking Model answers the question:

> **How should RKM represent the segmentation choices that shape retrieval quality, citation quality, context efficiency and downstream answer grounding?**

---

# Core Principle

Chunking is a first-class modeling concern when segmentation decisions materially affect retrieval or generation behavior.

A chunking strategy is not only a numeric chunk size.

It is a reusable method with boundary policies, content assumptions, configuration parameters, output artifacts, metadata propagation behavior, retrieval effects, operational tradeoffs and evidence.

```text
Chunking Strategy USES Embedding Model
Retriever DEPENDS_ON Chunking Strategy
Framework IMPLEMENTS Chunking Strategy
Benchmark EVALUATES Chunking Strategy
Evaluation Metric MEASURES Chunking Strategy
Evidence SUPPORTS Claim
```

Representing chunking explicitly allows RKM to compare segmentation approaches, preserve evaluation context and explain why retrieval behavior changes across corpora or workflows.

---

# Chunking Strategy

A Chunking Strategy is an entity that defines how source content is divided into retrievable and reusable units.

A chunking strategy may operate on:

* plain text
* Markdown
* HTML
* PDF text
* code
* tables
* transcripts
* chat conversations
* structured documents
* graph-derived content

Chunking strategy entities should describe the strategy type, chunking unit, boundary policy, supported content types, configuration, input requirements, output artifacts, metadata propagation, retrieval effects, evaluation context and operational characteristics.

Preferred:

```text
Section-based chunking that preserves heading hierarchy and source offsets for Markdown documentation.
```

Avoid:

```text
Split text into chunks.
```

The avoided statement does not identify boundary policy, input assumptions, output artifacts or retrieval impact.

---

# Strategy Type

Strategy type describes the dominant segmentation method.

Common strategy types include:

* fixed size
* recursive character
* token based
* sentence based
* paragraph based
* section based
* semantic
* structure aware
* Markdown aware
* code aware
* table aware
* hierarchical
* sliding window
* late chunking
* LLM guided
* hybrid

The strategy type should describe the reusable method, not only one implementation detail.

When a strategy combines multiple methods, the entity should identify the dominant method and use structured configuration or relationships to describe the supporting methods.

---

# Chunking Unit

The chunking unit is the primary unit used to determine chunk size or boundaries.

Important units include:

* character
* token
* word
* sentence
* paragraph
* section
* heading
* document element
* semantic segment
* code block
* table row
* table cell
* graph node

The chunking unit should be explicit because chunk size values cannot be interpreted safely without knowing what is being counted.

For example, a target size of 512 tokens and a target size of 512 characters describe very different retrieval behavior.

---

# Boundary Policy

Boundary policy defines how chunk edges are selected or preserved.

Common boundary policies include:

* fixed length
* delimiter based
* recursive separator
* natural language boundary
* structural boundary
* semantic similarity boundary
* model predicted boundary
* sliding window boundary
* hybrid boundary

Boundary policy should be represented when it affects chunk coherence, citation precision, retrieval recall, context duplication or source traceability.

A boundary policy may preserve natural document structure, ignore it intentionally or use model predictions to infer boundaries that are not explicit in the source.

---

# Configuration

Important chunking configuration should be structured when it affects reproducibility, evaluation or comparison.

Examples include:

* target chunk size
* minimum chunk size
* maximum chunk size
* overlap type
* overlap size
* overlap unit
* separator priority
* structure preservation
* attached context headers

Configuration values should be interpreted together with the strategy type, chunking unit and boundary policy.

A chunking strategy with overlap should state whether overlap is fixed, percentage based, semantic, structural or adaptive.

---

# Input Requirements

Chunking strategies may depend on preprocessing or external capabilities.

Common requirements include:

* parser
* tokenizer
* embedding model
* language model
* document structure
* metadata
* domain rules

Requirements should be modeled as structured knowledge when the strategy cannot be applied correctly without them or when they materially change quality, cost or latency.

```text
Chunking Strategy REQUIRES Component
Chunking Strategy USES Embedding Model
Chunking Strategy OPTIONALLY_USES Language Model
Component IMPLEMENTS Chunking Strategy
```

The chunking strategy remains distinct from the parser, tokenizer, model or component that implements it.

---

# Output Artifacts

Output artifacts describe what the chunking strategy produces.

Common outputs include:

* chunk
* passage
* document section
* context window
* parent chunk
* child chunk
* chunk metadata
* chunk graph

Output artifact knowledge matters when downstream retrieval, reranking, context assembly or citation behavior depends on the shape of produced units.

Important output properties include whether the strategy preserves source offsets, parent document references, section hierarchy, page numbers or access-control metadata.

---

# Metadata Propagation

Metadata propagation describes which source metadata is copied, transformed or attached to produced chunks.

Important metadata includes:

* source document identifier
* source offsets
* section hierarchy
* page numbers
* access controls
* custom metadata

Metadata propagation should be explicit when it affects filtering, authorization, citation quality, deduplication, provenance or graph export.

A chunk without source identity may still support retrieval, but it weakens evidence tracing and citation generation.

---

# Retrieval Effects

Chunking affects retrieval and context assembly by changing the units that can be embedded, indexed, scored, retrieved and cited.

Important effects include:

* recall
* precision
* grounding
* context fragmentation
* duplicate context
* citation granularity
* context-window efficiency

Claims about retrieval effects should be scoped to the corpus, retrieval depth, embedding model, retriever, reranker, benchmark, metric and evaluation protocol that support them.

```text
Chunking Strategy SUPPORTS Retriever
Chunking Strategy DEPENDS_ON Embedding Model
Benchmark EVALUATES Chunking Strategy
Evaluation Metric MEASURES Chunking Strategy
Evidence SUPPORTS Claim
```

Chunking claims should not imply universal quality improvements unless evidence supports that scope.

---

# Evaluation

Chunking evaluation should identify the task, corpus, retriever, index configuration, retrieval depth, context assembly behavior, generation model and metric.

Common evaluation metrics include:

* recall at K
* precision at K
* mean reciprocal rank
* normalized discounted cumulative gain
* hit rate
* context relevance
* faithfulness
* answer correctness
* chunk coherence
* chunk boundary quality
* latency
* cost

Evaluation should distinguish intrinsic chunk quality from end-to-end RAG quality.

Intrinsic evaluation can assess boundary quality or coherence. End-to-end evaluation can assess whether the strategy improves retrieval, grounding or answer quality in a complete workflow.

---

# Operational Characteristics

Chunking strategies have operational characteristics that affect selection and deployment.

Important characteristics include:

* implementation complexity
* preprocessing cost
* retrieval quality impact
* context efficiency impact
* domain sensitivity

A simple fixed-size strategy may be easy to implement but may fragment structured content.

A semantic or LLM-guided strategy may preserve meaning better for some corpora but can introduce higher preprocessing cost, model dependency, latency or reproducibility concerns.

Operational characteristics should be represented as claims with evidence when they influence adoption decisions.

---

# Relationship Guidance

Chunking strategy relationships should describe semantic dependencies and effects rather than implementation coincidence.

Use relationships when the connection is reusable knowledge:

```text
Framework IMPLEMENTS Chunking Strategy
Component IMPLEMENTS Chunking Strategy
Chunking Strategy REQUIRES Component
Chunking Strategy USES Embedding Model
Chunking Strategy OPTIONALLY_USES Language Model
Retriever DEPENDS_ON Chunking Strategy
Benchmark EVALUATES Chunking Strategy
Evaluation Metric MEASURES Chunking Strategy
Paper DESCRIBES Chunking Strategy
Paper INTRODUCES Chunking Strategy
```

Avoid using prose-only references for important dependencies that should participate in graph export.

---

# Modeling Boundary

Use a Chunking Strategy entity when the segmentation method is reusable across systems, frameworks, corpora or evaluations.

Use a Component entity when modeling a bounded software or architectural unit that performs chunking inside a system.

Use a Technique entity when modeling a broader retrieval or indexing method that may include chunking as one part of its approach.

Use a Benchmark or Evaluation Metric entity when the focus is how chunking quality is measured rather than how content is segmented.

This boundary keeps chunking strategies focused on segmentation semantics while still allowing relationships to implementation components, retrieval systems, papers, evidence and evaluation artifacts.
