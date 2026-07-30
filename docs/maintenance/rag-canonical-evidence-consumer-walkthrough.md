# Canonical RAG Evidence Consumer Walkthrough

## Purpose

This walkthrough demonstrates how a downstream consumer can inspect the
canonical projection of the reviewed NASA RAG evidence without changing
canonical data, application defaults, or production routing.

The projection is an internal evaluation artifact. It is not a RAG
recommendation approval and it does not grant redistribution or commercial
rights for the referenced sources.

## Verify the projection first

Run the integrity gate before consuming the projection:

```bash
make canonical-rag-evidence-projection-validate
```

The gate verifies the projection schema, source bundle hash, source-review
hash, provenance consistency, relationship endpoints, duplicate identities,
and equality with a fresh deterministic build.

## Query reviewed source metadata

To retrieve the projection records for one reviewed source:

```bash
python3 scripts/query-canonical-rag-evidence-projection.py \
  --entity-type Reference \
  --source-id nasa-sun-facts
```

The result includes the source reference and any relationships touching that
record. The response must report:

- `status: verified`;
- `scope: INTERNAL_EVALUATION_ONLY`;
- `productionPromotionAllowed: false`.

## Query the complete evidence projection

To inspect all projected evidence records:

```bash
python3 scripts/query-canonical-rag-evidence-projection.py \
  --entity-type Evidence
```

Each evidence record preserves its source identifier, human review decision,
reviewer, review date, bundle hash, and review-record hash. A consumer must
use these fields to retain provenance when presenting source-backed output.

## Lifecycle boundary

The source review is `Human Reviewed` for `INTERNAL_EVALUATION_ONLY`. The
external evidence bundle and the RAG recommendation decision remain separate
lifecycle objects. In particular:

- source review approval does not approve the RAG recommendation;
- the recommendation remains Draft and non-promotable;
- the projection cannot change application defaults or production routes;
- a missing, stale, mismatched, or tampered source record must fail closed.

## Consumer limitations

This walkthrough intentionally performs no network access, provider call,
model inference, database write, application configuration update, or
production promotion. It demonstrates provenance-aware consumption only.
