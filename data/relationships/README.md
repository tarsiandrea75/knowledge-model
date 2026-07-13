# Relationship Data

This directory contains declared relationship sets for populated RKM data.

A relationship set is a validated JSON document that groups relationship instances between existing data records. Relationship sets are useful when a relationship is about how two data records can be connected, but the relationship should not be embedded in either record.

Relationship set files are declared in `data/manifest.json` and validated through the normal data validation path:

```bash
make data-validate
```

Validation has two layers. First, each relationship-set file is JSON-schema validated against `schema/relationship-set.schema.json`. Second, each relationship instance is semantically validated against the registered predicates and declared data records.

Semantic validation checks that:

- every `predicate` exists in `registries/relationship-type-registry.json`
- every `sourceId` and `targetId` exists in a data entity record listed in `data/manifest.json`
- `sourceDataFile` and `targetDataFile` point to the files that actually contain the source and target records
- relationship IDs are unique across relationship sets
- semantic triples of `sourceId`, `predicate`, and `targetId` are unique across relationship sets

The data graph exporter reads relationship-set files listed in `data/manifest.json` and emits each declared relationship as a graph edge. These edges are declared, not inferred. The exporter must not invent domain graph edges from names, descriptions, stages, or other record fields.

Declared relationship instances can be supported by relationship support sets under `data/relationship-support/`. A support set links relationship IDs to structured references, claims, and evidence. This keeps the relationship declaration separate from the rationale and support metadata while allowing validation to check that all identifiers resolve.

Current relationship sets:

- `rag-technique-relationships.json`: conservative workflow relationships among the seed RAG technique records.
