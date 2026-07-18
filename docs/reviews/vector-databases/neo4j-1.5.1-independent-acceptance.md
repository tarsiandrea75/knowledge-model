# Neo4j 1.5.1 Independent Acceptance Provenance

## Status and purpose

Neo4j record version `1.5.1` is currently **Approved**. This document is the durable RKM provenance index for the independent acceptance, lifecycle approval, and release integration of that record. It records the identities of immutable review-run artifacts without copying, rerunning, or rewriting their reviews.

This document is a historical evidence record, not a new review and not a competing lifecycle authority. The canonical JSON record remains the authority for the current lifecycle state.

## Canonical record binding

| Property | Bound value |
| --- | --- |
| Canonical record | `data/vector-databases/neo4j.json` |
| Entity identifier | `VECTOR-DATABASE-10011` |
| Record version | `1.5.1` |
| Current review state | `Approved` |
| Canonical file SHA-256 | `6ea8eb9ac34d995c3759a71ce7cf43e7c8ee6445947720bbb71354b3bb473e55` |
| Canonical Git blob | `c98ac1e352e216b712ccd2f3cdd84d9f9b986d82` |
| Approval commit | `a617864fff7f56b25f3a37ab259d727275648de4` |
| Release integration commit | `b41b206887fee1ace942b9bf939a4df7e0365b24` |

The approval commit contains the canonical blob identified above. The release integration commit contains the same blob at the same canonical path. This binds the current `Approved` review state to the exact repository content rather than to a path or version label alone.

## Independent acceptance evidence

The primary substantive acceptance evidence is the following immutable run artifact:

| Property | Value |
| --- | --- |
| Independent Neo4j acceptance run | `neo4j-acceptance-review-20260718T182701Z-788` |
| Report artifact | `independent-review.md` |
| Report SHA-256 | `121186cd598652dc54afcd99fbdb7690b494517ac16300e5bbd53a8eedbbbc01` |
| Verdict | `ACCEPT` |

The report states that the sole delegated `rkm_reviewer` performed the substantive review independently and read-only. It reviewed `data/vector-databases/neo4j.json` version `1.5.0` at commit `fcf4e171599b3a068afecb951048763e3af2ac77`, bound that reviewed target to Git object `ffd9ef356cbae2bcc2faf79e3c0d39d04d0c5ab3` and SHA-256 `df660096e74c466b9ece00d006129a52bcf6866a8ba3efa4807cad983250c856`, returned `ACCEPT`, recommended `Approved`, and explicitly left the lifecycle mutation to a separately authorized update.

Approval commit `a617864fff7f56b25f3a37ab259d727275648de4` performed that lifecycle update. Its Neo4j diff changed the record version from `1.5.0` to `1.5.1` and `metadata.reviewState` from `Changes Requested` to `Approved`; it did not alter the accepted substantive claims, evidence, references, capability boundaries, limitations, or guidance. The commit also updated the corresponding generated graph-export lifecycle fields. The independent report and the approval commit therefore form the primary acceptance-and-approval chain for version `1.5.1`.

## Findings disposition

The independent Neo4j report concluded that all four bounded corrections were resolved and that no required corrections remained:

1. **Encryption origins:** self-managed Neo4j TLS was separated as a product-core capability from host-platform storage-volume encryption, and neither was represented as Neo4j DBMS-core encryption at rest.
2. **Immutable provenance:** mutable and version-sensitive sources were version-pinned, commit-pinned, or digest-bound; no `/current/` reference remained, and Neo4j GraphRAG `1.17.0` behavior was tied to commit `7b69354deb8182eba067001ea23549a196f94404`.
3. **AuraDB Free recovery:** AuraDB Free was limited to its documented on-demand snapshot availability and excluded from the paid-plan restore, export, retention, and create-from-snapshot claims.
4. **Local licensing:** Community and Enterprise/Infinigraph licensing scopes covered both `Local` and `Self Hosted`, Aura remained scoped to `Managed Cloud`, and the RKM artifact license remained distinct from Neo4j product licensing.

The report also found no material regression, dangling mapping, contradictory guidance, stale export, schema failure, or unrelated substantive change. Its known limitations remain authoritative: it assessed documented semantics and source scope rather than live performance, recall, latency, cost, availability, or disaster-recovery execution; it did not use a private Aura plan or UI; mutable pages can change after capture; and legal applicability depends on the governing agreements and circumstances.

## Approval and integration chain

The provenance chain is:

