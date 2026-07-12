# Observability Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how observability is represented in the RAG Knowledge Model.

Observability covers the traces, logs, metrics, evaluations and operational signals used to understand how a RAG system behaves during ingestion, retrieval, generation, evaluation and deployment.

The Observability Model answers the question:

> **What should be recorded, measured or linked so RAG behavior can be inspected, evaluated, debugged and governed?**

---

# Core Principle

Observability is first-class knowledge when it explains behavior, supports claims, validates evaluation results or provides audit evidence.

It is not only operational telemetry.

Observable signals connect workflows, components, models, tools, providers, artifacts, policies, evaluation metrics, claims and evidence into a reproducible account of system behavior.

```text
Workflow OBSERVED_BY Component
Component LOGGED_BY Tool
Provider MONITORED_BY Tool
Evaluation Metric MEASURES Artifact
Evidence SUPPORTS Claim
```

Representing observability explicitly helps RKM consumers compare implementations, diagnose failures, evaluate quality and preserve provenance.

---

# Observable Signal

An observable signal is a structured record that describes behavior observed during a RAG process.

Common observable signals include:

* trace span
* log event
* metric sample
* retrieval score
* reranking score
* generated answer quality score
* citation verification result
* model invocation record
* tool invocation record
* provider latency measurement
* cost measurement
* policy decision
* human review outcome

Observable signals should be modeled when they have reusable semantic meaning for evaluation, debugging, governance, reproducibility or evidence.

Preferred:

```text
Retrieval trace recording query text, retriever identifier, top-k value, retrieved chunk identifiers, scores and latency.
```

Avoid:

```text
Debug data.
```

The avoided statement does not identify the observed behavior, structure or use of the signal.

---

# Observation Boundary

Every observation should have a clear boundary.

The boundary identifies:

* what behavior was observed
* which workflow, component, model, provider or tool produced the behavior
* when the observation was captured
* which input and output artifacts were involved
* which metric, policy or evaluation context gives the observation meaning
* whether the observation is transient, retained or used as evidence

Observations with unclear boundaries are difficult to compare, reproduce or cite.

---

# Signal Type

Signal type describes the primary semantic role of an observation.

Canonical signal types include:

```text
Trace Span
Log Event
Metric Sample
Evaluation Observation
Model Invocation
Tool Invocation
Retrieval Observation
Reranking Observation
Generation Observation
Citation Observation
Policy Observation
Cost Observation
Latency Observation
Failure Observation
Human Review Observation
Other
```

The signal type should describe what was observed, not only where the signal is stored.

---

# Trace

A trace represents an ordered record of related observations for one execution of a workflow or workflow step.

Trace structure should preserve:

* workflow identifier
* execution identifier
* step identifier
* parent-child span relationships
* start and end times
* participating entities
* consumed artifacts
* produced artifacts
* errors or warnings
* evaluation observations
* policy observations

Trace records are especially important when a claim depends on execution behavior rather than static documentation.

---

# Metric Observation

A metric observation records a measured value in a defined context.

Important fields include:

* metric name or evaluation metric identifier
* measured entity or artifact
* value
* unit
* measurement window
* aggregation method
* dataset or benchmark context
* threshold or policy expectation
* evidence reference

Metric observations should avoid ambiguous values without units, context or measurement scope.

---

# Failure Observation

A failure observation records behavior that prevents, degrades or invalidates a RAG process.

Common failure observations include:

* empty retrieval result
* low retrieval confidence
* citation mismatch
* source access failure
* provider timeout
* rate limit response
* context overflow
* policy violation
* evaluation threshold failure
* hallucinated unsupported answer

Failure observations should identify the failed step, affected artifacts, suspected cause and downstream impact when known.

---

# Retention and Governance

Observability records may contain user input, retrieved content, generated text, source identifiers, provider metadata or sensitive operational details.

Retention and governance should be explicit when observations affect:

* privacy
* security
* compliance
* auditability
* reproducibility
* cost analysis
* incident review
* model or provider comparison

Policies should define whether a signal is stored, redacted, aggregated, sampled, deleted or promoted to evidence.

---

# Relationship Use

Observability should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Workflow OBSERVED_BY Component
Component OBSERVED_BY Tool
Provider MONITORED_BY Tool
Component LOGGED_BY Tool
Evaluation Metric MEASURES Artifact
Evidence SUPPORTS Claim
Evidence REFERENCES Reference
Policy GOVERNED_BY Reference
```

Relationship targets should use stable identifiers whenever the target concept is represented as an RKM entity.

Plain prose may explain local instrumentation behavior, but reusable observation, monitoring, logging, evidence and policy relationships should be represented structurally.

---

# Observability vs Evidence

Observability records describe what was observed.

Evidence records explain why a claim is supported, contradicted or qualified.

An observation becomes evidence when it is selected, contextualized and linked to a claim or evaluation result.

For example, a trace showing retrieved chunk identifiers and citation verification results is an observability record. The same trace may become evidence for a claim that a workflow preserves citation provenance when it is linked through an evidence object.

---

# Observability vs Metadata

Metadata describes the RKM document.

Observability describes runtime, evaluation or operational behavior of the represented RAG concept.

For example, `metadata.updatedAt` records when an RKM file changed. A latency observation records how long a retriever took during a benchmark or workflow execution.
