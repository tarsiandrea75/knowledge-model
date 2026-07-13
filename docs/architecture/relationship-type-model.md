# Relationship Type Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how relationship types are represented in the RAG Knowledge Model.

A relationship type is the semantic predicate that gives meaning to a relationship between two entities.

The Relationship Type Model answers the question:

> **What does a relationship predicate mean, and how is that meaning governed before it is used in entity knowledge?**

---

# Core Principle

A relationship type is ontology vocabulary.

It is not an arbitrary label, local tag or prose shortcut.

Every canonical relationship type must have stable meaning, governed direction, valid endpoint rules and lifecycle metadata.

Example:

```text
Framework IMPLEMENTS Workflow
```

In this statement, `IMPLEMENTS` is the relationship type.

The relationship instance connects a particular framework to a particular workflow.

---

# Relationship Type vs Relationship

A relationship type defines the reusable predicate.

A relationship uses that predicate in a concrete graph statement.

Relationship type:

```json
{
  "type": "IMPLEMENTS",
  "label": "Implements",
  "description": "Indicates that the source entity implements the target entity."
}
```

Relationship:

```json
{
  "type": "IMPLEMENTS",
  "sourceId": "FRAMEWORK-0001",
  "targetId": "WORKFLOW-0001"
}
```

The relationship type controls what the predicate means.

The relationship records where that predicate is used.

---

# Canonical Name

Every relationship type has one canonical `type` value.

Relationship type names must use uppercase snake case.

Examples:

```text
REQUIRES
DEPENDS_ON
IMPLEMENTS
EVALUATES
INTRODUCES
PART_OF
CONTAINS
```

The canonical name is stable ontology vocabulary.

Changing it is a breaking semantic change unless the previous value is deprecated with an explicit replacement.

---

# Semantic Definition

Every relationship type must have a precise description.

The description must explain what the predicate means when read from source entity to target entity.

For example, `REQUIRES` means that the target entity is a mandatory dependency for the source entity to function as defined.

This is different from `DEPENDS_ON`, which can represent a conceptual, operational or indirect dependency that is not necessarily mandatory.

Adjacent predicates must remain distinguishable so contributors can choose the correct relationship type without relying on local interpretation.

---

# Canonical Direction

Every relationship type must define a canonical direction.

The canonical direction specifies:

* the semantic role of the source entity
* the semantic role of the target entity
* the preferred stored direction for graph export and validation

Example:

```text
Agent EXECUTES Workflow
```

The source is the executor.

The target is the executed workflow.

The reverse statement should not be stored as a separate canonical relationship unless the relationship type registry explicitly defines that behavior.

---

# Endpoint Rules

Relationship types constrain which entity types can appear as sources and targets.

Endpoint rules make invalid graph statements detectable before they become repository knowledge.

Example valid statement:

```text
Benchmark EVALUATES Reranker
```

Rejected noncanonical invalid statement:

```text
Rejected noncanonical example: Dataset EVALUATES Reranker
```

The invalid statement gives an evaluation predicate to an entity type that is not modeled as the evaluator for that predicate.

Endpoint rules belong in the relationship type registry because they are controlled ontology rules, not local documentation advice.

---

# Inverse Behavior

Some relationship types have useful inverse views.

An inverse may be:

* derived for query or documentation views
* stored only when explicitly allowed
* absent when an inverse would be ambiguous or misleading

Example canonical relationship:

```text
Component PART_OF Workflow
```

Example derived inverse view:

```text
Workflow CONTAINS Component
```

Derived inverse views must not create duplicate authored knowledge unless the registry allows the inverse to be stored.

---

# Cardinality and Reasoning

Relationship types may declare reasoning constraints such as cardinality, transitivity or symmetry.

These constraints describe how tools may validate, infer or export relationships.

Examples:

* `SPECIALIZES` may be transitive.
* `PART_OF` may support containment traversal.
* `ALTERNATIVE_TO` may be symmetric when the registry defines it that way.

Reasoning constraints should be explicit because they affect graph queries and generated documentation.

---

# Evidence and Claim Requirements

Some relationship types require stronger support than others.

A relationship type may define whether relationship instances should include claims, evidence or references.

For example, a relationship asserting that a paper `INTRODUCES` a technique should usually be supported by a structured reference to the paper.

A relationship asserting broad compatibility may need evidence that explains version, scope or tested conditions.

These requirements protect RKM from treating unsupported interpretation as established knowledge.

---

# Lifecycle

Relationship types follow the ontology lifecycle.

Canonical lifecycle values are:

```text
Draft
Review
Published
Deprecated
Archived
```

Published relationship types are available for normal repository use.

Deprecated relationship types remain readable for historical compatibility but should not be used in new relationships.

Archived relationship types are retained only to interpret older data.

---

# Registry Authority

The relationship type registry is the authoritative source for canonical relationship type entries.

The architecture defines the meaning and governance rules.

The registry lists the accepted predicates.

The schema validates the registry structure.

A new relationship type should be added to the registry before it appears as canonical vocabulary in entity data, relationship data or architecture examples.

---

# Graph Export

Relationship types are exported as edge predicates in graph representations.

Exporters should preserve:

* canonical predicate name
* source and target role semantics
* endpoint constraints
* inverse behavior
* lifecycle status
* evidence and claim requirements

This allows RKM graphs to remain explainable after export to property graphs, RDF-like models, search indexes or generated documentation.

---

# Acceptance Criteria

A relationship type definition is coherent when:

* its canonical name uses uppercase snake case
* its description defines source-to-target meaning
* its canonical direction is explicit
* its endpoint rules align with registered entity types
* its inverse behavior is defined when an inverse exists
* its lifecycle state is declared
* its evidence expectations are clear when support is required
* its examples use canonical relationship predicates
