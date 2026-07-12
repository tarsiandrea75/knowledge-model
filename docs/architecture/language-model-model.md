# Language Model Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how language models are represented in the RAG Knowledge Model.

Language models are model entities used for generation, reasoning, synthesis, query transformation, context compression, citation behavior, tool use, evaluation or workflow control in Retrieval-Augmented Generation systems.

The Language Model Model answers the question:

> **How should RKM describe language models whose behavior affects retrieval, grounding, generation or orchestration in a RAG system?**

---

# Core Principle

A language model is not only a model name, provider endpoint or generic generator.

A language model is a reusable capability with defined inputs, outputs, context limits, generation behavior, access conditions, operational constraints and evidence-supported claims.

```text
Provider PROVIDES Language Model
Framework SUPPORTS Language Model
Technique USES Language Model
Prompt Technique REQUIRES Language Model
Agent USES Language Model
Benchmark EVALUATES Language Model
Language Model HAS_LIMITATION Limitation
```

Representing language models explicitly allows RKM to describe grounded generation quality, context handling, tool-use support, structured-output behavior, latency, cost, provider access, safety constraints and evaluation evidence separately from prompts, agents, workflows and frameworks.

---

# Language Model

A Language Model is an entity that consumes language-centered or multimodal input and produces generated text, code, structured data, tool calls or other language-mediated output.

Language models may be used to:

* generate grounded answers
* summarize retrieved context
* rewrite or expand queries
* decompose questions
* judge candidate relevance
* compress context
* produce citations
* call tools
* plan agent steps
* generate structured outputs
* evaluate answer faithfulness

Language model entities should identify what the model consumes, what it produces, which RAG stages it supports, what capabilities it exposes and which evidence supports claims about its behavior.

Preferred:

```text
Instruction-tuned language model that generates grounded answers from retrieved context and can emit structured citation objects.
```

Avoid:

```text
AI model for RAG.
```

The avoided statement does not identify the model role, inputs, outputs, grounding behavior or RAG responsibility.

---

# Language Model Boundary

Every language model should have a clear boundary.

The boundary identifies:

* whether the entity represents a concrete model, model family, release, checkpoint, hosted variant or fine-tuned derivative
* which input modalities the model accepts
* which output modalities the model can produce
* which context window, output limit or truncation behavior affects use
* which generation, reasoning, tool-use or structured-output capabilities are supported
* which provider, license, repository or access channel makes the model available
* which prompt techniques, agents, frameworks, benchmarks or workflows depend on the model

A language model should not be collapsed into the provider that serves it, the framework that integrates it or the prompt technique that shapes its behavior. Those entities have separate responsibilities and may change independently.

---

# Model Family and Type

Model family describes the broad architecture or product family of the language model.

Model type describes the primary operational role of the model.

Common language model types include:

```text
Base Model
Instruction Model
Chat Model
Reasoning Model
Tool Use Model
Long Context Model
Multimodal Generation Model
Code Generation Model
Domain Specific Model
Other
```

The type should describe the model capability, not the hosting provider or application that uses it.

More detailed knowledge should be represented through modalities, capabilities, context window, access profile, relationships, claims and evidence.

---

# Inputs and Outputs

Language model inputs describe what the model can consume.

Common inputs include:

* text
* code
* images
* audio
* video
* tables
* graphs
* multimodal records
* tool results
* retrieved context

Language model outputs describe what downstream components can consume.

Common outputs include:

* generated text
* code
* structured data
* tool calls
* citations
* relevance judgments
* plans
* summaries
* abstention decisions

Inputs and outputs should be structured when another prompt technique, agent, workflow, evaluator or component depends on them.

---

# Context Window

Context window knowledge describes the amount of input and output a language model can handle.

Important context knowledge includes:

* maximum input tokens
* maximum output tokens
* combined context limits
* tokenizer behavior
* context truncation behavior
* support for long-context retrieval workflows
* sensitivity to context ordering

