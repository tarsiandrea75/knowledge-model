# Adding Relationship Support

## Purpose

Connect declared relationships to structured references, claims, and evidence.

## When to Use

Use this guide when adding or editing files under `data/relationship-support/**`.

## Required Readings

- `AGENTS.md`
- `data/AGENTS.md`
- The active relationship support schema.
- The relationship set being supported.

## Required Checks

- Relationship IDs must reference declared relationships.
- Claim IDs, evidence IDs, and reference IDs must be unique where validation requires uniqueness.
- Claims, evidence, references, and relationship IDs must cross-reference valid IDs.
- Support source types, confidence, strength, and status must match active schemas.
- Use conservative Maintainer Analysis support for seed modeling rationale when external evidence is not appropriate.
- Run `make validate`.

## Common Failure Modes

- Referencing a relationship ID that does not exist.
- Linking a claim or evidence item to a reference ID that is not declared.
- Using unsupported confidence, strength, status, or source type values.
- Presenting maintainer rationale as external evidence.

## Done Criteria

- Every support link resolves to a valid relationship, claim, evidence item, and reference.
- Support semantics match active schemas.
- Validation passes or unrelated pre-existing failures are reported.
