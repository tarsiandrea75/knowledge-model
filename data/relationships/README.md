# Relationship Data

This directory contains declared relationship sets for populated RKM data.

A relationship set is a validated JSON document that groups relationship instances between existing data records. Relationship sets are useful when a relationship is about how two data records can be connected, but the relationship should not be embedded in either record.

Relationship set files are declared in `data/manifest.json` and validated against `schema/relationship-set.schema.json` through the normal data validation path:

```bash
make data-validate
```

The data graph exporter reads relationship-set files listed in `data/manifest.json` and emits each declared relationship as a graph edge. These edges are declared, not inferred. The exporter must not invent domain graph edges from names, descriptions, stages, or other record fields.

Current relationship sets:

- `rag-technique-relationships.json`: conservative workflow relationships among the seed RAG technique records.
