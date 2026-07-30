# RKM-022 Human Source Review Record

## Objective

Persist the operator's explicit review of the five NASA source records as a
scoped human review decision. The record must bind to the immutable external
evidence bundle and must not imply approval of a RAG pipeline or production
route.

## Scope

- Add a strict review-record schema and fixture.
- Record reviewer identity, review date, scope, source decisions, and bundle
  hash.
- Limit approval to internal evaluation use.
- Keep production promotion disabled and the recommendation decision separate.

## Acceptance criteria

- [x] The review record validates against a strict schema.
- [x] All five source identifiers are covered exactly once.
- [x] Every decision is `APPROVED` only within `INTERNAL_EVALUATION_ONLY` scope.
- [x] The record is bound to the current evidence-bundle SHA-256.
- [x] Production promotion remains false.
- [x] The original evidence and recommendation records remain unchanged.

## Boundary

This record does not certify legal rights, authorize redistribution or
commercial use, mark the RAG recommendation as reviewed, change application
defaults, or promote any pipeline.

## Handoff

Completed locally on 2026-07-30 from the operator's explicit source-review
decision. The scope is internal evaluation only.
