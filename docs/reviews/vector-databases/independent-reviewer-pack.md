# RKM Vector Database Independent Reviewer Pack

## Purpose

Review canonical VectorDatabase records independently from their creation.
The comparison output is descriptive and non-ranking. A matching value does
not prove semantic equivalence, and a missing value means not recorded rather
than unsupported.

## Baseline and provenance

- Branch: `experiment/dataset-expansion`
- Comparison-data commit:
  `74ca2d05ff02e051fafab189e0fcbc07892d3596`
- Reviewer Pack introduction commit:
  `2979527681323a0704396b69afcdeed2c43e61ad`
- Provenance verification commit:
  `866c41636e6ad91c82310874f9803e1263b3ce85`
- Records remain `Draft` and `Not Reviewed`.
- No record should be modified during the initial read-only review.

The comparison output was generated from the three canonical records as they
existed at the comparison-data commit. The Reviewer Pack was added by the next
commit without modifying those records. The later adjudication commit also did
not modify them.

The record contents were verified as identical across all three commits using
both Git blob identifiers and SHA-256 content hashes:

| Record | Git blob | SHA-256 |
|---|---|---|
| `data/vector-databases/neo4j.json` | `24082b87e8ae4aafe17aa7abd6d00a101c25e828` | `8f59da948793cf956c78d1c5754608b4d38983b9d82b14d7640f17d12ccc85b7` |
| `data/vector-databases/amazon-neptune-analytics.json` | `f058559f9183c449ebde7edfe93e5a0aa302d6f3` | `bea14fcf4c81e6058696c90907ba17aa6be8ee4a708820dd386143fdc4ecac4e` |
| `data/vector-databases/memgraph.json` | `76798c56ce058f3536fe59f8c311cddb826d25b0` | `49b9581e922762968fb98ccbcea14f93556cc742ef6c3d6e265c21c8ff500670` |

The distinction between the comparison-data commit and the Reviewer Pack
introduction commit is therefore an artifact-provenance distinction, not a
record-content difference.

## Required verdicts

- `APPROVED`
- `APPROVED WITH MINOR CHANGES`
- `REVISION REQUIRED`
- `REJECTED`

## Group: Graph plus vector

Compared entities:

- `VECTOR-DATABASE-10011` — Neo4j (`neo4j`; Draft; Not Reviewed)
- `VECTOR-DATABASE-10016` — Amazon Neptune Analytics (`amazon-neptune-analytics`; Draft; Not Reviewed)
- `VECTOR-DATABASE-10017` — Memgraph (`memgraph`; Draft; Not Reviewed)

### RV-001 — Operational Characteristics / Supported Modalities

- **Initial severity:** `HIGH`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `["Text", "Code", "Image", "Audio", "Video", "Table", "Multimodal"]`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `["Text", "Code", "Image", "Audio", "Video", "Table", "Multimodal"]`
  - `VECTOR-DATABASE-10017` — Memgraph: `["Text", "Code", "Image", "Audio", "Video", "Table", "Multimodal"]`
- **Reviewer question:** Determine whether modalities describe a database capability or merely the type of embeddings that can be stored.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-002 — Operational Characteristics / Metadata Filtering / Pre Filter Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Different`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `True`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `True`
  - `VECTOR-DATABASE-10017` — Memgraph: `False`
- **Reviewer question:** Verify that pre-filtering has the same operational meaning for every product and query API.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-003 — Operational Characteristics / Metadata Filtering / Post Filter Supported

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `True`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `True`
  - `VECTOR-DATABASE-10017` — Memgraph: `True`
- **Reviewer question:** Verify missing values and distinguish native post-filtering from application-side filtering.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-004 — Operational Characteristics / Hybrid Search / Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `True`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `True`
  - `VECTOR-DATABASE-10017` — Memgraph: `True`
- **Reviewer question:** Distinguish native hybrid retrieval from composition requiring an external search engine, SQL query, graph traversal, or application logic.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-005 — Operational Characteristics / Hybrid Search / Score Normalization Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `False`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `False`
  - `VECTOR-DATABASE-10017` — Memgraph: `False`
- **Reviewer question:** Clarify whether the field means automatic normalization, configurable fusion, or merely the ability to combine scores manually.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-006 — Operational Characteristics / Scalability / Horizontal Scaling

- **Initial severity:** `HIGH`
- **Comparison status:** `Different`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `High`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `High`
  - `VECTOR-DATABASE-10017` — Memgraph: `Medium`
- **Reviewer question:** Identify the measurable criteria behind High, Medium, and Variable.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-007 — Operational Characteristics / Scalability / Sharding Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Different`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `True`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `False`
  - `VECTOR-DATABASE-10017` — Memgraph: `False`
