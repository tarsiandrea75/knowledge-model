# Relationship Support Data

This directory contains relationship support sets for populated RKM data.

A relationship support set connects declared relationship instances to structured references, claims, and evidence. The relationship instance remains authoritative in `data/relationships/`; the support set explains why that relationship is included in the seed dataset and records the support objects that justify the declaration.

Relationship support files are declared in `data/manifest.json` and validated through the normal data validation path:

```bash
make data-validate
```

Validation has two layers. First, each support-set file is JSON-schema validated against `schema/relationship-support-set.schema.json`. Second, each support object is semantically validated so relationship, claim, evidence, and reference identifiers resolve inside the declared dataset and support set.

The first support file uses a `Maintainer Analysis` reference. This is conservative internal support for seed dataset modeling rationale, not an external factual source and not a benchmark claim. It explains why these relationships are included as possible seed dataset relationships without claiming that every RAG system uses the same sequence.

Relationship support is declared and validated. It is not inferred from relationship descriptions, technique names, pipeline stages, or graph export behavior.

Current relationship support sets:

- `rag-technique-relationship-support.json`: conservative internal support for the seed RAG technique relationships.
