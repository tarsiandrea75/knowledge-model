# Registry Agent Rules

These rules apply to all work under `registries/**`.

## Scope

Registries define controlled vocabularies used by schemas, data validation, documentation, and graph export behavior.

## Rules

- Reuse existing registry entries before adding new entries.
- New relationship predicates must have explicit semantics and a clear modeling justification.
- Avoid hard dependency predicates such as `REQUIRES` unless the dependency is truly mandatory in the RKM domain model.
- Relationship predicate names must be uppercase snake case.
- Registry changes must preserve compatibility with validation scripts, documentation examples, and graph export behavior.
- Do not add near-duplicates with different names when an existing predicate or entity type already fits.
- Registry evolution requires documentation and validation updates when semantics, allowed values, or downstream behavior change.

## Required Checks

Run `make validate` after registry changes and inspect any documentation relationship validation failures carefully.
