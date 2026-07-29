# RAG Recommendation Consumer Walkthrough

## Purpose

This walkthrough demonstrates the bounded RAG-to-RKM consumer path using the
existing `rag-recommendation-report-v1` adapter. It validates a lab-shaped
source artifact, emits the RKM adapter envelope, validates that envelope
against the checked-in RKM schema, and inspects the policy profiles.

The checked-in input is a compatibility fixture. It is not a live provider
run, a production recommendation, or a universal ranking of RAG strategies.
When the RAG Engineering Lab produces a real report, substitute that report
for the fixture without changing the adapter or schema commands.

## Preconditions

Run from the RKM repository root with Python and the repository validation
dependencies installed:

```bash
make validate
```

The source contract and RKM adapter are intentionally separate:

- source contract: `rag-recommendation-report-v1`;
- adapter envelope: `rkm-recommendation-artifact-adapter-v1`;
- source fixture: `examples/fixtures/rag-recommendation-report-v1.json`;
- generated RAG fixture: `examples/fixtures/rag-recommendation-report-v1-generated.json`;
- cross-index review fixture: `examples/fixtures/rag-recommendation-report-v1-index-review.json`;
- adapter: `scripts/import-rag-recommendation-artifact.py`;
- envelope schema: `schema/rag-recommendation-artifact-adapter-v1.schema.json`.

## Consume the generated RAG artifact

From the RAG repository, first run the provider-free walkthrough:

```bash
mvn -q -Dtest=OfflineRagExecutionWalkthroughTest test
```

It emits `target/rag-eval/rag-recommendation-report-v1-generated.json`. The
same deterministic output is preserved in the RKM generated fixture and can
be passed directly to the adapter:

```bash
python3 scripts/import-rag-recommendation-artifact.py \
  examples/fixtures/rag-recommendation-report-v1-generated.json \
  > /tmp/rkm-generated-envelope.json
```

The generated report identifies experiment `offline-rag-e2e-walkthrough`,
policy `quality-cost-profiles-v1`, pipeline `naive`, and index profile
`offline-fixture-index-v1`. It remains compatibility evidence; consuming it
does not persist a canonical decision or promote a production route.

## Create the review-ready decision record

The persistence adapter creates an RKM-owned decision record only after the
source envelope and explicit provenance metadata are available. Its default
lifecycle is `Draft` and `Not Reviewed`, and production promotion is always
false:

```bash
python3 scripts/persist-rag-recommendation-decision.py --self-test
```

The checked-in result is
`examples/fixtures/rkm-rag-recommendation-decision-v1.json`. It is validated by
the fixture manifest and remains a review-ready evidence projection, not a
canonical production policy or automatic route change.

## Execute the walkthrough

Use a temporary directory outside the repository for generated output:

```bash
WORK_DIR="$(mktemp -d /tmp/rkm-recommendation-walkthrough.XXXXXX)"
python3 scripts/import-rag-recommendation-artifact.py \
  examples/fixtures/rag-recommendation-report-v1.json \
  > "$WORK_DIR/envelope.json"
python3 -c '
import json, sys
from jsonschema import Draft202012Validator

with open("schema/rag-recommendation-artifact-adapter-v1.schema.json", encoding="utf-8") as handle:
    schema = json.load(handle)
with open(sys.argv[1], encoding="utf-8") as handle:
    envelope = json.load(handle)

errors = sorted(Draft202012Validator(schema).iter_errors(envelope), key=lambda error: list(error.path))
if errors:
    raise SystemExit("envelope schema validation failed: " + "; ".join(error.message for error in errors))
print("envelope schema validation passed")
print("adapterContractVersion=" + envelope["adapterContractVersion"])
print("decisionId=" + envelope["policyDecision"]["decisionId"])
for name, recommendation in envelope["policyDecision"]["profiles"].items():
    print(name + "=" + recommendation["pipelineId"])
' "$WORK_DIR/envelope.json"
```

Expected output includes:

```text
envelope schema validation passed
adapterContractVersion=rkm-recommendation-artifact-adapter-v1
decisionId=rkm-consumer-walkthrough-001:recommendation
economical=NAIVE
balanced=NAIVE
maximumQuality=NAIVE
```

Run the adapter boundary self-test separately:

```bash
make rag-recommendation-adapter-test
```

## Consuming a real lab artifact

The RAG Engineering Lab owns production experiment execution and artifact
generation. A consumer must receive the resulting JSON as an ordinary input
file, then replace the fixture path in the command above. The consumer must
not infer missing fields, rewrite contract versions, or treat a rejected
artifact as a recommendation.

The RKM envelope preserves:

- source contract and artifact type;
- experiment and policy identity;
- quality floor;
- all three quality/cost recommendation profiles;
- index profile identity when supplied by a multi-index report;
- a deterministic policy-decision identity derived from the experiment ID.

The adapter does not persist the envelope into canonical RKM data. Persistence
as Evaluation, Artifact, or Policy Decision entities requires a separate
reviewed task with provenance, lifecycle, and compatibility decisions.

The cross-index review fixture demonstrates the fail-closed case. Its three
profiles remain unavailable and retain `INDEX_PROFILE_REVIEW_REQUIRED`; no
consumer-side selection is allowed.

## Failure behavior and limits

The adapter rejects unknown fields, missing fields, unsupported contract
versions and artifact types, malformed profile objects, invalid numeric ranges,
and profile identifiers that do not match their declared profile. Parser
details and source contents are not echoed as public error output.

This walkthrough proves structural interoperability only. It does not prove
that a recommended pipeline is suitable for every corpus, authorize automatic
production promotion, convert an unavailable recommendation into an available
one, or replace independent evaluation evidence.

## Cleanup

Generated output is outside the repository. Remove the temporary directory
after inspection when the walkthrough is complete:

```bash
rm -rf "$WORK_DIR"
```

The cleanup target is the walkthrough-specific temporary directory only; do
not use it against a repository or an unresolved broad path.
