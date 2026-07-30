# RKM-021 Source Freshness Readiness

## Objective

Extend the external RAG evidence gate with deterministic freshness and human
review readiness checks. The gate may prove that metadata is complete and
fresh enough for review, but it must not decide legal rights or mark evidence
as human-reviewed.

## Scope

- Validate source retrieval dates against an explicit review date and maximum
  age threshold.
- Reject future-dated or stale sources with source identifiers and dates.
- Require HTTPS canonical URLs and non-empty rights/attribution metadata.
- Emit a human-review-required list without changing lifecycle state.
- Add a review checklist documenting decisions that remain human-owned.

## Acceptance criteria

- [x] Fresh sources pass deterministically with an explicit review date.
- [x] Future and stale sources fail with actionable source identifiers.
- [x] Rights and attribution remain required metadata, not an automated legal
      approval.
- [x] Output retains `Draft`, `Not Reviewed`, and non-promotable state.
- [x] Self-tests cover fresh, stale, future, and malformed URL cases.

## Boundary

This task does not fetch sources, infer licence permissions, change rights
statements, mark evidence as reviewed, or promote a RAG recommendation.

## Handoff

Completed locally on 2026-07-30. The evidence bundle passes with an explicit
review date and 30-day freshness threshold; five source-specific human review
items remain open.
