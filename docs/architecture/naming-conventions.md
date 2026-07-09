# Naming Conventions
## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines the naming conventions used throughout the RAG Knowledge Model repository.

It applies to:

- directories
- files
- schemas
- JSON properties
- entity identifiers
- slugs
- relationship names
- ontology terms
- generated artifacts
- documentation
- examples

Consistent naming is required for maintainability, automation, validation and graph export.

---

# Core Principles

## 1. Names Must Be Predictable

A contributor should be able to infer where a file belongs and how it should be named.

Example:

```
techniques/hyde.json
```

not:

```
techniques/HypotheticalDocumentEmbedding.json
```

---

## 2. Identifiers Are Not Names

Identifiers are stable machine-oriented values.

Names are human-oriented labels.

Example:

```
id: TECHNIQUE-0007
slug: hyde
display name: HyDE
official name: Hypothetical Document Embedding
```

These values serve different purposes and must not be confused.

---

## 3. Prefer Explicitness Over Brevity

Names should be clear even if slightly longer.

Preferred:

```
parent-document-retrieval.json
```

Avoid:

```
parent-rag.json
```

unless the shorter form is the canonical term.

---

## 4. Use Canonical Vocabulary

All names must follow the Ubiquitous Language.

Do not introduce synonyms unless they are explicitly registered as aliases.

---

## 5. Optimize for Git

File names should be:

- lowercase
- stable
- portable
- readable
- friendly to diffs
- friendly to shell commands

Avoid spaces, uppercase letters and special characters.

---

# Directory Names

Directory names MUST use lowercase kebab-case.

Preferred:

```
vector-databases/
embedding-models/
chunking-strategies/
evaluation-metrics/
prompt-techniques/
```

Avoid:

```
VectorDatabases/
vector_databases/
vector databases/
EmbeddingModels/
```

---

# Top-Level Directory Names

The following top-level directory names are canonical.

```
docs/
schema/
ontology/
techniques/
frameworks/
components/
papers/
datasets/
benchmarks/
embedding-models/
language-models/
rerankers/
retrievers/
vector-databases/
graph-databases/
chunking-strategies/
prompt-techniques/
evaluation-metrics/
agents/
workflows/
tools/
providers/
examples/
generators/
exports/
```

---

# Documentation Directory Names

Documentation directories MUST use lowercase kebab-case.

Canonical documentation structure:

```
docs/
  architecture/
  diagrams/
  decisions/
  guides/
  references/
  contributing/
```

Architecture Decision Records may live in:

```
docs/architecture/
```

or:

```
docs/decisions/
```

The repository SHOULD choose one location and keep it consistent.

Current canonical location:

```
docs/architecture/
```

---

# File Names

File names MUST use lowercase kebab-case.

Preferred:

```
self-rag.json
corrective-rag.json
parent-document-retrieval.json
contextual-compression.json
multi-query-retrieval.json
```

Avoid:

```
SelfRAG.json
corrective_rag.json
Parent Document Retrieval.json
contextualCompression.json
```

---

# Markdown File Names

Markdown files MUST use lowercase kebab-case.

Preferred:

```
domain-model.md
ontology.md
ubiquitous-language.md
naming-conventions.md
```

Avoid:

```
DomainModel.md
ontology_document.md
Ubiquitous Language.md
```

---

# JSON File Names

JSON instance files MUST use lowercase kebab-case.

The file name SHOULD match the entity slug.

Example:

```
slug: hyde
file: hyde.json
```

Example:

```
slug: parent-document-retrieval
file: parent-document-retrieval.json
```

---

# JSON Schema File Names

JSON Schema files MUST use lowercase kebab-case and end with:

```
.schema.json
```

Preferred:

```
entity.schema.json
knowledge-entity.schema.json
relationship.schema.json
technique.schema.json
framework.schema.json
paper.schema.json
```

Reusable definitions SHOULD be stored under:

```
schema/definitions/
```

Example:

```
schema/definitions/identity.schema.json
schema/definitions/metadata.schema.json
schema/definitions/reference.schema.json
```

---

# PlantUML File Names

PlantUML files MUST use lowercase kebab-case and end with:

```
.puml
```

Preferred:

```
domain-model.puml
entity-relations.puml
inheritance.puml
technique-workflow.puml
```

---

# Entity Identifiers

Entity identifiers MUST be:

- uppercase
- stable
- globally unique
- immutable
- independent from names
- independent from file paths

