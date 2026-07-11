# Relationship Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how relationships are represented in the RAG Knowledge Model.

Relationships are not secondary metadata.

Relationships are first-class knowledge.

The repository models knowledge as a graph:

```text
Entity ── Relationship ──► Entity
```

A relationship explains how two entities are connected.

---

# Core Principle

A relationship is a semantic statement.

It says something meaningful about the source entity and the target entity.

Example:

```text
HyDE REQUIRES Embedding Model
```

This is not a loose tag.

It is a structured claim.

---

# Relationship as Knowledge

A relationship may answer questions such as:

* What does this technique require?
* Which paper introduced this technique?
* Which framework implements this component?
* Which benchmark evaluates this method?
* Which problems does this technique solve?
* Which limitations does this approach introduce?

Because of this, relationships must be structured, versioned and traceable.

---

# Relationship Direction

All relationships are directional.

A relationship has:

* a source entity
* a relationship type
* a target entity

Example:

```text
Paper INTRODUCES Technique
```

The source is:

```text
Paper
```

The relationship type is:

```text
INTRODUCES
```

The target is:

```text
Technique
```

---

# Canonical Direction

Every relationship type must have a canonical direction.

Preferred:

```text
Framework IMPLEMENTS Technique
```

Avoid storing both:

```text
Framework IMPLEMENTS Technique
```

and a separate inverse relationship that restates the same meaning from Technique to Framework, unless the inverse relationship is explicitly defined as derived.

---

# Derived Inverse Relationships

Some inverse relationships are useful for querying or generated documentation.

Example canonical relationship:

```text
Framework IMPLEMENTS Technique
```

Derived inverse query view:

```text
Technique <- IMPLEMENTS Framework
```

Derived inverse views should be generated from the canonical relationship and should not be manually duplicated unless required.

They may be generated automatically.

---

# Relationship Identity

Every persisted relationship may have a stable identifier.

Example:

```text
RELATIONSHIP-0001
```

Relationship identifiers are useful when:

* a relationship has evidence
* a relationship has lifecycle metadata
* a relationship may be deprecated
* a relationship may be reviewed
* a relationship has confidence
* a relationship is exported to graph databases

---

# Minimal Relationship

A minimal relationship contains:

```json
{
  "type": "IMPLEMENTS",
  "sourceId": "FRAMEWORK-0001",
  "targetId": "TECHNIQUE-0007"
}
```

---

# Full Relationship

A full relationship may contain:

```json
{
  "id": "RELATIONSHIP-0001",
  "type": "IMPLEMENTS",
  "sourceId": "FRAMEWORK-0001",
  "sourceSlug": "spring-ai",
  "targetId": "TECHNIQUE-0007",
  "targetSlug": "hyde",
  "confidence": "High",
  "status": "Published",
  "evidence": [],
  "rationale": "Spring AI can implement HyDE through query transformation and embedding-based retrieval.",
  "notes": [],
  "introducedInVersion": "1.0.0",
  "deprecatedInVersion": null
}
```

The identifier is authoritative.

Slugs and names are optional readability helpers.

---

# Relationship Type

The relationship type is the semantic predicate.

Relationship types must use uppercase snake case.

Examples:

```text
REQUIRES
USES
OPTIONALLY_USES
IMPLEMENTS
INTRODUCES
EVALUATES
COMPATIBLE_WITH
ALTERNATIVE_TO
COMPLEMENTS
```

---

# Relationship Type Registry

Every relationship type should be registered in the ontology.

A relationship type definition should include:

* name
* description
* canonical direction
* allowed source entity types
* allowed target entity types
* inverse relationship when applicable
* whether the inverse is derived or stored
* cardinality rules
* examples

---

# Relationship Properties

Relationships may have properties.

Typical properties:

* id
* type
* sourceId
* targetId
* confidence
* evidence
* rationale
* notes
* status
* version
* introducedInVersion
* deprecatedInVersion
* createdAt
* updatedAt

---

# Confidence

Confidence describes how reliable the relationship is.

Canonical values:

```text
Very Low
Low
Medium
High
Very High
```

Example:

```json
{
  "type": "COMPATIBLE_WITH",
  "sourceId": "TECHNIQUE-0007",
  "targetId": "TECHNIQUE-0011",
  "confidence": "High"
}
```

Confidence should be based on evidence when possible.

---

# Evidence

