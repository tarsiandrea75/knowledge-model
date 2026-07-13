# Observable Signal Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how observable signals are represented in the RAG Knowledge Model.

Observable signals are structured records of behavior, measurement, outcome or review captured during a RAG process. They make traces, logs, metrics, invocations, policy decisions and human review outcomes usable as knowledge rather than opaque operational data.

The Observable Signal Model answers the question:

> **What behavior was observed, in what context, with what measured values, outcome and governance constraints?**

---

# Core Principle

An observable signal is first-class structured knowledge when it explains RAG behavior, supports evaluation, qualifies a claim, preserves provenance or enables governance.

It is not only telemetry.

Observable signals connect runtime behavior to entities, artifacts, measurements, claims, evidence and references.

```text
Evidence SUPPORTS Claim
Evaluation Metric MEASURES Artifact
Workflow CONTAINS Component
Component DEPENDS_ON Provider
Tool PRODUCES Artifact
```

The signal itself may be embedded inside an entity, workflow, evaluation, evidence record or operational knowledge object. It should preserve enough structure for a reader or graph consumer to understand what was observed and why it matters.

---

# Observable Signal

An Observable Signal represents one meaningful observation of RAG system behavior.

Examples include:

* trace span for a workflow step
* log event emitted by a retrieval component
* metric sample for latency or cost
* evaluation observation for generated answer quality
* model invocation record
* tool invocation record
* retrieval observation with result count and scores
* reranking observation with candidate ordering
* citation observation with support status
* policy observation for an allow or deny decision
* failure observation for a timeout or empty retrieval result
* human review observation

Preferred:

```text
Retrieval observation for a query execution that records the retriever, workflow step, top-k setting, result count, retrieval scores, latency and failure outcome.
```

Avoid:

```text
Runtime data.
```

The avoided statement does not identify the observed behavior, context, measured values or interpretation.

---

# Signal Boundary

Every observable signal should have a clear boundary.

The boundary identifies:

* the observed behavior
* the RAG stage or execution context
* the workflow execution or workflow step when known
* the entity or entities involved
* the input artifacts consumed by the behavior
* the output artifacts produced, transformed or evaluated
* the measurements captured
* the outcome assigned to the observation
* the retention and governance constraints that apply

Signals with unclear boundaries are difficult to compare, aggregate, cite or promote to evidence.

---

# Signal Type

Signal type describes the primary semantic role of the observation.

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

The signal type should describe what was observed, not only where the observation was stored.

For example, a JSON log line that records a provider timeout should be modeled as a `Failure Observation` when the failure is the reusable semantic fact.

---

# Observation Context

Observation context describes where the signal was captured within a RAG process.

Canonical context types include:

```text
Ingestion
Parsing
Chunking
Embedding
Indexing
Query Understanding
Retrieval
Reranking
Context Assembly
Generation
Evaluation
Orchestration
Monitoring
Governance
Other
```

Observation context may also include workflow execution identifiers, workflow step identifiers, parent signal identifiers, capture timestamps and environment names.

These fields are important when a signal participates in a trace hierarchy or when an evaluation claim depends on a specific execution environment.

---

# Measurements

Measurements record values associated with an observable signal.

Common measurement types include:

* latency
* cost
* token count
* retrieval score
* reranking score
* similarity score
* quality score
* error count
* result count
* throughput

A measurement should include a unit, aggregation method or measurement window when those details affect interpretation.

Preferred:

```text
Latency measurement with value 430, unit milliseconds and aggregation Single Sample for a retrieval workflow step.
```

Avoid:

```text
Fast.
```

The avoided statement is a claim-like judgment without a measured value or context.

---

# Outcome

Outcome describes the result or interpretation of the observed behavior.

Canonical outcome types include:

```text
Success
Partial Success
Failure
Warning
Policy Allowed
Policy Denied
Human Approved
Human Rejected
Unknown
Other
```

An outcome should be modeled when the signal is used for evaluation, policy enforcement, incident review, workflow control or evidence.

Outcome reasons should be concrete enough to explain the result without replacing structured measurements, artifacts or relationships.

---

# Retention and Governance

Observable signals may contain sensitive or operationally significant data.

Retention should describe whether the signal is retained, sampled, aggregated, redacted, ephemeral, audit retained or governed by another policy.

Governance should identify constraints that apply to the signal, such as:

* privacy
* security
* compliance
* audit
* reproducibility
* incident review
* cost analysis
* model monitoring
* provider monitoring

These constraints matter because observable signals may include user queries, retrieved content, generated answers, provider metadata, evaluation judgments or policy decisions.

---

# Claims, Evidence and References

Observable signals may support claims, become evidence or cite references.

Use a claim when interpreting what a signal means.

Use evidence when the signal supports, qualifies or contradicts a claim.

Use references when the signal depends on external documentation, evaluation protocol, provider documentation, benchmark specification or audit material.

Preferred:

```text
Signal: Retrieval observation records 0 retrieved chunks for a query.
Evidence: The observation supports a failure analysis claim.
Claim: The retriever fails on the evaluated query class under the specified index configuration.
```

This keeps the observation, evidence and claim separate while preserving their connection.

---

# Relationship Use

Observable signals should use canonical RKM relationships indirectly through the entities, artifacts, evidence and claims they connect.

Common relationship patterns include:

```text
Evidence SUPPORTS Claim
Evidence REFERENCES Reference
Evaluation Metric MEASURES Artifact
Workflow CONTAINS Component
Component DEPENDS_ON Provider
Tool PRODUCES Artifact
Component TRANSFORMS Artifact
```

Do not invent observation-specific relationship predicates when the same meaning can be represented with existing canonical relationships and structured signal fields.

---

# Schema Alignment

The reusable observable signal schema is `schema/definitions/observable-signal.schema.json`.

The schema represents observable signals as embedded structured fragments rather than first-class knowledge entities. This is intentional because observable signals may appear inside workflows, evaluations, evidence records, operational knowledge and other entity documents.

A first-class observable signal entity should only be introduced if the identity model, entity type registry and relationship constraints are extended to support it coherently.

---

# Modeling Guidance

Use observable signals when observed behavior has reusable semantic value.

Do not model every raw log line as an observable signal. Prefer signals that explain behavior, support evaluation, preserve provenance, document governance or help compare RAG implementations.

Separate:

* observed behavior from claims about the behavior
* measured values from qualitative judgments
* runtime artifacts from evidence records
* execution context from metadata
* retention policy from signal content

This separation keeps RKM usable for graph export, evaluation analysis, audit review and system comparison.