- **Reviewer question:** Separate product-native sharding from capabilities inherited from an underlying database, extension, or managed service.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-008 — Operational Characteristics / Scalability / Replication Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `True`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `True`
  - `VECTOR-DATABASE-10017` — Memgraph: `True`
- **Reviewer question:** Separate product-native replication from the hosting platform or underlying database.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-009 — Operational Characteristics / Scalability / Disk Backed Indexing Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Different`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `True`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `False`
  - `VECTOR-DATABASE-10017` — Memgraph: `False`
- **Reviewer question:** Define whether this means the ANN index itself is disk-resident, memory-mapped, persisted, or merely reloadable from durable storage.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-010 — Operational Characteristics / Consistency / Consistency Model

- **Initial severity:** `HIGH`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `Configurable`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `Configurable`
  - `VECTOR-DATABASE-10017` — Memgraph: `Configurable`
- **Reviewer question:** Verify scope: metadata writes, vector visibility, replicas, graph updates, and query results may have different consistency semantics.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-011 — Operational Characteristics / Consistency / Transaction Support

- **Initial severity:** `HIGH`
- **Comparison status:** `Different`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `Full ACID`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `Limited`
  - `VECTOR-DATABASE-10017` — Memgraph: `Limited`
- **Reviewer question:** Define the transaction boundary and distinguish Full ACID, Document Level, Limited, and None using equivalent criteria.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-012 — Operational Characteristics / Operations / Access Control

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Different`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `Variable`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `High`
  - `VECTOR-DATABASE-10017` — Memgraph: `Variable`
- **Reviewer question:** Replace or qualify coarse High and Variable labels with edition, plan, deployment, and IAM context.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-013 — Operational Characteristics / Operations / Encryption

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `High`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `High`
  - `VECTOR-DATABASE-10017` — Memgraph: `High`
- **Reviewer question:** Distinguish encryption in transit, at rest, customer-managed keys, and deployment-dependent behavior.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-014 — Operational Characteristics / Operations / Backup And Restore

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `High`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `High`
  - `VECTOR-DATABASE-10017` — Memgraph: `High`
- **Reviewer question:** Verify whether backup and restore are product-native, provider-managed, edition-dependent, or externally orchestrated.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-015 — Operational Characteristics / Operations / Observability

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `High`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `High`
  - `VECTOR-DATABASE-10017` — Memgraph: `High`
- **Reviewer question:** Qualify metrics, logs, tracing, audit events, and provider integrations.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-016 — Operational Characteristics / Operations / Multi Tenancy

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `Variable`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `Variable`
  - `VECTOR-DATABASE-10017` — Memgraph: `Variable`
- **Reviewer question:** Clarify logical namespaces, database isolation, account isolation, and edition or service-plan constraints.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-017 — Evidence Coverage / Claim Count

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `5`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `5`
  - `VECTOR-DATABASE-10017` — Memgraph: `5`
- **Reviewer question:** Check whether identical claim counts reflect natural evidence coverage or a fixed authoring template.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-018 — Evidence Coverage / Evidence Count

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `5`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `5`
  - `VECTOR-DATABASE-10017` — Memgraph: `5`