Format:

```
PREFIX-0000
```

Examples:

```
TECHNIQUE-0001
FRAMEWORK-0001
COMPONENT-0001
PAPER-0001
DATASET-0001
BENCHMARK-0001
```

---

# Entity Identifier Prefixes

The following prefixes are canonical.

| Entity Type | Prefix |
|---|---|
| Technique | TECHNIQUE |
| Framework | FRAMEWORK |
| Component | COMPONENT |
| Paper | PAPER |
| Dataset | DATASET |
| Benchmark | BENCHMARK |
| Embedding Model | EMBEDDING-MODEL |
| Language Model | LANGUAGE-MODEL |
| Reranker | RERANKER |
| Retriever | RETRIEVER |
| Vector Database | VECTOR-DATABASE |
| Graph Database | GRAPH-DATABASE |
| Chunking Strategy | CHUNKING-STRATEGY |
| Prompt Technique | PROMPT-TECHNIQUE |
| Evaluation Metric | EVALUATION-METRIC |
| Agent | AGENT |
| Workflow | WORKFLOW |
| Tool | TOOL |
| Provider | PROVIDER |
| Problem | PROBLEM |
| Advantage | ADVANTAGE |
| Limitation | LIMITATION |
| Tradeoff | TRADEOFF |
| Use Case | USE-CASE |
| Relationship | RELATIONSHIP |
| Reference | REFERENCE |
| Claim | CLAIM |
| Evidence | EVIDENCE |

---

# Identifier Numbering

Identifier numbers MUST use four digits.

Preferred:

```
TECHNIQUE-0001
TECHNIQUE-0002
TECHNIQUE-0003
```

Avoid:

```
TECHNIQUE-1
TECHNIQUE-01
TECHNIQUE-001
```

---

# Identifier Stability

Once assigned, an identifier MUST NOT change.

This remains true even if:

- the entity is renamed
- the entity slug changes
- the file path changes
- the description changes
- the entity is deprecated

---

# Slugs

Slugs MUST use lowercase kebab-case.

Slugs are human-readable and URL-safe.

Preferred:

```
hyde
self-rag
corrective-rag
parent-document-retrieval
multi-query-retrieval
```

Avoid:

```
HyDE
self_rag
CorrectiveRAG
parent document retrieval
```

---

# Slug Stability

Slugs SHOULD remain stable.

However, unlike identifiers, slugs MAY change if the canonical name changes.

If a slug changes, maintainers SHOULD preserve the old slug as an alias.

---

# Display Names

Display names are human-readable names used in documentation and UI.

Display names MAY use uppercase letters, punctuation or official stylization.

Examples:

```
HyDE
Self-RAG
Corrective RAG
GraphRAG
RAPTOR
Spring AI
LlamaIndex
```

---

# Official Names

Official names SHOULD use the name used by the original paper, project or official documentation.

Examples:

```
Hypothetical Document Embeddings
Self-Reflective Retrieval-Augmented Generation
Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
```

When official naming is ambiguous, prefer the most widely cited form.

---

# Acronyms

Acronyms MUST preserve official capitalization.

Examples:

```
RAG
HyDE
CRAG
RAPTOR
LLM
VLM
BM25
RRF
ANN
MTEB
BEIR
```

Avoid normalizing acronyms to lowercase unless used in file names or slugs.

---

# JSON Property Names

JSON property names MUST use camelCase.

Preferred:

```json
{
  "createdAt": "2026-07-08",
  "updatedAt": "2026-07-08",
  "schemaVersion": "1.0.0",
  "entityType": "Technique",
  "officialName": "Hypothetical Document Embedding"
}
```

Avoid:

```json
{
  "created_at": "2026-07-08",
  "UpdatedAt": "2026-07-08",
  "schema-version": "1.0.0"
}
```

---

# JSON Enum Values

Enum values SHOULD use Title Case for human-oriented values.

Preferred:

```json
{
  "status": "Published",
  "maturity": "Production",
  "difficulty": "Intermediate"
}
```

Avoid:

```json
{
  "status": "published",
  "maturity": "production_ready",
  "difficulty": "INTERMEDIATE"
}
```

Exception:

Relationship types use uppercase snake case.

---

# Relationship Type Names

Relationship type names MUST use uppercase snake case.

Preferred:

```
REQUIRES
OPTIONALLY_USES
IMPLEMENTS
INTRODUCES
EVALUATES
COMPATIBLE_WITH
ALTERNATIVE_TO
```