Relationships may be supported by evidence.

Evidence can include:

* academic papers
* official documentation
* source code
* benchmark results
* experiments
* production reports
* maintainer analysis

Example:

```json
{
  "type": "INTRODUCES",
  "sourceId": "PAPER-0004",
  "targetId": "TECHNIQUE-0009",
  "evidence": [
    {
      "sourceType": "Paper",
      "referenceId": "PAPER-0004",
      "claim": "The paper introduces the Self-RAG framework."
    }
  ]
}
```

---

# Rationale

Rationale explains why the relationship exists.

Evidence supports factual correctness.

Rationale explains interpretation.

Example:

```json
{
  "rationale": "HyDE is classified as a query transformation technique because it transforms the user query into a hypothetical document representation before retrieval."
}
```

---

# Notes

Notes may contain additional maintainer comments.

Notes should not replace structured fields.

Preferred:

```json
{
  "notes": [
    "Some frameworks implement this pattern indirectly rather than as a named feature."
  ]
}
```

Avoid using notes to hide important structured information.

---

# Relationship Lifecycle

Relationships may have lifecycle status.

Canonical values:

```text
Draft
Review
Published
Deprecated
Archived
```

---

# Draft Relationship

A relationship is in Draft when it has been proposed but not reviewed.

---

# Review Relationship

A relationship is in Review when maintainers are evaluating its correctness.

---

# Published Relationship

A relationship is Published when accepted as part of the knowledge model.

---

# Deprecated Relationship

A relationship is Deprecated when it should no longer be used.

Example:

A framework may have supported a technique in the past but removed support later.

---

# Archived Relationship

A relationship is Archived when preserved only for historical reasons.

---

# Cardinality

Relationships may specify cardinality.

Cardinality describes how many targets may be associated with a source.

Examples:

```text
0..1
1..1
0..N
1..N
```

Example:

```text
Paper AUTHORED_BY 1..N Author
```

Example:

```text
Technique REQUIRES 1..N Component
```

---

# Mandatory vs Optional

A relationship may indicate whether the target is mandatory or optional.

Preferred canonical relationship types:

```text
REQUIRES
OPTIONALLY_USES
```

Example mandatory relationship:

```text
Naive RAG REQUIRES Retriever
```

Example optional relationship:

```text
Naive RAG OPTIONALLY_USES Reranker
```

Avoid representing mandatory or optional only as prose.

---

# Relationship Categories

Relationship types are grouped into semantic categories.

The main categories are:

* Structural
* Dependency
* Implementation
* Knowledge Origin
* Evaluation
* Compatibility
* Workflow
* Production
* Evidence
* Taxonomy

---

# Structural Relationships

Structural relationships describe hierarchy or specialization.

Canonical structural relationship types:

```text
EXTENDS
SPECIALIZES
GENERALIZES
BELONGS_TO
PART_OF
CONTAINS
```

---

# EXTENDS

Indicates that one entity builds upon another.

Example:

```text
Advanced RAG EXTENDS Naive RAG
```

Use EXTENDS when the source entity preserves the core idea of the target entity while adding new capabilities.

---

# SPECIALIZES

Indicates that one entity is a more specific form of another.

Example:

```text
Hybrid Retrieval SPECIALIZES Retrieval
```

---

# GENERALIZES

Indicates that one entity is a broader abstraction of another.

Example:

```text
Retrieval GENERALIZES Hybrid Retrieval
```

GENERALIZES is usually the inverse of SPECIALIZES.

It may be generated rather than manually stored.

---

# BELONGS_TO

Indicates membership in a taxonomy, family or category.

Example:

```text
HyDE BELONGS_TO Query Transformation Technique
```

---

# PART_OF

Indicates that one entity is part of another.

Example:

```text
Retriever PART_OF RAG Pipeline
```

---

# CONTAINS

Indicates that one entity contains another.

Example:

```text
RAG Pipeline CONTAINS Retriever
```

CONTAINS is usually the inverse of PART_OF.

---

# Dependency Relationships

Dependency relationships describe requirements or usage.

Canonical dependency relationship types:

```text
REQUIRES
DEPENDS_ON
USES
OPTIONALLY_USES
CONSUMES
PRODUCES
TRANSFORMS
```

---

# REQUIRES

Indicates a mandatory dependency.

Example:

```text
Naive RAG REQUIRES Retriever
```

