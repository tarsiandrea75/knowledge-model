# Memory Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how memory is represented in the RAG Knowledge Model.

Memory describes state that is retained, retrieved, updated or reused across turns, workflow steps, sessions, users, agents or system executions.

The Memory Model answers the question:

> **What state is preserved during or across RAG activity, and how does that state affect retrieval, generation, grounding, evaluation and governance?**

---

# Core Principle

Memory is a first-class modeling concern when retained state affects behavior.

It is not only implementation storage.

Memory may influence what a retriever searches for, what context an agent trusts, how a workflow resumes, how user preferences are applied, how feedback is accumulated or how policy constraints are enforced.

```text
Agent USES Memory Strategy
Workflow USES Memory Strategy
Memory Strategy DEPENDS_ON Vector Database
Memory Strategy PRODUCES Evidence
Memory Strategy GOVERNED_BY Policy
Evaluation Metric MEASURES Memory Strategy
```

Representing memory explicitly makes stateful RAG systems easier to compare, evaluate, audit and export as graph knowledge.

---

# Memory Strategy

A Memory Strategy describes how a RAG system stores, retrieves, updates and expires state.

A memory strategy may define:

* what state is retained
* where state is stored
* how state is retrieved
* how state is summarized or compressed
* how conflicts are resolved
* how stale state is expired
* which actors may read or write state
* which governance rules apply

The strategy should be modeled when memory behavior has reusable semantic meaning.

Preferred:

```text
Conversation memory strategy that summarizes prior turns, stores user-approved facts and retrieves them only when relevant to the current question.
```

Avoid:

```text
The system has memory.
```

The avoided statement does not identify retained state, access rules, retrieval behavior or lifecycle.

---

# Memory Boundary

Every memory strategy should define a clear boundary.

The boundary identifies:

* what state is eligible for memory
* what state must not be stored
* whether memory is local to a workflow, session, user, tenant or system
* what reads memory
* what writes memory
* what deletes or expires memory
* what evidence supports claims about memory behavior

Memory boundaries matter because state may affect privacy, reproducibility, personalization, grounding and evaluation.

Short-lived workflow state should be distinguished from durable memory that persists beyond the current execution.

---

# Memory Scope

Memory scope describes where retained state applies.

Canonical memory scopes include:

```text
Step Local
Workflow Local
Session
Conversation
User
Tenant
Application
Corpus
Global
Unknown
```

The scope should be explicit when state can affect more than one query, user or workflow execution.

---

# Memory Type

Memory type describes the dominant kind of retained state.

Common memory types include:

```text
Conversation History
Retrieved Context
User Preference
User Fact
Task State
Intermediate Plan
Tool Output
Feedback Signal
Evaluation Trace
Policy State
Cache
Index State
Other
```

The memory type should describe the semantic role of the state, not only the storage mechanism.

For example, a vector database may store conversation summaries, retrieved chunks, tool outputs or feedback signals. Those are different memory types even when they share infrastructure.

---

# Persistence

Persistence describes how long memory is retained.

Canonical persistence levels include:

```text
Ephemeral
Turn
Session
Time Limited
User Controlled
Durable
Versioned
Unknown
```

Persistence should be modeled when it affects reproducibility, privacy, cost, evaluation or user expectations.

Durable memory should identify deletion, correction and expiration behavior when known.

---

# Read and Write Behavior

Memory should distinguish reads from writes.

Important read behavior includes:

* retrieval trigger
* relevance criteria
* ranking method
* access control
* fallback behavior
* maximum retrieved memory

Important write behavior includes:

* write trigger
* approval requirement
* deduplication behavior
* conflict resolution
* summarization behavior
* retention policy

Read and write behavior should be represented when it changes agent autonomy, workflow control flow, grounding, privacy or operational risk.

---

# Relationship Use

Memory strategies should be connected through canonical relationships when those relationships have reusable semantic value.

Useful memory relationships include:

