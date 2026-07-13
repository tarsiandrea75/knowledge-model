# Minimal Fixtures

These fixtures provide the smallest practical RKM package for testing a downstream consumer.

## Files

- `minimal-rag-technique.json`: one RAG technique entity for Hybrid Retrieval.
- `minimal-relationship.json`: one relationship from the technique to a retriever component.
- `minimal-claim-with-evidence.json`: one claim, one evidence object, and one reference object connected by stable identifiers.

## Intended Consumption

A consumer can load these files to test the basic RKM graph shape:

```text
TECHNIQUE-9001 DEPENDS_ON COMPONENT-9001
CLAIM-9001 supported by EVIDENCE-9001
EVIDENCE-9001 derived from REFERENCE-9001
```

The example target `COMPONENT-9001` is referenced to demonstrate relationship consumption. It is not included as a full entity fixture in this first package.

## Validation

From the repository root, run:

```bash
make validate
```

`make validate` reads `fixture-manifest.json` and validates each fixture against the schema contract declared there. Paths in the manifest are resolved from the repository root.

The manifest maps:

- `minimal-rag-technique.json` to `schema/rag-technique.schema.json`
- `minimal-relationship.json` to `schema/definitions/relationship.schema.json`
- `minimal-claim-with-evidence.json` to separate validations for its `claim`, `evidence`, and `reference` objects

The combined claim package is a consumer fixture envelope. Its nested objects use existing RKM definition contracts, so the validator checks those nested objects through JSON Pointer entries in the manifest.
