# Context Assembly Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how context assembly is represented in the RAG Knowledge Model.

Context assembly is the RAG stage that selects, orders, formats and constrains retrieved or generated supporting material before it is supplied to a language model, evaluator, agent or downstream workflow step.

The Context Assembly Model answers the question:

> **Which information is included in the model-facing context, why is it included, how is it ordered and what constraints govern its use?**

---

# Core Principle

Context assembly is structured knowledge when it materially affects grounding, citation quality, cost, latency, safety, answer quality or reproducibility.

It is not only string concatenation.

```text
Component CONSUMES Artifact
Component PRODUCES Artifact
Prompt Technique SUPPORTS Component
Evaluation Metric MEASURES Artifact
Evidence SUPPORTS Claim
```

RKM represents context assembly explicitly so retrieval outputs, prompt inputs, citation candidates, policy constraints and evaluation results can be traced as reusable graph knowledge.

---

# Context Assembly

Context Assembly is the process of constructing a context package from candidate artifacts.

Candidate artifacts may include:

* retrieved chunks
* retrieved documents
* graph nodes
* triples
* table rows
* citations
* metadata records
* summaries
* tool outputs
* conversation history
* policy instructions

The assembled context should preserve enough structure to explain what was selected, what was excluded, where each item came from and how downstream components may use it.

Preferred:

```text
Context assembler that selects the top-ranked retrieved chunks, applies citation metadata, removes duplicate passages and emits an ordered context package with token budget information.
```

Avoid:

```text
Add context to the prompt.
```

The avoided statement does not identify selection behavior, ordering, source traceability or constraints.

---

# Context Package

A Context Package is the structured artifact produced by context assembly.

A context package may contain:

* selected context items
* source references
* citation candidates
* item order
* ranking scores
* section labels
* token counts
* inclusion rationale
* exclusion rationale
* freshness metadata
* access-control decisions
* compression or summarization notes

The context package may later be transformed into prompt text, structured model input, evaluation input or an agent observation.

When context package details affect claims or evidence, they should be represented as structured artifacts rather than prose-only descriptions.

---

# Assembly Boundary

Every context assembly description should define a clear boundary.

The boundary identifies:

* the candidate artifacts consumed
* the ordering or selection method applied
* the constraints applied during assembly
* the context package produced
* the downstream entity that consumes the package
* the evidence or trace data preserved for evaluation

Boundaries matter because context assembly may be performed by a component, prompt technique, workflow step, agent, framework or language model. RKM should make that responsibility explicit when it affects system behavior.

---

# Selection and Ordering

Selection determines which candidate artifacts are included.

Ordering determines how included artifacts are arranged.

Common selection and ordering signals include:

* retrieval rank
* reranking score
* citation support
* source authority
* source freshness
* metadata filters
* diversity requirements
* redundancy removal
* graph neighborhood priority
* temporal ordering
* section ordering
* policy constraints

Selection and ordering should be represented when they affect answer quality, faithfulness, citation behavior, cost or reproducibility.

Claims about context quality should identify whether the claim concerns candidate retrieval, reranking, assembly selection, prompt construction or final answer generation.

---

# Constraints

Context assembly is often governed by constraints.

Important constraints include:

* token budget
* maximum number of context items
* source diversity
* source freshness
* required citation metadata
* access-control policy
* privacy policy
* safety policy
* source licensing
* context window size
* latency budget
* cost budget

Constraints should be represented structurally when they determine what can be included in a context package.

For example, a context assembler may exclude a highly ranked passage because the user lacks access, because the source is stale or because the package already contains a near-duplicate passage.

---

# Compression and Transformation

Context assembly may transform candidate artifacts before they are supplied downstream.

Common transformations include:

* passage trimming
* chunk merging
* deduplication
* summarization
* quote extraction
* metadata normalization
* citation formatting
* table serialization
* graph neighborhood serialization
* prompt-specific formatting

Transformations should preserve source traceability when the transformed context is used for grounding, citation generation or evaluation.

If a transformation removes source boundaries, changes meaning or hides uncertainty, related claims should be supported by evidence and evaluated against appropriate quality attributes.

---

# Citation and Grounding Use

Context assembly is closely related to citation behavior.

The assembled context may determine:

* which sources are available for citation
* which source locations are visible to the generator
* which snippets are used as grounding evidence
* whether citations can be traced back to references
* whether citation faithfulness can be evaluated

RKM should distinguish between available context and cited context.

A context item can be included without being cited.

A citation can appear in an answer even when the supporting context is insufficient.

This distinction allows evidence and evaluation records to identify whether a failure came from retrieval, context assembly, generation or citation selection.

---

# Relationship Use

Context assembly should use canonical relationships when the links have reusable semantic value.

Common relationship patterns include:

```text
Workflow CONTAINS Component
Component CONSUMES Artifact
Component PRODUCES Artifact
Component USES Retriever
Component OPTIONALLY_USES Reranker
Prompt Technique SUPPORTS Component
Evaluation Metric MEASURES Artifact
Evidence SUPPORTS Claim
Reference REFERENCES Artifact
```

Relationships should connect the entities that are responsible for assembly, the artifacts consumed or produced, and the evidence used to justify assembly behavior.

---

# Evaluation

Context assembly can be evaluated directly or through downstream effects.

Useful evaluation dimensions include:

* context relevance
* context sufficiency
* citation coverage
* citation faithfulness
* redundancy
* diversity
* source freshness
* token efficiency
* latency
* cost
* policy compliance

Evaluation records should identify the context package, candidate set, assembly method, downstream task, metric, dataset, benchmark and date when available.

This prevents claims about assembled context from being generalized beyond the evidence that supports them.
