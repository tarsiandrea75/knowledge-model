# Canonical RAG Evidence Projection — Internal Release Readiness

## Decision

The canonical RAG evidence projection is technically ready for an internal,
read-only evaluation package. It is not approved for production promotion,
public redistribution, commercial use, or application-default changes.

## Verified coverage

- One versioned projection envelope is validated against the RKM schema.
- Sixteen projected entities preserve source and review provenance.
- Ten projected relationships have stable identities and existing predicate
  vocabulary.
- The source bundle and human review record are bound by SHA-256 values.
- A fresh provider-free build is byte-equivalent to the committed fixture.
- Tampered hashes, duplicate identities, missing endpoints, and divergent
  provenance fail closed.
- A read-only consumer can query references and evidence while preserving the
  review scope and non-promotable lifecycle.

## Human and policy boundary

The five NASA sources were reviewed by Andrea Tarsi on 2026-07-30 for
`INTERNAL_EVALUATION_ONLY`. That review confirms metadata and attribution
consistency for this package; it is not a legal license opinion and does not
authorize redistribution or commercial reuse.

The RAG recommendation remains a separate Draft and non-promotable decision.
Source review, evidence projection, and recommendation approval must not be
collapsed into one lifecycle state.

## Unresolved limitations

- Source identity hashes identify canonical URLs rather than downloaded
  payload bytes.
- The projection does not add factual claims about NASA content.
- The provider-free artifact does not measure live model quality, billing, or
  production latency.
- Canonical `data/**` promotion is intentionally deferred until a separate
  ontology and release review confirms the required entity and relationship
  contracts.

## Release boundary

The package may be used by internal evaluation tooling after local validation.
Any publication, external distribution, production route change, or default
configuration change requires a separate human-authorized decision and is not
performed by the projection builder or consumer.

## Required checks

```bash
make canonical-rag-evidence-projection-validate
make validate
```
