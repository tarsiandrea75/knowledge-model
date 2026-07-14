# Graph Node Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines the architecture role of graph nodes in RKM graph export.

A graph node is an exported representation of a canonical RKM knowledge object that needs to be addressable in graph-oriented consumers. Graph nodes support traversal, indexing, lineage queries and downstream graph validation while preserving the authority of the original repository data.

This document answers the question:

> **What does a graph export node represent, and which parts of it are canonical versus export-specific?**

---

# Core Principle

A graph node is a projection, not a new source of truth.

The canonical RKM entity, relationship support record, claim, evidence item or reference remains authoritative in its source file. A graph node must carry enough information for graph consumers to identify and inspect that source, but it must not introduce new canonical semantics that are absent from the repository model.

Graph node fields may optimize graph loading, querying or display. Those fields must be derivable from canonical RKM data or from the export process itself.

---

# Node Identity

The graph node `id` is the stable address used by exported graph edges and graph consumers.

When the source object is a first-class RKM entity, the graph node `id` must use the entity identity `id`.

When the source object is not a first-class entity, the exporter must use a deterministic identifier derived from the canonical source object and its position in the source document. The derived identifier must remain stable for the same source object across repeated exports.

The graph node `id` must not be replaced by display names, slugs or generated labels.

---

# Node Type

The graph node `type` identifies the exported node category.

For first-class entities, `type` should align with the canonical `identity.entityType` value, such as `Technique`, `Framework`, `Paper`, `Component`, `Retriever` or `Reranker`.

For provenance or operational nodes, `type` may describe the exported concept, such as `Claim`, `Evidence`, `Reference` or `Metadata`, provided that the value does not claim to be a registered entity type unless it is supported by the identity model.

The node type is an export classification. It does not extend the entity type registry by itself.

---

# Node Label

The graph node `label` is a human-readable display value.

For first-class entities, the preferred label is the entity display name. When no display name is available, exporters may use the official name, slug or stable identifier in that order.

For non-entity nodes, the label should be concise and deterministic. Labels help people inspect exported graphs, but graph consumers must use `id` for joins and edge endpoints.

---

# Source Traceability

Every graph node must include `sourceDataFile`.

The `sourceDataFile` value identifies the repository data file or fixture file from which the node was exported. This preserves traceability from the graph projection back to canonical RKM content.

Architecture documents and schemas are not normally graph node sources. They define the model and validation rules used to interpret source data.

---

# Properties

The graph node `properties` object contains exported attributes that are useful for graph consumers.

Common properties include:

* `slug`
* `name`
* `status`
* `reviewState`
* `schemaVersion`
* `repositoryVersion`
* `description`
* source-specific provenance fields

Properties should keep structured values when the source is structured. Exporters should not flatten meaningful nested data into prose when the target graph format can preserve the structure.

Properties must not be treated as a place to invent relationship predicates. Canonical relationship semantics belong on graph edges and must use registered relationship predicates such as `CONTAINS`, `PART_OF`, `REQUIRES` or `DEPENDS_ON`.

---

# Relationship To Graph Edges

Graph nodes are connected by graph edges.

An edge `sourceId` or `targetId` must resolve to a graph node `id` in the same exported graph. This resolution requirement allows exported graphs to support traversal without consulting repository source files during query execution.

The node model does not define edge direction or relationship semantics. Those responsibilities belong to the relationship model, relationship type registry and graph edge schema.

---

# Validation Expectations

Graph node validation should confirm that:

* `id` is present and non-empty
* `type` is present and non-empty
* `label` is present and non-empty
* `sourceDataFile` is present and non-empty
* `properties` is present as an object
* first-class entity nodes preserve canonical entity identifiers
* edge endpoints resolve to exported node identifiers

Validation should report graph nodes that cannot be traced back to canonical source data.

---

# Compatibility

Adding an optional node property is usually backward compatible.

Changing a graph node `id`, changing the meaning of `type`, removing `sourceDataFile` or replacing structured properties with incompatible scalar values can break downstream graph consumers.

Graph node compatibility follows the same versioning principles as the broader graph export model.