Context limits affect chunking strategy, context assembly, citation behavior, latency, cost and evaluation interpretation.

Claims about effective long-context behavior should distinguish advertised limits from evidence-supported performance on retrieval, grounding or reasoning tasks.

---

# Capabilities

Language model capabilities describe reusable behavior that affects RAG design.

Common capabilities include:

* answer generation
* grounded generation
* citation generation
* summarization
* question answering
* reasoning
* planning
* tool use
* function calling
* structured output
* query rewriting
* context compression
* relevance judging
* code generation
* multilingual generation
* multimodal understanding

Capabilities should be represented structurally when they affect entity selection, relationship modeling, workflow design, evaluation or governance.

Capability claims should not be inferred from broad product descriptions when a precise behavior requires evidence.

---

# RAG Usage

RAG usage describes where the language model participates in a retrieval-augmented workflow.

Common usage roles include:

* query understanding
* query transformation
* retrieval planning
* context compression
* context assembly
* grounded answer generation
* citation generation
* tool selection
* agent planning
* answer verification
* evaluation

The same language model may support multiple RAG roles. Each role should be scoped to the prompt technique, workflow, framework or evidence context where the behavior is observed.

---

# Access and Deployment

Language model access describes how the model can be used.

Common access modes include:

* hosted API
* managed service
* open weights
* local runtime
* fine-tuning endpoint
* research release
* commercial license

Deployment characteristics may include latency class, cost class, batching support, quantization support, region availability, privacy constraints, rate limits and resource requirements.

Provider-hosted language models should be connected to Provider entities when provider behavior affects availability, pricing, policy, data handling, region support, versioning or reproducibility.

---

# Evaluation

Language model evaluation should identify the task, dataset, benchmark, metric, prompt technique, retrieval context and model configuration used to support a claim.

Important evaluation context includes:

* model version or release
* provider-hosted variant when relevant
* prompt technique
* retrieved context source
* dataset or benchmark
* evaluation metric
* decoding parameters
* tool-use configuration
* evaluation date

Claims about answer quality, faithfulness, citation behavior, reasoning, safety, latency, cost or structured-output reliability should not be generalized beyond the observed task, corpus, prompt, model version, provider configuration or workflow.

---

# Safety and Governance

Language model behavior may affect trust, compliance and operational risk.

Important safety and governance knowledge includes:

* safety policies
* usage restrictions
* data retention policy
* privacy constraints
* content filtering behavior
* refusal behavior
* prompt injection sensitivity
* auditability
* supported deployment controls

Safety and governance claims should be connected to references and evidence when they affect adoption, evaluation or suitability for a use case.

---

# Relationship Use

Language models should be connected through canonical relationships when those relationships have reusable semantic value.

Useful language model relationships include:

```text
Provider PROVIDES Language Model
Framework SUPPORTS Language Model
Technique USES Language Model
Prompt Technique REQUIRES Language Model
Agent USES Language Model
Workflow USES Language Model
Benchmark EVALUATES Language Model
Evaluation Metric MEASURES Language Model
Language Model COMPATIBLE_WITH Prompt Technique
Language Model HAS_LIMITATION Limitation
Language Model MITIGATES Problem
```

Relationship targets should use stable identifiers whenever the target is represented as an RKM entity.

Plain text may explain local context, but reusable support, dependency, compatibility, evaluation and limitation knowledge should be represented structurally.

---

# Claims and Evidence

Language model claims often become stale as providers update hosted models, publish new releases, change pricing, modify access policies or alter safety behavior.

Claims about quality, faithfulness, context length, supported modalities, tool-use support, structured-output reliability, latency, cost, availability, safety behavior or provider policy should cite evidence and references when they affect adoption or comparison.

Evidence should record the model version, provider context, evaluation date, dataset version, benchmark configuration, prompt technique and workflow configuration whenever those details are available.
