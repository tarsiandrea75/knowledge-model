# RAG Knowledge Model Codex Instructions

We are building an open source project called RAG Knowledge Model (RKM).

RKM is a structured, extensible, machine-readable and human-readable knowledge model of the Retrieval-Augmented Generation ecosystem.

The project is not a simple list of RAG techniques. It is a domain model, ontology and knowledge graph foundation for describing entities, relationships, claims, evidence, references and structured knowledge about the RAG ecosystem.

## Repository Scope

The repository models:

* RAG techniques
* frameworks
* papers
* components
* benchmarks
* datasets
* embedding models
* language models
* rerankers
* retrievers
* vector databases
* graph databases
* chunking strategies
* prompt techniques
* evaluation metrics
* agents
* workflows
* tools
* providers
* problems
* advantages
* limitations
* tradeoffs
* use cases
* claims
* evidence
* references
* relationships

## Current Project State

The repository already contains the initial RKM architecture and JSON Schema foundation.

Existing architecture documents include:

* README.md
* docs/data-model.md
* docs/architecture/ADR-0001-adopt-knowledge-entity-model.md
* docs/architecture/domain-model.md
* docs/architecture/entity-model.md
* docs/architecture/evidence-model.md
* docs/architecture/metadata-model.md
* docs/architecture/naming-conventions.md
* docs/architecture/ontology.md
* docs/architecture/relationship-model.md
* docs/architecture/ubiquitous-language.md
* docs/architecture/versioning.md

Existing schemas include:

* schema/definitions/claim.schema.json
* schema/definitions/description.schema.json
* schema/definitions/entity-type.schema.json
* schema/definitions/evidence.schema.json
* schema/definitions/identity.schema.json
* schema/definitions/knowledge-entity.schema.json
* schema/definitions/metadata.schema.json
* schema/definitions/reference.schema.json
* schema/definitions/relationship-type.schema.json
* schema/definitions/relationship.schema.json
* schema/entity-type-registry.schema.json
* schema/framework.schema.json
* schema/ontology.schema.json
* schema/rag-technique.schema.json
* schema/relationship-type-registry.schema.json

## Mandatory Execution Protocol

Unless the user explicitly instructs otherwise:

1. Create or modify exactly one project file per run.
2. Do not create batches of files.
3. Do not create IDE configuration files.
4. Do not create temporary review files.
5. Do not modify existing files unless the requested task requires it.
6. After creating or modifying the single allowed file, run `bash scripts/validate-rkm.sh`.
7. If validation fails, fix failures only in the file you touched when possible.
8. If validation fails because of pre-existing issues in other files, report those failures without modifying additional files.
9. Report which file was created or modified.
10. Report the validation command that was run and its result.
11. Report the final `git status --short` output.
12. Do not commit changes.
13. Stop immediately after completing the single requested file and validation report.
14. If the next natural step would require additional files, describe it instead of creating it.

## Reviewer Protocol

When the user asks Codex to review the current RKM git diff, Codex acts only as a reviewer.

Reviewer rules:

1. Do not create, modify, delete, format or normalize files.
2. Review only the current git diff.
3. Do not review unrelated repository content unless it appears in the current git diff.
4. Do not commit changes.
5. Return exactly one verdict: `ACCEPT`, `REVISE` or `STOP`.

Use `ACCEPT` when the current git diff is coherent with RKM architecture, follows repository rules, passes required validation or has only non-blocking issues, and is ready to commit.

Use `REVISE` when the current git diff is directionally correct but needs specific fixes before commit. Examples include schema inconsistencies, broken references, invalid naming, incomplete validation, unclear modeling choices, missing required structure, or content that conflicts with RKM architecture.

Use `STOP` when the current git diff should not be repaired as-is. Examples include changes outside the requested scope, multiple unrelated files when only one file was allowed, destructive changes, generated clutter, IDE files, temporary review files, severe architectural drift, or a validation failure that indicates the work should be abandoned and restarted.

Reviewer output must include:

* verdict
* touched files in the current git diff
* reasons for the verdict
* required fixes when the verdict is `REVISE` or `STOP`
* whether commit is recommended
* final `git status --short` output

## Content Rules

* Use English for repository content.
* Use Markdown for documentation.
* Use JSON Schema Draft 2020-12 for schemas.
* Use lowercase kebab-case for file names.
* Use uppercase snake case for relationship types.
* Treat entities, relationships, evidence, claims and references as first-class concepts.
* Prefer structured knowledge over plain strings.
* Preserve the RKM architecture already defined.
* Keep repository content directly usable.
* Do not use incomplete sections.
* Do not use filler content.
* Do not use ellipses.
* Do not summarize when the task asks for a complete file.

## Modeling Rules

Important knowledge should be represented structurally whenever it has reusable semantic meaning.

Prefer this style:

* entities over plain strings
* relationship objects over prose-only relationships
* claims linked to evidence
* references as structured sources
* metadata separated from domain knowledge
* stable identifiers over names as references
* registries for controlled vocabularies
* schemas that can support graph export

## Naming Rules

Use these canonical project names:

* Full project name: RAG Knowledge Model
* Short project name: RKM
* Do not use: RAG Knowledge Base
* Do not use: RAG-KB
* Do not use: ragkb

## Quality Bar

Every file must be coherent with:

* the domain model
* the entity model
* the relationship model
* the evidence model
* the metadata model
* the ontology
* the naming conventions
* the versioning rules

When creating a schema, ensure that:

* it declares JSON Schema Draft 2020-12
* it uses stable $id values under the RKM naming convention
* internal references resolve correctly
* required fields are intentional
* reusable concepts are placed under schema/definitions when appropriate
* specialized schemas compose reusable definitions where possible

When creating documentation, ensure that:

* terminology matches the ubiquitous language
* concepts are defined before being used
* examples are complete and valid
* relationships use uppercase snake case
* the file can be read independently
* the file fits naturally into the existing architecture