1. Commit `fcf4e171599b3a068afecb951048763e3af2ac77` supplied the corrected Neo4j `1.5.0` content accepted by the independent Neo4j report.
2. Run `neo4j-acceptance-review-20260718T182701Z-788`, artifact `independent-review.md`, SHA-256 `121186cd598652dc54afcd99fbdb7690b494517ac16300e5bbd53a8eedbbbc01`, returned `ACCEPT` and recommended a separately authorized `Approved` lifecycle update.
3. Approval commit `a617864fff7f56b25f3a37ab259d727275648de4` applied that recommendation, created record version `1.5.1`, set `metadata.reviewState` to `Approved`, and produced canonical blob `c98ac1e352e216b712ccd2f3cdd84d9f9b986d82`.
4. Run `dataset-expansion-protected-merge-20260718T215653Z-788`, artifact `independent-review.md`, SHA-256 `584d8ba0b8bfef03bf77716d679ac49f95b2cacd6a43c15204663718c3798516`, returned `ACCEPT` for the staged integration candidate whose `MERGE_HEAD` was the approval commit.
5. Release integration commit `b41b206887fee1ace942b9bf939a4df7e0365b24` merged the dataset history and preserved canonical blob `c98ac1e352e216b712ccd2f3cdd84d9f9b986d82`.

The integration report is later corroborating evidence, not the original Neo4j re-review. It independently confirmed that Neo4j remained `Draft` with record version `1.5.1` and review state `Approved`; that its 22 structured capabilities and three licensing profiles retained their boundaries; that the canonical record, manifest, graph export, and decision-query projection agreed; and that the dataset commit history was preserved. Its integration verdict was `ACCEPT` with no required corrections.

## Relationship to historical review snapshots

`docs/reviews/vector-databases/independent-reviewer-pack.md` and `docs/reviews/vector-databases/graph-plus-vector-review-adjudication.md` are authoritative historical, commit-bound snapshots. The Reviewer Pack binds its Neo4j comparison to commit `74ca2d05ff02e051fafab189e0fcbc07892d3596`, before the pack-introduction and provenance-verification commits, and identifies the historical Neo4j blob and digest. The adjudication binds its decisions to commit `2979527681323a0704396b69afcdeed2c43e61ad` and the records as reviewed on that baseline.

Their `Not Reviewed`, `Changes Requested`, and `REVISION REQUIRED` statements accurately describe the record and review process at those historical baselines. They are not errors and must not be retroactively rewritten as current-state statements. Subsequent corrections, independent acceptance, lifecycle approval, and integration advanced the record after those snapshots. Readers seeking the present lifecycle state must consult `data/vector-databases/neo4j.json`.

## Verification procedure

From the repository root, a maintainer can recompute the canonical content bindings:

```bash
sha256sum data/vector-databases/neo4j.json
git hash-object data/vector-databases/neo4j.json
git ls-tree a617864fff7f56b25f3a37ab259d727275648de4 data/vector-databases/neo4j.json
git ls-tree b41b206887fee1ace942b9bf939a4df7e0365b24 data/vector-databases/neo4j.json
```

The first command must return `6ea8eb9ac34d995c3759a71ce7cf43e7c8ee6445947720bbb71354b3bb473e55`. Each Git-object command must return blob `c98ac1e352e216b712ccd2f3cdd84d9f9b986d82`.

From the archive directory that directly contains the immutable run directories, a maintainer can recompute both report digests:

```bash
sha256sum neo4j-acceptance-review-20260718T182701Z-788/independent-review.md
sha256sum dataset-expansion-protected-merge-20260718T215653Z-788/independent-review.md
```

The expected values are, respectively, `121186cd598652dc54afcd99fbdb7690b494517ac16300e5bbd53a8eedbbbc01` and `584d8ba0b8bfef03bf77716d679ac49f95b2cacd6a43c15204663718c3798516`. The archived reports remain immutable run artifacts; this repository document durably records their run identifiers, artifact filenames, content digests, verdicts, and relationship to the canonical Git history.

The lifecycle-only approval transition can be inspected with:

```bash
git show --format=fuller a617864fff7f56b25f3a37ab259d727275648de4 -- data/vector-databases/neo4j.json
git show --format=fuller --summary b41b206887fee1ace942b9bf939a4df7e0365b24
```

## Limitations and non-claims

- This document does not perform or rerun an independent review, replace either archived report, or expand their conclusions.
- The integration review alone did not serve as the original Neo4j re-review; it corroborated the already accepted and approved record during protected integration.
- This document does not create a second lifecycle authority. `metadata.reviewState` in the canonical JSON record is authoritative for current review state.
- This document records approval only for Neo4j entity `VECTOR-DATABASE-10011`. It does not claim approval for any of the other sixteen VectorDatabase records included in the dataset expansion.
- The evidence establishes repository review provenance and documented semantic acceptance. It does not establish unqualified product performance, availability, security, legal, or operational guarantees beyond the archived reports' stated scope.
- The archived report files are intentionally not copied into the repository; their exact identities are preserved through run identifiers, artifact filenames, and SHA-256 digests.

## Current-state interpretation

For the canonical record at `data/vector-databases/neo4j.json`, entity `VECTOR-DATABASE-10011`, version `1.5.1`, the current review state is **Approved**. `Approved` refers specifically to `metadata.reviewState`; the record's separate identity and metadata status fields remain `Draft`.

Historical `Not Reviewed`, `Changes Requested`, and `REVISION REQUIRED` statements continue to govern interpretation of their pinned historical baselines, while the canonical JSON governs the current lifecycle state. The acceptance report, approval commit, integration report, and release integration commit provide the durable provenance chain for that current interpretation.
