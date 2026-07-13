# Data Graph Export Example

This directory contains graph export files derived from the validated RKM seed dataset under `data/`.

The data graph export is separate from `examples/graph-export/`, which is generated from the minimal pedagogical fixture package. This export reflects the current real seed data declared in `data/manifest.json`.

## Files

- `rag-techniques.nodes.json`: graph nodes derived from seed RAG technique records and their declared schema.
- `rag-techniques.edges.json`: graph edges derived from export provenance and declared domain relationships.

The current export emits RAG technique nodes, a schema node, `VALIDATED_BY_SCHEMA` provenance edges, and declared domain relationship edges from `data/relationships/rag-technique-relationships.json`. It does not fabricate relationships between techniques.

## Generation

Regenerate the files from the project root:

```bash
make data-graph-export
```

This runs:

```bash
python3 scripts/export-data-graph.py
```

## Validation

Committed data graph export files are checked during repository validation:

```bash
make validate
```

The validation path runs:

```bash
python3 scripts/export-data-graph.py --check
```

That check regenerates the data graph in memory and fails if the committed node or edge files differ from the seed-data-derived output.

The data graph export is also validated against the formal graph node and graph edge schemas through:

```bash
make graph-export-validate
```

Schema-level validation checks node and edge shape, duplicate IDs, and edge endpoints that must resolve to nodes in the same export.

## Current Scope

This export is minimal post-alpha work on `main`. It proves a deterministic graph export path for validated seed data and declared relationship sets, but it is not a complete downstream graph product and is not part of the already tagged `v0.1.0-alpha` package.
