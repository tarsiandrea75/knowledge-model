# Paper Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how papers are represented in the RAG Knowledge Model.

Papers are first-class knowledge entities when they introduce, describe, evaluate or contextualize RAG-relevant concepts.

The Paper Model answers the question:

> **What publication is being modeled, what knowledge does it contribute, and how should RKM use it as evidence?**

---

# Core Principle

A paper is not only a citation string.

A paper is a source-bearing entity with identity, authorship, publication context, contributions, evaluated artifacts, claims, evidence and references.

```text
Paper INTRODUCES Technique
Paper DESCRIBES Dataset
Paper EVALUATES Benchmark
Paper EVALUATES Retriever
Paper REFERENCES Paper
Claim REFERENCES Paper
Evidence SUPPORTS Claim
```

Representing papers explicitly allows RKM to preserve provenance, distinguish original contributions from later summaries and connect claims to the sources that justify them.

---

# Paper Boundary

Every paper entity should define a clear boundary.

The boundary identifies:

* the publication being represented
* the publication type and status
* the authors or responsible organizations
* the venue or publication channel when known
* the publication date or year
* stable external identifiers such as DOI or arXiv identifier
* the RAG-relevant contributions and evaluated artifacts
* the references and evidence records that support modeled claims

Preferred:

```text
Published conference paper that introduces a RAG technique, evaluates it against named baselines on named datasets and provides an implementation repository.
```

Avoid:

```text
Useful RAG paper.
```

The avoided statement does not identify the publication boundary, contribution, evidence role or reusable relationships.

---

# Publication Type

Publication type describes the form of the source.

Canonical publication types include:

```text
Conference Paper
Journal Article
Workshop Paper
Preprint
Technical Report
Thesis
White Paper
Specification
Documentation Paper
Other
```

Publication type should describe the source form, not the strength of its evidence.

Evidence strength depends on the source role, review context, claim being supported, methodology and source priority.

---

# Publication Status

Publication status records the lifecycle state of the paper.

Canonical publication statuses include:

```text
Published
Accepted
Preprint
Under Review
Withdrawn
Superseded
Unknown
```

Status matters because RAG research often appears first as a preprint and may later be revised, accepted, withdrawn or superseded.

Claims derived from papers should preserve the publication state that existed when the claim was modeled.

---

# Authorship and Venue

Paper authorship identifies the people or organizations responsible for the publication.

Authorship should be structured when it affects provenance, attribution, evidence interpretation or later graph export.

Venue information should be represented when it helps distinguish versions, assess review context or locate the source.

Examples include:

* conference name
* journal name
* workshop name
* repository or preprint server
* publisher
* institution

RKM does not require Author or Venue to be first-class entity types before a paper can be represented. When stable identifiers exist, they may be recorded as structured fields or relationships according to the available schema.

---

# Contributions

A paper contribution describes the RAG-relevant knowledge introduced, described, evaluated or analyzed by the publication.

Common contribution types include:

* introduces a technique
* describes a framework
* introduces a dataset
* introduces a benchmark
* introduces a model
* evaluates a retriever
* evaluates rerankers
* provides a survey
* provides an analysis

Important contributions should be connected through first-class relationships when the target exists as an RKM entity.

```text
Paper INTRODUCES Technique
Paper DESCRIBES Framework
Paper INTRODUCES Dataset
Paper INTRODUCES Benchmark
Paper EVALUATES Retriever
Paper EVALUATES Reranker
```

Textual contribution summaries are useful for review, but graph-relevant contribution knowledge should not remain only in prose.

---

# Introduced Concepts

Papers often introduce named concepts before those concepts are modeled as dedicated RKM entities.

An introduced concept may be represented as structured paper knowledge when:

* the concept has a stable name in the paper
* the concept may become a future entity
* the paper is the primary source for the concept
* the contribution should be searchable before the target entity exists

When the concept later becomes an entity, the paper should connect to it with a canonical relationship such as `INTRODUCES`, `DESCRIBES`, `EVALUATES` or `EXTENDS`.

---

# Evaluated Artifacts

Evaluated artifacts identify the systems, techniques, datasets, benchmarks, models or components assessed by the paper.

Evaluation context should be structured when it affects interpretation.

Useful context includes:

* proposed method
* baseline
* evaluated baseline or target
* ablation
* dataset
* benchmark
* metric
* configuration

Evaluation relationships should connect to stable RKM entities when they exist.