Use REQUIRES only when the target entity is necessary for the source entity to function as defined.

---

# DEPENDS_ON

Indicates a dependency that may be conceptual, operational or indirect.

Example:

```text
Vector Search DEPENDS_ON Embedding
```

DEPENDS_ON is broader than REQUIRES.

---

# USES

Indicates usage without specifying whether it is mandatory.

Example:

```text
Hybrid Retrieval USES Dense Retrieval
```

Prefer REQUIRES or OPTIONALLY_USES when mandatory status is known.

---

# OPTIONALLY_USES

Indicates an optional component or technique.

Example:

```text
Naive RAG OPTIONALLY_USES Reranker
```

---

# CONSUMES

Indicates that an entity receives an input.

Example:

```text
Language Model CONSUMES Prompt
```

---

# PRODUCES

Indicates that an entity creates an output.

Example:

```text
Embedding Model PRODUCES Embedding
```

---

# TRANSFORMS

Indicates that an entity converts one artifact into another.

Example:

```text
Chunking Strategy TRANSFORMS Document
```

When necessary, use properties to specify input and output artifacts.

---

# Implementation Relationships

Implementation relationships describe software realization.

Canonical implementation relationship types:

```text
IMPLEMENTS
SUPPORTS
PROVIDES
INTEGRATES_WITH
EXPOSES
```

---

# IMPLEMENTS

Indicates that a framework, library or component realizes a concept.

Example:

```text
Spring AI IMPLEMENTS Vector Store Abstraction
```

---

# SUPPORTS

Indicates supported capability or compatibility.

Example:

```text
Spring AI SUPPORTS pgvector
```

---

# PROVIDES

Indicates that an entity offers a component, feature or service.

Example:

```text
OpenAI PROVIDES Embedding Model
```

---

# INTEGRATES_WITH

Indicates integration between two systems.

Example:

```text
Spring AI INTEGRATES_WITH Ollama
```

---

# EXPOSES

Indicates that an entity exposes an interface or capability.

Example:

```text
Framework EXPOSES Retriever Interface
```

---

# Knowledge Origin Relationships

Knowledge origin relationships describe provenance.

Canonical knowledge origin relationship types:

```text
INTRODUCES
DESCRIBES
DEFINES
REFERENCES
CITES
AUTHORED_BY
PUBLISHED_IN
INSPIRED_BY
```

---

# INTRODUCES

Indicates that a paper, organization or author first introduced a concept.

Example:

```text
Self-RAG Paper INTRODUCES Self-RAG
```

---

# DESCRIBES

Indicates that a source explains an entity.

Example:

```text
Paper DESCRIBES Technique
```

---

# DEFINES

Indicates a formal or canonical definition.

Example:

```text
Specification DEFINES Relationship Type
```

---

# REFERENCES

Indicates a general reference.

Example:

```text
Technique REFERENCES Paper
```

---

# CITES

Indicates citation between papers or sources.

Example:

```text
Paper CITES Paper
```

---

# AUTHORED_BY

Indicates authorship.

Example:

```text
Paper AUTHORED_BY Author
```

---

# PUBLISHED_IN

Indicates publication venue.

Example:

```text
Paper PUBLISHED_IN Conference
```

---

# INSPIRED_BY

Indicates conceptual inspiration.

Example:

```text
Technique INSPIRED_BY Prior Technique
```

---

# Evaluation Relationships

Evaluation relationships describe measurement and validation.

Canonical evaluation relationship types:

```text
EVALUATES
EVALUATED_BY
MEASURES
VALIDATES
BENCHMARKED_BY
ACHIEVES_SCORE_ON
```

---

# EVALUATES

Indicates that one entity evaluates another.

Example:

```text
Benchmark EVALUATES Technique
```

---

# EVALUATED_BY

Inverse of EVALUATES.

Usually derived.

Example:

```text
Technique EVALUATED_BY Benchmark
```

---

# MEASURES

Indicates that a metric measures a quality attribute.

Example:

```text
Faithfulness MEASURES Groundedness
```

---

# VALIDATES

Indicates that evidence confirms or supports an entity.

Example:

```text
Experiment VALIDATES Technique
```

---

# BENCHMARKED_BY

Indicates that an entity has been benchmarked by a benchmark.

Usually derived from EVALUATES.

---

# ACHIEVES_SCORE_ON

Indicates a measured result.

