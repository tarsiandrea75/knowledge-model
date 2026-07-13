# Component Data

This directory contains the first populated Component records in RKM. These records are small, conservative, and intended for consumer testing rather than exhaustive coverage of RAG system architecture.

Seed components:

- Keyword Retriever retrieves candidates using lexical or keyword-oriented matching signals.
- Semantic Retriever retrieves candidates using semantic representations such as embeddings.
- Rank Fusion combines or reconciles ranked result lists from multiple retrieval signals.
- Cross-Encoder Reranker scores query-candidate pairs jointly for reranking.

Each record validates against `schema/component.schema.json` through `data/manifest.json`. Component records are first-class data entities with stable IDs, identity metadata, descriptions, and component-specific structured fields.

Components relate to RAG techniques through declared relationship sets under `data/relationships/`. Technique-component edges are declared by relationship-set files, validated against registered predicates and declared data records, and supported by relationship support sets under `data/relationship-support/`. They are not inferred from component names, technique descriptions, or graph export behavior.

Run direct data validation from the repository root:

```bash
make data-validate
```

Run full repository validation:

```bash
make validate
```
