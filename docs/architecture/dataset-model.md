# Dataset Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how datasets are represented in the RAG Knowledge Model.

Datasets are first-class knowledge entities when they provide source material, evaluation examples, training records, relevance judgments, annotations or grounding corpora that affect RAG system behavior.

The Dataset Model answers the question:

> **What data is being used, what role does it play, and what evidence is needed to interpret it correctly?**

---

# Core Principle

A dataset is not only a file, table or download link.

A dataset represents reusable data with a boundary, structure, provenance, access conditions, quality characteristics and intended use.

```text
Benchmark USES Dataset
Paper DESCRIBES Dataset
Provider PROVIDES Dataset
Retriever EVALUATED_BY Dataset
Dataset SUPPORTS Evaluation Metric
Dataset HAS_LIMITATION Limitation
```

Representing datasets explicitly helps RKM preserve the context required to compare evaluation results, reproduce benchmark claims, reason about grounding quality and identify data-related risks.

---

# Dataset

A Dataset represents a bounded collection of records used for training, fine-tuning, evaluation, benchmarking, retrieval testing or knowledge grounding.

A dataset may contain:

* source documents
* passages or chunks
* queries
* reference answers
* relevance judgments
* citations
* annotations
* conversation traces
* tool-use traces
* metadata records
* multimodal artifacts

The dataset boundary should be clear enough to distinguish the represented dataset from related versions, subsets, mirrors, derived datasets and benchmark packages.

Preferred:

```text
Question answering dataset containing queries, source documents, reference answers and supporting evidence labels.
```

Avoid:

```text
RAG data.
```

The avoided statement does not identify the dataset's contents, role or boundary.

---

# Dataset Type

Dataset type describes the primary role of the dataset.

Canonical dataset types include:

```text
Knowledge Corpus
Question Answering Dataset
Retrieval Dataset
Reranking Dataset
Embedding Dataset
Instruction Dataset
Conversation Dataset
Evaluation Dataset
Benchmark Dataset
Synthetic Dataset
Multimodal Dataset
Other
```

The dataset type should describe the dominant use of the data, not every possible downstream application.

---

# Dataset Boundary

Every dataset should define what is inside and outside the represented data collection.

The boundary should identify:

* dataset version or release
* included records and modalities
* splits
* labels or annotations
* source corpus
* preprocessing rules
* excluded data
* derived or filtered subsets
* mirrors or hosted copies

Boundary clarity matters because small changes in splits, preprocessing or annotation policy can change evaluation results and downstream claims.

---

# Structure

Dataset structure should be represented when it affects interpretation or reuse.

Common structural elements include:

* record identifiers
* document identifiers
* query fields
* answer fields
* passage or chunk fields
* relevance labels
* citation labels
* metadata fields
* split names
* language tags
* modality indicators

Important structure should not be hidden only in prose when it supports evaluation, reproducibility or graph export.

---

# Splits

Dataset splits describe named partitions of a dataset.

Common split names include:

```text
train
validation
test
dev
heldout
benchmark
```

Splits should be represented when benchmarks, papers, claims or evidence depend on them.

Example:

```text
Benchmark USES Dataset
Benchmark EVALUATES Retriever
Evidence SUPPORTS Claim
```

A claim based on a validation split should not be interpreted as a claim about the test split unless evidence supports that interpretation.

---

# Provenance

Dataset provenance explains where the data came from and how it was produced.

Important provenance details include:

* original source
* collection method
* annotation process
* synthetic generation method
* transformation or filtering process
* responsible provider or maintainer
* publication or release date
* cited paper or documentation

Provenance should be evidence-backed when it affects trust, licensing, privacy, reproducibility or interpretation.

---

# Access and Licensing

Dataset access and licensing affect whether a RAG system can legally and operationally use the data.

Access knowledge may include:

* public download availability
* hosted API access
* account requirements
* commercial restrictions
* research-only restrictions
* redistribution limits
* license identifier
* terms of use

RKM should distinguish between a dataset's technical availability and its permission to be used for a specific purpose.

---

# Quality

Dataset quality describes properties that affect reliability and suitability.

Quality characteristics may include:

* annotation quality
* label consistency
* coverage
* domain representativeness
* duplicate records
* leakage risk
* noise level
* freshness
* bias
* missing metadata

