# Reference Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how references are represented in the RAG Knowledge Model.

References make sources identifiable, reusable and citeable across entities, relationships, claims and evidence.

The Reference Model answers the question:

> **Which source is being cited, what kind of source is it, and how can it be found again?**

---

# Core Principle

A reference identifies a source.

It does not, by itself, assert that the source supports a claim.

Support, contradiction, qualification and interpretation belong to evidence.

```text
Reference ── IDENTIFIES ── Source

Claim ── SUPPORTED_BY ── Evidence ── DERIVED_FROM ── Reference
```

---

# Reference

A Reference is a structured description of a source used by RKM.

A reference may identify:

* an academic paper
* official documentation
* a source code repository
* a benchmark
* a dataset
* a standard or specification
* a technical article
* a conference talk
* an experiment
* maintainer analysis

References should be stable enough to support review, validation, graph export and citation generation.

---

# Reference vs Evidence

References and evidence are related but distinct.

## Reference

A Reference identifies where information comes from.

Example:

```text
The Self-RAG paper.
```

## Evidence

Evidence explains how a reference is used to support, contradict, qualify or contextualize a claim.

Example:

```text
The Self-RAG paper introduces reflection tokens for deciding when retrieval and critique are needed during generation.
```

A reference can exist without evidence.

Evidence always points to one or more references.

---

# Reference vs Claim

A Claim is an assertion.

A Reference is a source that may be used to evaluate an assertion.

Example claim:

```text
Hybrid retrieval combines dense retrieval and sparse retrieval.
```

Example reference:

```text
A paper, documentation page or implementation guide that describes hybrid retrieval.
```

The reference alone does not encode the assertion. The claim remains explicit and separately reviewable.

---

# Reference Identifier

Every reference has a stable identifier.

Reference identifiers use the `REFERENCE-0001` pattern.

The identifier is used by:

* evidence records
* claims
* relationship evidence
* entity-local reference lists
* generated graph exports

Reference identifiers must remain stable once published.

---

# Source Type

Every reference declares a source type.

Canonical source types are:

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

The source type describes what the source is, not whether it is authoritative.

---

# Source Priority

Source priority describes how directly authoritative a source is for a specific kind of knowledge.

Canonical source priorities are:

```text
Primary
Secondary
Tertiary
```

## Primary Source

A Primary source is the most direct source for a claim.

Examples:

* the original paper introducing a technique
* official framework documentation
* an official repository
* an official benchmark paper
* an official specification

Primary sources should be preferred when they are available and relevant.

## Secondary Source

A Secondary source interprets, summarizes, compares or explains primary sources.

Examples:

* survey papers
* technical articles
* comparison guides
* educational documentation

Secondary sources are useful for context, but important factual claims should still cite primary sources when possible.

## Tertiary Source

A Tertiary source aggregates or indexes other sources.

Examples:

* catalogs
* curated lists
* encyclopedia-style summaries
* metadata indexes

Tertiary sources may help discover references, but should not be the only support for important claims when stronger sources are available.

---

# Bibliographic Fields

References should include bibliographic fields when they are available.

Common fields include:

* title
* authors
* publisher
* publication date
* update date
* accessed date
* URL
* canonical URL
* DOI
* arXiv identifier
* ISBN
* repository URL
* version
* citation

Not every source type uses every field.

The model favors accurate partial metadata over invented completeness.

---

# Contributor

A Contributor is a person or organization responsible for a source.

Contributor records should include a name.

They may also include:

* ORCID
* organization identifier
* repository account
* contributor URL

Organizations may be modeled as contributors when they are the author or maintainer of a source.

---

# Versioned Sources

Some sources change over time.

Examples:

* framework documentation
* model documentation
* repository README files
* API references
* benchmark leaderboards

When a source is versioned or mutable, references should record enough context to recover the cited state.

Useful fields include:

* version
* publication date
* update date
* accessed date
* canonical URL
* repository URL
* commit hash

Version-specific claims should use evidence that points to versioned or dated references.

---

# URL and Canonical URL

The `url` field records the location that can be accessed.

The `canonicalUrl` field records the preferred stable location when it differs from the accessed URL.

Examples:

* a DOI landing page may be canonical while a PDF URL is the accessed URL
* an arXiv abstract page may be canonical while a versioned PDF URL is the accessed URL
* official documentation may have a canonical page and localized or redirected URLs

Canonical URLs improve deduplication and citation quality.

---

# Reference Scope

References may appear inside specialized entity documents.

The scope of a reference list is the document that contains it unless a repository-level reference registry is introduced in a future version.

Within a document:

* reference identifiers should be unique
* evidence records should cite references by identifier
* claims should rely on evidence rather than embedding citation prose
* duplicate references should be avoided

---

# Relationship to Entities

Some sources are also entities.

Examples:

* a Paper entity can also be cited as a reference
* a Dataset entity can also be cited as a reference
* a Benchmark entity can also be cited as a reference
* a Framework repository can be cited as a reference for implementation-specific claims

Entity identity and reference identity serve different purposes.

The entity represents the thing in the knowledge graph.

The reference identifies a source used to support knowledge about the thing.

---

# Required Reference Content

A valid reference should contain at least:

* stable reference identifier
* source type
* title

Additional fields should be included when they improve traceability or citation quality.

---

# Example Reference

```json
{
  "id": "REFERENCE-0001",
  "sourceType": "Paper",
  "sourcePriority": "Primary",
  "title": "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection",
  "authors": [
    {
      "name": "Akari Asai"
    }
  ],
  "publishedAt": "2023-10-17",
  "url": "https://arxiv.org/abs/2310.11511",
  "arxivId": "2310.11511",
  "citation": "Asai et al. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. 2023."
}
```

---

# Modeling Guidance

Use references when a source needs to be cited, reused, reviewed or linked from evidence.

Use evidence when a source is interpreted in relation to a claim or relationship.

Use claims when RKM asserts reusable knowledge.

Use relationships when knowledge connects two entities through a controlled relationship type.

Do not hide important source information in prose when it can be represented as a reference.

Do not treat a reference as proof without an evidence record explaining what the source contributes.

---

# Graph Interpretation

In graph exports, references may be represented as nodes.

Evidence records connect claims and relationships to references.

Example:

```text
CLAIM-0001
  └── SUPPORTED_BY
      └── EVIDENCE-0001
          └── DERIVED_FROM
              └── REFERENCE-0001
```

This preserves traceability while keeping claims, evidence and references independently addressable.

---

# Lifecycle

References may evolve as metadata improves.

Allowed maintenance changes include:

* adding missing authors
* adding canonical URLs
* adding source priority
* adding DOI, arXiv identifier or ISBN
* correcting citation formatting
* recording accessed or updated dates

Reference identifiers should not change for metadata corrections.

A reference should only be replaced when it identified the wrong source.
