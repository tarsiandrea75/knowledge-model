# RKM Quickstart

This quickstart gives a technical user the shortest practical path to inspect and validate the current RAG Knowledge Model repository. `v0.1.0-alpha` remains the first internal alpha checkpoint; capabilities added later on the current experimental branch do not retroactively expand that historical release scope.

## 1. Clone the Repository

```bash
git clone <repository-url>
cd knowledge-model
```

Use the project root for all commands below.

## 2. Validate the Repository

```bash
make validate
```

`make validate` runs the repository validation suite. It checks JSON Schema validity, schema prerequisites, schema contracts, registries, fixture instances, data instances, graph export consistency, RKM unit tests, documentation relationship usage, whitespace, encoding, line endings, forbidden naming, and incomplete content markers.

## 3. Query Evidence-Backed Decisions

Use the decision-query CLI to turn populated RKM data into source-linked entity views, technique pipeline views, and same-type comparisons. The current branch supports the existing technique examples and manifest-declared VectorDatabase records. This remains limited coverage, not comprehensive RAG ecosystem coverage, and the CLI is not a stable public API. VectorDatabase records and comparison mode were added after the alpha checkpoint.

For a compact Hybrid Retrieval decision brief, run:

```bash
python3 scripts/rkm-decision-query.py \
  --entity hybrid-retrieval
```

Text output defaults to `--detail compact`. Compact mode is a selective text presentation of the same complete decision model: it retains every recorded claim and shows source links, important experimental context, limitations, status, review state, and evaluation guidance.

For the full Reranking evidence view, run:

```bash
python3 scripts/rkm-decision-query.py \
  --entity reranking \
  --detail full
```

Full mode exposes all qualifiers, complete evidence interpretation, every recorded limitation, source-fragment locators, and complete source metadata.

For a full VectorDatabase entity view, run:

```bash
python3 scripts/rkm-decision-query.py \
  --entity neo4j \
  --detail full
```

All 17 manifest-declared VectorDatabase records retain `Draft` status. Neo4j alone has `metadata.reviewState` set to `Approved`; the other sixteen remain `Not Reviewed`. That approval applies only to the exact Neo4j record and review scope and does not turn the record into release approval or product guidance.

To inspect how the two techniques are modeled in a requested stage order, run:

```bash
python3 scripts/rkm-decision-query.py \
  --pipeline hybrid-retrieval reranking
```

The pipeline view presents the requested stage order, discovers direct canonical workflow relationships, and keeps each finding attributed to its technique. It does not numerically compare results from unrelated benchmarks, claim that the combined pipeline is universally superior, or imply that Reranking is mandatory after Hybrid Retrieval. Current relationship support is classified as `Maintainer rationale only`, not empirical validation.

To compare two VectorDatabase records of the same canonical entity type, run:

```bash
python3 scripts/rkm-decision-query.py \
  --compare neo4j qdrant
```

Comparison output is deterministic, descriptive, non-ranking, and evidence-traceable. It aligns recorded fields but does not select a winner or recommend a product. Matching values do not prove semantic equivalence, and an absent value means only that it is not recorded, not that the capability is unsupported.

For complete machine-readable output suitable for scripts and downstream consumers, use JSON:

```bash
python3 scripts/rkm-decision-query.py \
  --entity hybrid-retrieval \
  --format json

python3 scripts/rkm-decision-query.py \
  --pipeline hybrid-retrieval reranking \
  --format json

python3 scripts/rkm-decision-query.py \
  --compare neo4j qdrant \
  --format json
```

JSON always contains the complete entity, pipeline, or comparison model. `--detail compact` and `--detail full` affect text presentation only.

To inspect all CLI options, run:

```bash
python3 scripts/rkm-decision-query.py --help
```

**Evidence warning:** Current records may be `Draft` or `Not Reviewed`. Findings are bounded by their recorded datasets, metrics, models, hardware, and other qualifiers. A modeled relationship does not establish universal architecture guidance; inspect every limitation before applying a finding to another system.

## 4. Inspect Fixtures

```bash
ls examples/fixtures
```

Fixtures are small, controlled examples used to demonstrate valid schema shape and validation behavior. They are intended for learning, testing, and export checks. They are not the populated knowledge dataset.

## 5. Inspect Data

```bash
ls data
```

Data files are populated RKM knowledge instances. The current alpha includes a small validated seed dataset for consumer testing and feedback. It is not a complete RAG catalog.

## 6. Generate the Graph Export

```bash
make graph-export
```

This regenerates the minimal fixture-derived graph export.

## 7. Inspect the Graph Export

```bash
ls examples/graph-export
```

The current graph export is intentionally minimal. It proves the first export path from fixtures into graph nodes and edges.

## 8. Read the Consumer Guide

Read `docs/maintenance/consumer-guide.md` for the current consumption contract, stability expectations, validation details, and guidance for internal evaluation of `v0.1.0-alpha`.

## 9. Optional Pre-Tag Readiness Check

```bash
make release-check
```

`make release-check` is a stricter maintainer command for final `v0.1.0-alpha` pre-tag readiness. It requires a clean repository, checks local alignment with `origin/main` when that ref is available, runs validation, regenerates the graph export, and validates again. Use it before intentionally creating a git tag, not during ordinary dirty-worktree development.