```text
Paper EVALUATES Technique
Paper EVALUATES Retriever
Paper EVALUATES Reranker
Paper USES Dataset
Paper USES Evaluation Metric
Benchmark USES Dataset
```

Claims about quality, performance, latency, faithfulness, recall, precision or cost should cite evidence rather than relying only on the paper summary.

Comparative results should be modeled through canonical evaluation, citation, reference and claim structures. A paper may `EVALUATES` each assessed artifact, `CITES` or `REFERENCES` prior sources, and support explicit claims that describe the comparative finding.

---

# Evidence Use

Papers may serve different evidence roles.

A paper is usually a primary source for:

* concepts it introduces
* experiments it reports
* datasets or benchmarks it releases
* systems it describes
* definitions it proposes

A paper is usually a secondary source when it surveys, evaluates or interprets work introduced elsewhere.

A paper is usually a contextual source when it provides background that helps interpret RAG concepts but does not directly support a specific claim.

Evidence use is claim-specific. The same paper may be primary evidence for its own method and secondary evidence for a related method introduced by another paper.

---

# References and Citations

Paper entities may contain references to sources they cite or sources RKM uses to interpret the paper.

References identify sources.

Evidence explains how those sources support, contradict, qualify or contextualize claims.

Citation modeling should remain separate from paper identity.

```text
Paper REFERENCES Paper
Evidence REFERENCES Reference
Evidence SUPPORTS Claim
Claim REFERENCES Paper
```

A paper can be both:

* an RKM entity with paper-specific structured knowledge
* a reference cited by claims, evidence, relationships or other entities

When both forms exist, stable identifiers should connect the entity and reference so that provenance remains traceable.

---

# Relationship Use

Papers should be connected through canonical relationships when those relationships have reusable semantic value.

Common paper relationship patterns include:

```text
Paper INTRODUCES Technique
Paper INTRODUCES Dataset
Paper INTRODUCES Benchmark
Paper DESCRIBES Framework
Paper DESCRIBES Component
Paper EVALUATES Language Model
Paper EVALUATES Embedding Model
Paper EVALUATES Retriever
Paper EVALUATES Reranker
Paper EVALUATES Technique
Paper EXTENDS Technique
Paper REFERENCES Paper
Technique REFERENCES Paper
Claim REFERENCES Paper
```

Relationship targets should use stable identifiers whenever the target is represented as an RKM entity.

Plain text may explain local context, but reusable publication, contribution, evaluation and citation knowledge should be represented structurally.

---

# Paper vs Related Concepts

Papers overlap with references, evidence, claims and external links, but each concept has a distinct responsibility.

## Paper vs Reference

A Paper is a first-class entity describing a publication and its RAG-relevant knowledge.

A Reference is a reusable source identifier used by claims, evidence and relationships.

The same publication may appear as both a Paper entity and a Reference record.

## Paper vs Evidence

A Paper is a source.

Evidence records how a source supports, contradicts, qualifies or contextualizes a claim.

A paper should not be treated as evidence for every possible statement about its topic.

## Paper vs Claim

A Claim is an assertion.

A Paper may make claims, report evidence for claims or be cited by claims.

Claims should remain explicit so they can be reviewed independently from the source that supports them.

## Paper vs External Link

An external link points to a resource associated with the paper, such as a project page, repository or supplementary material.

When the linked resource supports a claim, it should also be represented as a reference and connected through evidence.

---

# Minimum Useful Paper Record

A useful paper record should include:

* identity
* metadata
* description
* publication type
* publication status
* authors
* publication date or year when known
* external identifiers when available
* RAG-relevant contributions
* relationships to modeled entities when available
* references, claims and evidence when the paper supports reusable knowledge

The minimum structure should make the paper identifiable, reviewable and useful for graph export without inventing unavailable metadata.

---

# Schema Alignment

Paper entities are validated by `schema/paper.schema.json`.

The schema requires:

* `identity`
* `metadata`
* `description`
* `paper`

The `paper` section contains paper-specific structured knowledge such as publication type, publication status, authors, venue, identifiers, source availability, research areas, contributions, introduced concepts, evaluated artifacts, methodology, evidence use and review notes.

Provenance, lifecycle, authorship of the RKM record and review state belong in metadata.

Assertions about the paper or claims derived from it belong in claims and should be connected to evidence.

Source materials cited by the paper or used to interpret it belong in references.
