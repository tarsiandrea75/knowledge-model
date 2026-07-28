# Graph Export Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how RKM knowledge is prepared for graph export.

The Graph Export Model explains how entities, relationships, claims, evidence, references and metadata can be projected into graph-oriented representations without changing their canonical repository form.

This document answers the question:

> **How does RKM preserve ontology meaning when knowledge is exported to graph databases, RDF stores or graph analysis tools?**

---

# Core Principle

Graph export is a projection of canonical RKM knowledge.

The repository source remains the authority.

An exported graph must not introduce new canonical entity types, relationship types, identifiers or lifecycle states that are absent from the RKM architecture, schemas or registries.

Export formats may add technical fields needed by a target system, but those fields must be derivable from canonical RKM documents.

---

# Export Boundaries

Graph export includes concepts that have reusable semantic meaning:

* entities
* relationships
* claims
* evidence
* references
* external links
* metadata needed for provenance, lifecycle and versioning

Graph export excludes presentation-only concerns:

* generated page layout
* table ordering
* editorial section headings
* local navigation
* rendering-specific labels

The exported graph should support querying, reasoning, lineage tracing, documentation generation and validation feedback.

---

# Nodes

Every exported entity should become a graph node.

The node identifier must use the canonical RKM identity `id` when available.

The entity `slug`, display name and entity type may be exported as node properties for readability and indexing, but they must not replace the stable identifier.

Example node:

```json
{
  "id": "TECHNIQUE-0001",
  "entityType": "Technique",
  "slug": "hyde",
  "name": "HyDE"
}
```

Claims, evidence and references may also be exported as nodes when the target graph needs first-class provenance queries.

---

# Edges

Every exported relationship should become a graph edge.

The edge type must use a canonical relationship predicate from the relationship type registry.

Example edge:

```json
{
  "id": "RELATIONSHIP-0001",
  "type": "REQUIRES",
  "sourceId": "TECHNIQUE-0001",
  "targetId": "EMBEDDING-MODEL-0001",
  "confidence": "High",
  "status": "Published"
}
```

The edge direction must match the canonical direction defined by the relationship model and relationship type registry.

Derived inverse edges may be generated for query convenience only when they are marked as derived and do not replace canonical relationships.

---

# Provenance Projection

Evidence, claims and references should remain distinguishable after export.

Preferred projection:

```text
Entity CONTAINS Claim
Evidence SUPPORTS Claim
Evidence REFERENCES Reference
```

This structure keeps factual assertions separate from the sources that support them.

When a graph target does not support rich edge properties, provenance fields should be represented as connected nodes instead of being flattened into prose strings.

---

# Metadata Projection

Metadata should be exported when it affects trust, lifecycle, compatibility or review.

Important metadata includes:

* version
* schema version
* repository version
* status
* review state
* creation and update timestamps
* creator attribution
* license
* provenance

Metadata should not obscure domain knowledge. Export consumers should be able to separate graph semantics from operational bookkeeping.

# Export Package Boundary

A graph export package is the bounded consumer artifact formed by the exported nodes and edges together with the metadata needed to interpret that projection. The package is a derived view of canonical RKM sources; it is not a second entity, relationship, claim, evidence or reference contract.

Package metadata should identify:

* the export and its projection type
* the RKM repository version or source snapshot
* the source authority and source paths used for the projection
* the node and edge members included in the package
* the schema contracts and generator version used to produce it
* the compatibility status and migration expectation for consumers

The package boundary gives a consumer enough information to decide whether an export can be loaded and compared with an existing graph. It must not imply that package metadata, generated node properties or generated edges have authority over the canonical source. A consumer should return to the declared source records when it needs domain meaning, evidence, claims, references or current lifecycle state.

Package compatibility has two distinct parts. Structural compatibility describes whether a consumer can parse and validate the package members. Semantic compatibility describes whether identifiers, entity types, relationship predicates, direction, provenance meaning and lifecycle interpretation remain usable for the consumer's existing graph. A package is not semantically compatible merely because its JSON remains parseable.

The current committed RKM graph exports are alpha/internal node-and-edge artifacts rather than complete package-envelope contracts. They have deterministic member files and source provenance, but consumers must treat package metadata, broader version negotiation and loader-specific mappings as unresolved until an explicit package contract is added.

# Package Envelope Contract

When RKM defines a package envelope for graph exports, the envelope should be a derived transport contract around the node and edge members, not a new domain entity. It should identify the export package, projection type, source snapshot, member locations or identities, schema contracts, generator version and compatibility status. The envelope should also state whether the package is structural-only, semantically compatible with a declared consumer contract, or requires migration before loading.

The envelope must preserve the authority boundary of graph export. Its identifiers, compatibility statements and generator metadata describe the projection; they do not establish new entities, relationships, predicates, evidence, claims, references or lifecycle facts. A consumer must be able to validate the envelope and its members independently, then use the declared source authority to interpret domain meaning.

Until a machine-readable envelope schema and deterministic package artifact are explicitly introduced, this section is an architectural contract for future package work rather than a claim that the current node-and-edge files already satisfy it.

---

# Format Independence

RKM graph export is format-independent.

The same canonical knowledge may be projected to:

* property graph
* RDF
* OWL
* JSON-LD
* GraphQL
* SQL graph-like views

Format-specific exporters may choose different physical encodings, but they must preserve:

* stable entity identifiers
* canonical relationship predicates
* canonical relationship direction
* evidence and reference traceability
* lifecycle and version metadata

---

# Validation Expectations

Graph export should run after schema and registry validation.

An exporter should reject or report:

* unknown entity types
* unknown relationship predicates
* relationships whose source or target identifiers cannot be resolved
* relationship directions that conflict with registry expectations
* evidence records that reference missing claims or references
* exported nodes without stable identifiers when the source document requires them

Export validation should not silently repair canonical data. Repairs belong in the repository source documents.

---

# Compatibility

Graph export compatibility follows RKM versioning rules.

Adding a new optional exported property is usually backward compatible.

Changing an entity identifier, changing a canonical relationship predicate or reversing a canonical relationship direction is a breaking ontology change.

Deprecation should preserve old identifiers and predicates long enough for downstream graph consumers to migrate.
