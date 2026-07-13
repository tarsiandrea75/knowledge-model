# RKM Data

The `data/` directory contains populated sample knowledge content for RAG Knowledge Model. It is distinct from `examples/fixtures/`, which contains minimal pedagogical examples used to demonstrate schema shape and validation mechanics.

This first dataset is intentionally small. It exists to support early consumer testing, validation, and release packaging without claiming to be a complete catalog of RAG techniques or the broader RAG ecosystem.

Data files are declared in `data/manifest.json`. Each manifest entry maps a repository-relative data file to the schema that validates it. `make validate` runs data instance validation after fixture validation, so malformed populated data fails the standard repository validation path.

`data/relationships/` contains declared relationship instances between populated data records. These relationship sets are validated through the same manifest and are exported as domain graph edges by the data graph exporter. Relationship edges are declared by data files, not inferred from technique names, descriptions, or stages.

`data/relationship-support/` contains declared support objects for relationship instances. These files connect relationship IDs to references, claims, and evidence so consumers can inspect why a relationship appears in the seed dataset. Support is validated through the manifest and is not inferred.

`data/components/` contains first-class seed Component records. These records validate against `schema/component.schema.json` and can be connected to techniques through declared relationship sets.

`data/retrievers/` contains first-class seed Retriever records. These records validate against `schema/retriever.schema.json` and can be connected to components through declared relationship sets.

`data/rerankers/` contains first-class seed Reranker records. These records validate against `schema/reranker.schema.json` and can be connected to components through declared relationship sets.

Run direct data validation from the repository root:

```bash
make data-validate
```

Run full repository validation:

```bash
make validate
```

Current populated data scope:

- `data/components/cross-encoder-reranker.json`
- `data/components/keyword-retriever.json`
- `data/components/rank-fusion.json`
- `data/components/semantic-retriever.json`
- `data/rerankers/cross-encoder-reranker.json`
- `data/rag-techniques/hybrid-retrieval.json`
- `data/rag-techniques/query-rewriting.json`
- `data/rag-techniques/reranking.json`
- `data/retrievers/embedding-retriever.json`
- `data/retrievers/lexical-retriever.json`
- `data/relationships/component-specialization-relationships.json`
- `data/relationships/rag-technique-component-relationships.json`
- `data/relationships/rag-technique-relationships.json`
- `data/relationship-support/component-specialization-relationship-support.json`
- `data/relationship-support/rag-technique-component-relationship-support.json`
- `data/relationship-support/rag-technique-relationship-support.json`
