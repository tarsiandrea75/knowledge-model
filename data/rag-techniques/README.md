# RAG Technique Data

This directory contains the first populated RAG technique records in RKM. These records are small, conservative, and intended for consumer testing rather than exhaustive coverage.

Seed techniques:

- Hybrid Retrieval combines complementary retrieval signals, commonly lexical matching and vector similarity, before context assembly.
- Query Rewriting transforms or expands a user query before retrieval to better align the retrieval request with available corpus content.
- Reranking reorders retrieved candidates before context assembly so downstream generation can use a more focused candidate set.

Each record is validated against `schema/rag-technique.schema.json` through `data/manifest.json`. The repository-wide validation command runs this check:

```bash
make validate
```

Direct data validation is also available:

```bash
make data-validate
```

To add a new technique safely:

1. Create one lowercase kebab-case JSON file in this directory.
2. Use `schema/rag-technique.schema.json` as the contract.
3. Use stable RKM-style identifiers and conservative descriptions.
4. Do not add fields unsupported by the schema.
5. Add the file and validating schema to `data/manifest.json`.
6. Run `make data-validate` and `make validate`.
