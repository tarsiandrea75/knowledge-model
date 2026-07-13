# Changelog

All notable changes to RAG Knowledge Model are documented in this file.

## Unreleased

### Added

- Deterministic data graph export for the validated seed dataset under `data/`, exposed through `make data-graph-export` and checked by `make validate`.
- JSON Schema validation for graph export node and edge files, including duplicate ID checks and edge endpoint integrity checks.

## v0.1.0-alpha - 2026-07-13

Initial internal alpha package for RKM evaluation, onboarding, and consumer feedback.

### Added

- JSON Schema Draft 2020-12 foundation for core RKM entities, relationships, claims, evidence, references, metadata, registries, and specialized RAG technique and framework records.
- Repository validation pipeline through `make validate`.
- Fixture instance validation for the minimal fixture package under `examples/fixtures`.
- Data instance validation for the seed dataset under `data`.
- Minimal fixture-derived graph export under `examples/graph-export`.
- Consumer guide for early internal users.
- Maintenance documentation covering maturity, consumability, and assistant handoff guidance.

### Notes

- This alpha is not production-ready.
- This alpha is not a complete RAG ecosystem catalog.
- No git tag is created by this documentation package.
