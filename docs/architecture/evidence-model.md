# Evidence Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how evidence, references, sources and claims are represented in the RAG Knowledge Model.

The purpose of the Evidence Model is to make knowledge traceable.

The repository should not only say what is true.

It should also explain:

* where the information comes from
* how reliable it is
* what claim it supports
* whether the claim is direct or inferred
* whether the evidence is primary or secondary
* how confident maintainers are in the interpretation

---

# Core Principle

Important knowledge should be supported by evidence whenever possible.

Evidence connects a claim to a source.

```text
Evidence ── SUPPORTS ── Claim
Evidence ── REFERENCES ── Source
```

---

# Why Evidence Matters

RAG systems are often evaluated by their ability to produce grounded answers.

A knowledge model about RAG should follow the same principle.

Grounded knowledge is more valuable than unsupported knowledge.

Evidence enables:

* trust
* review
* traceability
* citation
* verification
* correction
* source comparison
* graph reasoning
* documentation generation

---

# Evidence vs Reference

Evidence and Reference are related but not identical.

## Reference

A Reference identifies a source.

Example:

```text
The Self-RAG paper
```

## Evidence

Evidence explains how a source supports a specific claim.

Example:

```text
The Self-RAG paper introduces the Self-RAG framework and describes reflection tokens for retrieval and generation control.
```

A reference can exist without being used as evidence.

Evidence always points to one or more references.

---

# Evidence vs Claim

A Claim is a statement.

Evidence supports, weakens, contradicts or contextualizes a Claim.

Example claim:

```text
HyDE improves retrieval for short or underspecified queries.
```

Example evidence:

```text
The HyDE paper reports improved retrieval performance by embedding generated hypothetical documents instead of short user queries.
```

---

# Claim

A Claim is a statement about an entity.

Claims may be:

* factual
* interpretive
* comparative
* evaluative
* historical
* implementation-specific
* version-specific

Claims should be explicit when they are important.

---

# Examples of Claims

```text
HyDE uses a language model to generate a hypothetical document before retrieval.
```

```text
Self-RAG introduces reflection tokens for deciding when retrieval is needed.
```

```text
Reranking often improves precision at the cost of additional latency.
```

```text
Hybrid Retrieval combines dense and sparse retrieval methods.
```

```text
GraphRAG is useful when relationships between entities are important for answering queries.
```

---

# Evidence

Evidence is structured support for a claim.

Evidence may come from:

* academic papers
* official documentation
* source code
* benchmark results
* experiments
* production reports
* technical blogs
* maintainer analysis

Evidence should be structured, not hidden in prose.

---

# Source

A Source is the origin of information.

Sources include:

* Paper
* Official Documentation
* Repository
* Blog Post
* Benchmark
* Dataset
* Experiment
* Standard
* Specification
* Book
* Talk
* Production Report
* Maintainer Analysis

---

# Source Type

Every reference should declare its source type.

Canonical source types:

```text
Paper
Official Documentation
Repository
Specification
Standard
Benchmark
Dataset
Book
Blog Post
Technical Article
Conference Talk
Documentation Page
Experiment
Production Report
Maintainer Analysis
Other
```

---

# Primary Source

A Primary Source is the most authoritative source for a claim.

Examples:

* original paper introducing a technique
* official framework documentation
* official repository
* official benchmark paper
* official specification

Preferred whenever available.

---

# Secondary Source

A Secondary Source discusses, summarizes or interprets a primary source.

Examples:

* blog post explaining Self-RAG
* tutorial implementing HyDE
* third-party benchmark comparison
* community documentation

Secondary sources are useful but should not replace primary sources when primary sources exist.

---

# Tertiary Source

A Tertiary Source aggregates or summarizes other sources.

Examples:

* lists
* directories
* encyclopedic articles
* generated summaries

Tertiary sources are lowest priority for evidence.

---

# Evidence Strength

Evidence should have strength.

Canonical values:

```text
Very Weak
Weak
Moderate
Strong
Very Strong
```

---

# Evidence Strength Guidelines

## Very Strong

Use when the claim is directly stated by a primary source.

Example:

The original paper states that it introduces a technique.

---

## Strong

Use when a primary source strongly supports the claim, even if some interpretation is required.

---

## Moderate

Use when evidence supports the claim but requires interpretation or is based on secondary sources.

---

## Weak

Use when evidence is indirect, incomplete or comes from less authoritative sources.

---

## Very Weak

Use when evidence is speculative, anecdotal or based mainly on maintainer interpretation.

---

# Confidence

Confidence represents the maintainer's confidence in the claim or relationship.

Canonical confidence values:

```text
Very Low
Low
Medium
High
Very High
```

Confidence is not the same as evidence strength.

A claim may have strong evidence but low confidence if the interpretation is uncertain.