Example:

```text
Embedding Model ACHIEVES_SCORE_ON MTEB
```

This relationship should include score metadata.

---

# Compatibility Relationships

Compatibility relationships describe whether entities can be used together.

Canonical compatibility relationship types:

```text
COMPATIBLE_WITH
INCOMPATIBLE_WITH
ALTERNATIVE_TO
COMPLEMENTS
SUPERSEDES
REPLACED_BY
```

---

# COMPATIBLE_WITH

Indicates that two entities can be used together.

Example:

```text
HyDE COMPATIBLE_WITH Reranking
```

COMPATIBLE_WITH is usually symmetric.

If stored once, graph tooling may generate the reverse direction.

---

# INCOMPATIBLE_WITH

Indicates that two entities should not or cannot be used together.

Example:

```text
Technique INCOMPATIBLE_WITH Component
```

This relationship should include rationale.

---

# ALTERNATIVE_TO

Indicates that one entity may replace another in some scenarios.

Example:

```text
Multi-Query Retrieval ALTERNATIVE_TO HyDE
```

ALTERNATIVE_TO is usually symmetric but may not be equivalent in all contexts.

---

# COMPLEMENTS

Indicates that two entities work well together.

Example:

```text
Hybrid Retrieval COMPLEMENTS Reranking
```

COMPLEMENTS is usually symmetric.

---

# SUPERSEDES

Indicates that one entity replaces or improves upon another.

Example:

```text
New Technique SUPERSEDES Older Technique
```

---

# REPLACED_BY

Indicates that one entity has been replaced by another.

Usually inverse of SUPERSEDES.

---

# Workflow Relationships

Workflow relationships describe ordering and execution.

Canonical workflow relationship types:

```text
PRECEDES
FOLLOWS
EXECUTES
TRIGGERS
ROUTES_TO
BRANCHES_TO
```

---

# PRECEDES

Indicates that one step comes before another.

Example:

```text
Query Transformation PRECEDES Retrieval
```

---

# FOLLOWS

Inverse of PRECEDES.

Usually derived.

---

# EXECUTES

Indicates that an agent, workflow or system executes a step or tool.

Example:

```text
Agent EXECUTES Retrieval Workflow
```

---

# TRIGGERS

Indicates that one event or step causes another.

Example:

```text
Low Retrieval Confidence TRIGGERS Corrective Retrieval
```

---

# ROUTES_TO

Indicates conditional routing.

Example:

```text
Query Router ROUTES_TO Hybrid Retriever
```

---

# BRANCHES_TO

Indicates workflow branching.

Example:

```text
Evaluation Step BRANCHES_TO Retry Retrieval
```

---

# Problem and Quality Relationships

Problem and quality relationships describe goals, advantages, limitations and tradeoffs.

Canonical relationship types:

```text
SOLVES
MITIGATES
HAS_ADVANTAGE
HAS_LIMITATION
HAS_TRADEOFF
HAS_USE_CASE
HAS_ANTI_PATTERN
HAS_COMMON_MISTAKE
```

---

# SOLVES

Indicates that an entity directly solves a problem.

Example:

```text
Reranking SOLVES Low Precision
```

Use SOLVES only when the relationship is strong.

---

# MITIGATES

Indicates that an entity partially reduces a problem.

Example:

```text
Reranking MITIGATES Low Precision
```

MITIGATES is weaker than SOLVES.

---

# HAS_ADVANTAGE

Connects an entity to an advantage.

Example:

```text
Hybrid Retrieval HAS_ADVANTAGE Improved Recall
```

---

# HAS_LIMITATION

Connects an entity to a limitation.

Example:

```text
Naive RAG HAS_LIMITATION Sensitive To Chunking Quality
```

---

# HAS_TRADEOFF

Connects an entity to a tradeoff.

Example:

```text
Reranking HAS_TRADEOFF Increased Latency
```

---

# HAS_USE_CASE

Connects an entity to a use case.

Example:

```text
GraphRAG HAS_USE_CASE Enterprise Knowledge Graph Question Answering
```

---

# HAS_ANTI_PATTERN

Connects an entity to an anti-pattern.

Example:

```text
Naive RAG HAS_ANTI_PATTERN Blindly Trusting Top-K Results
```

---

# HAS_COMMON_MISTAKE

Connects an entity to a common implementation mistake.

Example:

