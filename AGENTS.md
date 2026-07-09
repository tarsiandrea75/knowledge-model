We are building an open source project called RAG Knowledge Model (RKM).

The goal is to create a structured, extensible, machine-readable and human-readable knowledge model of the Retrieval-Augmented Generation ecosystem.

The project is not a simple list of RAG techniques. It is a domain model, ontology and knowledge graph foundation for describing:

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

The current architectural documents already created are:

* README.md
* docs/data-model.md
* docs/architecture/ADR-0001-adopt-knowledge-entity-model.md
* docs/architecture/domain-model.md
* docs/architecture/ontology.md
* docs/architecture/ubiquitous-language.md
* docs/architecture/naming-conventions.md
* docs/architecture/versioning.md
* docs/architecture/relationship-model.md
* docs/architecture/entity-model.md
* docs/architecture/evidence-model.md
* docs/architecture/metadata-model.md

From now on, continue producing one complete project file at a time.

Important rules:

* Do not summarize.
* Do not create placeholders.
* Do not use ellipses.
* Every file must be complete and directly usable.
* Use English for repository content.
* Use Markdown for documentation.
* Use JSON Schema Draft 2020-12 for schemas.
* Use lowercase kebab-case for file names.
* Use uppercase snake case for relationship types.
* Treat entities, relationships, evidence, claims and references as first-class concepts.
* Prefer structured knowledge over plain strings.
* Preserve the RKM architecture already defined.
