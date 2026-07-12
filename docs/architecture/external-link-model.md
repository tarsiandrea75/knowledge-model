# External Link Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how external links are represented in the RAG Knowledge Model.

External links identify useful resources associated with an entity when those resources are not necessarily being cited as evidence.

The External Link Model answers the question:

> **Which resources help users find or inspect an entity, without asserting that those resources support a claim?**

---

# Core Principle

An external link is navigational metadata.

It is not evidence, a claim, or a citation.

External links help humans and tools reach relevant resources such as documentation, repositories, home pages, examples, datasets, benchmarks or papers.

When a resource is used to support, qualify, contradict or contextualize a claim, it should be represented as a Reference and connected through Evidence.

---

# External Link

An External Link is a structured pointer to a resource associated with a Knowledge Entity.

External links may point to:

* official documentation
* project home pages
* source code repositories
* package registries
* examples
* benchmark pages
* dataset pages
* paper landing pages
* hosted demonstrations
* dashboards

External links should remain lightweight. They make resources discoverable without turning every associated URL into a cited source.

---

# External Link vs Reference

External links and references both point to resources, but they serve different purposes.

## External Link

An External Link makes a useful resource reachable.

Example:

```text
A framework entity links to its official documentation page.
```

The link helps users inspect the framework, but no claim is being made from that link by default.

## Reference

A Reference identifies a source that may be cited by evidence, claims or relationships.

Example:

```text
A framework entity cites official documentation as the source for a claim about supported deployment targets.
```

The same URL may appear as an external link and as a reference when both roles are useful. The roles must remain distinct.

---

# External Link vs Evidence

Evidence explains how a source supports, weakens, contradicts or contextualizes a claim.

An external link does not explain support.

Example external link:

```text
LangChain documentation home page.
```

Example evidence:

```text
LangChain documentation states that LangChain provides integrations for retrieval, model invocation and agent workflows.
```

The first is a navigational resource. The second is interpreted support for a claim and should point to a Reference.

---

# External Link vs Citation

A Citation connects a statement to source material used for support or attribution.

An external link is not statement-specific.

External links belong at the entity level when they help users discover or inspect the entity. Citations belong with evidence when a specific assertion depends on source material.

---

# Required Structure

An external link should include:

* a human-readable label
* a resolvable URL

An external link may also include:

* a link type
* a resource owner or publisher
* a version or release when the URL is version-specific
* maintainer notes when the link has review significance

The minimum useful structure should remain small so that external links do not duplicate the Reference model.

---

# Link Types

Canonical link types should describe what the resource is.

Common link types include:

```text
Documentation
Repository
Homepage
Paper
Benchmark
Dataset
Example
Other
```

Link type values should be controlled by schema or registry support when they become shared vocabulary.

---

# Relationship Boundary

External links are usually attributes of a Knowledge Entity, not first-class relationship edges.

Use relationship objects when the target is another modeled entity or when the association has graph meaning.

Examples:

```text
Framework PROVIDES Component
Technique REFERENCES Paper
Benchmark EVALUATES Retriever
```

Use external links for resource pointers that are useful but do not need graph identity.

---

# Modeling Guidance

Use an external link when:

* the resource helps users locate, install, inspect or try an entity
* the resource is associated with the entity but does not support a specific claim
* the URL is useful operational metadata
* the target is not modeled as a first-class RKM entity

Use a Reference when:

* the resource supports an evidence record
* the resource is cited by a claim or relationship
* the resource has bibliographic, publication or provenance meaning
* source priority, access date or citation metadata matters

Use a Relationship when:

* both endpoints are modeled entities
* the association has reusable graph meaning
* the predicate belongs to the canonical relationship type registry

---

# Stability

External links may change more often than references.

Maintainers should prefer stable URLs, official resources and versioned documentation when available.

Broken or stale external links should be repaired without changing evidence semantics unless a linked resource was also used as a Reference.

---

# Schema Implications

Knowledge Entity schemas may expose external links as a first-class array outside the specialized detail object.

Specialized entity schemas should not hide external links inside domain-specific details because external links are common entity-level metadata.

External link schemas should stay intentionally smaller than Reference schemas. When citation metadata, source priority, source type, access dates or provenance interpretation are required, the resource belongs in References instead.
