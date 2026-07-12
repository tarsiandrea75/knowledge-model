# Deployment Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how deployment context is represented in the RAG Knowledge Model.

Deployment context describes where, how and under which operational constraints RAG entities are made available for use.

The Deployment Model answers the question:

> **What runtime or delivery context affects the behavior, governance, cost, reliability or reproducibility of a RAG entity or workflow?**

---

# Core Principle

Deployment context is first-class knowledge when it changes how a RAG system behaves or how claims about that system should be interpreted.

It is not only hosting metadata.

A retriever, language model, vector database, workflow or tool can have materially different latency, availability, privacy, observability, cost and compliance characteristics depending on deployment context.

```text
Framework SUPPORTS Provider
Provider PROVIDES Language Model
Workflow DEPENDS_ON Vector Database
Tool DEPLOYED_WITH Component
Workflow GOVERNED_BY Policy
Component OBSERVED_BY Evaluation Metric
```

Representing deployment context explicitly helps RKM preserve operational assumptions behind evidence, compare implementation choices and avoid treating incompatible runtime contexts as equivalent.

---

# Deployment Context

A Deployment Context describes the runtime, delivery and operational environment in which one or more RKM entities are used.

Deployment context may include:

* hosting model
* runtime environment
* provider dependency
* region or jurisdiction
* data residency constraint
* tenancy model
* network boundary
* scalability profile
* availability target
* observability coverage
* security control
* cost model
* version or release channel

Deployment context should be modeled when it affects entity selection, workflow design, evidence interpretation or governance.

Preferred:

```text
Managed vector database deployment in a specific provider region with metadata filtering, audit logging and production availability targets.
```

Avoid:

```text
Runs in the cloud.
```

The avoided statement does not identify provider dependency, operational boundary, region, controls or behavior that can be compared.

---

# Deployment Boundary

Every deployment context should define a clear boundary.

The boundary identifies:

* which entities are deployed or consumed in the context
* which provider, framework or infrastructure controls the runtime
* which data crosses the boundary
* which policies govern use
* which operational guarantees are claimed
* which evidence supports those guarantees

Deployment boundaries are especially important for RAG systems because retrieval content, embeddings, prompts, generated answers, traces and evaluation artifacts may have different governance requirements.

---

# Hosting Model

Hosting model describes how a capability is delivered.

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

The hosting model should be captured when it affects latency, control, isolation, upgrade cadence, compliance, cost or reproducibility.

For example, a self-hosted vector database and a managed vector database may expose similar APIs while having different scaling behavior, operational responsibilities and evidence requirements.

---

# Runtime Environment

Runtime environment describes the execution conditions for a deployed entity or workflow.

Important runtime characteristics include:

* programming runtime
* container or process model
* orchestration system
* hardware accelerator
* memory or storage limit
* network access
* concurrency model
* timeout behavior
* retry behavior
* release channel

Runtime details should be represented when they explain observed performance, compatibility, failure modes or operational constraints.

---

# Region, Tenancy and Data Boundary

Deployment context should preserve region, tenancy and data boundary information when those details affect governance or behavior.

Examples include:

* single-tenant deployment for regulated data
* multi-tenant managed service for shared retrieval infrastructure
* region-bound inference endpoint
* local embedding model used to avoid external data transfer
* isolated evaluation environment for benchmark reproducibility

These details should not be hidden in prose when they explain why a provider, model, database, tool or workflow is suitable for a use case.

---

# Operational Characteristics

Operational characteristics describe how deployment behaves under real use.

Important characteristics include:

* availability
* durability
* latency
* throughput
* scalability
* consistency
* recovery behavior
* indexing freshness
* version stability
* monitoring coverage
* auditability
* cost predictability

Operational claims require evidence when they compare systems, justify suitability or describe production behavior.

---

# Relationship Use

Deployment knowledge should use canonical relationships when the association has reusable graph meaning.

Useful deployment relationship patterns include:

```text
Provider PROVIDES Language Model
Provider PROVIDES Embedding Model
Provider PROVIDES Vector Database
Framework SUPPORTS Provider
Workflow DEPENDS_ON Provider
Workflow DEPENDS_ON Vector Database
Tool DEPLOYED_WITH Component
Component SECURED_BY Policy
Workflow GOVERNED_BY Policy
Component MONITORED_BY Evaluation Metric
```

Deployment relationships should express graph-ready knowledge about dependency, availability, compatibility, governance and operational context.

---

# Evidence and Claims

Deployment claims should be evidence-backed when they describe production suitability, compliance support, latency, availability, regional coverage, cost, scaling limits or security behavior.

Examples of evidence-scoped deployment claims include:

* a provider offers a model endpoint in a named region
* a workflow meets a latency target in a documented runtime environment
* a vector database deployment supports a specific availability configuration
* a tool invocation is logged by an observability component
* a local deployment avoids sending source documents to an external provider

Claims should not generalize beyond the deployment version, hosting model, provider, region, configuration, workload or observation date supported by evidence.

---

# Integration With Other Models

Deployment context connects several existing RKM models.

It connects to the Provider Model when an external or internal provider supplies hosted capabilities.

It connects to the Storage Model when vector databases, graph databases or indexes have deployment-specific behavior.

It connects to the Tool Model when callable capabilities have runtime boundaries, side effects, authorization rules or invocation constraints.

It connects to the Workflow Model when execution order, retries, routing, human approval or evaluation gates depend on deployed infrastructure.

It connects to the Policy Model when access, privacy, security, data residency, retention or cost constraints govern deployed behavior.

It connects to the Evidence Model when operational observations support claims about deployed behavior.

---

# Modeling Guidance

Model deployment context when:

* runtime placement changes system behavior
* provider dependency affects availability or governance
* region or tenancy affects data handling
* operational characteristics support a claim
* workflow reproducibility depends on configuration
* a benchmark or evaluation result depends on runtime conditions

Avoid modeling deployment context when:

* the information is a transient local setup detail
* the context does not affect reusable knowledge
* the same fact is already captured as generic metadata
* the deployment detail cannot be interpreted without evidence

Deployment knowledge should remain close to the entities and claims it explains. It should not become a separate inventory of infrastructure unless that infrastructure has reusable semantic meaning in the RAG ecosystem.
