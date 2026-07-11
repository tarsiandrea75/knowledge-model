# Evaluation Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how evaluation knowledge is represented in the RAG Knowledge Model.

Evaluation knowledge explains how RAG entities are measured, compared, validated and interpreted. It connects benchmarks, datasets, evaluation metrics, claims, evidence and references into a coherent model that can support analysis, graph export and reproducible comparison.

This document answers the question:

> **How does RKM represent what was evaluated, how it was evaluated and what the result means?**

---

# Core Principle

Evaluation is first-class knowledge.

An evaluation is not only a score or leaderboard position. It is a structured assessment that depends on a target, task, dataset, metric, protocol, result, evidence and interpretation.

```text
Benchmark EVALUATES Retriever
Evaluation Metric MEASURES Grounding Quality
Benchmark USES Dataset
Evidence SUPPORTS Claim
Paper DESCRIBES Evaluation Protocol
```

Evaluation knowledge should preserve enough structure for readers and systems to understand whether a result is comparable, reproducible and relevant to a specific RAG decision.

---

# Evaluation Target

An Evaluation Target is the entity or behavior being assessed.

Common targets include:

* retrievers
* rerankers
* embedding models
* language models
* generated answers
* retrieved context
* citations
* agents
* workflows
* end-to-end RAG systems

Targets should be referenced by stable identifiers when the evaluated entity is represented in RKM.

When the evaluated target is an external system that is not yet modeled as an entity, the evaluation record should still describe the target clearly enough to preserve interpretability.

---

# Evaluation Task

An Evaluation Task defines the capability or behavior under assessment.

Examples include:

* document retrieval
* passage retrieval
* reranking
* grounded question answering
* citation faithfulness
* answer correctness
* hallucination detection
* context relevance
* agent tool use
* workflow reliability

Tasks should be narrower than broad system categories.

Preferred:

```text
Measure whether generated citations support the answer spans they are attached to.
```

Avoid:

```text
Evaluate quality.
```

The avoided statement does not identify the assessed behavior.

---

# Dataset Role

Datasets provide the evaluation material.

A dataset may provide:

* source documents
* queries
* reference answers
* relevance judgments
* citation labels
* graded preferences
* conversation traces
* tool-use traces
* safety labels

The same dataset may support different evaluation tasks depending on its splits, labels and protocol.

RKM should distinguish between the dataset as an entity and the dataset's role inside a specific benchmark or evaluation protocol.

---

# Benchmark Role

A Benchmark is a reusable evaluation package.

A benchmark may define:

* tasks
* datasets
* metrics
* scoring rules
* baselines
* leaderboards
* submission constraints
* evaluation protocol
* release version

Benchmarks should not be treated as universal measures of quality. A benchmark result is meaningful only within the benchmark's task, data, metric and protocol boundaries.

---

# Evaluation Metric Role

An Evaluation Metric defines how an evaluation observation is measured or scored.

Metrics may measure:

* retrieval quality
* ranking quality
* answer correctness
* faithfulness
* citation quality
* latency
* cost
* safety
* reliability
* user preference

Metrics should declare what they consume and what they produce when that information is known.

For example, a retrieval metric may consume ranked document identifiers and relevance judgments, while a faithfulness metric may consume a generated answer, retrieved context and a judgment procedure.

---

# Evaluation Protocol

An Evaluation Protocol defines the procedure used to produce results.

Important protocol details include:

* dataset split
* preprocessing rules
* retrieval depth
* model configuration
* prompt template
* scoring method
* aggregation method
* judge model or human annotation process
* baseline selection
* random seed policy
* version of the evaluated system

Protocol details should be explicit when they affect comparability or reproducibility.

Preferred:

```text
Retrieve 100 candidates, rerank the top 50 and report recall at 20 on the validation split.
```

Avoid:

```text
Run the retriever and report performance.
```

The avoided statement omits key evaluation conditions.

---

# Evaluation Result

An Evaluation Result is the observed output of applying a metric under a protocol to a target.

Results may include:

* scalar scores
* ranks
* categorical judgments
* pass or fail outcomes
* latency values
* cost values
* confidence intervals
* error categories
* qualitative judgments

Results should not be modeled as unsupported claims when they have measurable structure. A result can support a claim, but the result and the claim are distinct.

Example:

```text
Result: Recall at 20 is 0.83 on a named benchmark split.
Claim: The retriever improves recall for the benchmark task.
```

---

# Claims and Evidence

Evaluation results often support claims about an entity.

Claims should state the interpretation.

Evidence should identify the result, benchmark, dataset, metric, paper, report or experiment that supports the claim.

References should identify the source material where the evaluation is described or published.

This separation prevents a score from being confused with the broader conclusion drawn from that score.

---

# Comparability

Evaluation knowledge is comparable only when the relevant conditions align.

Important comparability dimensions include:

* target type
* task definition
* dataset version
* split
* metric
* protocol
* implementation constraints
* model version
* reporting date
* aggregation method

RKM should preserve these dimensions when known so downstream users can avoid comparing incompatible results.

---

# Limitations

Evaluation artifacts should record known limitations when they affect interpretation.

Common limitations include:

* benchmark contamination
* narrow domain coverage
* missing relevance judgments
* weak citation labels
* judge model bias
* incomplete baseline reporting
* stale dataset versions
* non-reproducible system settings
* mismatch between benchmark task and production use case

Limitations may be represented as structured limitation entities when they have reusable semantic value, or as local guidance when they apply only to a specific benchmark, metric or dataset.

---

# Relationship Use

Evaluation knowledge should use canonical relationships when the connection has reusable semantic meaning.

Common relationship patterns include:

```text
Benchmark EVALUATES Technique
Benchmark EVALUATES Retriever
Benchmark USES Dataset
Benchmark USES Evaluation Metric
Evaluation Metric MEASURES Retrieval Quality
Paper DESCRIBES Benchmark
Benchmark VALIDATES Technique
Technique ACHIEVES_SCORE_ON Benchmark
Dataset SUPPORTS Benchmark
```

Relationship direction should follow the relationship model and should preserve the entity that performs the semantic action.

---

# Modeling Guidance

Evaluation records should keep the following concepts separate:

* benchmark
* dataset
* metric
* protocol
* evaluated target
* result
* claim
* evidence
* reference

Avoid storing a benchmark name as a plain string when the benchmark is represented as an entity.

Avoid storing a dataset name as a plain string when the dataset is represented as an entity.

Avoid treating a metric score as a claim without recording the metric, target and evaluation context.

---

# Acceptance Criteria

Evaluation modeling is coherent when:

* the evaluated target is clear
* the task is scoped
* datasets, benchmarks and metrics remain distinct
* protocol details are present when they affect interpretation
* results are not confused with claims
* evidence links claims to evaluation sources
* references identify the source material
* relationship predicates are canonical
* limitations are represented when they affect comparison or adoption
