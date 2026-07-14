# Architecture Documentation Agent Rules

These rules apply to all work under `docs/architecture/**`.

## Scope

Architecture documents define RKM concepts, boundaries, terminology, relationships, evidence expectations, metadata rules, ontology structure, and versioning principles.

## Rules

- Use canonical RKM terminology from the ubiquitous language and existing architecture documents.
- Define concepts before using them in a way that could confuse new readers.
- Examples must be either fully real seed examples or clearly abstract examples.
- Do not mix invented IDs with concrete repository paths.
- Concrete examples that reference repository paths must use real IDs and matching files.
- Relationship predicates must be canonical or explicitly marked as noncanonical candidates, rejected terms, or deprecated terms.
- Keep architecture documents independently readable and aligned with the domain model, entity model, relationship model, evidence model, metadata model, ontology, naming conventions, and versioning rules.

## Required Task Guide

Use this guide before editing:

- `docs/maintenance/task-guides/writing-architecture-doc.md`

## Required Checks

Run `make validate` after architecture documentation changes.
