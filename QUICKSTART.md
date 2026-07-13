# RKM Quickstart

This quickstart gives a technical user the shortest practical path to inspect and validate the first internal alpha package for RAG Knowledge Model.

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

## 3. Inspect Fixtures

```bash
ls examples/fixtures
```

Fixtures are small, controlled examples used to demonstrate valid schema shape and validation behavior. They are intended for learning, testing, and export checks. They are not the populated knowledge dataset.

## 4. Inspect Data

```bash
ls data
```

Data files are populated RKM knowledge instances. The current alpha includes a small validated seed dataset for consumer testing and feedback. It is not a complete RAG catalog.

## 5. Generate the Graph Export

```bash
make graph-export
```

This regenerates the minimal fixture-derived graph export.

## 6. Inspect the Graph Export

```bash
ls examples/graph-export
```

The current graph export is intentionally minimal. It proves the first export path from fixtures into graph nodes and edges.

## 7. Read the Consumer Guide

Read `docs/maintenance/consumer-guide.md` for the current consumption contract, stability expectations, validation details, and guidance for internal evaluation of `v0.1.0-alpha`.
