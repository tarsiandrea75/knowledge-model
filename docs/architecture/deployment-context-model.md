# Deployment Context Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines the reusable embedded Deployment Context model in the RAG Knowledge Model.

A Deployment Context is an embedded structured description of runtime, hosting, boundary and operational conditions that affect how an RKM entity, workflow, evaluation or evidence record should be interpreted.

The broader conceptual authority for deployment knowledge is `docs/architecture/deployment-model.md`. This document narrows that architecture into schema-focused guidance for representing deployment assumptions inside another RKM object.

This embedded model answers the question:

> **Which deployment assumptions materially affect behavior, governance, reproducibility or evidence interpretation?**

---

# Core Principle

Deployment context is embedded when runtime conditions change the meaning of a claim or the behavior of a RAG capability and those conditions need structured representation within another RKM object.

Deployment Context is not a first-class knowledge entity by default. It is a reusable embedded model that can be attached to entities, workflows, evaluations, evidence records or operational knowledge when the deployment conditions need structured representation.

Deployment Context preserves the boundary around an observed or intended behavior so that RKM does not treat incompatible runtime situations as equivalent. When deployment knowledge needs its own entity-level treatment or broader conceptual explanation, use the Deployment Model instead.

---

# Scope

A Deployment Context can embed schema fields for:

* the hosting model for a capability or system
* the runtime boundary where responsibility begins and ends
* operational behavior such as availability, latency, throughput or recovery
* provider dependencies
* deployed entities whose behavior depends on the context
* data movement, residency, tenancy or access boundaries
* policy, observability, evidence, claims and references tied to deployment assumptions

Deployment Context should be embedded when those details affect selection, comparison, governance, reproducibility or claim interpretation and must travel with the object being described.

---

# Hosting Model

Hosting model describes how a capability is delivered for use.

Common hosting models include:

```text
Managed Service
Self Hosted
Serverless
Embedded
Local
Edge
Hybrid
Research Hosted
Marketplace
Other
```

The hosting model should be recorded when it affects operational responsibility, control, isolation, upgrade cadence, compliance, cost or reproducibility.

---

# Runtime Boundary

The runtime boundary identifies the execution and responsibility boundary for the deployment context.

The boundary should describe:

* the boundary type, such as model endpoint, retrieval service, workflow runtime or evaluation environment
* responsibilities inside the boundary
* dependencies outside the boundary
* runtime environments used by the deployed behavior
* release channel or stability track when it materially affects behavior

A runtime boundary should be precise enough for a reader to understand which assumptions belong to the modeled deployment context and which dependencies sit outside it.

---

# Operational Context

Operational context describes runtime properties that can affect behavior, evaluation or governance.

Important operational properties include:

* availability target
* latency profile
* throughput profile
* scalability profile
* cost model
* recovery behavior
* version stability
* configuration artifacts

Operational properties should be evidence-backed when they support comparative, production-readiness, governance or reproducibility claims.

---

# Data Boundaries

Data boundaries describe where data may move, persist or be accessed.

A data boundary may capture:

* region or locality
* jurisdiction
* tenant isolation
* network boundary
* access scope
* data residency
* provider boundary
* storage boundary

These details are important when RAG behavior depends on retrieved content, embeddings, prompts, traces, generated answers, evaluation artifacts or source documents crossing a deployment boundary.

---

# Relationship Use

Deployment Context may include first-class relationships when those relationships carry reusable graph meaning.

Useful relationship patterns include:

```text
Provider PROVIDES Language Model
Provider PROVIDES Embedding Model
Provider PROVIDES Vector Database
Workflow DEPENDS_ON Provider
Workflow DEPENDS_ON Vector Database
Tool DEPLOYED_WITH Component
Workflow GOVERNED_BY Policy
Component MONITORED_BY Evaluation Metric
```

Relationships should not duplicate generic prose. They should identify reusable semantic links between RKM entities.

---

# Evidence and Claims

Deployment Context can contain claims and evidence when deployment assumptions support or constrain a statement.

Evidence is especially important for claims about:

* regional availability
* latency or throughput
* availability targets
* data residency
* isolation or tenancy
* observability coverage
* cost behavior
* reproducibility of evaluation results

Claims should remain scoped to the hosting model, runtime boundary, provider dependency, region, workload, version, configuration and observation date supported by evidence.

---

# Modeling Guidance

Use Deployment Context when:

* runtime placement changes behavior
* provider dependency affects governance or availability
* a workflow or evaluation depends on a specific runtime boundary
* data movement or residency changes suitability
* operational measurements require deployment assumptions
* configuration artifacts affect reproducibility

Avoid Deployment Context when:

* the information is transient local setup
* the detail does not affect reusable RKM knowledge
* the same fact is already represented as ordinary metadata
* the statement cannot be interpreted or supported with useful evidence

Deployment Context should stay close to the entity, workflow, evaluation, claim or evidence record it explains. It should not become a separate infrastructure inventory unless the deployment itself becomes a first-class entity in a future schema.