- **Reviewer question:** Check whether one-evidence-per-claim was imposed mechanically.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-019 — Evidence Coverage / Residual Limitation Count

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10011` — Neo4j: `10`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `10`
  - `VECTOR-DATABASE-10017` — Memgraph: `10`
- **Reviewer question:** Check whether identical limitation counts reflect product reality or a fixed template.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### Complete evidence commands

```bash
python3 scripts/rkm-decision-query.py --entity neo4j --detail full
```

```bash
python3 scripts/rkm-decision-query.py --entity amazon-neptune-analytics --detail full
```

```bash
python3 scripts/rkm-decision-query.py --entity memgraph --detail full
```

## Group: Self-hosted vector storage

Compared entities:

- `VECTOR-DATABASE-10001` — pgvector (`pgvector`; Draft; Not Reviewed)
- `VECTOR-DATABASE-10002` — Qdrant (`qdrant`; Draft; Not Reviewed)
- `VECTOR-DATABASE-10003` — Weaviate (`weaviate`; Draft; Not Reviewed)
- `VECTOR-DATABASE-10004` — Milvus (`milvus`; Draft; Not Reviewed)

### RV-020 — Operational Characteristics / Metadata Filtering / Pre Filter Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `True`
  - `VECTOR-DATABASE-10002` — Qdrant: `True`
  - `VECTOR-DATABASE-10003` — Weaviate: `True`
  - `VECTOR-DATABASE-10004` — Milvus: `True`
- **Reviewer question:** Verify that pre-filtering has the same operational meaning for every product and query API.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-021 — Operational Characteristics / Metadata Filtering / Post Filter Supported

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Incomplete`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `True`
  - `VECTOR-DATABASE-10002` — Qdrant: `Not recorded`
  - `VECTOR-DATABASE-10003` — Weaviate: `Not recorded`
  - `VECTOR-DATABASE-10004` — Milvus: `Not recorded`
- **Reviewer question:** Verify missing values and distinguish native post-filtering from application-side filtering.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-022 — Operational Characteristics / Hybrid Search / Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `True`
  - `VECTOR-DATABASE-10002` — Qdrant: `True`
  - `VECTOR-DATABASE-10003` — Weaviate: `True`
  - `VECTOR-DATABASE-10004` — Milvus: `True`
- **Reviewer question:** Distinguish native hybrid retrieval from composition requiring an external search engine, SQL query, graph traversal, or application logic.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-023 — Operational Characteristics / Scalability / Horizontal Scaling

- **Initial severity:** `HIGH`
- **Comparison status:** `Different`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `Variable`
  - `VECTOR-DATABASE-10002` — Qdrant: `High`
  - `VECTOR-DATABASE-10003` — Weaviate: `High`
  - `VECTOR-DATABASE-10004` — Milvus: `High`
- **Reviewer question:** Identify the measurable criteria behind High, Medium, and Variable.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-024 — Operational Characteristics / Scalability / Sharding Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `True`
  - `VECTOR-DATABASE-10002` — Qdrant: `True`
  - `VECTOR-DATABASE-10003` — Weaviate: `True`
  - `VECTOR-DATABASE-10004` — Milvus: `True`
- **Reviewer question:** Separate product-native sharding from capabilities inherited from an underlying database, extension, or managed service.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-025 — Operational Characteristics / Scalability / Replication Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `True`
  - `VECTOR-DATABASE-10002` — Qdrant: `True`
  - `VECTOR-DATABASE-10003` — Weaviate: `True`
  - `VECTOR-DATABASE-10004` — Milvus: `True`
- **Reviewer question:** Separate product-native replication from the hosting platform or underlying database.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-026 — Operational Characteristics / Scalability / Disk Backed Indexing Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `True`
  - `VECTOR-DATABASE-10002` — Qdrant: `True`
  - `VECTOR-DATABASE-10003` — Weaviate: `True`
  - `VECTOR-DATABASE-10004` — Milvus: `True`
- **Reviewer question:** Define whether this means the ANN index itself is disk-resident, memory-mapped, persisted, or merely reloadable from durable storage.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-027 — Operational Characteristics / Consistency / Consistency Model

- **Initial severity:** `HIGH`
- **Comparison status:** `Different`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `Strong`
  - `VECTOR-DATABASE-10002` — Qdrant: `Configurable`
  - `VECTOR-DATABASE-10003` — Weaviate: `Configurable`
  - `VECTOR-DATABASE-10004` — Milvus: `Configurable`
- **Reviewer question:** Verify scope: metadata writes, vector visibility, replicas, graph updates, and query results may have different consistency semantics.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-028 — Operational Characteristics / Consistency / Transaction Support

