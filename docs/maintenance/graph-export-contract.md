# Graph Export Contract

## Purpose

The first RKM graph export gives consumers a small, reproducible nodes-and-edges view of the minimal fixtures. It is intended for loading into graph tools, checking endpoint semantics, and testing consumer import code without requiring a populated RAG ecosystem dataset.

The export is not a replacement for the source fixtures or schemas. The fixtures remain the authoritative RKM examples. The graph export is a derived consumer view.

## Files

The minimal export writes two JSON files:

- `examples/graph-export/minimal-graph.nodes.json`
- `examples/graph-export/minimal-graph.edges.json`

Both files are deterministic JSON arrays. Array ordering is stable so that source control diffs and validation checks are meaningful.

## Nodes

A graph node represents a first-class RKM concept or a minimal endpoint needed to make an edge loadable.

Each node has:

- `id`: the stable RKM identifier used as the graph node key.
- `type`: the node type.
- `label`: a short human-readable label for display.
- `sourceFixture`: the fixture file that caused the node to be emitted.
- `properties`: a compact object with useful source fields.

The first minimal export emits nodes for:

- `Technique`
- `Component`
- `Claim`
- `Evidence`
- `Reference`

`COMPONENT-9001` is emitted as a minimal referenced endpoint because `examples/fixtures/minimal-relationship.json` points to it. The component is not expanded into a full component entity in the fixture package.

## Edges

A graph edge represents a directed connection between two node IDs.

Each edge has:

- `id`: a stable edge identifier.
- `predicate`: an uppercase snake case edge predicate.
- `sourceId`: the source node ID.
- `targetId`: the target node ID.
- `sourceFixture`: the fixture file that caused the edge to be emitted.
- `properties`: a compact object with useful source fields.

The first minimal export emits:

- the fixture relationship edge `TECHNIQUE-9001 DEPENDS_ON COMPONENT-9001`
- a claim edge from `TECHNIQUE-9001` to `CLAIM-9001` using the claim predicate `HAS_ADVANTAGE`
- an evidence edge `EVIDENCE-9001 SUPPORTS CLAIM-9001`
- a reference edge `EVIDENCE-9001 REFERENCES REFERENCE-9001`
- a direct citation edge `CLAIM-9001 CITES REFERENCE-9001`

## Stable Identifiers

Node IDs are the stable identifiers already present in the fixtures. Edge IDs use the persisted relationship ID when the source fixture already has one. Derived claim, evidence, and reference edges use deterministic IDs built from the source ID, predicate, and target ID.

Consumers should use `id`, `sourceId`, and `targetId` as join keys. Labels are display helpers and are not durable identifiers.

## Labels

Labels are derived from the most specific human-readable source field available:

- technique nodes use `identity.name.display`
- component endpoint nodes use `targetSlug`
- claim nodes use the claim statement
- evidence nodes use the evidence summary
- reference nodes use the reference title

Labels may change when source fixtures improve their wording. IDs remain the durable graph keys.

## Node Types

Node types mirror RKM concepts where possible. `Technique`, `Claim`, `Evidence`, and `Reference` are first-class RKM concepts. `Component` is included here as a referenced relationship endpoint so consumers can load a complete edge list without inventing missing nodes.

## Edge Predicates

The relationship fixture preserves its canonical relationship predicate, `DEPENDS_ON`.

Claim, evidence, and reference links use uppercase snake case predicates that expose fixture semantics:

- `HAS_ADVANTAGE` comes from the claim predicate.
- `SUPPORTS` represents evidence support for the claim.
- `REFERENCES` represents evidence use of a reference.
- `CITES` represents the claim reference link.

These predicates are intended as the first minimal graph view of the fixture package, not as a complete graph vocabulary.

## Source Fixture Provenance

Every node and edge includes `sourceFixture`. This value is a repository-relative path to the fixture file that caused the graph item to be emitted.

When a graph item is a referenced endpoint, `sourceFixture` points to the relationship fixture that introduced the endpoint. This makes provenance explicit even when the endpoint does not yet have its own entity fixture.

## Claims, Evidence, And References

The first export represents claims, evidence, and references as nodes because they are first-class RKM concepts.

The claim node carries the claim statement, claim type, confidence, status, subject, predicate, and literal object value in `properties`. The evidence node carries role, strength, confidence, status, and source fragments. The reference node carries source type, source priority, publisher, accessed date, URL, citation, and abstract when present.

Connections are represented as edges:

- the technique connects to the claim through the claim predicate
- evidence supports the claim
- evidence references the source record
- the claim cites the source record

This keeps the graph explicit while preserving the richer fixture objects as the source of truth.

## Stable And Evolving Contract

Stable for this initial export:

- the export is generated from `examples/fixtures/`
- nodes and edges are JSON arrays
- node objects include `id`, `type`, `label`, `sourceFixture`, and `properties`
- edge objects include `id`, `predicate`, `sourceId`, `targetId`, `sourceFixture`, and `properties`
- stable RKM identifiers are used as graph keys
- committed export files are checked during validation

Still evolving:

- graph coverage beyond the minimal fixtures
- package-level graph metadata
- loader-specific mappings for graph databases and indexers
- schemas for graph export files
- version compatibility policy for future export formats

## Commands

Generate the export:

```bash
make graph-export
```

Check that committed export files match the fixtures:

```bash
python3 scripts/export-fixtures-graph.py --check
```

Run full repository validation:

```bash
make validate
```
