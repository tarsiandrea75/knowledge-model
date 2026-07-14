# Adding a Relationship Set

## Purpose

Add declared relationship instances for populated data.

## When to Use

Use this guide when adding or editing files under `data/relationships/**`.

## Required Readings

- `AGENTS.md`
- `data/AGENTS.md`
- `registries/AGENTS.md`
- `registries/relationship-type-registry.json`
- `data/manifest.json`

## Required Checks

- Reuse existing predicates when their semantics fit.
- Confirm source and target IDs exist.
- Confirm source and target data files match the files that contain those IDs.
- Ensure each relationship ID is unique.
- Avoid duplicate semantic triples.
- Consider whether relationship support is needed.
- Run `make validate`.

## Common Failure Modes

- Adding a predicate when an existing predicate fits.
- Using a hard dependency predicate such as `REQUIRES` for a softer relationship.
- Pointing a relationship to an ID that exists in a different file than the declared source or target file.
- Adding relationships without support when the claim needs evidence.

## Done Criteria

- Predicates are registered and semantically justified.
- Relationship endpoints and data file fields resolve.
- Semantic validation passes.
- Support implications were handled or explicitly reported.