- **Initial severity:** `HIGH`
- **Comparison status:** `Different`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `Full ACID`
  - `VECTOR-DATABASE-10002` — Qdrant: `Limited`
  - `VECTOR-DATABASE-10003` — Weaviate: `Limited`
  - `VECTOR-DATABASE-10004` — Milvus: `Limited`
- **Reviewer question:** Define the transaction boundary and distinguish Full ACID, Document Level, Limited, and None using equivalent criteria.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-029 — Evidence Coverage / Claim Count

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `5`
  - `VECTOR-DATABASE-10002` — Qdrant: `5`
  - `VECTOR-DATABASE-10003` — Weaviate: `5`
  - `VECTOR-DATABASE-10004` — Milvus: `5`
- **Reviewer question:** Check whether identical claim counts reflect natural evidence coverage or a fixed authoring template.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-030 — Evidence Coverage / Evidence Count

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `5`
  - `VECTOR-DATABASE-10002` — Qdrant: `5`
  - `VECTOR-DATABASE-10003` — Weaviate: `5`
  - `VECTOR-DATABASE-10004` — Milvus: `5`
- **Reviewer question:** Check whether one-evidence-per-claim was imposed mechanically.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-031 — Evidence Coverage / Residual Limitation Count

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `10`
  - `VECTOR-DATABASE-10002` — Qdrant: `10`
  - `VECTOR-DATABASE-10003` — Weaviate: `10`
  - `VECTOR-DATABASE-10004` — Milvus: `10`
- **Reviewer question:** Check whether identical limitation counts reflect product reality or a fixed template.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-032 — Operational Characteristics / Hybrid Search / Score Normalization Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Incomplete`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `Not recorded`
  - `VECTOR-DATABASE-10002` — Qdrant: `True`
  - `VECTOR-DATABASE-10003` — Weaviate: `True`
  - `VECTOR-DATABASE-10004` — Milvus: `True`
- **Reviewer question:** Clarify whether the field means automatic normalization, configurable fusion, or merely the ability to combine scores manually.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-033 — Operational Characteristics / Integration / Sdk Languages

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Incomplete`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `Not recorded`
  - `VECTOR-DATABASE-10002` — Qdrant: `["Python", "Java", "JavaScript", "TypeScript", "Go", "Rust", "C#"]`
  - `VECTOR-DATABASE-10003` — Weaviate: `["Python", "Java", "JavaScript", "TypeScript", "Go"]`
  - `VECTOR-DATABASE-10004` — Milvus: `["Python", "Java", "JavaScript", "TypeScript", "Go", "C#"]`
- **Reviewer question:** Determine whether the missing value represents unavailable knowledge, an unsupported capability, or an authoring omission.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-034 — Operational Characteristics / Operations / Access Control

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Incomplete`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `Not recorded`
  - `VECTOR-DATABASE-10002` — Qdrant: `Not recorded`
  - `VECTOR-DATABASE-10003` — Weaviate: `High`
  - `VECTOR-DATABASE-10004` — Milvus: `High`
- **Reviewer question:** Replace or qualify coarse High and Variable labels with edition, plan, deployment, and IAM context.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-035 — Operational Characteristics / Operations / Encryption

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Incomplete`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `Not recorded`
  - `VECTOR-DATABASE-10002` — Qdrant: `Not recorded`
  - `VECTOR-DATABASE-10003` — Weaviate: `Variable`
  - `VECTOR-DATABASE-10004` — Milvus: `Variable`
- **Reviewer question:** Distinguish encryption in transit, at rest, customer-managed keys, and deployment-dependent behavior.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-036 — Operational Characteristics / Operations / Backup And Restore

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Incomplete`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `Not recorded`
  - `VECTOR-DATABASE-10002` — Qdrant: `Not recorded`
  - `VECTOR-DATABASE-10003` — Weaviate: `High`
  - `VECTOR-DATABASE-10004` — Milvus: `High`
- **Reviewer question:** Verify whether backup and restore are product-native, provider-managed, edition-dependent, or externally orchestrated.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-037 — Operational Characteristics / Operations / Observability

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Incomplete`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `Not recorded`
  - `VECTOR-DATABASE-10002` — Qdrant: `Not recorded`
  - `VECTOR-DATABASE-10003` — Weaviate: `High`
  - `VECTOR-DATABASE-10004` — Milvus: `High`