Avoid:

```
requires
optionallyUses
ImplementedBy
compatible-with
```

---

# Relationship Direction Names

Relationship names SHOULD be written from source to target.

Preferred:

```
Paper INTRODUCES Technique
Framework IMPLEMENTS Technique
Technique REQUIRES Retriever
Technique OPTIONALLY_USES Reranker
```

Avoid unclear inverse names unless explicitly defined.

Acceptable inverse relationships may exist, but they must be canonical.

Example:

```
Technique IS_IMPLEMENTED_BY Framework
```

may be derived from:

```
Framework IMPLEMENTS Technique
```

The repository SHOULD prefer one canonical direction to avoid duplication.

---

# Boolean Property Names

Boolean properties SHOULD begin with:

- is
- has
- supports
- requires
- allows
- uses
- can

Preferred:

```json
{
  "isExperimental": false,
  "hasNativeSupport": true,
  "supportsHybridRetrieval": true,
  "requiresVectorDatabase": true
}
```

Avoid:

```json
{
  "experimental": false,
  "nativeSupport": true,
  "hybridRetrieval": true
}
```

---

# Date and Time Property Names

Date and time properties MUST use `At` suffix when representing timestamps.

Preferred:

```json
{
  "createdAt": "2026-07-08T00:00:00Z",
  "updatedAt": "2026-07-08T00:00:00Z"
}
```

Date-only properties MAY use `Date` suffix.

Preferred:

```json
{
  "publicationDate": "2023-10-01"
}
```

---

# Version Property Names

Use:

```
version
```

for the entity document version.

Use:

```
schemaVersion
```

for the schema version.

Use:

```
introducedInVersion
```

for the repository version where something was introduced.

Use:

```
deprecatedInVersion
```

for the repository version where something was deprecated.

---

# Status Values

Canonical lifecycle status values:

```
Draft
Review
Published
Deprecated
Archived
```

Do not use:

```
Active
Inactive
Enabled
Disabled
Complete
Incomplete
```

unless describing a different lifecycle dimension.

---

# Maturity Values

Canonical maturity values:

```
Experimental
Research
Emerging
Growing
Production
Industry Standard
Legacy
Deprecated
```

---

# Difficulty Values

Canonical difficulty values:

```
Beginner
Intermediate
Advanced
Expert
Research
```

---

# Impact Values

Canonical impact values:

```
Very Low
Low
Medium
High
Very High
```

---

# Confidence Values

Canonical confidence values:

```
Very Low
Low
Medium
High
Very High
```

---

# Priority Values

Canonical priority values:

```
Very Low
Low
Medium
High
Very High
Critical
```

---

# Compatibility Values

Canonical compatibility values:

```
Unknown
Poor
Limited
Fair
Good
Excellent
Native
Not Applicable
```

---

# Cost Values

Canonical qualitative cost values:

```
None
Very Low
Low
Medium
High
Very High
```

---

# Latency Values

Canonical qualitative latency values:

```
None
Very Low
Low
Medium
High
Very High
```

---

# Complexity Values

Canonical qualitative complexity values:

```
Very Low
Low
Medium
High
Very High
```

---

# Language Codes

Language codes SHOULD follow BCP 47 when applicable.

Preferred:

```
en
it
es
es-AR
pt-BR
fr
de
```

---

# License Names

License names SHOULD use SPDX identifiers.

Preferred:

```
Apache-2.0
MIT
CC-BY-4.0
CC-BY-SA-4.0
```

Avoid:

```
Apache 2
Apache License
Creative Commons
```

---

# Schema IDs

Schema `$id` values SHOULD use stable absolute URLs.

Preferred:

```json
{
  "$id": "https://ragknowledge.org/schema/technique.schema.json"
}
```

Definition schemas:

```json
{
  "$id": "https://ragknowledge.org/schema/definitions/identity.schema.json"
}
```

---

# Internal References

Internal references SHOULD use entity identifiers.

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

When readability is useful, include both:

```json
{
  "targetId": "TECHNIQUE-0007",
  "targetSlug": "hyde",
  "targetName": "HyDE"
}
```

The identifier remains authoritative.

---

# External References

External references SHOULD include:

- title
- url
- sourceType
- accessedAt
- authors when applicable
- publicationDate when applicable

Do not use raw URLs without metadata when possible.

---

# Collection Names

