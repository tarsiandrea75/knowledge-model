# Benchmark Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how benchmarks are represented in the RAG Knowledge Model.

Benchmarks are reusable evaluation packages that define tasks, datasets, metrics, protocols and reporting boundaries for assessing RAG entities or RAG system behavior.

The Benchmark Model answers the question:

> **What evaluation package is being used, what does it measure, and what context is required to interpret its results correctly?**

---

# Core Principle

A benchmark is first-class knowledge when it provides a reusable evaluation context.

It is not only a leaderboard, score table or dataset name.

A benchmark connects evaluated entities, datasets, metrics, protocols, claims, evidence and references into a structured evaluation context.

```text
Benchmark EVALUATES Retriever
Benchmark USES Dataset
Benchmark USES Evaluation Metric
Benchmark DEFINES Evaluation Protocol
Paper DESCRIBES Benchmark
Evidence SUPPORTS Claim
```

Representing benchmarks explicitly helps RKM preserve the conditions under which results are meaningful, comparable and reproducible.

---

# Benchmark

A Benchmark represents a named evaluation package used to assess one or more RAG capabilities.

A benchmark may evaluate:

* retrieval quality
* reranking quality
* embedding behavior
* grounded question answering
* citation quality
* answer faithfulness
* hallucination resistance
* long-context reasoning
* agent task completion
* end-to-end RAG system behavior

A benchmark should have a clear evaluation boundary.

Preferred:

```text
Benchmark that evaluates passage retrieval and grounded answer generation over a fixed question answering dataset with published metrics and protocol.
```

Avoid:

```text
RAG score.
```

The avoided statement does not identify the task, data, metric, protocol or evaluated behavior.

---

# Benchmark Type

Benchmark type describes the primary evaluation package represented by the benchmark.

Canonical benchmark types include:

```text
Retrieval Benchmark
RAG Benchmark
Question Answering Benchmark
Embedding Benchmark
Reranking Benchmark
Long Context Benchmark
Hallucination Benchmark
Grounded Generation Benchmark
Agent Benchmark
System Benchmark
Other
```

The benchmark type should describe the dominant evaluation purpose, not every metric or dataset included in the benchmark.

---

# Evaluation Scope

Evaluation scope identifies the RAG capabilities or lifecycle stages assessed by the benchmark.

Common scopes include:

* ingestion
* chunking
* embedding
* indexing
* query understanding
* retrieval
* reranking
* context assembly
* generation
* grounding
* citation
* faithfulness
* orchestration
* end-to-end system behavior

Scope should be explicit because a benchmark for retrieval quality does not automatically evaluate answer correctness, and a benchmark for generated answers does not automatically evaluate index quality.

---

# Tasks

A benchmark task defines the behavior being evaluated.

Examples include:

* passage retrieval
* document retrieval
* question answering
* multi-hop question answering
* answer generation
* citation generation
* claim verification
* summarization
* reranking
* embedding evaluation
* agent task execution

Tasks should be narrower than broad system categories.

Preferred:

```text
Retrieve passages that support a reference answer for each query.
```

Avoid:

```text
Evaluate the model.
```

The avoided statement does not identify the behavior under assessment.

---

# Dataset Use

Benchmarks use datasets, but a benchmark is not the same thing as a dataset.

A dataset provides records, labels, source documents, queries or annotations. A benchmark defines how those materials are used for evaluation.

Benchmark dataset use should identify:

* dataset identifier or name
* dataset version or release
* split
* source documents
* queries
* reference answers
* relevance judgments
* citation labels
* preprocessing rules

When the same dataset supports multiple benchmarks, each benchmark should still preserve its own task, metric and protocol context.

---

# Metrics

Benchmarks report one or more evaluation metrics.

Metrics may measure:

* recall
* precision
* ranking quality
* answer correctness
* faithfulness
* citation quality
* latency
* cost
* safety
* reliability
* task success

RKM should distinguish between the benchmark, the metric entity and the observed result.

Example:

```text
Benchmark USES Evaluation Metric
Evaluation Metric MEASURES Retrieval Quality
Evidence SUPPORTS Claim
```

A metric explains how something is measured. A benchmark explains the evaluation package that applies metrics under a protocol.

---

# Evaluation Protocol

The evaluation protocol defines the procedure used to produce benchmark results.

Important protocol details include:

