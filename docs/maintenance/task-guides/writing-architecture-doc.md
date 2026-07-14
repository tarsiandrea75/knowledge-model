# Writing Architecture Documentation

## Purpose

Keep architecture documents coherent with the RKM domain model, ontology, evidence model, metadata model, relationship model, and naming rules.

## When to Use

Use this guide before creating or editing files under `docs/architecture/**`.

## Required Readings

- `AGENTS.md`
- `docs/architecture/AGENTS.md`
- Existing architecture documents that define the concept being changed.

## Required Checks

- Use canonical RKM terms.
- Define concepts before relying on them.
- Use canonical relationship names or explicitly mark names as noncanonical candidates, rejected terms, or deprecated terms.
- Concrete examples must use real IDs and real files.
- Abstract examples must avoid repository paths.
- Do not mix invented identifiers with concrete repository paths.
- Run `make validate`.

## Common Failure Modes

- Introducing a relationship predicate that is not registered or marked as noncanonical.
- Combining invented IDs with real file paths.
- Explaining a concept only through prose when a structured entity, relationship, claim, evidence item, or reference is needed.
- Duplicating terminology already defined in the ubiquitous language with a new name.

## Done Criteria

- The document can be read independently.
- Examples are valid as real examples or clearly abstract.
- Relationship language matches the canonical model or is explicitly marked.
- Validation passes or unrelated pre-existing failures are reported.