Collection names MUST be plural.

Preferred:

```
techniques/
frameworks/
components/
papers/
datasets/
benchmarks/
```

Individual entity names MUST be singular.

Preferred:

```
Technique
Framework
Component
Paper
Dataset
Benchmark
```

---

# Generated Code Naming

Generated code SHOULD follow the idioms of the target language.

## Java

Use PascalCase for classes and records.

Examples:

```java
Technique
KnowledgeEntity
Relationship
EmbeddingModel
```

Use camelCase for fields.

Examples:

```java
createdAt
schemaVersion
entityType
```

---

## TypeScript

Use PascalCase for interfaces and types.

Examples:

```ts
Technique
KnowledgeEntity
Relationship
```

Use camelCase for fields.

Examples:

```ts
createdAt
schemaVersion
entityType
```

---

## GraphQL

Use PascalCase for types.

Examples:

```graphql
type Technique
type KnowledgeEntity
type Relationship
```

Use camelCase for fields.

Examples:

```graphql
createdAt
schemaVersion
entityType
```

---

## SQL

Use snake_case for table and column names when generating SQL.

Examples:

```sql
knowledge_entity
schema_version
created_at
entity_type
```

SQL naming is a generated artifact convention, not the canonical JSON convention.

---

## Neo4j

Use PascalCase for node labels.

Examples:

```
Technique
Framework
Paper
Component
```

Use uppercase snake case for relationships.

Examples:

```
REQUIRES
IMPLEMENTS
INTRODUCES
EVALUATES
```

---

# Acronym Handling in Slugs

Acronyms in slugs MUST be lowercase.

Preferred:

```
rag
hyde
crag
raptor
llm
mteb
beir
```

Examples:

```
self-rag
corrective-rag
hyde
raptor
llm-reranking
```

Avoid:

```
Self-RAG
HyDE
CRAG
LLM-Reranking
```

---

# Acronym Handling in Display Names

Display names MUST preserve canonical acronym casing.

Preferred:

```
Self-RAG
HyDE
CRAG
RAPTOR
LLM Reranking
```

---

# Avoided Characters

File names, slugs and identifiers MUST NOT contain:

- spaces
- tabs
- accented characters
- punctuation other than hyphen
- emoji
- parentheses
- commas
- slashes
- backslashes
- colons
- semicolons
- quotes

---

# Reserved Words

Avoid using the following as entity slugs because they are too generic:

```
model
database
search
retrieval
generation
context
agent
tool
index
metric
score
document
chunk
paper
framework
component
```

Use qualified names instead.

Preferred:

```
embedding-model
vector-database
semantic-search
retrieval-technique
evaluation-metric
```

---

# Deprecated Names

Deprecated names SHOULD remain searchable as aliases.

Example:

```json
{
  "aliases": [
    {
      "value": "Graph RAG",
      "type": "Spelling Variant",
      "status": "Deprecated"
    }
  ]
}
```

---

# Naming Conflict Resolution

If two concepts appear to share the same name:

1. preserve the canonical name of the older or more established concept;
2. qualify the newer or narrower concept;
3. register aliases if needed;
4. document the decision in an ADR if the conflict is significant.

Example:

```
Vector Store
```

may refer to a framework abstraction.

```
Vector Database
```

refers to a database system.

They must not be merged.

---

# Examples

## Technique Example

```json
{
  "id": "TECHNIQUE-0007",
  "slug": "hyde",
  "entityType": "Technique",
  "name": {
    "display": "HyDE",
    "official": "Hypothetical Document Embedding"
  }
}
```

---

## Framework Example

```json
{
  "id": "FRAMEWORK-0001",
  "slug": "spring-ai",
  "entityType": "Framework",
  "name": {
    "display": "Spring AI",
    "official": "Spring AI"
  }
}
```

---

## Relationship Example

```json
{
  "id": "RELATIONSHIP-0001",
  "type": "IMPLEMENTS",
  "sourceId": "FRAMEWORK-0001",
  "targetId": "TECHNIQUE-0007",
  "confidence": "High"
}
```

---

# Enforcement

Naming conventions SHOULD be enforced through:

- JSON Schema validation
- repository linting
- CI checks
- review guidelines
- generated documentation

Manual review alone is insufficient.

---

# Summary

Naming is part of the model.

Stable, predictable and explicit names make the repository easier to maintain, query, validate, generate and extend.

Every future file, schema and entity must follow these conventions.