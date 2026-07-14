# Graph Edge Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines the architecture role of graph edges in RKM graph export.

A graph edge is an exported representation of a canonical RKM relationship or provenance connection between graph nodes. Graph edges support traversal, dependency analysis, lineage queries, provenance inspection and downstream graph validation while preserving the authority of the original repository data.

This document answers the question:

> **What does a graph export edge represent, and how does it preserve canonical relationship meaning?**

---

# Core Principle

A graph edge is a projection of existing RKM knowledge, not a new relationship source.

The canonical relationship, claim, evidence link, reference link or provenance connection remains authoritative in its source file. A graph edge must carry enough information for graph consumers to traverse and inspect that connection, but it must not introduce relationship semantics that are absent from the relationship model, relationship type registry or source data.

Graph edge fields may optimize graph loading, querying or display. Those fields must be derivable from canonical RKM data or from the export process itself.

---

# Edge Identity

The graph edge `id` is the stable address used by graph consumers when they need to inspect, deduplicate or annotate an exported connection.

When the source connection is a first-class RKM relationship, the graph edge `id` should use the relationship identifier from the source relationship object.

When the source connection is derived from structured provenance, such as a claim supported by evidence or evidence citing a reference, the exporter must use a deterministic identifier derived from the source object identifiers and the source file. The derived identifier must remain stable for the same source connection across repeated exports.

The graph edge `id` must not be replaced by display labels, generated sequence numbers or target-system internal identifiers.

---

# Predicate

The graph edge `predicate` identifies the relationship semantics.

For first-class relationships, `predicate` must use the canonical uppercase snake case relationship type from the relationship type registry, such as `REQUIRES`, `DEPENDS_ON`, `IMPLEMENTS`, `SUPPORTS`, `CONTAINS`, `PART_OF`, `EXECUTES`, `TRIGGERS`, `ROUTES_TO` or `BRANCHES_TO`.

For provenance edges, `predicate` should use a canonical relationship predicate when one exists, such as `SUPPORTS`, `REFERENCES` or `CITES`.

Exporters must not invent ad hoc predicates during graph export. If a needed predicate is not supported by the relationship type registry, the source model should be updated through the normal architecture and registry process before exported edges depend on it.

---

# Direction

Graph edge direction must match the canonical direction defined by the source relationship and relationship type registry.

The `sourceId` identifies the exported graph node where the relationship starts.

The `targetId` identifies the exported graph node where the relationship points.

Example:

```json
{
  "id": "RELATIONSHIP-0001",
  "predicate": "REQUIRES",
  "sourceId": "TECHNIQUE-0001",
  "targetId": "RETRIEVER-0001",
  "sourceDataFile": "data/relationships/rag-technique-component-relationships.json",
  "properties": {
    "relationshipKind": "Dependency",
    "confidence": "High",
    "status": "Published"
  }
}
```

Derived inverse edges may be emitted for graph-query convenience only when they are explicitly marked as derived in `properties` and do not replace the canonical edge.

---

# Endpoint Resolution

Every graph edge endpoint must resolve to a graph node in the same exported graph.

The `sourceId` and `targetId` values must match graph node `id` values. They must not use display names, slugs, file paths or target-system internal identifiers.

If a source relationship points to an entity that is not exported as a node, the exporter should report the unresolved endpoint instead of silently dropping or rewriting the edge. Missing endpoints indicate either incomplete export scope or source data that needs validation feedback.

---

# Source Traceability

Every graph edge must include `sourceDataFile`.

The `sourceDataFile` value identifies the repository data file or fixture file from which the edge was exported. This preserves traceability from the graph projection back to canonical RKM content.

For derived provenance edges, `sourceDataFile` should identify the file that contains the claim, evidence, reference or metadata connection that produced the edge.

Architecture documents and schemas are not normally graph edge sources. They define the model and validation rules used to interpret source data.

---

# Properties

The graph edge `properties` object contains exported attributes that are useful for graph consumers.

Common properties include:

* `relationshipKind`
* `confidence`
* `status`
* `reviewState`
* `evidenceIds`
* `claimIds`
* `referenceIds`
* `derived`
* source-specific provenance fields

Properties should keep structured values when the source is structured. Exporters should not flatten meaningful nested data into prose when the target graph format can preserve the structure.

Properties must not be treated as a place to override `predicate`, `sourceId` or `targetId`. Relationship semantics and direction belong on the graph edge itself.

---

# Relationship To Graph Nodes

Graph edges connect graph nodes.

A graph edge is valid only when its `sourceId` and `targetId` can be resolved to graph node identifiers in the same exported graph. This resolution requirement allows exported graphs to support traversal without consulting repository source files during query execution.

The graph edge model does not define node identity, node labels or node properties. Those responsibilities belong to the graph node model and graph node schema.

---

# Validation Expectations

Graph edge validation should confirm that:

* `id` is present and non-empty
* `predicate` is present and non-empty
* `predicate` is canonical when the edge represents a first-class RKM relationship
* `sourceId` is present and resolves to an exported graph node
* `targetId` is present and resolves to an exported graph node
* `sourceDataFile` is present and non-empty
* `properties` is present as an object
* canonical relationship direction is preserved
* derived inverse edges are explicitly marked as derived

Validation should report graph edges that cannot be traced back to canonical source data.

---

# Compatibility

Adding an optional edge property is usually backward compatible.

Changing a graph edge `id`, changing a canonical `predicate`, reversing `sourceId` and `targetId`, removing `sourceDataFile` or replacing structured properties with incompatible scalar values can break downstream graph consumers.

Graph edge compatibility follows the same versioning principles as the broader graph export model.
