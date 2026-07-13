# Reranker Data

This directory contains seed Reranker records for RKM. These records are small, conservative, and intended for consumer testing rather than exhaustive coverage of reranking systems.

Seed rerankers:

- Cross-Encoder Reranker scores query-candidate pairs jointly to support reranking.

Each record validates against `schema/reranker.schema.json` through `data/manifest.json`. Reranker records are first-class data entities with stable IDs, identity metadata, descriptions, and reranker-specific structured fields.

Reranker records connect to Component records through declared relationship sets under `data/relationships/`. The current seed specialization edges are declared, validated, and supported by relationship support sets under `data/relationship-support/`; they are not inferred from names, summaries, capabilities, or component roles.

Run direct data validation from the repository root:

```bash
make data-validate
```

Run full repository validation:

```bash
make validate
```
