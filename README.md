# RAG Knowledge Model (RKM)

> An open, structured and extensible knowledge base describing Retrieval-Augmented Generation (RAG) techniques, architectures, components, frameworks and best practices.

## Mission

The purpose of this project is to create the most comprehensive machine-readable and human-readable knowledge base about Retrieval-Augmented Generation (RAG).

Unlike a traditional document or a collection of notes, this repository is designed to be:

- searchable
- queryable
- versionable
- extensible
- framework-agnostic
- suitable for LLMs
- suitable for software developers
- suitable for academic research

Every concept is represented using structured JSON documents validated through JSON Schema.

The repository can therefore be used as:

- documentation
- educational material
- dataset
- RAG corpus
- benchmarking dataset
- semantic search corpus
- graph database source
- JSONB source
- vector database source

---

# Design Principles

The project follows several fundamental principles.

## 1. Structured Information

Every concept is represented as structured data.

No free-form documents are required for automated processing.

---

## 2. One Object = One File

Every entity has its own JSON document.

Examples:

```
techniques/hyde.json

techniques/self-rag.json

frameworks/spring-ai.json

frameworks/langchain.json

papers/crag-paper.json
```

This minimizes merge conflicts and makes the repository Git-friendly.

---

## 3. Stable Identifiers

Every object owns a stable identifier that never changes.

Names may evolve.

Identifiers do not.

---

## 4. Extensibility

The schema is designed to allow new fields without breaking compatibility.

Older clients should continue to work correctly.

---

## 5. Human Readable

Although optimized for machines, every description should also be understandable by developers.

---

## 6. Vendor Neutral

This project is not tied to any company or framework.

Spring AI

LangChain

LlamaIndex

Haystack

Semantic Kernel

OpenAI

Anthropic

Google

Azure AI

are all first-class citizens.

---

## 7. Citation Friendly

Whenever possible, information should reference:

- research papers
- official documentation
- RFCs
- standards
- academic publications

---

## Repository Structure

```
metadata/

schema/

techniques/

families/

frameworks/

patterns/

components/

papers/

examples/

evaluation/

glossary/

diagrams/

images/
```

---

## Versioning

The project follows Semantic Versioning.

```
Major.Minor.Patch
```

Examples

```
1.0.0

1.1.0

2.0.0
```

---

## License

Apache 2.0 (recommended)

---

## Contributing

Contributions should preserve:

- schema consistency
- naming consistency
- citation quality
- technical accuracy

---

## Long-Term Vision

The long-term objective is to become a structured reference dataset describing the RAG ecosystem.

Rather than documenting only algorithms, the project aims to model the entire Retrieval-Augmented Generation landscape, including:

- retrieval techniques
- query transformations
- chunking strategies
- embedding models
- rerankers
- vector databases
- graph databases
- evaluation methodologies
- prompt engineering techniques
- orchestration patterns
- agent architectures
- benchmark datasets
- implementation examples
- production best practices

The repository is intentionally designed so that it can later be transformed into:

- PostgreSQL JSONB
- Neo4j
- RDF
- OWL
- GraphQL
- REST APIs
- Vector Databases
- Knowledge Graphs

without requiring structural changes.