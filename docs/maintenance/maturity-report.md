# Maturity Report

## Summary

RAG Knowledge Model is currently around **3.5 / 5** overall maturity.

It is no longer an exploratory prototype. The repository has a coherent conceptual model, a broad schema foundation, validation discipline, automation, recovery tooling, registry checks, and an operational workflow. It should be treated as a strong foundation and production-oriented repository system.

It is not yet a finished consumable product. RKM has validated fixtures, a small populated dataset, deterministic fixture and data graph exports, formal graph node and edge schemas, an internal alpha tag and release notes, and a consumer guide. The scorecard below separates those capabilities because they are not equally mature: validation and automation are comparatively strong, while populated data remains narrow, seed relationship evidence is mostly weak internal maintainer analysis, graph export compatibility remains alpha/internal, release packaging is limited, and loader-specific consumer guidance is still missing. These gaps keep the overall assessment below level 4.

`make validate` now checks schema validity, schema prerequisites, schema contracts, duplicate schema contracts, fixture instance validity, data instance validity, relationship-set semantics, fixture graph export consistency, data graph export consistency, graph export schema validity, graph endpoint integrity, documentation relationship rules, and distributed agent rule routing.

## Scale

The maturity scale used here is:

- **1 / 5:** Idea or notes. Little structure, low repeatability.
- **2 / 5:** Prototype. Core direction exists, but contracts and workflows are incomplete.
- **3 / 5:** Foundation. Architecture, schemas, validation, and automation are coherent enough for disciplined development.
- **4 / 5:** Consumable system. External users can understand, load, validate, test, and use releases with limited maintainer help.
- **5 / 5:** Mature product or platform. Stable releases, rich content, strong compatibility guarantees, documented integrations, and proven downstream consumption.

## Granular Maturity Scorecard

The dimension scores are diagnostic signals, not values that are mechanically averaged into the overall score. The overall assessment remains a conservative judgment of whether the repository can be consumed with limited maintainer help.

| Dimension | Current Level | Current Signals | Remaining Gap Or Advancement Condition |
| --- | ---: | --- | --- |
| Conceptual model | 3.3 / 5 | The domain, entity, relationship, evidence, metadata, ontology, and naming documents form a coherent conceptual foundation under `docs/architecture/`. | Demonstrate the model across broader populated content and integrations while preventing semantic duplication between adjacent concepts. |
| Schema | 3.3 / 5 | JSON Schema Draft 2020-12 first-class schemas and reusable definitions cover a broad set of RKM concepts, and schema contract and duplicate-contract checks run in normal validation. | Add representative valid instances for more contracts, clarify compatibility expectations, and prove that broad schema coverage maps to real consumer use. |
| Validation discipline | 4.0 / 5 | `make validate` checks repository hygiene, schemas, registries, fixtures, data, relationship and support semantics, deterministic graph exports, graph integrity, unit tests, documentation relationships, and agent rule routing. | Close demonstrated enforcement gaps such as new-entity package completeness, runtime artifacts, recovery-state blocking, and semantic predicate reuse without weakening current checks. |
| Data | 2.5 / 5 | `data/manifest.json` declares six RAG techniques, four Components, two Retrievers, one Reranker, three relationship sets, and three relationship support sets, all on the standard validation path. | Expand beyond the small retrieval-oriented seed into representative frameworks, models, datasets, benchmarks, tools, providers, evaluations, and tradeoffs. |
| Evidence | 2.3 / 5 | The fixture package demonstrates a claim supported by evidence and an official reference, and the three relationship support sets provide linked claims, evidence, references, and relationship IDs. Seed support is deliberately draft, low-confidence, weak maintainer analysis rather than external proof. | Add primary or authoritative external sources, stronger evidence, and supported claims across populated entities and relationships while preserving explicit limitations and provenance. |
| Graph export | 3.3 / 5 | The fixture and data exporters produce deterministic node and edge arrays; committed outputs are checked for freshness, JSON Schema shape, duplicate IDs, endpoint integrity, provenance, and declared relationship support metadata. | Expand content coverage, export support claims, evidence, and references more completely, define package metadata and version compatibility, and provide tested loader mappings. |
| Release | 3.0 / 5 | The `v0.1.0-alpha` tag, release notes, changelog, release index, and `make release-check` provide an intentional internal-alpha checkpoint and readiness path. | Produce richer versioned release artifacts, define compatibility and migration expectations, and demonstrate a repeatable downstream evaluation from a clean release package. |
| Automation | 3.8 / 5 | Cockpit, bounded autopilot and autocycle flows, recovery planning, budget controls, safe push, commit automation, task routing, and distributed governance checks support disciplined operation. | Reduce dependence on operator judgment for recovery and artifact hygiene, and prove reliable unattended operation across repeated failure and recovery scenarios. |
| Consumer documentation | 3.2 / 5 | `QUICKSTART.md`, `docs/maintenance/consumer-guide.md`, the graph export contract, example READMEs, and release notes explain validation, fixtures, seed data, exports, stability, and current limitations. | Add end-to-end loader examples for graph, document, search, and vector-oriented consumers; keep package scope synchronized; and document versioned compatibility boundaries. |

