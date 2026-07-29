# RKM-020 External Evidence Review Gate

## Objective

Provide a deterministic, provider-free review gate for the RKM external RAG
evidence bundle. The gate must verify local file hashes, source repository
commit presence, strict bundle structure, and the fail-closed lifecycle before
human review.

## Scope

- Add a validator for `rkm-external-rag-evidence-bundle-v1`.
- Verify corpus and dataset hashes against an explicitly supplied RAG root.
- Verify generated artifact and decision-record hashes against the RKM root.
- Verify that the declared RAG source commit exists locally.
- Add self-tests and a Make target.
- Document the review command and its non-promoting boundary.

## Acceptance criteria

- [x] Valid evidence passes with no network or provider call.
- [x] Corpus, dataset, artifact, decision, and source-commit mismatches fail
      with actionable paths and identifiers.
- [x] Missing or unsafe paths fail closed.
- [x] Lifecycle must remain `Draft`, `Not Reviewed`, and non-promotable.
- [x] Standard RKM validation runs the self-test.
- [x] No production route, default, canonical entity, or external source is
      modified.

## Required validation

```bash
make validate
make external-rag-evidence-review RAG_ROOT=/path/to/BuildingRAGAgentsWithLLMs
```

## Boundary

This gate verifies evidence integrity only. It does not review source rights,
fetch external pages, mark evidence as reviewed, or promote a production
recommendation.

## Handoff

Completed locally on 2026-07-29. The local evidence bundle verification passed
against both authorized repositories. Human rights and freshness review remain
outside this technical gate.
