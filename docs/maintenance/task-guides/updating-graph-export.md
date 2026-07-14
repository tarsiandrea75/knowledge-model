# Updating Graph Export

## Purpose

Change graph export behavior or generated graph export artifacts while preserving schema validity and endpoint integrity.

## When to Use

Use this guide when editing graph exporters, graph export schemas, fixture exports, data exports, or examples derived from exports.

## Required Readings

- `AGENTS.md`
- `scripts/AGENTS.md` when exporter code changes.
- `examples/AGENTS.md` when generated examples change.
- Relevant graph export schemas under `schema/**`.

## Required Checks

- Update the exporter when source-to-export behavior changes.
- Regenerate affected graph export output.
- Validate graph export node and edge files against graph export schemas.
- Check endpoint integrity for every edge.
- Preserve provenance edge consistency.
- Update docs when export semantics or consumer expectations change.
- Run `make validate`.

## Common Failure Modes

- Editing generated export files without updating the exporter.
- Adding nodes without matching provenance expectations.
- Emitting edges whose endpoints do not exist in the same export.
- Changing export semantics without updating docs or consumers.

## Done Criteria

- Exporter behavior and generated output agree.
- Node and edge files validate.
- Edge endpoint integrity and provenance consistency checks pass.
- Documentation reflects any changed export semantics.