Quality claims should cite evidence when they influence selection, evaluation or trust.

Example:

```text
Claim: The dataset has human-verified relevance judgments.
Evidence: Annotation protocol described in the dataset paper.
Reference: Dataset paper or documentation.
```

---

# Privacy and Safety

Datasets may carry privacy, safety or governance risks.

Important concerns include:

* personally identifiable information
* sensitive attributes
* copyrighted material
* unsafe content
* private or confidential records
* consent constraints
* retention constraints
* regional compliance requirements

These concerns should be represented when they affect whether the dataset can be used for training, retrieval, evaluation or publication.

---

# Relationship Use

Datasets should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Benchmark USES Dataset
Provider PROVIDES Dataset
Paper DESCRIBES Dataset
Dataset REFERENCES Paper
Dataset EXTENDS Dataset
Dataset SPECIALIZES Dataset
Dataset HAS_LIMITATION Limitation
Dataset SUPPORTS Evaluation Metric
Benchmark EVALUATES Retriever
Evaluation Metric MEASURES Retrieval Quality
```

Relationship targets should use stable identifiers whenever the target is represented as an RKM entity.

Plain prose may explain local context, but reusable source, benchmark, evaluation, provenance and limitation relationships should be represented structurally.

---

# Claims and Evidence

Dataset claims should be explicit when they affect interpretation, trust or reuse.

Examples of claims that should usually cite evidence include:

* the dataset supports a specific RAG evaluation task
* labels were created by humans
* synthetic examples were generated by a named method
* a split is leakage-free
* the dataset covers a specific domain or language
* the dataset license permits commercial use
* a benchmark result depends on a specific dataset version

Evidence may come from papers, dataset cards, documentation, annotation guidelines, repository metadata, release notes, licenses or independent analyses.

---

# Dataset vs Benchmark

A Dataset provides data.

A Benchmark defines an evaluation package that may use one or more datasets, metrics, protocols and scoring rules.

Example:

```text
Benchmark USES Dataset
Benchmark EVALUATES Retriever
Evaluation Metric MEASURES Ranking Quality
```

The dataset supplies evaluation material. The benchmark defines how that material is used to produce comparable results.

---

# Dataset vs Reference

A Reference identifies a source of information.

A Dataset is the data collection being represented.

A paper can be a reference for a dataset, but the paper is not the dataset unless the dataset itself is only represented as a publication artifact.

---

# Dataset vs Evidence

Evidence supports a claim.

A dataset may be evidence when a claim depends on observations from the data, but the dataset entity should still preserve its own identity, structure, provenance and access information.

Example:

```text
Evidence SUPPORTS Claim
Dataset REFERENCES Paper
```

The evidence explains why the claim is trusted. The dataset describes the reusable data resource.

---

# Graph Export

Dataset knowledge should support graph export.

At minimum, a graph export should preserve:

* dataset identity
* dataset type
* modalities
* intended uses
* splits
* provenance
* access and license constraints
* quality and limitation claims
* relationships to benchmarks, papers, providers, models, retrievers and evaluation metrics
* evidence and references attached to dataset claims

This allows RKM consumers to ask which datasets support a benchmark, which claims depend on a dataset version and which limitations may affect a RAG evaluation result.

---

# Modeling Guidance

Model a dataset when:

* the data is reused across techniques, benchmarks, papers or tools
* evaluation claims depend on the data
* provenance, licensing, safety or quality affects use
* dataset version or split identity matters
* the dataset is cited as evidence
* the dataset is a grounding corpus for a RAG system

Do not model a dataset when a simple reference is sufficient.

Example:

```text
Paper REFERENCES Dataset Documentation
```

This may be enough when the data itself is not a reusable RKM entity.

---

# Schema Implications

The dataset schema composes the common Knowledge Entity envelope and adds dataset-specific structured knowledge.

Dataset-specific fields include:

* dataset type
* data modalities
* intended uses
* domains
* languages
* size
* splits
* structure
* access
* license
* provenance
* quality
* privacy and safety
* versioning
* known limitations
* usage guidance

The schema should preserve the separation between dataset identity, descriptive metadata, domain-specific structure, relationships, claims, evidence and references.
