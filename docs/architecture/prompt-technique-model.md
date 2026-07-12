# Prompt Technique Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how prompt techniques are represented in the RAG Knowledge Model.

Prompt techniques are reusable methods for shaping language model behavior in query understanding, retrieval planning, context assembly, answer generation, citation behavior, tool use, evaluation and workflow control.

The Prompt Technique Model answers the question:

> **How should RKM describe prompting methods that materially affect RAG behavior, grounding, retrieval quality or evaluation?**

---

# Core Principle

A prompt technique is a first-class knowledge entity when the prompting method has reusable semantic meaning.

It is not only prompt text.

A prompt technique describes the role, inputs, outputs, model assumptions, grounding behavior, control properties, evaluation context and failure modes of a prompting method used in a RAG system.

```text
Prompt Technique SUPPORTS Technique
Prompt Technique USES Language Model
Prompt Technique DEPENDS_ON Component
Prompt Technique SUPPORTS Retriever
Prompt Technique SUPPORTS Agent
Evaluation Metric MEASURES Prompt Technique
Benchmark EVALUATES Prompt Technique
Paper INTRODUCES Prompt Technique
```

Representing prompt techniques explicitly makes prompt-mediated retrieval, generation and evaluation behavior easier to compare, govern, reproduce and export as graph knowledge.

---

# Prompt Technique

A Prompt Technique represents a reusable prompting method that guides model behavior.

A prompt technique may:

* rewrite or expand a user query
* generate a hypothetical document for retrieval
* decompose a question into subquestions
* select a retriever or tool
* ask a model to ground an answer in retrieved context
* require citations from supplied sources
* critique or verify generated output
* score relevance, faithfulness or answer quality
* coordinate chained prompts in a workflow

The technique should be modeled when the prompting method affects retrieval, grounding, orchestration, evaluation, safety, cost, latency or reproducibility.

Preferred:

```text
Query rewriting prompt technique that transforms a conversational question into a standalone retrieval query.
```

Avoid:

```text
Better prompt.
```

The avoided statement does not identify the prompting role, input, output or RAG behavior being shaped.

---

# Prompt Boundary

Every prompt technique should define a clear boundary.

The boundary identifies:

* what input context the prompt expects
* what output artifact or decision the prompt should produce
* which RAG stage the prompt affects
* which model capabilities the technique assumes
* whether retrieved context, examples, tools or schemas are required
* whether the technique changes retrieval behavior, generation behavior or evaluation behavior

Prompt boundaries matter because the same wording pattern may have different meaning when used for query rewriting, answer generation, tool selection or evaluation.

---

# Technique Type

Technique type describes the primary prompting method.

Canonical prompt technique types include:

```text
Instruction Prompting
System Prompting
Few Shot Prompting
Chain Of Thought
Self Consistency
Query Rewriting
Query Expansion
Hypothetical Document Generation
Step Back Prompting
Contextual Prompting
Citation Prompting
Grounding Prompting
Tool Use Prompting
Router Prompting
Evaluator Prompting
Critique Prompting
Reflection Prompting
Prompt Chaining
Other
```

The technique type should describe the dominant method. More specific behavior should be represented through inputs, outputs, grounding behavior, relationships, claims and evidence.

---

# Prompt Role

Prompt role describes the primary RAG responsibility performed by the prompt technique.

Common prompt roles include:

* query understanding
* query transformation
* retrieval planning
* retriever selection
* context selection
* context compression
* context assembly
* answer generation
* citation generation
* grounding verification
* tool selection
* evaluation
* workflow control

Prompt role should not be inferred from the name of a prompting method alone.

For example, chain-of-thought prompting may support answer generation, evaluation or workflow control depending on how it is used.

---

# Inputs and Outputs

Prompt techniques should model important inputs and outputs structurally.

Common inputs include:

* user query
* conversation history
* retrieved context
* document metadata
* schema
* tool description
* evaluation rubric
* reference answer
* system instruction
* example

Common outputs include:

