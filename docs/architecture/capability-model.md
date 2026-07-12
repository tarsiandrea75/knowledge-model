# Capability Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how capabilities are represented in the RAG Knowledge Model.

Capabilities describe what an entity can do, provide, expose or support in a RAG system.

The Capability Model answers the question:

> **What reusable function or behavior is made available by a RAG entity, and how should that capability be described, bounded and evidenced?**

---

# Core Principle

A capability is first-class knowledge when it has reusable semantic meaning for selecting, comparing, composing, evaluating or governing RAG entities.

It is not only a marketing phrase, tag or implementation detail.

A capability may be provided by a provider, exposed by a tool, implemented by a component, supported by a framework, used by an agent or required by a workflow.

```text
Provider PROVIDES Capability
Tool EXPOSES Capability
Component IMPLEMENTS Capability
Framework SUPPORTS Capability
Agent USES Capability
Workflow REQUIRES Capability
```

Capabilities make it possible to compare entities by behavior without conflating the behavior with the entity that delivers it.

---

# Capability

A Capability represents a bounded function, behavior or serviceable ability that matters in a RAG context.

Examples include:

* semantic retrieval
* hybrid retrieval
* metadata filtering
* query rewriting
* document chunking
* embedding generation
* reranking
* context assembly
* citation generation
* answer faithfulness evaluation
* trace logging
* human approval

A capability should describe what can be done, not who does it or how it is branded.

Preferred:

```text
Rerank retrieved candidates by estimated relevance to the user query.
```

Avoid:

```text
Smart search.
```

The avoided statement does not define the capability boundary, input, output or evaluation basis.

---

# Capability Boundary

Every capability should have a clear boundary.

The boundary identifies:

* the behavior made available
* the expected input artifacts
* the expected output artifacts
* the entity or entities that provide, expose, implement or support it
* the RAG stages where it applies
* the conditions or constraints under which it is available
* the evidence needed to support capability claims

Capability boundaries prevent broad product or framework descriptions from becoming vague lists of features.

---

# Capability Type

Capability type describes the primary behavior represented by the capability.

Canonical capability types include:

```text
Retrieval Capability
Ranking Capability
Embedding Capability
Chunking Capability
Parsing Capability
Generation Capability
Evaluation Capability
Routing Capability
Transformation Capability
Storage Capability
Orchestration Capability
Monitoring Capability
Governance Capability
Security Capability
Operational Capability
Other
```

The capability type should describe the dominant behavior, not every entity that may participate in delivering it.

---

# Capability Scope

Capability scope describes where and how the capability applies.

Common scope dimensions include:

* RAG stage
* supported artifact types
* supported input modalities
* deployment model
* access model
* provider dependency
* framework integration
* runtime environment
* evaluation context
* governance constraints

Scope should be explicit when the same capability varies materially across implementations.

For example, metadata filtering may apply only to indexed document chunks in one vector database, while another system may support filtering across chunks, documents and tenants.

---

# Inputs and Outputs

Capabilities should model important inputs and outputs structurally when they affect interoperability, evaluation or governance.

Common capability inputs include:

* user query
* rewritten query
* source document
* chunk
* embedding vector
* metadata filter
* candidate result set
* prompt
* generated answer
* evaluation criterion

Common capability outputs include:

* ranked results
* embedding vector
* chunk list
* transformed document
* assembled context
* generated answer
* citation set
* evaluation score
* validation finding
* trace event

Inputs and outputs should be precise enough that a workflow, tool or component can depend on the capability without relying on prose-only interpretation.

---

# Capability Provider

The entity that makes a capability available should be modeled separately from the capability itself.

Examples:

* a Provider may provide an embedding API capability
* a Framework may support hybrid retrieval capability
* a Component may implement context assembly capability
* a Tool may expose repository search capability
* an Agent may use citation verification capability

This separation allows RKM to compare multiple providers, frameworks or tools that deliver similar behavior with different access models, quality attributes, policies or operational constraints.

---

# Quality Attributes

Capability knowledge should represent quality attributes when they affect selection or evaluation.

Relevant attributes include:

* retrieval quality
* ranking quality
* grounding
* latency
* throughput
* cost
* scalability
* reliability
* explainability
* auditability
* privacy
* security
* interoperability

Quality attributes should not be asserted as universal properties without claims and evidence.

---

# Relationship Use

Capabilities should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Provider PROVIDES Capability
Tool EXPOSES Capability
Component IMPLEMENTS Capability
Framework SUPPORTS Capability
Agent USES Capability
Workflow REQUIRES Capability
Capability DEPENDS_ON Component
Capability CONSUMES Artifact
Capability PRODUCES Artifact
Capability GOVERNED_BY Policy
Benchmark EVALUATES Capability
Evaluation Metric MEASURES Capability
```

Relationship targets should use stable identifiers whenever those concepts are represented as entities.

When a capability is not yet promoted to a specialized entity type, it may be represented as structured knowledge inside the entity that provides, exposes, implements or supports it.

---

# Claims and Evidence

Claims about capabilities should be evidence-backed when they affect trust, comparison, governance or operational use.

Examples of claims that should cite evidence include:

* a framework supports a specific retrieval capability
* a tool exposes a state-changing operational capability
* a provider offers a capability only through a managed service
* a component implements a capability with a known latency constraint
* a capability supports a specific artifact type or deployment model
* an evaluation metric measures a quality attribute of a capability

Evidence may come from documentation, source code, papers, benchmark reports, release notes, provider documentation or observed behavior.

Version-specific capability claims should include the relevant version or observation context when available.

---

# Capability vs Entity

A capability is not automatically an entity.

Promote a capability to a first-class entity only when it needs stable identity, relationships, claims, evidence, lifecycle state or graph export independent of the entity that provides it.

Keep a capability embedded when it is only a local property of one entity and has no reusable semantic value.

Preferred entity-level modeling:

```text
Multiple frameworks support hybrid retrieval capability, and benchmarks evaluate that capability across implementations.
```

Preferred embedded modeling:

```text
A specific tool accepts metadata filters as one part of its invocation contract.
```

---

# Capability vs Tool

A tool is a callable boundary.

A capability is the behavior made available by that boundary.

One tool may expose multiple capabilities, and one capability may be exposed by multiple tools.

For example, a search connector may expose semantic retrieval, metadata filtering and result citation capabilities. Those capabilities should be modeled separately when they need independent comparison, evidence or governance.

---

# Capability vs Component

A component is an architectural building block.

A capability is what the component can do.

For example, a reranker component may implement ranking capability, consume candidate results and produce reranked results. The component boundary describes responsibility and placement in the system, while the capability describes the reusable behavior.

---

# Modeling Guidance

Use capabilities when behavior is important across entity boundaries.

Do not use capabilities as a substitute for precise entity types, relationships, claims or evidence.

Capability descriptions should be:

* action-oriented
* bounded by inputs and outputs
* scoped to relevant RAG stages
* connected to providers, tools, components, frameworks, agents or workflows when useful
* supported by evidence when used for comparison, trust or governance

Avoid broad feature labels that cannot be evaluated, governed or connected to graph relationships.

---

# Schema Implications

The current schema set may represent capabilities as structured fields inside specialized entity schemas, claims, relationships or descriptions.

A dedicated capability schema should be introduced only after identity support and registry entries are added for a Capability entity type.

Until then, architecture and schemas must not require `identity.entityType` to use an unsupported `Capability` value.
