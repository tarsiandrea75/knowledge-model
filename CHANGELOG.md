# Changelog

All notable changes to RAG Knowledge Model are documented in this file.

## Unreleased

### Added

- Distributed agent rule routing with local rule files and task-specific maintenance guides, so repository-wide invariants stay concise while detailed rules live near the areas they govern.
- Automated validation for distributed agent rule routing, exposed through `make agent-routing-validate` and the standard `make validate` pipeline.
- Duplicate schema contract validation, exposed through `make schema-duplicate-contracts-validate` and the standard `make validate` pipeline, so same-name reusable definitions must be composed by their first-class schemas.
- Rule coverage report for distinguishing documented, partially validated, and validated governance rules.
- Deterministic data graph export for the validated seed dataset under `data/`, exposed through `make data-graph-export` and checked by `make validate`.
- JSON Schema validation for graph export node and edge files, including duplicate ID checks and edge endpoint integrity checks.
- Validated relationship sets under `data/relationships/` for declared seed dataset domain relationships.
- Relationship support sets under `data/relationship-support/` for connecting declared relationship instances to references, claims, and evidence.
- Data graph export now includes declared domain relationship edges from validated relationship-set files without inferring undeclared relationships.
- Data graph export now enriches declared domain relationship edges with declared support metadata when relationship support is available.
- Validated seed Component data records under `data/components/` and declared technique-component relationships connecting seed techniques to reusable components.
- Validated seed Retriever and Reranker data records under `data/retrievers/` and `data/rerankers/`, with declared `SPECIALIZES` relationships connecting them to existing Component records.
- Semantic validation for data relationship instances, including registered predicate checks, source and target data record integrity checks, data file consistency checks, duplicate relationship ID checks, and duplicate semantic triple checks.
- Semantic validation for relationship support sets, including relationship, claim, evidence, and reference identifier integrity checks.
- Documented unattended automation and recovery guardrails for run logs, failed newly added files, schema-definition duplication risks, valid documentation examples, and safer bounded autopilot rounds.
- Codified automation, recovery, schema-contract, and unattended-run guardrails for clean worktrees, runtime logs, failed new files, bounded autopilot rounds, schema duplication prevention, valid JSON examples, and handoff checks.

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