---

# Evidence Role

Evidence may play different roles.

Canonical evidence roles:

```text
Supports
Contradicts
Qualifies
Motivates
Illustrates
Implements
Evaluates
Benchmarks
Defines
Introduces
Describes
```

---

# Supports

The evidence supports the claim.

Example:

```text
The paper supports the claim that HyDE embeds hypothetical documents.
```

---

# Contradicts

The evidence contradicts the claim.

Contradictory evidence should not be discarded automatically.

It may reveal:

* disagreement between sources
* version differences
* context dependence
* benchmark differences
* terminology differences

---

# Qualifies

The evidence limits or contextualizes the claim.

Example:

```text
A benchmark may show that a technique improves recall only on specific datasets.
```

---

# Motivates

The evidence explains why a technique was introduced.

---

# Illustrates

The evidence provides an example but does not fully prove the claim.

---

# Implements

The evidence shows that a framework or repository implements a concept.

---

# Evaluates

The evidence evaluates a technique, model or component.

---

# Benchmarks

The evidence provides benchmark data.

---

# Defines

The evidence provides a definition.

---

# Introduces

The evidence establishes that a paper, author or organization introduced a concept.

---

# Describes

The evidence explains or documents a concept.

---

# Claim Types

Claims may be classified by type.

Canonical claim types:

```text
Definition
Historical
Technical
Comparative
Performance
Implementation
Compatibility
Limitation
Advantage
Tradeoff
Evaluation
Operational
Security
Privacy
Licensing
Interpretive
```

---

# Definition Claim

A claim that defines what something is.

Example:

```text
Hybrid Retrieval combines dense and sparse retrieval.
```

---

# Historical Claim

A claim about origin, chronology or evolution.

Example:

```text
The RAG paper introduced retrieval-augmented generation for knowledge-intensive NLP tasks.
```

---

# Technical Claim

A claim about how something works.

Example:

```text
HyDE generates a hypothetical document and embeds it for retrieval.
```

---

# Comparative Claim

A claim comparing two entities.

Example:

```text
Reranking generally improves precision compared to raw top-k vector retrieval.
```

---

# Performance Claim

A claim about measured or expected performance.

Example:

```text
Hybrid Retrieval can improve recall compared to dense retrieval alone.
```

---

# Implementation Claim

A claim about software implementation.

Example:

```text
Spring AI provides vector store abstractions.
```

---

# Compatibility Claim

A claim about whether two entities can be used together.

Example:

```text
HyDE is compatible with reranking.
```

---

# Limitation Claim

A claim describing a weakness or boundary.

Example:

```text
Naive RAG is sensitive to chunking quality.
```

---

# Advantage Claim

A claim describing a positive effect.

Example:

```text
Parent Document Retrieval helps preserve broader context.
```

---

# Tradeoff Claim

A claim describing a compromise.

Example:

```text
Reranking improves precision but increases latency and cost.
```

---

# Evaluation Claim

A claim about evaluation results or methodology.

Example:

```text
RAGAS evaluates faithfulness, answer relevance and context relevance.
```

---

# Operational Claim

A claim about production behavior.

Example:

```text
Federated Retrieval increases operational complexity.
```

---

# Security Claim

A claim about security implications.

Example:

```text
Metadata filtering can enforce document-level access control.
```

---

# Privacy Claim

A claim about privacy implications.

Example:

```text
External embedding APIs may expose document content to third-party providers.
```

---

# Licensing Claim

A claim about license terms or usage rights.

Example:

```text
A framework is distributed under the Apache-2.0 license.
```

---

# Interpretive Claim

A claim based on maintainer interpretation.

Interpretive claims should be clearly marked.

---

# Evidence Object

A structured evidence object should include:

```json
{
  "id": "EVIDENCE-0001",
  "claimId": "CLAIM-0001",
  "referenceId": "REFERENCE-0001",
  "role": "Supports",
  "strength": "Strong",
  "confidence": "High",
  "summary": "The paper describes the technique and reports its retrieval behavior.",
  "quote": null,
  "location": {
    "section": "Method",
    "page": null,
    "figure": null,
    "table": null
  },
  "notes": []
}
```

---

# Reference Object

A structured reference object should include:

```json
{
  "id": "REFERENCE-0001",
  "sourceType": "Paper",
  "title": "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection",
  "authors": [],
  "url": "https://example.org",
  "doi": null,
  "arxivId": null,
  "publicationDate": null,
  "accessedAt": "2026-07-08T00:00:00Z",
  "publisher": null,
  "license": null
}
```

---

# Claim Object

A structured claim object should include:

```json
{
  "id": "CLAIM-0001",
  "entityId": "TECHNIQUE-0007",
  "claimType": "Technical",
  "statement": "HyDE generates a hypothetical document and embeds it for retrieval.",
  "confidence": "High",
  "status": "Published",
  "evidenceIds": [
    "EVIDENCE-0001"
  ]
}
```

---

# Evidence Location

Evidence should identify where support appears within a source whenever practical.

Possible location fields:

* page
* section
* chapter
* paragraph
* figure
* table
* codePath
* commitHash
* urlFragment
* timestamp
* lineStart
* lineEnd

---

# Evidence From Papers

For papers, evidence location may include:

```json
{
  "section": "Method",
  "page": 4,
  "figure": "Figure 2",
  "table": null
}
```

---

# Evidence From Documentation

For documentation, evidence location may include:

```json
{
  "section": "Vector Stores",
  "urlFragment": "#vector-stores",
  "accessedAt": "2026-07-08T00:00:00Z"
}
```

---

# Evidence From Source Code

For repositories, evidence location may include:

```json
{
  "codePath": "src/main/java/example/Retriever.java",
  "lineStart": 10,
  "lineEnd": 42,
  "commitHash": "abc123"
}
```

---

# Evidence From Benchmarks

For benchmarks, evidence location may include:

```json
{
  "dataset": "BEIR",
  "metric": "nDCG@10",
  "score": 0.52,
  "experimentId": "EXPERIMENT-0001"
}
```

---

# Quotation Policy

Short quotations may be used when they materially improve traceability.

Quotes should be:

* short
* accurate
* attributed
* legally safe
* not excessive

Long passages should be summarized instead.

---

# Interpretation Policy

When maintainers infer a claim from evidence, the claim should be marked as interpretive.

Example:

```json
{
  "claimType": "Interpretive",
  "confidence": "Medium",
  "notes": [
    "This classification is based on maintainer interpretation of the method section."
  ]
}
```

---

# Unsupported Claims

Unsupported claims may exist temporarily in Draft status.

Published claims should have evidence whenever feasible.

Unsupported published claims should be avoided.

---

# Evidence Requirements by Claim Type

## Must Have Evidence

The following claim types should normally include evidence:

* Historical
* Performance
* Implementation
* Compatibility
* Evaluation
* Security
* Privacy
* Licensing
* Comparative

---

## Should Have Evidence

The following claim types should preferably include evidence:

* Technical
* Limitation
* Advantage
* Tradeoff
* Operational

---

## May Rely on Maintainer Analysis

The following claim types may sometimes rely on maintainer analysis:

* Interpretive
* Classification
* Common Mistake
* Anti-Pattern
* Use Case

Even then, evidence is preferred.

---

# Evidence Quality

High-quality evidence should be:

* specific
* source-linked
* correctly interpreted
* current enough for the claim
* preferably primary
* independently verifiable
* attached to a clear claim

---

# Conflicting Evidence

Conflicting evidence should be represented explicitly.

Do not silently discard conflicting evidence.

Possible resolutions:

* different versions
* different datasets
* different implementations
* different evaluation methods
* different terminology
* source error
* unresolved disagreement

---

# Conflict Example

```json
{
  "claimId": "CLAIM-0009",
  "statement": "Technique X improves retrieval latency.",
  "evidence": [
    {
      "role": "Supports",
      "strength": "Moderate"
    },
    {
      "role": "Contradicts",
      "strength": "Strong"
    }
  ],
  "confidence": "Low",
  "notes": [
    "Evidence conflicts across benchmark settings."
  ]
}
```

---

# Temporal Evidence

Some evidence becomes stale.

Examples:

* framework feature support
* model performance
* benchmark rankings
* API availability
* license changes
* provider pricing
* supported integrations

Temporal evidence should include:

* observedAt
* validFrom
* validUntil
* accessedAt
* frameworkVersion
* modelVersion

---

# Version-Specific Evidence

Implementation claims should often include version context.

Example:

```json
{
  "frameworkVersion": "1.0.0",
  "validFrom": "2025-05-01",
  "validUntil": null
}
```

---

# Evidence Status

Evidence may have lifecycle status.

Canonical values:

```text
Draft
Review
Published
Deprecated
Archived
```

---

# Draft Evidence

Evidence is Draft when added but not reviewed.

---

# Review Evidence

Evidence is in Review when maintainers are verifying its relevance or interpretation.

---

# Published Evidence

Evidence is Published when accepted.

---

# Deprecated Evidence

Evidence is Deprecated when it should no longer be used.

Example:

Official documentation for an obsolete framework version.

---

# Archived Evidence

Evidence is Archived when preserved only for historical reasons.

---

# Evidence Confidence vs Entity Confidence

Evidence confidence does not automatically determine entity confidence.

An entity may be well-established even if one particular claim has weak evidence.

Similarly, one strong claim does not make all claims about an entity reliable.

