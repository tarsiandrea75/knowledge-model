# Maturity Report

## Summary

RAG Knowledge Model is currently around **3.5 / 5** overall maturity.

It is no longer an exploratory prototype. The repository has a coherent conceptual model, a broad schema foundation, validation discipline, automation, recovery tooling, registry checks, and an operational workflow. It should be treated as a strong foundation and production-oriented repository system.

It is not yet a finished consumable product. The first minimal fixture-derived graph export now exists and is checked during validation, and the first small populated dataset now exists under `data/`. Post-alpha work on `main` also includes a deterministic data graph export for the validated seed dataset, declared relationship sets among seed techniques, and declared technique-component relationships. Graph and export readiness has improved because exported graph node and edge files now have JSON Schema validation plus duplicate ID and edge endpoint integrity checks. Populated content and graph usefulness improved because the seed graph now includes Component nodes, conservative declared domain edges, support metadata, and provenance. Relationship and data integrity also improved modestly because relationship-set validation now checks registered predicates, source and target data record existence, declared source and target data files, duplicate relationship IDs, and duplicate semantic triples. Relationship quality and traceability improved modestly because declared relationship edges can now be connected to conservative maintainer-analysis claims, evidence, and references. The first internal alpha release documentation for `v0.1.0-alpha` exists, which improves release readiness slightly by making scope, commands, limitations, and consumer expectations explicit. The populated knowledge base is still thin. The repository still needs broader dataset coverage, richer release packaging, and clearer downstream usage guidance before it can be adopted easily by people outside the immediate project.

`make validate` now checks schema validity, fixture instance validity, data instance validity, relationship-set semantics, fixture graph export consistency, data graph export consistency, graph export schema validity, and graph endpoint integrity.

## Scale

The maturity scale used here is:

- **1 / 5:** Idea or notes. Little structure, low repeatability.
- **2 / 5:** Prototype. Core direction exists, but contracts and workflows are incomplete.
- **3 / 5:** Foundation. Architecture, schemas, validation, and automation are coherent enough for disciplined development.
- **4 / 5:** Consumable system. External users can understand, load, validate, test, and use releases with limited maintainer help.
- **5 / 5:** Mature product or platform. Stable releases, rich content, strong compatibility guarantees, documented integrations, and proven downstream consumption.

## Maturity Dimensions

| Dimension | Current Level | Assessment |
| --- | ---: | --- |
| Conceptual model | 3.3 / 5 | The domain model, entity model, relationship model, evidence model, metadata model, ontology, and naming conventions provide a coherent conceptual foundation. |
| Schema coverage | 3.3 / 5 | Many entity and reusable definition schemas exist, with JSON Schema Draft 2020-12 as the contract format. Coverage is broad but still needs richer examples, fixtures, and clearer consumer contracts. |
| Validation discipline | 4.0 / 5 | Validation covers schemas, schema prerequisites, schema contracts, registries, fixture instances, data instances, relationship-set semantics, graph export consistency, and documentation relationship usage. Validation is part of normal operation rather than a late manual step. |
| Automation | 3.7 / 5 | The repository has cockpit summaries, autopilot, autocycle, safe push, recovery planning, budget guardrails, force mode, budget grace, working target caps, and validated commit automation. |
| Populated data/content | 2.4 / 5 | The model foundation is stronger than the actual populated knowledge base. RKM now has a first seed dataset with validated RAG technique records, Component records, conservative relationship sets, and conservative relationship support metadata, but still needs broader representative entities, claims, evidence, references, and examples. |
| Consumability | 3.4 / 5 | Maintainers can work with the repo, and early consumers can inspect validated fixtures, a first seed dataset, a minimal fixture graph export, and a minimal data graph export with Technique nodes, Component nodes, provenance, declared relationship edges, and support metadata. Outside consumers still need richer data, loading guidance, release packaging, and expanded export documentation. |
| Release readiness | 3.0 / 5 | The repository can be validated and operated, and first alpha release documentation now describes scope, validation, limitations, and expected use. It still needs an intentional git tag, stronger compatibility policy, versioned examples, and downstream integration guidance. |

## Why RKM Is No Longer Level 2

RKM has moved beyond prototype maturity because the project now has:

- A defined domain model and ontology.
- Reusable JSON Schema definitions.
- Specialized entity schemas.
- Registries for entity types and relationship types.
- Schema contract validation that catches semantic mistakes, not only syntax errors.
- Documentation relationship validation.
- Fixture instance validation.
- Data instance validation for the first seed dataset.
- Semantic validation for declared relationship-set predicates, endpoints, data file references, relationship IDs, and semantic triples.
- Semantic validation for declared relationship support links among relationship IDs, claims, evidence, and references.
- Minimal fixture-derived graph export generation and consistency checks.
- Minimal data graph export generation and consistency checks for the validated seed dataset, including Component nodes and declared relationship-set edges.
- Graph export node and edge schema validation with duplicate ID and edge endpoint integrity checks.
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