## Why RKM Is No Longer Level 2

RKM has moved beyond prototype maturity because the project now has:

- A defined domain model and ontology.
- Reusable JSON Schema definitions.
- Specialized entity schemas.
- Registries for entity types and relationship types.
- Schema contract validation that catches semantic mistakes, not only syntax errors.
- Duplicate schema contract validation that requires same-name first-class schemas to compose from same-name reusable definitions.
- Documentation relationship validation.
- Fixture instance validation.
- Data instance validation for the first seed dataset.
- Semantic validation for declared relationship-set predicates, endpoints, data file references, relationship IDs, and semantic triples.
- Semantic validation for declared relationship support links among relationship IDs, claims, evidence, and references.
- Minimal fixture-derived graph export generation and consistency checks.
- Minimal data graph export generation and consistency checks for the validated seed dataset, including Component, Retriever, and Reranker nodes and declared relationship-set edges.
- Graph export node and edge schema validation with duplicate ID and edge endpoint integrity checks.
- Automated validation for distributed agent rule routing.
- A Makefile-based operational surface.
- Cockpit summary and next-action automation.
- Autopilot and autocycle flows.
- Recovery planning and autopilot recovery.
- Budget guardrails, working target caps, force mode, and budget grace.
- Commit automation with both single-file and multi-file support.

These are characteristics of a disciplined repository system, not a loose prototype.

## Why RKM Is Not Yet Level 4

RKM is not yet level 4 because external consumption is still underdeveloped.

The project needs:

- Richer examples showing additional valid entities, relationships, claims, evidence, and references beyond the minimal fixture path.
- Broader fixtures that can exercise tests, demos, importers, and downstream consumers across more modeling patterns.
- Dataset breadth beyond the first seed RAG techniques and components.
- Expansion of the current minimal graph export and first declared data relationships into a broader documented export contract.
- Release artifacts beyond repository documentation and the internal alpha tag, with compatibility and migration expectations.
- Loader-specific consumer documentation for querying and integrating the model with downstream systems.
- A clearer separation between model definitions, sample content, and production-ready data.
- More populated knowledge content across RAG techniques, frameworks, models, datasets, benchmarks, tools, providers, and tradeoffs.

The repository is strong enough to build on, but not yet easy enough for new users to adopt without maintainer context.

## Definition of Done for Level 4

RKM should be considered level 4 only when an external user can evaluate and use a versioned package with limited maintainer help.

The measurable criteria are:

- Examples and fixtures cover representative entities, relationships, claims, evidence, and references beyond one minimal package.
- At least one validated dataset exists, with enough representative content to test loading and inspection.
- The graph export contract covers nodes, edges, identifiers, labels, predicates, evidence links, references, provenance, package metadata, and version compatibility.
- Consumer documentation explains validation, inspection, schema and registry usage, expected stability, and at least one end-to-end downstream loading path.
- A versioned release package exists with a tag, release notes, scope, reproducible validation instructions, and actionable compatibility expectations.
- Validation can be reproduced by a new user from a clean checkout using documented commands.
- Schema, data, and registry coverage can be inspected through documented commands or reports.

These criteria preserve the distinction between a strong foundation and a consumable system. They do not require RKM to be complete across the whole RAG ecosystem, but they do require enough packaging for real downstream evaluation.

## Recommended Immediate Next Step

The core consumable RAG evidence path is now complete: a deterministic RAG
artifact is generated, consumed by RKM, and converted into a review-ready
decision record with provenance and fail-closed lifecycle state. The next
evidence milestone is authoritative external sourcing and review; it must not
be conflated with the completed runtime-generated evidence path.

## Key Risks

**Conceptual duplication**

As more schemas and definitions are added, the same concept may be modeled in multiple places with slightly different names or structures. Duplicate schema contract validation now catches same-name first-class schema and reusable definition pairs that do not compose, but it does not prove semantic equivalence or prevent differently named conceptual duplication.

**Embedded definitions behaving like first-class entities**

Some reusable definitions may grow identity, relationships, evidence, or lifecycle semantics. When that happens, they may need to be promoted to first-class entities or explicit relationship structures instead of remaining embedded objects.

**Limited examples, fixtures, and data breadth**

Without richer representative examples and broader populated data, it is difficult for humans and programs to understand how the schemas should be used beyond the minimal fixture package and the six seed RAG technique records plus their first Component, Retriever, and Reranker records. This also limits regression testing and makes onboarding slower.

**Minimal graph export scope**

RKM now has a first minimal fixture-derived graph export and a first minimal data graph export with Technique, Component, Retriever, and Reranker nodes, declared seed relationship edges, and conservative support metadata on those edges. Validation checks that both stay consistent with their source files and that exported node and edge files satisfy schema and endpoint integrity rules. Consumers still need expanded export coverage, documented semantics for broader content, a compatibility policy, and clearer guidance for loading the export into graph tooling.

**Budget and automation complexity**

The automation system is powerful, but budget guardrails, force mode, recovery paths, working target caps, and ledgers add operational complexity. Documentation must keep these concepts understandable.

**Onboarding complexity**

The project combines ontology design, JSON Schema, repository automation, validation, and AI-assisted workflows. New contributors need a clear path from concept to valid contribution.

## Recommended Next Milestones

1. Broaden the seed dataset with representative claims, evidence, references, and additional entity types.
2. Expand fixtures so they demonstrate richer valid entity, relationship, claim, evidence, reference, and graph export cases.
3. Add a tested consumer walkthrough that loads, queries, and inspects an export in at least one representative downstream system.
4. Use the tagged `v0.1.0-alpha` internal package to collect feedback, then plan the next versioned release without changing the existing alpha tag.
5. Expand the graph exports beyond the current minimal fixture-derived and seed-data provenance contracts, including clearer node, edge, identifier, label, predicate, evidence link, reference, and provenance semantics.
6. Add documentation that explains the difference between architecture, schemas, definitions, registries, examples, fixtures, graph export, and populated knowledge data.
7. Expand populated content in small validated increments, prioritizing representative coverage over volume.

## Current Bottom Line

RKM is a validated and automated foundation for a structured RAG knowledge model, with deterministic fixture and seed-data graph exports, six seed RAG techniques plus Component, Retriever, and Reranker records, semantically checked relationship edges, conservative support metadata, graph schema and endpoint checks, consumer documentation, and a tagged internal alpha release. Its next maturity step is not proving that schemas, data, evidence, exports, automation, or release mechanics can exist. The next gaps are breadth, externally grounded evidence, versioned compatibility, richer release packaging, and demonstrated downstream loading.
