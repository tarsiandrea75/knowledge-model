# Evaluation Metric Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how evaluation metrics are represented in the RAG Knowledge Model.

Evaluation metrics are first-class knowledge entities when they define reusable measurement logic for retrieval, ranking, grounding, generation, citation quality, efficiency, safety or end-to-end RAG behavior.

The Evaluation Metric Model answers the question:

> **What is being measured, what inputs are required, what output is produced and how should the result be interpreted?**

---

# Core Principle

An evaluation metric is not only a score name.

An evaluation metric defines a measurement boundary. It identifies the assessed target, required inputs, measurement scale, calculation profile, aggregation behavior, interpretation rules, limitations and evidence needed to support claims that use the metric.

```text
Evaluation Metric MEASURES Retriever
Benchmark USES Evaluation Metric
Dataset SUPPORTS Evaluation Metric
Paper DEFINES Evaluation Metric
Evidence SUPPORTS Claim
```

Representing metrics explicitly helps RKM distinguish a measurement method from a benchmark package, dataset, observed result or unsupported performance claim.

---

# Evaluation Metric

An Evaluation Metric represents a reusable method for measuring a RAG entity, artifact or behavior.

A metric may measure:

* retrieval quality
* ranking quality
* reranking quality
* generated answer correctness
* grounding quality
* faithfulness
* citation quality
* context relevance
* latency
* cost
* safety
* reliability
* task success

A metric should have a clear measurement boundary.

Preferred:

```text
Metric that measures whether retrieved passages contain evidence required to answer each query.
```

Avoid:

```text
Good retrieval score.
```

The avoided statement does not identify the target, required evidence, measurement logic or interpretation.

---

# Metric Type

Metric type describes the primary measurement category.

Canonical metric types include:

```text
Retrieval Quality
Ranking Quality
Reranking Quality
Generation Quality
Grounding Quality
Faithfulness
Citation Quality
Answer Correctness
Context Quality
Efficiency
Cost
Safety
User Experience
System Reliability
Other
```

The metric type should describe what the metric primarily measures, not every benchmark or task where it may appear.

---

# Evaluation Targets

Evaluation targets identify the entities, artifacts or behaviors the metric is intended to assess.

Common targets include:

* retrievers
* rerankers
* embedding models
* language models
* generated answers
* retrieved context
* citations
* grounding behavior
* agents
* workflows
* end-to-end RAG systems

Targets should be represented with stable entity references when the evaluated target exists in RKM.

When a metric applies to an artifact rather than a first-class entity, the artifact should still be named precisely enough to support graph export and interpretation.

---

# Required Inputs

Metrics should model required inputs structurally when those inputs affect comparability or reproducibility.

Common metric inputs include:

* query
* ranked retrieval results
* relevance judgments
* reference answer
* generated answer
* retrieved context
* citation set
* supporting passages
* judge rubric
* latency trace
* cost record
* task completion outcome

Input requirements should not be inferred only from a metric name. For example, a citation metric may require cited spans, source passages and human labels, while another citation metric may use automated source-overlap checks.

---

# Outputs and Scale

Metric outputs describe the form of the measured result.

Common output forms include:

* binary outcome
* categorical label
* ordinal judgment
* integer count
* ratio
* percentage
* probability
* scalar score
* rank
* latency value
* cost value
* textual judgment

The measurement scale should be explicit because it affects aggregation, comparison, thresholding and graph export.

When known, the metric should state whether higher values normally indicate better performance.

---

# Calculation Profile

The calculation profile describes how metric outputs are produced from inputs.

Important calculation details include:

* formula
* matching rule
* normalization rule
* threshold
* retrieval depth
* judge model or human annotation process
* treatment of missing values
* deterministic or stochastic behavior
* implementation dependency

Calculation details should be represented when they materially affect whether two reported scores are comparable.

Preferred:

```text
Recall at 20 computed from ranked passage identifiers and binary relevance judgments.
```

Avoid:

```text
Recall.
```

The avoided statement omits the cutoff and required judgment structure.

---

# Aggregation

Aggregation describes how per-example measurements become dataset-level, benchmark-level or system-level results.

Aggregation knowledge may include:

* mean
* median
* weighted mean
* macro average
* micro average
* percentile
* pass rate
* confidence interval
* stratified reporting
* leaderboard ranking

Aggregation should be explicit when claims compare systems, techniques, models or providers.

---

# Interpretation

Metric interpretation explains what a score means and what it does not mean.

Interpretation knowledge may include:

* preferred score direction
* acceptable threshold
* known ceiling effects
* sensitivity to dataset construction
* sensitivity to prompt or model settings
* relationship to user-visible quality
* failure modes not captured by the metric

A high retrieval score does not automatically imply answer faithfulness. A high answer correctness score does not automatically imply citation quality. RKM should preserve these distinctions through metric targets, claims, evidence and relationships.

---

# Relationship Use

Evaluation metrics should use canonical relationships when the relationship has reusable semantic value.

Common relationships include:

```text
Benchmark USES Evaluation Metric
Evaluation Metric MEASURES Retriever
Evaluation Metric MEASURES Generated Answer
Dataset SUPPORTS Evaluation Metric
Paper DEFINES Evaluation Metric
Paper DESCRIBES Evaluation Metric
Evidence SUPPORTS Claim
```

Use relationships for graph-relevant links. Use metric fields for intrinsic measurement details such as input requirements, scale, calculation and aggregation.

---

# Evidence and Claims

Claims about metrics should be evidence-backed when they affect interpretation, adoption or comparison.

Examples of evidence-backed claims include:

* a metric correlates with human preference in a named evaluation setting
* a metric is sensitive to retrieval depth
* a metric requires relevance judgments
* a metric is unreliable for long-context answers
* a metric is commonly used by a named benchmark

The metric entity should not embed unsupported generalizations as facts. Claims should remain separate from evidence, references and observed benchmark results.

---

# Boundary With Related Models

An Evaluation Metric is different from a Benchmark.

A benchmark defines an evaluation package, including tasks, datasets, metrics and protocol. A metric defines the measurement method used within or outside a benchmark.

An Evaluation Metric is different from a Dataset.

A dataset provides records, labels or source material. A metric defines how those materials are scored or judged.

An Evaluation Metric is different from Evidence.

Evidence records support claims about a metric or results produced with a metric. The metric itself defines the reusable measurement concept.

An Evaluation Metric is different from a Claim.

A claim may assert that a metric is appropriate, limited or predictive. The metric provides the structured measurement context that makes such claims interpretable.

---

# Modeling Guidance

Create an Evaluation Metric entity when:

* the metric is reused across benchmarks, papers, systems or tools
* the metric has distinct input requirements or interpretation rules
* the metric supports claims about retrieval, grounding, generation, safety, cost or reliability
* the metric affects comparability between RAG entities
* the metric should appear as a graph node

Do not create a separate metric entity for a one-off score label when the measurement method is not reusable or distinguishable from a benchmark-specific reporting field.

Metric records should preserve enough structure for a reader or consumer to decide whether a result is comparable, reproducible and relevant to a RAG decision.