```text
Vector Search HAS_COMMON_MISTAKE Using Wrong Embedding Dimension
```

---

# Production Relationships

Production relationships describe operational concerns.

Canonical production relationship types:

```text
DEPLOYED_WITH
OBSERVED_BY
MONITORED_BY
LOGGED_BY
SECURED_BY
GOVERNED_BY
```

---

# DEPLOYED_WITH

Indicates production deployment association.

Example:

```text
RAG Pipeline DEPLOYED_WITH Vector Database
```

---

# OBSERVED_BY

Indicates observability tooling or methods.

Example:

```text
RAG Pipeline OBSERVED_BY Tracing System
```

---

# MONITORED_BY

Indicates monitoring relationship.

Example:

```text
Retriever MONITORED_BY Recall Metric
```

---

# LOGGED_BY

Indicates logging relationship.

Example:

```text
Agent Workflow LOGGED_BY Execution Trace
```

---

# SECURED_BY

Indicates security mechanism.

Example:

```text
Document Retrieval SECURED_BY Access Control Filter
```

---

# GOVERNED_BY

Indicates governance or compliance mechanism.

Example:

```text
Enterprise RAG GOVERNED_BY Data Access Policy
```

---

# Symmetric Relationships

Some relationships are conceptually symmetric.

Examples:

```text
COMPATIBLE_WITH
INCOMPATIBLE_WITH
ALTERNATIVE_TO
COMPLEMENTS
```

Even when symmetric, relationships should still be stored in one canonical direction unless graph export requires both directions.

---

# Transitive Relationships

Some relationships may be transitive.

Examples:

```text
EXTENDS
SPECIALIZES
PART_OF
BELONGS_TO
```

If:

```text
A EXTENDS B
B EXTENDS C
```

then:

```text
A indirectly EXTENDS C
```

Transitive inference should be handled by graph tooling or query logic.

---

# Relationship Validation

Every relationship should be validated against:

* known relationship type
* allowed source entity type
* allowed target entity type
* required fields
* cardinality rules
* status values
* confidence values
* evidence structure

Invalid relationships should fail validation.

---

# Allowed Source and Target Types

Every relationship type should specify allowed source and target entity types.

Example:

```json
{
  "type": "INTRODUCES",
  "allowedSources": [
    "Paper",
    "Organization",
    "Author"
  ],
  "allowedTargets": [
    "Technique",
    "Component",
    "Pattern",
    "Benchmark"
  ]
}
```

---

# Relationship Constraints

Examples of invalid relationships:

```text
Paper IMPLEMENTS Technique
```

Invalid because papers describe or introduce techniques, but do not implement them.

```text
Embedding Model AUTHORED_BY Framework
```

Invalid because frameworks do not author models.

```text
Dataset REQUIRES LLM
```

Usually invalid because datasets do not require language models.

Constraints prevent semantic corruption.

---

# Relationship Storage

Relationships may be stored in two ways.

## Embedded Relationships

The relationship is stored inside the source entity document.

Example:

```json
{
  "relationships": [
    {
      "type": "REQUIRES",
      "targetId": "COMPONENT-0001"
    }
  ]
}
```

---

## Standalone Relationship Documents

The relationship is stored as its own document.

Example:

```text
relationships/relationship-0001.json
```

Standalone relationship documents are useful when relationships contain rich metadata or independent lifecycle.

---

# Preferred Storage Strategy

For early versions of the repository, relationships may be embedded inside entity documents.

For mature versions, important relationships should become standalone documents when they need:

* evidence
* lifecycle
* review
* versioning
* confidence
* detailed rationale

The model supports both approaches.

---

# Relationship Duplication

Avoid duplicate relationships.

Do not store both:

```text
Framework IMPLEMENTS Technique
```

and:

```text
a separate inverse relationship that restates the same meaning from Technique to Framework
```

unless one is explicitly marked as derived.

---

# Relationship Normalization

Prefer referencing entity identifiers.

Preferred:

```json
{
  "targetId": "TECHNIQUE-0007"
}
```

Avoid:

```json
{
  "target": "HyDE"
}
```

When readability is needed, include optional helper fields:

```json
{
  "targetId": "TECHNIQUE-0007",
  "targetSlug": "hyde",
  "targetName": "HyDE"
}
```

The identifier remains authoritative.

---

# Relationship Evidence Policy

Relationships with high semantic importance should include evidence.

