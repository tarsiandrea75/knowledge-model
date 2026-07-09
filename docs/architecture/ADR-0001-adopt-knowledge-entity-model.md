# ADR-0001
# Adopt a Knowledge Entity Model as the Foundation of the RAG Knowledge Model

**Status**

Accepted

---

## Context

The initial design of the RAG Knowledge Model modeled each entity as an independent JSON document with a dedicated schema.

For example:

- Technique
- Framework
- Paper
- Component

Each schema independently defined descriptive information such as:

- summary
- description
- advantages
- disadvantages
- goals
- limitations
- references

While this approach is straightforward, it quickly leads to duplication.

Every entity shares a large portion of its semantic structure.

As the repository grows, duplicated schema definitions become increasingly difficult to maintain.

Additionally, representing important concepts as plain strings severely limits machine reasoning.

For example:

```json
{
    "advantages":[
        "Improves Recall",
        "Improves Precision"
    ]
}
```

This representation is readable by humans, but machines cannot attach additional meaning to each advantage.

---

## Problem

The repository is intended to become more than documentation.

It should become a structured knowledge base suitable for:

- Retrieval-Augmented Generation
- Knowledge Graphs
- Graph Databases
- Semantic Search
- AI Agents
- Automated Reasoning
- Documentation Generation

Simple string arrays are insufficient for these goals.

---

## Decision

The repository adopts a **Knowledge Entity Model**.

Instead of modeling each JSON document independently, every document will inherit a common conceptual model.

```
Knowledge Entity

    │

    ├── Technique

    ├── Framework

    ├── Paper

    ├── Component

    ├── Dataset

    ├── Benchmark

    ├── Pattern

    ├── Prompt Technique

    ├── Vector Database

    └── Embedding Model
```

Knowledge Entity becomes the fundamental abstraction of the repository.

---

## Knowledge Entity

Every entity possesses:

- identity
- description
- relationships
- evidence
- metadata

Specialized entities extend the base model with domain-specific information.

For example:

Technique adds:

- workflow
- retrieval strategy
- implementation complexity
- supported architectures

Paper adds:

- publication metadata
- authors
- conference
- citations

Framework adds:

- implementation status
- supported features
- official documentation

---

## Structured Knowledge

The repository adopts the following principle:

> Important knowledge must not be represented as plain strings whenever it has its own semantic meaning.

Example:

Instead of:

```json
{
    "advantages":[
        "Improves Recall"
    ]
}
```

The repository prefers:

```json
{
    "advantages":[
        {
            "id":"ADV-0001",
            "title":"Improves Recall",
            "description":"A documented improvement in retrieval recall under defined evaluation conditions.",
            "impact":"High",
            "category":"Retrieval Quality"
        }
    ]
}
```

The second representation enables:

- filtering
- graph traversal
- semantic queries
- impact analysis
- richer documentation

---

## Knowledge Graph Compatibility

The model is intentionally designed to be directly convertible into a property graph.

Typical relationships include:

```
Technique

HAS_ADVANTAGE

Advantage

BELONGS_TO

Category
```

No structural transformation should be required.

---

## Reusable Building Blocks

Rather than defining every concept multiple times, reusable schema definitions will be introduced.

Examples include:

- Identity
- Description
- Relationship
- Reference
- Metadata
- Capability
- Requirement
- Metric
- Evidence

These definitions become the vocabulary from which all higher-level entities are composed.

---

## Semantic Richness

The project prioritizes semantic richness over minimal document size.

Storage efficiency is considered secondary to expressiveness.

The expected consumers of this repository include:

- LLMs
- Knowledge Graph engines
- Graph databases
- Semantic search systems
- Documentation generators
- IDE plugins
- AI agents

---

## Consequences

Positive:

- Strong normalization
- Reduced duplication
- Rich semantic representation
- Easier reasoning
- Better graph compatibility
- Better long-term maintainability
- Easier future extensions

Negative:

- Larger JSON documents
- More complex schemas
- Slightly steeper learning curve
- More relationships to maintain

The maintainers consider these trade-offs acceptable.

---

## Alternatives Considered

### Independent Schemas

Rejected.

Reason:

High duplication and weak semantic expressiveness.

---

### Flat JSON Documents

Rejected.

Reason:

Poor graph compatibility.

---

### RDF Only

Rejected.

Reason:

The repository should remain approachable for software developers.

JSON remains the canonical representation.

RDF can be generated automatically.

---

## Future Evolution

The Knowledge Entity Model intentionally leaves room for future ontology layers.

Possible future additions include:

- JSON-LD
- RDF
- OWL
- SHACL
- GraphQL
- Property Graph generation

without requiring redesign of the conceptual model.

---

## Decision

Accepted.

All future schemas will be designed around the Knowledge Entity Model.