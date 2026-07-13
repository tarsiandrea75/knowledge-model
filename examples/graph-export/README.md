# Minimal Graph Export Example

This directory contains the first reproducible graph export derived from the RKM fixture package.

## Files

- `minimal-graph.nodes.json`: graph nodes derived from fixture entities, claims, evidence, references, and referenced relationship endpoints.
- `minimal-graph.edges.json`: graph edges derived from the relationship fixture and the claim, evidence, and reference links.

## Generation

The export is generated from:

- `examples/fixtures/minimal-rag-technique.json`
- `examples/fixtures/minimal-relationship.json`
- `examples/fixtures/minimal-claim-with-evidence.json`

Generate the files from the project root:

```bash
python3 scripts/export-fixtures-graph.py
```

The `Makefile` also exposes:

```bash
make graph-export
```

## Validation

Committed graph export files are checked during repository validation:

```bash
make validate
```

The validation path runs:

```bash
python3 scripts/export-fixtures-graph.py --check
```

That check regenerates the graph in memory and fails if the committed node or edge files differ from the fixture-derived output.

The fixture graph export is also validated against the formal graph node and graph edge schemas through:

```bash
make graph-export-validate
```

Schema-level validation checks node and edge shape, duplicate IDs, and edge endpoints that must resolve to nodes in the same export.