* dataset split
* preprocessing rules
* retrieval depth
* reranking depth
* prompt template
* model configuration
* judge model or human annotation process
* aggregation method
* scoring script
* baseline selection
* submission constraints
* random seed policy
* reporting date

Protocol details should be represented when they affect comparability, reproducibility or interpretation.

Preferred:

```text
Retrieve 100 candidates, rerank the top 50, and report recall at 20 on the test split.
```

Avoid:

```text
Run the benchmark normally.
```

The avoided statement hides evaluation conditions that may change the result.

---

# Leaderboards and Results

A leaderboard is an optional reporting surface for benchmark results.

RKM should avoid treating a leaderboard rank as a universal quality statement. Rank depends on the benchmark version, task, metric, submission rules, evaluated system version and reporting date.

Benchmark results may support claims, but the result and the claim are distinct.

Example:

```text
Result: A retriever reports recall at 20 of 0.83 on a named benchmark split.
Claim: The retriever improves recall for that benchmark task under the reported protocol.
Evidence: Benchmark result record or paper table.
```

This separation preserves both the measured observation and the interpretation.

---

# Baselines

Baselines provide comparison points inside a benchmark.

Baselines may be:

* models
* retrievers
* rerankers
* frameworks
* components
* agents
* complete RAG systems
* heuristic methods

Baseline descriptions should include version, configuration and evaluation protocol context when known.

Comparing against an unspecified baseline weakens the claim because readers cannot determine what changed or whether the comparison is reproducible.

---

# Release and Versioning

Benchmarks may change over time.

Important versioning details include:

* benchmark release
* dataset release
* metric version
* scoring script version
* leaderboard snapshot date
* task additions or removals
* annotation updates
* protocol changes

RKM should preserve benchmark version context when claims or evidence depend on a particular release.

---

# Limitations

Benchmarks have limitations that affect interpretation.

Common limitations include:

* narrow domain coverage
* synthetic data artifacts
* stale source material
* incomplete relevance judgments
* metric blind spots
* leaderboard overfitting
* weak reproducibility
* unclear baseline configuration
* missing cost or latency measurement
* mismatch with production use cases

Limitations should be represented explicitly when they affect selection, comparison or trust.

---

# Relationship Use

Benchmarks should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Benchmark EVALUATES Retriever
Benchmark EVALUATES Reranker
Benchmark EVALUATES Agent
Benchmark USES Dataset
Benchmark USES Evaluation Metric
Benchmark DEFINES Evaluation Protocol
Benchmark REFERENCES Reference
Paper DESCRIBES Benchmark
Technique BENCHMARKED_BY Benchmark
Evidence SUPPORTS Claim
```

Relationship targets should use stable identifiers whenever the target concept is represented as an RKM entity.

Plain prose may describe benchmark context, but reusable evaluation, dataset, metric, protocol and evidence relationships should be represented structurally.

---

# Benchmark vs Dataset

A dataset is a bounded collection of records.

A benchmark is an evaluation package that uses data under a task, metric and protocol.

Example:

```text
Dataset: Questions, source documents and reference answers.
Benchmark: Retrieval and grounded answer evaluation that uses those records with specified metrics and scoring rules.
```

The same dataset can support multiple benchmarks, and the same benchmark can use multiple datasets.

---

# Benchmark vs Evaluation Metric

An evaluation metric defines how a behavior or artifact is measured.

A benchmark defines the package that applies metrics to tasks and datasets.

Example:

```text
Evaluation Metric: Recall at 20.
Benchmark: Passage retrieval evaluation that reports recall at 20 over a named split with a fixed protocol.
```

RKM should avoid storing metric meaning only inside benchmark prose when the metric has reusable semantic value.

---

# Claims and Evidence

Claims about benchmarks or benchmark results should be evidence-backed when they affect selection, comparison or trust.

Examples of benchmark claims include:

* a benchmark evaluates citation faithfulness
* a benchmark uses human-verified relevance judgments
* a benchmark result shows improved retrieval recall
* a benchmark leaderboard compares systems under a fixed submission protocol
* a benchmark has limited coverage for production enterprise search

Evidence should identify the benchmark release, dataset version, metric, protocol, evaluated target and source reference when that information is available.

References should identify papers, documentation, benchmark cards, source repositories, scoring scripts or leaderboard pages that define the benchmark.
