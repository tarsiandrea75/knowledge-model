# Glossary Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how glossary terms are represented in the RAG Knowledge Model.

Glossary terms provide canonical definitions, lexical variants, scope boundaries and disambiguation guidance for RAG concepts that need consistent interpretation across architecture documents, schemas, registries, entity instances and graph exports.

The Glossary Model answers the question:

> **Which term is being used, what does it mean in RKM, and how should it be distinguished from nearby concepts?**

---

# Core Principle

A glossary term is a first-class knowledge entity when a word, phrase, acronym or concept affects semantic interpretation across the model.

Glossary terms are not passive documentation notes.

They define controlled meaning that can be referenced, related, cited and reused.

```text
Glossary SPECIALIZES Glossary
Technique USES Glossary
Component DEPENDS_ON Glossary
Paper INTRODUCES Glossary
Glossary REFERENCES Paper
```

Representing glossary terms explicitly helps RKM preserve stable meaning while allowing domain terminology to evolve.

---

# Glossary Term

A Glossary entity represents one canonical term or concept.

A glossary term may represent:

* a RAG concept
* a technique name
* a component name
* a metric name
* a dataset name
* a benchmark name
* a model name
* a framework name
* an acronym
* a synonym

A term should be modeled when its meaning is reused across entities, affects classification, appears in relationship interpretation or needs evidence-backed disambiguation.

---

# Term Boundary

Every glossary term should have a clear semantic boundary.

The boundary identifies:

* what the term means in RKM
* where the definition applies
* which nearby concepts it should not be confused with
* which lexical variants refer to the same concept
* which related entities use, introduce, specialize or depend on the concept
* which references support important definitional claims

Preferred:

```text
Retrieval is the RAG stage that selects candidate source material from an indexed or otherwise queryable knowledge source for later use by generation, evaluation or downstream processing.
```

Avoid:

```text
Finding documents.
```

The avoided statement is too broad to support reuse, disambiguation or graph export.

---

# Term Type

Term type describes the primary kind of term represented by the glossary entity.

Canonical term types include:

```text
Concept
Technique Name
Component Name
Metric Name
Dataset Name
Benchmark Name
Model Name
Framework Name
Acronym
Synonym
Other
```

The term type classifies the term itself, not necessarily every entity that may be related to it.

For example, an acronym can point to a technique, model, benchmark or framework while remaining an acronym as a glossary term.

---

# Definition

Every glossary term must include a canonical definition.

The definition should be precise enough to guide modeling decisions.

It should explain the meaning of the term within RKM, not merely reproduce a generic dictionary definition.

A good definition:

* identifies the concept being named
* states the relevant RAG context
* avoids circular wording
* avoids marketing language
* does not merge distinct concepts into one term
* is stable enough to support graph export and generated documentation

Definitions may be revised as the model improves, but published changes should preserve identity continuity unless the original term boundary was wrong.

---

# Scope

Scope describes the domain context in which the definition applies.

Common scopes include:

```text
General RAG
Retrieval
Indexing
Chunking
Embedding
Reranking
Generation
Evaluation
Orchestration
Governance
Implementation
Research
Other
```

Scope prevents overloaded terminology from being treated as universal.

For example, "context" may mean retrieved source material, prompt context, conversation state or evaluation context depending on the scope.

---

# Lexical Variants

Glossary terms should distinguish canonical identity from lexical variants.

Important lexical information includes:

* preferred term
* alternate terms
* abbreviations
* acronyms
* aliases
* common spelling variants

Lexical variants are useful for search, generated documentation and import mapping.

They should not replace relationships to other entities when the variant has independent semantic meaning.

---

# Disambiguation

Disambiguation notes explain how a term differs from nearby or overloaded concepts.

A disambiguation note should identify:

* the nearby term
* the semantic distinction
* the relationship predicate when the distinction should also be represented structurally

Examples:

```text
Retriever SPECIALIZES Component
Reranker SPECIALIZES Component
Hybrid Retrieval EXTENDS Retrieval
Context Assembly DEPENDS_ON Retrieval
```

Disambiguation should be used when a reader, importer or graph consumer could reasonably confuse two concepts.

---

# Usage Notes

Usage notes provide editorial guidance for consistent RKM content.

Usage notes may explain:

* when to use the term
* when not to use the term
* whether a synonym is preferred or discouraged
* how the term should appear in generated documentation
* which entity types commonly use the term

Usage notes should not carry important evidence-backed claims that belong in claims and evidence.

---

# Examples and Non-Examples

Examples clarify valid usage.

Non-examples clarify boundaries.

Both should be concrete enough to prevent misclassification.

Example:

```text
"Dense retrieval" is an example of a retrieval concept because it describes retrieving candidates by comparing dense vector representations.
```

Non-example:

```text
"Answer generation" is not a retrieval concept because it uses selected context to produce an answer rather than selecting candidate source material.
```

Examples and non-examples are explanatory aids. When an example introduces reusable knowledge about another entity, that knowledge should also be represented through relationships, claims or evidence.

---

# Relationship Use

Glossary terms should be connected through canonical relationships when the relationship has reusable semantic value.

Common relationship patterns include:

```text
Glossary SPECIALIZES Glossary
Glossary GENERALIZES Glossary
Glossary REFERENCES Paper
Paper INTRODUCES Glossary
Technique USES Glossary
Component DEPENDS_ON Glossary
Metric MEASURES Glossary
Benchmark EVALUATES Glossary
```

Relationships should use stable identifiers for represented entities whenever possible.

Plain prose may define and explain a term, but graph-relevant meaning should be represented structurally.

---

# Claims, Evidence and References

Glossary definitions may require evidence when they depend on a paper, specification, framework documentation, benchmark definition or established community usage.

Evidence-backed glossary claims may include:

* a paper introduced a term
* a benchmark defines a metric name
* a framework uses a term with a specific meaning
* a term changed meaning between versions
* a term is ambiguous across retrieval, generation or evaluation contexts

References identify the source material.

Evidence explains how the source supports, contradicts or qualifies the definitional claim.

Claims preserve the assertion being evaluated.

---

# Glossary vs Related Entities

Glossary terms are distinct from the entities they help define.

## Glossary vs Component

A Component is an architectural building block.

A Glossary term may define the word used to name that building block.

For example, a retriever component and the glossary term "retriever" may be related, but they are not the same entity.

## Glossary vs Technique

A Technique describes a method or approach used in RAG.

A Glossary term may define the name, acronym or conceptual boundary of that technique.

## Glossary vs Description

A Description explains an entity.

A Glossary term defines reusable terminology that may apply across many entities.

Descriptions are entity-local.

Glossary terms are reusable knowledge entities.

## Glossary vs Taxonomy

A taxonomy classifies entities into families, categories or domains.

A glossary term defines the meaning of a concept or lexical form.

Taxonomies answer where an entity belongs.

Glossary terms answer what a term means.

---

# Modeling Guidance

Create a glossary term when:

* the term appears across multiple architecture documents or schemas
* the term affects entity classification
* the term is overloaded in the RAG ecosystem
* the term has important synonyms or abbreviations
* the term needs evidence-backed definition or disambiguation
* the term should participate in graph relationships

Do not create a glossary term only to restate an ordinary word with no RAG-specific meaning.

Do not use a glossary term as a substitute for modeling a technique, component, benchmark, dataset, model, provider or paper when that entity has independent semantic meaning.
