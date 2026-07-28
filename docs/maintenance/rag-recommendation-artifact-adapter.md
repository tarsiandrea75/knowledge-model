# RAG Recommendation Artifact Adapter

The RAG Engineering Lab is the execution system for corpus experiments. RKM
is the consumer that turns the resulting evidence into knowledge and policy
decisions. The boundary between them is the versioned
`rag-recommendation-report-v1` JSON artifact.

## Purpose

The adapter at
`scripts/import-rag-recommendation-artifact.py` performs a fail-closed
boundary check and emits an RKM ingestion envelope. It does not write RKM
data, infer missing evidence, or allow the language model to invent citations
or policy decisions.

The adapter accepts exactly these source fields:

- `contractVersion`: `rag-recommendation-report-v1`;
- `artifactType`: `RAG_RECOMMENDATION_REPORT`;
- `experimentId`, `policyVersion`, and `qualityFloor`;
- one recommendation each for `economical`, `balanced`, and `maximumQuality`.

Each recommendation preserves availability, pipeline identity, quality,
latency, estimated cost, currency, and the evidence-backed reason emitted by
the Lab. Unknown fields and non-finite numeric values are rejected.

## Usage

Run the adapter self-test:

```bash
python3 scripts/import-rag-recommendation-artifact.py --self-test
```

Convert a Lab artifact to an RKM envelope:

```bash
python3 scripts/import-rag-recommendation-artifact.py path/to/recommendation.json > rkm-envelope.json
```

The command exits with status `2` when the artifact is invalid. Validation
errors are written to stderr without echoing the artifact contents.

## Output boundary

The output contains three deliberately separate sections:

- `adapterContractVersion` identifies this consumer contract;
- `sourceArtifact` records the source contract, experiment, policy version,
  and quality floor;
- `policyDecision` contains the normalized recommendation profiles and a
  stable decision identifier derived from `experimentId`.

Persistence into RKM entities remains a separate step. That step must attach
the original artifact as evidence and preserve the experiment identifier,
policy version, metrics, and source provenance. It must not overwrite an
existing decision without an explicit versioning policy.

## Operational rules

Use artifacts produced by the Lab's declared contract only. Do not pass
credentials, document contents, prompts, or raw model responses through this
boundary. Before persistence, verify the experiment's corpus version and
evaluation dataset version so that a recommendation remains reproducible.

After changing the adapter or this contract documentation, run:

```bash
TMPDIR=/tmp make validate
```

