# External RAG Source Review Checklist

This checklist is the human review boundary for the NASA-based external RAG
evidence bundle. The technical verifier can prove metadata completeness,
freshness, local hashes, and source-commit reachability. It cannot determine
licence permissions, endorsement implications, or whether a source remains
appropriate for a particular redistribution or commercial use.

## Review inputs

- bundle: `examples/fixtures/rkm-external-rag-evidence-bundle-v1.json`;
- report: `docs/maintenance/external-rag-evidence-report.md`;
- verifier command:

```bash
python3 scripts/verify-external-rag-evidence.py \
  --rag-root /mnt/c/Users/andrea.tarsi/projects/AI/BuildingRAGAgentsWithLLMs \
  --as-of-date 2026-07-30 \
  --max-age-days 30
```

## Per-source review

For each source in the bundle, the reviewer must independently confirm:

- the canonical URL resolves to the intended first-party source;
- the title and media kind describe the referenced page or asset accurately;
- the rights statement is sufficient for the intended use;
- attribution requirements are recorded and operationally feasible;
- third-party material, endorsement, and redistribution restrictions are
  understood;
- the retrieval date is acceptable for the claim and use case;
- the source identity hash and derived text are traceable to the declared
  corpus version.

## Decision

Record the reviewer, review date, scope, unresolved limitations, and decision
for every source. Until all required reviews are complete, retain:

```text
status: Draft
reviewState: Not Reviewed
productionPromotionAllowed: false
```

This checklist does not authorize changing those values. A later task must
define the reviewed-state contract and any canonical persistence migration.