- **Reviewer question:** Qualify metrics, logs, tracing, audit events, and provider integrations.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-038 — Operational Characteristics / Operations / Multi Tenancy

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Incomplete`
- **Recorded values:**
  - `VECTOR-DATABASE-10001` — pgvector: `Not recorded`
  - `VECTOR-DATABASE-10002` — Qdrant: `Not recorded`
  - `VECTOR-DATABASE-10003` — Weaviate: `High`
  - `VECTOR-DATABASE-10004` — Milvus: `High`
- **Reviewer question:** Clarify logical namespaces, database isolation, account isolation, and edition or service-plan constraints.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### Complete evidence commands

```bash
python3 scripts/rkm-decision-query.py --entity pgvector --detail full
```

```bash
python3 scripts/rkm-decision-query.py --entity qdrant --detail full
```

```bash
python3 scripts/rkm-decision-query.py --entity weaviate --detail full
```

```bash
python3 scripts/rkm-decision-query.py --entity milvus --detail full
```

## Group: Managed vector search

Compared entities:

- `VECTOR-DATABASE-10005` — Pinecone (`pinecone`; Draft; Not Reviewed)
- `VECTOR-DATABASE-10014` — Azure AI Search (`azure-ai-search`; Draft; Not Reviewed)
- `VECTOR-DATABASE-10015` — Vertex AI Vector Search (`vertex-ai-vector-search`; Draft; Not Reviewed)
- `VECTOR-DATABASE-10016` — Amazon Neptune Analytics (`amazon-neptune-analytics`; Draft; Not Reviewed)

### RV-039 — Operational Characteristics / Metadata Filtering / Pre Filter Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `True`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `True`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `True`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `True`
- **Reviewer question:** Verify that pre-filtering has the same operational meaning for every product and query API.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-040 — Operational Characteristics / Hybrid Search / Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `True`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `True`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `True`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `True`
- **Reviewer question:** Distinguish native hybrid retrieval from composition requiring an external search engine, SQL query, graph traversal, or application logic.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-041 — Operational Characteristics / Hybrid Search / Score Normalization Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `False`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `False`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `False`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `False`
- **Reviewer question:** Clarify whether the field means automatic normalization, configurable fusion, or merely the ability to combine scores manually.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-042 — Operational Characteristics / Scalability / Horizontal Scaling

- **Initial severity:** `HIGH`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `High`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `High`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `High`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `High`
- **Reviewer question:** Identify the measurable criteria behind High, Medium, and Variable.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-043 — Operational Characteristics / Scalability / Sharding Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Different`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `True`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `True`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `True`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `False`
- **Reviewer question:** Separate product-native sharding from capabilities inherited from an underlying database, extension, or managed service.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-044 — Operational Characteristics / Scalability / Replication Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `True`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `True`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `True`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `True`
- **Reviewer question:** Separate product-native replication from the hosting platform or underlying database.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-045 — Operational Characteristics / Scalability / Disk Backed Indexing Supported

- **Initial severity:** `HIGH`
- **Comparison status:** `Different`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `True`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `False`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `True`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `False`
- **Reviewer question:** Define whether this means the ANN index itself is disk-resident, memory-mapped, persisted, or merely reloadable from durable storage.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-046 — Operational Characteristics / Consistency / Consistency Model

- **Initial severity:** `HIGH`
- **Comparison status:** `Different`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `Eventual`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `Eventual`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `Eventual`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `Configurable`
- **Reviewer question:** Verify scope: metadata writes, vector visibility, replicas, graph updates, and query results may have different consistency semantics.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-047 — Operational Characteristics / Consistency / Transaction Support

