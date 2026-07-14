# Provider Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how providers are represented in the RAG Knowledge Model.

Providers are organizations, projects, communities or individuals that make RAG-relevant capabilities available through models, services, infrastructure, datasets, frameworks, tools, documentation or managed platforms.

The Provider Model answers the question:

> **Who makes a RAG-relevant capability available, under what access model, and with which operational or governance constraints?**

---

# Core Principle

A provider is a first-class knowledge entity when the source of a capability affects selection, trust, interoperability, availability, cost, governance or evidence interpretation.

The provider is not the same as the thing provided.

For example, a cloud vendor may provide an embedding model service, a research lab may publish a benchmark, and an open source project may maintain a framework. Each provided artifact can be modeled as its own entity when it has reusable semantic meaning.

```text
Provider PROVIDES Language Model
Provider PROVIDES Embedding Model
Provider SUPPORTS Framework
Provider IMPLEMENTS Retrieval Service
Provider DEPENDS_ON Infrastructure
```

Representing providers explicitly helps RKM distinguish capability descriptions from ownership, delivery, support, governance and operational dependency.

---

# Provider

A Provider represents a source that makes one or more RAG-relevant offerings available.

A provider may be:

* a company
* a cloud provider
* a research lab
* a foundation
* an open source project
* an academic institution
* a government organization
* a community
* an individual maintainer

The provider should be modeled when its role affects how an entity is selected, trusted, accessed, evaluated or operated.

---

# Provider as Role-Bearing Entity

Provider is the RKM entity for a RAG-relevant source role, not a generic organization directory entry.

An organization, project, community or individual should be represented as a Provider when it makes models, services, infrastructure, datasets, frameworks, tools, documentation or managed platforms available in a way that affects RAG selection, trust, access, operation, governance or evidence interpretation.

RKM should not introduce a parallel Organization entity only to describe the same source at a different label. A separate organization-like entity type should be considered only when existing architecture establishes responsibilities that are not provider responsibilities, such as authorship, institutional affiliation, ownership history or non-RAG organizational metadata that must be related independently from any provided offering.

This boundary keeps provider records focused on offerings and accountability while avoiding duplicate records for the same source.

---

# Provider Boundary

Every provider should have a clear boundary.

The boundary identifies:

* which offerings belong to the provider
* which offerings are only integrated or redistributed
* whether the provider controls hosting, support or release cadence
* which access channels are available
* which governance or compliance constraints apply
* which external systems the provider depends on

Preferred:

```text
Provider that offers managed embedding and reranking APIs with documented access controls and regional availability.
```

Avoid:

```text
AI platform.
```

The avoided statement does not identify the provider boundary, offering categories or operational responsibility.

---

# Provider Type

Provider type describes the primary organizational or operational form of the provider.

Canonical provider types include:

```text
Company
Cloud Provider
Research Lab
Foundation
Open Source Project
Academic Institution
Government Organization
Community
Individual
Other
```

Provider type should describe the source of accountability for an offering, not the technical category of the offering itself.

---

# Service Categories

Service categories describe the RAG-relevant offerings made available by the provider.

Common categories include:

* language models
* embedding models
* reranking models
* retrieval services
* vector databases
* graph databases
* RAG frameworks
* agent frameworks
* evaluation services
* datasets
* benchmarks
* developer tools
* model hosting
* inference APIs
* observability
* security

Service categories should remain broad enough to support comparison across providers while detailed capabilities are represented through relationships, claims, evidence and specialized entity schemas.

---

# Delivery Model

Delivery model describes how a provider makes an offering available.

Common delivery models include:

* managed service
* API
* SDK
* library
* open source release
* hosted platform
* self-hosted software
* marketplace listing
* research release
* documentation

The same provider may use multiple delivery models for different offerings.

Delivery model matters because it affects reproducibility, deployment control, cost, data handling, support expectations and operational risk.

---

# Access and Availability

Provider knowledge should represent access characteristics when they affect use of the offering.

Important access details include:

* public availability
* private preview status
* enterprise-only access
* research-only availability
* authentication requirements
* quota or rate limits
* pricing model
* supported regions
* discontinuation status

Access and availability fields should avoid implying that a provider endorsement is evidence of technical quality. Quality claims require claims, evidence and references.

---

# Governance

Provider governance describes policies and constraints that affect trust, safety, compliance or operational adoption.

Governance details may include:

* licensing
* data retention policy
* model usage policy
* security controls
* auditability
* compliance statements
* responsible AI documentation
* support and incident processes

Governance should be structured when it affects whether an offering is suitable for a use case, workflow, deployment environment or regulated context.

---

# Relationship Use

Providers should be connected to other entities through canonical relationships when those relationships have reusable semantic value.

Useful provider relationships include:

```text
Provider PROVIDES Language Model
Provider PROVIDES Embedding Model
Provider PROVIDES Dataset
Provider SUPPORTS Framework
Provider IMPLEMENTS Component
Provider DEPENDS_ON Infrastructure
Technique USES Provider
Framework COMPATIBLE_WITH Provider
Benchmark EVALUATES Provider
```

Provider relationships should not duplicate prose-only vendor descriptions. They should express graph-ready knowledge about availability, compatibility, implementation, support or dependency.

---

# Evidence and Claims

Provider facts often change over time.

Claims about provider availability, supported regions, pricing, service-level commitments, compliance posture, model access, benchmark results or product behavior should be linked to evidence and references when they are important to adoption decisions.

Examples of provider claims include:

* a provider offers a managed vector database service
* a provider supports a specific framework integration
* a provider exposes an embedding model through an API
* a provider's service is available in a named region
* a provider documents a specific data retention policy

Evidence should identify the source and the date-sensitive context when the claim may become stale.

---

# Provider vs Related Entities

Provider is distinct from the entities it offers or maintains.

## Provider vs Framework

A Framework is a software abstraction for building RAG systems.

A Provider may maintain, host, document or support that framework.

## Provider vs Model

A Language Model, Embedding Model or Reranker is the model capability being used.

A Provider may train, host, distribute or expose that model through an API.

## Provider vs Tool

A Tool is a bounded callable capability.

A Provider may operate the service behind the tool or publish the SDK that invokes it.

## Provider vs Dataset or Benchmark

A Dataset or Benchmark is the evaluation or data artifact.

A Provider may publish, host, curate or sponsor that artifact.

---

# Schema Representation

Provider entities are validated by `schema/provider.schema.json`.

The provider schema requires:

* identity
* metadata
* description
* provider-specific structured details

Provider-specific details should capture provider type, service categories, delivery models, supported RAG stages, access, governance, interoperability, operational characteristics, compliance, limitations and usage guidance when that information is known.

Relationships, claims, evidence, references and external links remain first-class fields outside the provider-specific detail object.