Examples requiring evidence:

* Paper INTRODUCES Technique
* Framework IMPLEMENTS Technique
* Benchmark EVALUATES Technique
* Technique SUPERSEDES Technique
* Technique SOLVES Problem

Relationships that may not require strong evidence:

* Technique HAS_ADVANTAGE Advantage
* Technique HAS_LIMITATION Limitation
* Technique BELONGS_TO Family

However, evidence is always preferred.

---

# Relationship Conflict Policy

Two relationships may conflict.

Example:

```text
Technique COMPATIBLE_WITH Component
```

and:

```text
Technique INCOMPATIBLE_WITH Component
```

Conflicts should be resolved by:

1. checking evidence;
2. checking version constraints;
3. checking context;
4. checking whether compatibility differs by implementation;
5. documenting the resolution.

If the conflict remains unresolved, both relationships may be kept with lower confidence and explicit notes.

---

# Contextual Relationships

Some relationships are context-dependent.

Example:

```text
Framework SUPPORTS Technique
```

may depend on:

* framework version
* plugin
* provider
* programming language
* deployment environment

Context should be represented as relationship properties.

Example:

```json
{
  "type": "SUPPORTS",
  "sourceId": "FRAMEWORK-0001",
  "targetId": "TECHNIQUE-0007",
  "sinceVersion": "1.0.0",
  "supportLevel": "Custom Implementation"
}
```

---

# Relationship Version Constraints

Relationships may specify version constraints.

Example:

```json
{
  "type": "SUPPORTS",
  "sourceId": "FRAMEWORK-0001",
  "targetId": "VECTOR-DATABASE-0003",
  "sinceVersion": "1.0.0",
  "untilVersion": null
}
```

---

# Relationship Quality

A high-quality relationship should be:

* semantically precise
* directionally correct
* supported by evidence
* expressed using canonical vocabulary
* linked by stable identifiers
* non-duplicative
* version-aware when needed

---

# Graph Export Mapping

Relationships map naturally to graph database edges.

Example JSON:

```json
{
  "type": "REQUIRES",
  "sourceId": "TECHNIQUE-0001",
  "targetId": "COMPONENT-0001"
}
```

Neo4j-style graph:

```cypher
(:Technique {id: "TECHNIQUE-0001"})
-[:REQUIRES]->
(:Component {id: "COMPONENT-0001"})
```

---

# RDF Mapping

Relationships can also map to RDF triples.

Example:

```text
subject: TECHNIQUE-0001
predicate: REQUIRES
object: COMPONENT-0001
```

Relationship properties may be represented using RDF reification or named graphs.

---

# Query Examples

The relationship model enables queries such as:

```text
Which techniques require rerankers?
```

```text
Which frameworks implement GraphRAG?
```

```text
Which papers introduced query transformation techniques?
```

```text
Which techniques solve low recall but increase latency?
```

```text
Which benchmarks evaluate retrieval quality?
```

```text
Which vector databases support hybrid retrieval?
```

---

# Relationship Anti-Patterns

Avoid the following anti-patterns.

---

## String Relationships

Avoid:

```json
{
  "compatibleWith": [
    "HyDE",
    "Reranking"
  ]
}
```

Prefer:

```json
{
  "relationships": [
    {
      "type": "COMPATIBLE_WITH",
      "targetId": "TECHNIQUE-0007"
    }
  ]
}
```

---

## Ambiguous Relationship Names

Avoid:

```text
RELATED_TO
```

unless no more precise relationship exists.

Prefer:

```text
REQUIRES
IMPLEMENTS
INTRODUCES
COMPLEMENTS
ALTERNATIVE_TO
```

---

## Bidirectional Duplication

Avoid manually storing both directions of the same relationship.

---

## Relationship Without Context

Avoid claims like:

```text
Framework SUPPORTS Technique
```

when support depends on version, plugin or custom implementation.

---

## Evidence-Free Strong Claims

Avoid strong claims without evidence.

Example:

```text
Technique SUPERSEDES Technique
```

should almost always include evidence and rationale.

---

# Summary

Relationships are the connective tissue of the RAG Knowledge Model.

Entities describe what exists.

Relationships describe what is true between entities.

The quality of the repository depends as much on relationship quality as on entity quality.

Every future schema and JSON document must treat relationships as structured, semantic and evidence-aware knowledge.
