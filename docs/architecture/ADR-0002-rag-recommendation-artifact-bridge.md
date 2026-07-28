# ADR-0002
# Establish a RAG Recommendation Artifact Bridge

**Status**

Accepted

---

## Context

The RAG Engineering Lab executes corpus experiments and emits the versioned
`rag-recommendation-report-v1` artifact. RKM describes RAG knowledge,
evaluation semantics and decision boundaries. The two repositories must
exchange evidence without sharing implementation classes, database state or
provider credentials.

The Lab artifact already contains three quality/cost profiles, experiment
identity, policy version, quality floor, pipeline identity, latency, estimated
cost and recommendation rationale. RKM already models reusable Artifact,
Evaluation and embedded Policy concepts. The missing piece is a strict,
versioned consumer boundary that preserves the Lab report as evidence and
prevents an importer from silently inventing RKM knowledge.

## Decision

Establish a provider-neutral RAG recommendation artifact bridge with three
explicit boundaries:

1. The Lab report is the immutable source artifact. Its contract version,
   artifact type, experiment identifier, policy version and recommendation
   values remain unchanged at the RKM boundary.
2. RKM consumes a separate, strict adapter envelope identified by
   `rkm-recommendation-artifact-adapter-v1`. The envelope records source
   identity and a normalized policy decision, but it is not itself a new RAG
   technique, benchmark, provider or model claim.
3. Materialization into RKM knowledge uses existing Artifact, Evaluation and
   embedded Policy semantics wherever they fit. The first bridge phase does
   not introduce a new first-class `RagRecommendation` entity or a billing
   model. A new entity is justified only if a concrete consumer query cannot
   be represented by the existing model without loss of provenance.

The bridge is fail-closed. It rejects unknown fields, unsupported contract
versions, missing profiles, profile mismatches, invalid quality or cost
ranges, non-finite numbers and malformed identifiers. It must never infer a
winner from missing evidence or convert a model-generated rationale into an
independent RKM claim without preserving its source artifact and evaluation
context.

## Exchange shape

The initial exchange has this conceptual shape:

```text
RAG Lab recommendation report
    -> strict adapter validation
    -> RKM adapter envelope
    -> validated Artifact/Evaluation/Policy materialization
```

The envelope must preserve:

- source contract version and artifact type;
- experiment and policy identifiers;
- quality floor;
- economical, balanced and maximum-quality profiles;
- pipeline identity, availability, quality score, p95 latency, estimated
  cost, currency and rationale;
- provenance needed to locate the original Lab artifact.

The adapter envelope is transport and ingestion infrastructure. Domain
meaning remains authoritative in the source report and in the validated RKM
records produced from it.

## Consequences

Positive consequences:

- The Lab and RKM remain independently buildable and testable.
- Recommendation evidence can be replayed without provider calls.
- RKM consumers can compare cost and quality without treating a recommendation
  as an unconditional truth.
- Contract failures are visible before persistence.
- The design leaves room for future metrics, datasets and profile types through
  explicit contract versioning rather than silent schema drift.

Negative consequences:

- The first bridge requires an additional validation and materialization step.
- Some RKM consumers will initially need the source artifact and envelope
  together until a persistent integration record is introduced.
- Adding a new profile or metric requires a contract review and likely a new
  contract version.

## Scope of the next implementation slices

The next slices are intentionally ordered:

1. Add a machine-readable RKM-side envelope schema and a minimal valid fixture.
2. Extend validation and self-tests for source provenance, profile integrity
   and fail-closed behavior.
3. Make the adapter emit the schema-valid envelope from a Lab artifact.
4. Add a deterministic end-to-end fixture proving Lab artifact to RKM envelope
   conversion without network, credentials or paid model calls.

Persistence into populated RKM data and consumer query APIs follow only after
these contract and replay guarantees pass review.