```text
Agent USES Memory Strategy
Workflow USES Memory Strategy
Memory Strategy USES Embedding Model
Memory Strategy DEPENDS_ON Vector Database
Memory Strategy DEPENDS_ON Graph Database
Memory Strategy PRODUCES Evidence
Memory Strategy SUPPORTS Agent
Memory Strategy GOVERNED_BY Policy
Evaluation Metric MEASURES Memory Strategy
Benchmark EVALUATES Memory Strategy
Memory Strategy HAS_LIMITATION Limitation
Memory Strategy HAS_TRADEOFF Tradeoff
Memory Strategy HAS_USE_CASE Use Case
```

Relationship targets should use stable identifiers whenever those entities are represented in RKM.

Plain prose may explain a memory strategy, but reusable dependencies, evaluation context, governance constraints and behavioral effects should be represented structurally.

---

# Evidence and Claims

Claims about memory should be evidence-backed when they affect selection, trust, privacy, safety or operational use.

Examples of claims that should usually cite evidence include:

* a memory strategy improves answer relevance
* a memory strategy reduces repeated retrieval
* memory is isolated per user or tenant
* memory requires human approval before durable writes
* memory expires after a defined retention period
* memory improves or degrades faithfulness in a benchmark setting

Evidence may come from documentation, papers, evaluation runs, production traces, source code, policy documents or observed behavior.

Implementation-specific claims should include version, configuration, storage backend, retrieval method and retention policy when available.

---

# Governance

Memory often retains user, organizational or operational state.

Governance information should be represented when memory may contain sensitive data, personal preferences, private context, compliance-relevant records or state that affects future decisions.

Important governance dimensions include:

* consent
* access control
* deletion
* correction
* retention
* auditability
* tenant isolation
* write approval
* policy enforcement

Governance details should not be hidden in descriptions when they determine whether an agent, workflow or tool may safely read or write memory.

---

# Distinction From Dataset

A Dataset is a structured collection of data used for retrieval, training, evaluation or benchmarking.

A Memory Strategy describes how state is retained and reused during operation.

Example:

```text
A support knowledge base is a Dataset.
```

```text
A user preference memory strategy decides when to store and retrieve durable user preferences.
```

The dataset represents a collection. The memory strategy represents state lifecycle and behavioral rules.

---

# Distinction From Cache

A cache is one possible memory type.

Caching usually preserves computed results to reduce cost or latency.

Memory may also preserve semantic state such as conversation history, preferences, feedback, plans or evaluation traces.

Do not collapse all memory into cache behavior unless the retained state is only reused as an optimization and has no semantic effect beyond performance.

---

# Modeling Guidance

Model memory explicitly when:

* retained state affects retrieval, generation, routing, evaluation or governance
* state persists beyond a single workflow step
* memory behavior is selected, compared or evaluated independently
* privacy, retention or access constraints matter
* claims about personalization, continuity or learning depend on memory
* the memory strategy participates in graph relationships

Do not model memory as a first-class entity when state is a trivial local variable with no reusable semantic meaning.

When uncertain, prefer modeling the memory strategy only when it can be named, bounded, related and evidenced independently.

---

# Schema Implications

The reusable embedded memory definition is `schema/definitions/memory.schema.json`.

That definition represents memory strategy structure inside another entity, workflow, agent, evaluation, evidence record or architecture record. It intentionally omits the full Knowledge Entity envelope: first-class identity, metadata, description and top-level entity relationships remain responsibilities of the containing document.

Use the embedded definition when memory strategy structure is needed as supporting knowledge but the memory strategy is not yet an independently managed entity.

A future first-class memory strategy schema should compose the common Knowledge Entity envelope and add memory-specific structured knowledge.

Expected memory-specific fields include:

* memory type
* memory scope
* persistence level
* retained state categories
* storage backends
* read behavior
* write behavior
* summarization behavior
* expiration behavior
* access control
* governance constraints
* evaluation profile
* limitations
* usage guidance

Before a specialized top-level memory strategy schema is introduced, the shared identity model and entity type registry must support `MemoryStrategy` as an allowed entity type. The specialized schema should then reuse or compose the embedded memory definition for the memory-specific structure instead of creating a parallel contract.