- Complete examples showing valid entities, relationships, claims, evidence, and references.
- Fixtures that can be used by tests, demos, importers, and downstream consumers.
- Dataset breadth beyond the first seed RAG techniques and components.
- Expansion of the current minimal graph export and first declared data relationships into a broader documented export contract.
- Release artifacts, release notes, and an intentional git tag when maintainers decide to create one.
- Consumer documentation for loading, validating, querying, and extending the model.
- A clearer separation between model definitions, sample content, and production-ready data.
- More populated knowledge content across RAG techniques, frameworks, models, datasets, benchmarks, tools, providers, and tradeoffs.

The repository is strong enough to build on, but not yet easy enough for new users to adopt without maintainer context.

## Definition of Done for Level 4

RKM should be considered level 4 only when an external user can evaluate and use a versioned package with limited maintainer help.

The measurable criteria are:

- Examples and fixtures exist for valid entities, relationships, claims, evidence, and references.
- At least one validated dataset exists, with enough representative content to test loading and inspection.
- A graph export contract exists for nodes, edges, identifiers, labels, predicates, evidence links, references, and provenance.
- A consumer guide exists and explains validation, loading, inspection, schema location, registry usage, and expected stability.
- A release tag exists with release notes, scope, validation instructions, and compatibility expectations.
- Validation can be reproduced by a new user from a clean checkout using documented commands.
- Schema, data, and registry coverage can be inspected through documented commands or reports.

These criteria preserve the distinction between a strong foundation and a consumable system. They do not require RKM to be complete across the whole RAG ecosystem, but they do require enough packaging for real downstream evaluation.

## Recommended Immediate Next Step

Build the first consumable fixture and data package before expanding many more schemas. A small validated package with examples, a dataset, consumer guidance, and an initial export path will make the current foundation easier to evaluate and will expose the next modeling gaps more clearly than broad schema expansion alone.

## Key Risks

**Conceptual duplication**

As more schemas and definitions are added, the same concept may be modeled in multiple places with slightly different names or structures. This can weaken graph consistency and make downstream consumers uncertain about which field is authoritative.

**Embedded definitions behaving like first-class entities**

Some reusable definitions may grow identity, relationships, evidence, or lifecycle semantics. When that happens, they may need to be promoted to first-class entities or explicit relationship structures instead of remaining embedded objects.

**Limited examples, fixtures, and data breadth**

Without richer representative examples and broader populated data, it is difficult for humans and programs to understand how the schemas should be used beyond the minimal fixture package and the first three seed RAG technique records. This also limits regression testing and makes onboarding slower.

**Minimal graph export scope**

RKM now has a first minimal fixture-derived graph export and a first minimal data graph export with Technique nodes, Component nodes, declared seed relationship edges, and conservative support metadata on those edges. Validation checks that both stay consistent with their source files and that exported node and edge files satisfy schema and endpoint integrity rules. Consumers still need expanded export coverage, documented semantics for broader content, a compatibility policy, and clearer guidance for loading the export into graph tooling.

**Budget and automation complexity**

The automation system is powerful, but budget guardrails, force mode, recovery paths, working target caps, and ledgers add operational complexity. Documentation must keep these concepts understandable.

**Onboarding complexity**

The project combines ontology design, JSON Schema, repository automation, validation, and AI-assisted workflows. New contributors need a clear path from concept to valid contribution.

## Recommended Next Milestones

1. Broaden the seed dataset with representative claims, evidence, references, and additional entity types.
2. Expand fixtures so they demonstrate richer valid entity, relationship, claim, evidence, reference, and graph export cases.
3. Add a consumer quickstart that explains how to validate, load, inspect, and regenerate the minimal export.
4. Use the `v0.1.0-alpha` internal package documentation to collect feedback, then prepare an intentionally tagged release when the package is ready for that step.
5. Expand the graph exports beyond the current minimal fixture-derived and seed-data provenance contracts, including clearer node, edge, identifier, label, predicate, evidence link, reference, and provenance semantics.
6. Add documentation that explains the difference between architecture, schemas, definitions, registries, examples, fixtures, graph export, and populated knowledge data.
7. Expand populated content in small validated increments, prioritizing representative coverage over volume.

## Current Bottom Line

RKM is a validated and automated foundation for a structured RAG knowledge model, with a first minimal graph export generated from fixtures, a first small seed dataset checked by validation, seed Component records, semantically checked relationship-set edges, conservative support metadata for those relationships, a post-alpha data graph export generated from that seed dataset, graph export schema and endpoint checks, and first internal alpha release documentation for `v0.1.0-alpha`. Its next maturity step is not proving that populated data can exist. The next gap is dataset breadth, release packaging, graph export expansion beyond the first conservative relationships, and clearer downstream consumption guidance.