* rewritten query
* expanded query
* retrieval plan
* tool selection
* context selection
* generated answer
* citation set
* grounding judgment
* evaluation score
* critique
* routing decision

Inputs and outputs should be explicit when another workflow step, agent, retriever, evaluator or component consumes the result.

---

# Model Requirements

Some prompt techniques depend on language model capabilities.

Important model requirements include:

* instruction following
* long-context handling
* structured output generation
* tool calling
* citation formatting
* reasoning over retrieved context
* multilingual behavior
* deterministic formatting under constrained decoding

Model requirements should be represented when they affect portability across language models or providers.

Claims about model-specific prompt behavior should identify the model, version, settings and evaluation context when available.

---

# Grounding Behavior

Grounding behavior describes how the prompt technique constrains model output to supplied sources, retrieved context or evidence.

Important grounding knowledge includes:

* whether retrieved context is required
* whether citations are required
* whether unsupported claims are forbidden
* whether the prompt asks the model to abstain
* whether source passages must be quoted, referenced or summarized
* whether the model verifies claims against context before answering

Grounding behavior should be evidence-backed when it is used to justify trust, safety or compliance claims.

Prompt instructions alone do not prove that a technique guarantees grounded output.

---

# Control Properties

Control properties describe how predictable, composable and operationally constrained the prompt technique is.

Important control properties include:

* expected output format
* determinism expectations
* compatibility with structured output validation
* use in prompt chains
* dependence on temperature or sampling configuration
* need for retries or repair prompts
* susceptibility to prompt injection
* sensitivity to context ordering

These properties matter when the prompt technique participates in automated workflows, agentic planning, evaluation pipelines or governed production systems.

---

# Evaluation

Prompt techniques should be evaluated in the context where they are used.

Common evaluation targets include:

* retrieval recall after query rewriting
* relevance of expanded queries
* faithfulness of generated answers
* citation precision
* answer abstention quality
* tool selection accuracy
* evaluator agreement with human labels
* latency and token cost

Evaluation claims should name the dataset, benchmark, metric, model, prompt configuration and workflow context when available.

```text
Benchmark EVALUATES Prompt Technique
Evaluation Metric MEASURES Prompt Technique
Evidence SUPPORTS Claim
Claim REFERENCES Paper
```

Claims about prompt technique effectiveness should not be generalized beyond the task, model, corpus, metric and evaluation protocol supported by evidence.

---

# Relationship Use

Prompt techniques should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Prompt Technique SUPPORTS Technique
Prompt Technique SPECIALIZES Prompt Technique
Prompt Technique USES Language Model
Prompt Technique DEPENDS_ON Component
Prompt Technique SUPPORTS Retriever
Prompt Technique SUPPORTS Reranker
Prompt Technique SUPPORTS Agent
Prompt Technique SUPPORTS Framework
Prompt Technique HAS_USE_CASE Use Case
Prompt Technique HAS_LIMITATION Limitation
Prompt Technique HAS_TRADEOFF Tradeoff
Prompt Technique GOVERNED_BY Policy
Benchmark EVALUATES Prompt Technique
Evaluation Metric MEASURES Prompt Technique
Paper INTRODUCES Prompt Technique
```

Relationship targets should use stable identifiers whenever those entities are represented in RKM.

Plain prose may explain prompting behavior, but reusable support, dependency, evaluation, governance and provenance relationships should be represented structurally.

---

# Evidence and Claims

Claims about prompt techniques should be evidence-backed when they affect selection, trust, safety or operational use.

Examples of claims that should usually cite evidence include:

* a prompt technique improves retrieval recall
* a prompt technique reduces hallucination
* a prompt technique improves citation faithfulness
* a prompt technique works reliably with a specific model family
* a prompt technique requires long-context input
* a prompt technique increases latency or token cost
* a prompt technique is vulnerable to prompt injection
* a prompt technique produces valid structured output

Evidence may come from papers, benchmark reports, evaluation runs, documentation, source code, release notes or observed behavior.

Implementation-specific claims should include model version, prompt text or template version, retrieval configuration, evaluation dataset and metric when available.