---

# Evidence and Relationships

Relationships may require evidence.

Example:

```text
Paper INTRODUCES Technique
```

should usually be supported by evidence from the paper.

Example relationship evidence:

```json
{
  "relationshipId": "RELATIONSHIP-0001",
  "claim": "The paper introduces the technique.",
  "evidenceIds": [
    "EVIDENCE-0001"
  ]
}
```

---

# Evidence and Advantages

Advantages should preferably be linked to evidence or claims.

Example:

```text
Technique HAS_ADVANTAGE Improved Recall
```

should be supported by a claim such as:

```text
The technique improves recall on specified benchmarks or under specified conditions.
```

---

# Evidence and Limitations

Limitations should be evidence-aware.

Some limitations are theoretical.

Some are empirical.

Some are implementation-specific.

The type should be made explicit where possible.

---

# Evidence and Benchmarks

Benchmark evidence should include:

* benchmark name
* dataset
* metric
* score
* baseline
* experimental setting
* model version
* retrieval setup
* date
* source

Benchmark claims without setup details should be treated cautiously.

---

# Evidence and Official Documentation

Official documentation is authoritative for framework features, APIs and configuration.

However, documentation may become stale.

Always include `accessedAt` for web-based documentation references.

---

# Evidence and Papers

Papers are authoritative for concepts they introduce.

However, papers may not reflect production maturity.

A paper can introduce a technique without proving that it is production-ready.

---

# Evidence and Maintainer Analysis

Maintainer analysis is allowed but should be clearly identified.

Use maintainer analysis when:

* synthesizing multiple sources
* classifying a technique
* identifying tradeoffs
* interpreting architecture
* mapping framework concepts to ontology concepts

Maintainer analysis should not masquerade as primary evidence.

---

# Evidence Anti-Patterns

Avoid the following anti-patterns.

---

## Raw URL as Evidence

Bad:

```json
{
  "evidence": "https://example.org"
}
```

Better:

```json
{
  "referenceId": "REFERENCE-0001",
  "role": "Supports",
  "summary": "The documentation describes native support for vector stores."
}
```

---

## Unsupported Strong Claim

Bad:

```text
This technique is the best retrieval method.
```

Better:

```text
This technique improves recall in specific benchmark settings.
```

with evidence.

---

## Evidence Without Claim

Bad:

```json
{
  "references": [
    "paper-url"
  ]
}
```

Better:

```json
{
  "claim": "The paper introduces the technique.",
  "evidence": [
    {
      "referenceId": "REFERENCE-0001",
      "role": "Supports"
    }
  ]
}
```

---

## Claim Hidden in Evidence

Bad:

```json
{
  "evidence": [
    {
      "summary": "HyDE is better than normal retrieval."
    }
  ]
}
```

Better:

```json
{
  "claim": {
    "statement": "HyDE can improve retrieval quality compared to embedding the original query directly."
  },
  "evidence": [
    {
      "summary": "The paper reports improved retrieval results in the evaluated settings."
    }
  ]
}
```

---

## No Temporal Context

Bad:

```text
Framework X supports Technique Y.
```

Better:

```text
Framework X supports Technique Y since version 1.2.0.
```

---

# Evidence Review Checklist

Before publishing evidence, maintainers should verify:

* Is the source identified?
* Is the source type correct?
* Is the claim explicit?
* Does the evidence actually support the claim?
* Is the source primary when possible?
* Is the confidence appropriate?
* Is temporal context needed?
* Is location information included when useful?
* Are conflicting sources considered?
* Is interpretation clearly marked?

---

# Minimal Evidence Contract

A minimal evidence object should contain:

```json
{
  "id": "EVIDENCE-0001",
  "role": "Supports",
  "referenceId": "REFERENCE-0001",
  "summary": "A concise explanation of how the source supports the claim.",
  "confidence": "Medium"
}
```

---

# Minimal Reference Contract

A minimal reference object should contain:

```json
{
  "id": "REFERENCE-0001",
  "sourceType": "Paper",
  "title": "Source title",
  "url": "https://example.org",
  "accessedAt": "2026-07-08T00:00:00Z"
}
```

---

# Minimal Claim Contract

A minimal claim object should contain:

```json
{
  "id": "CLAIM-0001",
  "claimType": "Technical",
  "statement": "A clear statement about the entity.",
  "confidence": "Medium",
  "evidenceIds": []
}
```

---

# Summary

The Evidence Model makes the RAG Knowledge Model trustworthy.

Entities describe concepts.

Relationships connect concepts.

Claims state facts or interpretations.

Evidence supports claims.

References identify sources.

A knowledge base without evidence is only a catalog.

A knowledge base with evidence becomes a trustworthy foundation for humans, tools and AI agents.
