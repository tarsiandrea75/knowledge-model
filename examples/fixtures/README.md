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

Direct schema validation can be added by a consumer using any JSON Schema Draft 2020-12 validator:

- validate `minimal-rag-technique.json` against `schema/rag-technique.schema.json`
- validate `minimal-relationship.json` against `schema/definitions/relationship.schema.json`
- validate the inner `claim`, `evidence`, and `reference` objects in `minimal-claim-with-evidence.json` against their corresponding definition schemas

The combined claim package is a consumer fixture envelope. Its nested objects use existing RKM definition contracts, while a package-level schema is still evolving.