- **Initial severity:** `HIGH`
- **Comparison status:** `Different`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `None`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `Document Level`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `Document Level`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `Limited`
- **Reviewer question:** Define the transaction boundary and distinguish Full ACID, Document Level, Limited, and None using equivalent criteria.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-048 — Operational Characteristics / Operations / Access Control

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `High`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `High`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `High`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `High`
- **Reviewer question:** Replace or qualify coarse High and Variable labels with edition, plan, deployment, and IAM context.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-049 — Operational Characteristics / Operations / Encryption

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `High`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `High`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `High`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `High`
- **Reviewer question:** Distinguish encryption in transit, at rest, customer-managed keys, and deployment-dependent behavior.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-050 — Operational Characteristics / Operations / Backup And Restore

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Different`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `High`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `Variable`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `Variable`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `High`
- **Reviewer question:** Verify whether backup and restore are product-native, provider-managed, edition-dependent, or externally orchestrated.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-051 — Operational Characteristics / Operations / Observability

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `High`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `High`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `High`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `High`
- **Reviewer question:** Qualify metrics, logs, tracing, audit events, and provider integrations.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-052 — Operational Characteristics / Operations / Multi Tenancy

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Different`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `High`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `Variable`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `Variable`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `Variable`
- **Reviewer question:** Clarify logical namespaces, database isolation, account isolation, and edition or service-plan constraints.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-053 — Evidence Coverage / Claim Count

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `5`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `5`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `5`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `5`
- **Reviewer question:** Check whether identical claim counts reflect natural evidence coverage or a fixed authoring template.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-054 — Evidence Coverage / Evidence Count

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `5`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `5`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `5`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `5`
- **Reviewer question:** Check whether one-evidence-per-claim was imposed mechanically.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-055 — Evidence Coverage / Residual Limitation Count

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Same`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `10`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `10`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `10`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `10`
- **Reviewer question:** Check whether identical limitation counts reflect product reality or a fixed template.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-056 — Operational Characteristics / Supported Modalities

- **Initial severity:** `HIGH`
- **Comparison status:** `Incomplete`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `Not recorded`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `["Text", "Code", "Image", "Multimodal"]`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `["Text", "Code", "Image", "Audio", "Video", "Table", "Multimodal"]`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `["Text", "Code", "Image", "Audio", "Video", "Table", "Multimodal"]`
- **Reviewer question:** Determine whether modalities describe a database capability or merely the type of embeddings that can be stored.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-057 — Operational Characteristics / Metadata Filtering / Post Filter Supported

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Incomplete`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `Not recorded`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `True`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `False`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `True`
- **Reviewer question:** Verify missing values and distinguish native post-filtering from application-side filtering.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### RV-058 — Operational Characteristics / Consistency / Streaming Updates Supported

- **Initial severity:** `MEDIUM`
- **Comparison status:** `Incomplete`
- **Recorded values:**
  - `VECTOR-DATABASE-10005` — Pinecone: `Not recorded`
  - `VECTOR-DATABASE-10014` — Azure AI Search: `True`
  - `VECTOR-DATABASE-10015` — Vertex AI Vector Search: `True`
  - `VECTOR-DATABASE-10016` — Amazon Neptune Analytics: `True`
- **Reviewer question:** Determine whether the missing value represents unavailable knowledge, an unsupported capability, or an authoring omission.
- **Required examination:** official documentation cited by each record, applicable editions or plans, version and date, contrary limitations, and consistency with the other records.

### Complete evidence commands

```bash
python3 scripts/rkm-decision-query.py --entity pinecone --detail full
```

```bash
python3 scripts/rkm-decision-query.py --entity azure-ai-search --detail full
```

```bash
python3 scripts/rkm-decision-query.py --entity vertex-ai-vector-search --detail full
```

```bash
python3 scripts/rkm-decision-query.py --entity amazon-neptune-analytics --detail full
```

## Reviewer output required for every finding

- Finding ID
- Verdict
- Claim or field affected
- Sources examined
- Factual or semantic problem
- Required correction
- Severity
- Remaining uncertainty

## Global questions

1. Are capabilities inherited from PostgreSQL, cloud infrastructure, or an
   external component clearly distinguished from native product capabilities?
2. Are qualitative labels such as High, Medium, Variable, Limited, and
   Configurable applied using equivalent criteria?
3. Are modalities properties of the storage system or of upstream embedding
   and ingestion pipelines?
4. Does the broad `VectorDatabase` entity type create misleading comparisons
   between dedicated vector databases, search services, relational extensions,
   and graph databases with vector support?
5. Do the repeated counts of five claims, five evidence objects, and ten
   limitations reflect the sources or the authoring template?

## Stop rule

Do not approve a record solely because schemas, links, exports, or repository
validation pass. Formal validity is not semantic or factual approval.
