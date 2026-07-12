# Framework Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how frameworks are represented in the RAG Knowledge Model.

Frameworks are software abstractions, libraries, SDKs, runtimes or platforms that help build, compose, operate or evaluate RAG systems.

The Framework Model answers the question:

> **What software framework supports RAG work, and how should its capabilities, integrations, deployment targets and governance be represented?**

---

# Core Principle

A framework is a first-class knowledge entity when it provides reusable structure for building or operating RAG systems.

It is not only a package name, repository name, vendor label or implementation detail.

A framework may provide abstractions for ingestion, chunking, embedding, retrieval, reranking, context assembly, generation, evaluation, orchestration, monitoring or agent workflows.

```text
Framework IMPLEMENTS Technique
Framework PROVIDES Component
Framework INTEGRATES_WITH Vector Database
Framework COMPATIBLE_WITH Language Model
Provider SUPPORTS Framework
```

Framework entities help RKM compare development approaches, supported RAG stages, ecosystem maturity, integration surface, deployment constraints and operational tradeoffs.

---

# Framework

A Framework represents a reusable software layer for constructing or operating RAG systems.

A framework may be:

* a RAG application framework
* an agent framework
* an LLM orchestration framework
* an evaluation framework
* a data pipeline framework
* a vector search framework
* a Graph RAG framework
* a serving framework
* an integration framework
* a managed platform with framework-like abstractions

A framework should be modeled when its abstractions, integrations or runtime behavior affect how a RAG system is designed, implemented, evaluated or operated.

Preferred:

```text
RAG framework that provides document loading, chunking, retriever composition, prompt construction and model integration abstractions for Python applications.
```

Avoid:

```text
Python library.
```

The avoided statement does not identify the RAG role, abstraction boundary or supported capabilities.

---

# Framework Boundary

Every framework should define what is inside and outside the framework boundary.

The boundary should identify:

* primary abstractions exposed by the framework
* supported RAG stages
* official implementation languages or SDKs
* native integrations and adapter-based integrations
* deployment targets supported by the framework
* runtime responsibilities handled by the framework
* governance, maintenance and licensing facts

Clear boundaries prevent framework entities from becoming broad summaries of an ecosystem, provider or application.

---

# Framework Type

Framework type describes the primary role of the framework in the RAG ecosystem.

Canonical framework types include:

```text
Application Framework
RAG Framework
Agent Framework
LLM Orchestration Framework
Evaluation Framework
Data Pipeline Framework
Vector Search Framework
Graph RAG Framework
Serving Framework
Integration Framework
Other
```

The framework type should describe the dominant role of the framework. Additional capabilities should be represented through supported stages, integration capabilities, relationships, claims and evidence.

---

# Implementation Language

Implementation language identifies the programming languages directly supported by the framework implementation or official SDKs.

Implementation language should distinguish official support from community support when that distinction affects adoption, compatibility or maintenance risk.

Examples include:

* Python
* Java
* JavaScript
* TypeScript
* Go
* Rust
* C#
* Kotlin
* Scala

Language support should not be inferred from unofficial examples unless there is evidence that the framework maintains that language surface.

---

# Delivery Model

Delivery model describes how the framework is consumed.

Common delivery models include:

* library
* SDK
* service
* CLI
* server
* cloud platform
* local runtime
* plugin

Delivery model matters because it affects deployment control, reproducibility, governance, observability, cost and operational ownership.

For example, a library framework and a managed cloud platform may expose similar RAG abstractions while creating different operational dependencies.

---

# Supported RAG Stages

Frameworks should identify the RAG pipeline stages they directly support.

Common supported stages include:

* ingestion
* chunking
* embedding
* indexing
* query understanding
* retrieval
* reranking
* context assembly
* generation
* evaluation
* orchestration
* monitoring

Stage support should describe capabilities the framework directly exposes, not every stage that a user could implement manually on top of it.

---

# Integration Capabilities

Integration capabilities describe the kinds of external or internal capabilities the framework can connect to.

Examples include:

* embedding model integrations
* language model integrations
* retriever integrations
* reranker integrations
* vector database integrations
* graph database integrations
* document loader integrations
* chunking strategy integrations
* prompt template integrations
* tool calling integrations
* agent workflow integrations
* evaluation metric integrations
* observability integrations
* caching integrations

Integration capabilities should identify whether support is native, plugin-based, adapter-based, community-maintained, external or unknown.

Important integrations should also be represented as relationships when the target entity is modeled in RKM.

---

# Deployment Targets

Deployment targets describe where the framework is intended or commonly used to run.

Deployment targets may include:

* local development
* server deployment
* container deployment
* Kubernetes deployment
* serverless deployment
* cloud deployment
* edge deployment
* browser deployment
* mobile deployment

Deployment knowledge should be represented when it affects framework selection, runtime constraints, data governance, latency, cost or operational support.

---

# Operational Characteristics

Frameworks often differ by operational characteristics that affect adoption and production use.

Relevant characteristics include:

* learning curve
* configuration complexity
* production readiness
* ecosystem maturity
* observability support
* integration stability
* release cadence
* debugging support

Operational characteristics should be linked to claims and evidence when they influence selection or comparison.

For example, a framework may reduce orchestration complexity while increasing dependency surface or runtime opacity.

---

# Governance

Framework governance describes ownership, maintenance and project-level constraints.

Important governance facts include:

* maintainer type
* maintainer name
* license
* homepage
* repository
* documentation
* project status
* release and support expectations

Governance should be modeled separately from technical capability. A framework can have strong RAG abstractions while also carrying maintenance, licensing or provider-dependency considerations.

---

# Relationship Use

Frameworks should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Framework IMPLEMENTS Technique
Framework PROVIDES Component
Framework IMPLEMENTS Workflow
Framework PROVIDES Tool
Framework INTEGRATES_WITH Vector Database
Framework INTEGRATES_WITH Graph Database
Framework COMPATIBLE_WITH Language Model
Framework COMPATIBLE_WITH Embedding Model
Framework DEPENDS_ON Provider
Provider SUPPORTS Framework
Benchmark EVALUATES Framework
Paper DESCRIBES Framework
```

Relationship targets should use stable identifiers whenever the target entity is represented in RKM.

Plain prose may describe framework behavior, but reusable implementation, compatibility, integration, evaluation and provider knowledge should be represented structurally.

---

# Evidence and Claims

Claims about frameworks should be scoped to the framework version, configuration and integration context when those details affect correctness.

Examples of framework claims include:

* a framework supports a specific RAG pipeline stage
* a framework integrates with a specific vector database
* a framework implements a named RAG technique
* a framework supports tool calling or agent workflows
* a framework improves development velocity for a class of RAG applications
* a framework introduces operational complexity through additional runtime dependencies

Evidence should identify the source, date, framework version and configuration when those details may change over time.

---

# Framework vs Related Entities

Framework is distinct from the entities it supports, integrates with or depends on.

## Framework vs Component

A Component is a bounded functional building block in a RAG architecture.

A Framework may provide, compose or configure components, but the framework is not the same as each component it exposes.

## Framework vs Technique

A Technique is a method or approach used in RAG systems.

A Framework may implement or support a technique, but the technique remains independently meaningful.

## Framework vs Provider

A Provider is the organization, project, community or person that makes a capability available.

A Provider may maintain or distribute a framework, but provider facts should not be folded into framework capability descriptions.

## Framework vs Tool

A Tool is a bounded callable capability.

A Framework may expose tools, call tools or integrate with tool runtimes, but a framework is broader than a single callable boundary.
