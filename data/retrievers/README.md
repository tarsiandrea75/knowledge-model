# Retriever Data

This directory contains seed Retriever records for RKM. These records are small, conservative, and intended for consumer testing rather than exhaustive coverage of retrieval systems.

Seed retrievers:

- Lexical Retriever retrieves candidate records using lexical, term-based, or keyword-oriented matching signals.
- Embedding Retriever retrieves candidate records by comparing vector or embedding representations.

Each record validates against `schema/retriever.schema.json` through `data/manifest.json`. Retriever records are first-class data entities with stable IDs, identity metadata, descriptions, and retriever-specific structured fields.

Retriever records connect to Component records through declared relationship sets under `data/relationships/`. The current seed specialization edges are declared, validated, and supported by relationship support sets under `data/relationship-support/`; they are not inferred from names, summaries, capabilities, or component roles.

Run direct data validation from the repository root:

```bash
make data-validate
```

Run full repository validation:

```bash
make validate
```
