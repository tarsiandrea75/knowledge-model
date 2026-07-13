# RKM Data

The `data/` directory contains populated sample knowledge content for RAG Knowledge Model. It is distinct from `examples/fixtures/`, which contains minimal pedagogical examples used to demonstrate schema shape and validation mechanics.

This first dataset is intentionally small. It exists to support early consumer testing, validation, and release packaging without claiming to be a complete catalog of RAG techniques or the broader RAG ecosystem.

Data files are declared in `data/manifest.json`. Each manifest entry maps a repository-relative data file to the schema that validates it. `make validate` runs data instance validation after fixture validation, so malformed populated data fails the standard repository validation path.

Run direct data validation from the repository root:

```bash
make data-validate
```

Run full repository validation:

```bash
make validate
```

Current populated data scope:

- `data/rag-techniques/hybrid-retrieval.json`
- `data/rag-techniques/query-rewriting.json`
- `data/rag-techniques/reranking.json`
