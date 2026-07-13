# Description Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how descriptive knowledge is represented in the RAG Knowledge Model.

Description fields provide human-readable explanation for an entity while preserving the distinction between prose, identity, metadata, structured relationships, claims, evidence and references.

The Description Model answers the question:

> **How should RKM explain what an entity is without hiding reusable knowledge inside unstructured prose?**

---

# Core Principle

Descriptions make structured knowledge understandable to humans.

They do not replace structured knowledge.

Important reusable meaning should be modeled through identity, relationships, claims, evidence, references or specialized entity fields when it needs to be queried, validated, reused or exported as graph data.

Description text may introduce, summarize and contextualize that structured knowledge, but it should not be the only place where important facts are stored.

---

# Description Scope

The description object applies to first-class RKM entities.

It may explain:

* what the entity is
* why the entity exists
* which problem it addresses
* what its core idea is
* how it works at a conceptual level
* when it is useful
* what assumptions it relies on
* which limitations, tradeoffs and risks are known
* which related concepts help readers understand it

Description fields should be written for readers who need accurate domain understanding, not only for display snippets.

---

# Required Description Fields

Every entity description should include a concise summary and a complete description.

The summary is a short overview suitable for indexes, search results and generated documentation.

The complete description explains the entity in enough detail that a reader can understand its role in the RAG ecosystem without relying on external context.

Both fields should be factual, specific and consistent with the entity identity, specialized schema fields and supporting references.

---

# Optional Explanatory Fields

Optional descriptive fields should be used when they add meaningful understanding.

Examples include:

* abstract
* motivation
* history
* problem statement
* core idea
* intuition
* technical explanation
* algorithm overview
* implementation notes
* future directions

These fields should not be filled merely to make a document appear complete.

An omitted field is preferable to vague or repetitive prose.

---

# Goals And Non-Goals

Goals describe intended outcomes, design objectives or capabilities associated with the entity.

Non-goals describe objectives the entity intentionally does not address.

Goals and non-goals are descriptive unless they need to become reusable claims, explicit requirements, evaluation criteria or relationships.

For example, a sentence saying that a retriever is designed to improve recall may appear in description text. A stronger assertion that a specific retriever improves recall on a benchmark should be represented as a claim supported by evidence.

---

# Problems, Advantages, Limitations And Tradeoffs

Descriptions may include readable lists of problems solved, advantages, disadvantages, limitations and tradeoffs.

These fields are useful for orientation, but they are not substitutes for the dedicated structured models that represent reusable semantic knowledge.

Use structured problem, advantage, limitation and tradeoff fragments when the information needs stable shape, evidence, relationship targets or graph export.

Use descriptive lists when the information is local explanatory context and does not need independent reuse.

---

# Use Cases And Anti-Patterns

Best use cases describe scenarios where the entity is a good fit.

Anti-patterns describe scenarios where the entity is commonly misapplied or should be avoided.

These fields should identify concrete RAG contexts, such as retrieval over highly regulated documents, long-context answer generation, latency-sensitive search, agentic tool use or benchmark-driven evaluation.

Avoid generic statements such as "use when quality matters" because they do not identify a meaningful RKM context.

---

# Considerations

Security, privacy and ethical considerations may be summarized in description fields when they help readers understand the entity.

Reusable controls, policies, protected assets, evidence or governance requirements should be represented through the relevant structured models rather than only as prose.

Description text should point readers toward the concern; structured fields should carry the reusable semantics when the concern affects validation, comparison or graph export.

---

# Description vs Identity

Identity defines what the entity is and how it is referenced.

Description explains the entity for human readers.

Identity fields should remain stable enough for linking and registry use. Description fields may evolve as the repository improves its understanding of the entity.

Names, aliases, slugs and entity types belong in identity, not description prose.

---

# Description vs Metadata

Metadata describes the RKM document and its lifecycle.

Description describes the modeled entity.

For example, metadata records review state, provenance and repository version. Description records the entity's motivation, core idea, limitations and use cases.

Document governance facts should not be stored in description fields.

---

# Description vs Claims And Evidence

Descriptions may contain explanatory statements, but evidence-backed assertions should be represented as claims when they affect evaluation, comparison or trust.

Evidence should support or qualify claims rather than being embedded only as informal prose.

References should identify source material in structured form instead of appearing only as names or URLs inside description text.

This separation allows RKM to remain readable while preserving machine-readable support for provenance and graph export.

---

# Writing Guidance

Descriptions should be specific, neutral and complete enough to stand alone.

Use consistent RKM terminology from the ubiquitous language.

Prefer direct explanations over marketing language.

Avoid stub text, incomplete sections, unsupported superlatives and statements that imply evidence without linking to evidence.

When a descriptive statement becomes important for selection, evaluation, governance or reuse, model it structurally in addition to explaining it in prose.
