# Risk Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how risk is represented in the RAG Knowledge Model.

Risk describes an uncertain condition that may negatively affect trust, safety, quality, cost, compliance, security, reliability or operational suitability in a RAG system.

The Risk Model answers the question:

> **What could go wrong in a RAG context, what entity or workflow is exposed, and how should that exposure be connected to controls, claims, evidence and tradeoffs?**

---

# Core Principle

Risk is structured knowledge when it affects selection, evaluation, operation, governance or comparison.

It is not only a warning label.

A risk statement should identify the exposed entity or artifact, the triggering condition, the likely impact, the affected quality attributes, the mitigation strategy and the evidence or claim context that supports the assessment.

```text
Workflow GOVERNED_BY Policy
Component SECURED_BY Policy
Tool LOGGED_BY Component
Provider MONITORED_BY Tool
Technique MITIGATES Problem
Evidence SUPPORTS Claim
Evidence REFERENCES Reference
```

RKM may describe risks before representing them as first-class identity-backed entities. A risk becomes a candidate entity only when it needs stable identity, lifecycle metadata, relationships, evidence, ownership or independent governance across the repository.

---

# Risk

A risk is an uncertain condition that may cause harm, reduce suitability or invalidate a claim if it occurs.

RAG risks may involve:

* unsupported generated answers
* retrieval from stale source material
* unauthorized access to private documents
* prompt injection through retrieved content
* citation mismatch
* provider outage
* high or unpredictable inference cost
* weak evaluation coverage
* incomplete observability
* unsafe tool invocation
* loss of reproducibility

A risk should be scoped to a concrete context.

Preferred:

```text
Retrieved content may contain instructions that conflict with the system prompt when untrusted documents are inserted into the generation context without isolation.
```

Avoid:

```text
Prompt injection is risky.
```

The avoided statement names a concern but does not identify the exposed workflow, triggering condition, impact or control boundary.

---

# Risk Boundary

Every risk statement should define a boundary.

The boundary identifies:

* the exposed entity, workflow, tool, provider or artifact
* the condition that can trigger the risk
* the affected quality attributes or governance concerns
* the likely impact if the risk occurs
* the assumptions that limit the assessment
* the mitigation or control that reduces the exposure
* the evidence that supports the risk assessment

Risk boundaries prevent RKM from treating local implementation concerns as universal properties of a technique, model or provider.

For example, stale retrieval results may be a workflow risk when the corpus changes frequently and the indexing workflow does not preserve freshness evidence. The same retriever may be suitable for a static archive where source freshness is not a primary quality attribute.

---

# Risk Type

Risk type describes the dominant source of exposure.

Canonical risk types include:

```text
Retrieval Risk
Generation Risk
Citation Risk
Security Risk
Privacy Risk
Provider Risk
Cost Risk
Latency Risk
Evaluation Risk
Observability Risk
Governance Risk
Operational Risk
Reproducibility Risk
Tool Invocation Risk
Other
```

The risk type should describe the primary exposure, not every downstream consequence.

---

# Likelihood and Impact

Risk assessment may include likelihood and impact when there is enough evidence or operational context.

Likelihood describes how probable the risk is under the stated conditions.

Impact describes the severity of the consequence if the risk occurs.

Both values should be qualified by scope. A high-impact privacy risk in a production workflow may be irrelevant to a public benchmark dataset, while a low-likelihood provider outage may still matter for a workflow with strict availability requirements.

When likelihood or impact is uncertain, the assessment should be represented as a claim with confidence and evidence instead of an unconditional fact.

---

# Mitigation

A mitigation is a technique, policy, control, workflow step, component or evaluation method that reduces risk likelihood, impact or uncertainty.

Mitigations may include:

* source trust filtering
* instruction isolation
* citation verification
* document-level authorization
* provider fallback routing
* budget limits
* timeout and retry policy
* human review
* audit logging
* redaction
* benchmark coverage
* freshness monitoring

Mitigation should be modeled separately from risk so that RKM can compare alternatives and preserve tradeoffs.

Examples:

```text
Technique MITIGATES Problem
Workflow GOVERNED_BY Policy
Component SECURED_BY Policy
Tool LOGGED_BY Component
Evaluation Metric MEASURES Artifact
Evidence SUPPORTS Claim
```

A mitigation should not imply that a risk is eliminated unless evidence supports that stronger claim.

---

# Relationship Use

Risk knowledge should use canonical relationships when the association has reusable graph meaning.

Risk itself is not currently a registered first-class entity type. Until identity and registry support exists, risk should be represented through structured fields, claims, limitations, problems, policies, controls, evidence and documented concepts.

Useful relationship patterns include:

```text
Workflow GOVERNED_BY Policy
Tool GOVERNED_BY Policy
Component SECURED_BY Policy
Provider MONITORED_BY Tool
Component OBSERVED_BY Tool
Technique MITIGATES Problem
Workflow HAS_LIMITATION Limitation
Technique HAS_TRADEOFF Tradeoff
Evidence SUPPORTS Claim
Evidence REFERENCES Reference
```

Plain prose may explain local risk context, but reusable risk exposure, mitigation, evidence and governance should be modeled structurally whenever possible.

---

# Risk vs Problem

A problem is a known challenge or failure mode.

A risk is exposure to a possible negative outcome under specific conditions.

For example, citation mismatch is a problem. A workflow has citation risk when it generates answers with citations that may not support the cited answer spans under its retrieval, assembly and verification design.

Problems can be targets for mitigation relationships. Risks can describe why a problem matters in a particular workflow, entity, use case or deployment context.

---

# Risk vs Limitation

A limitation is a known boundary of usefulness.

A risk is an uncertain exposure that may or may not occur during use.

For example, an embedding model may have a limitation around rare identifier matching. A workflow using that model has retrieval risk when users ask identifier-heavy questions and no lexical fallback is available.

Limitations should be used when the constraint is known. Risk should be used when the concern depends on conditions, probability, controls or operational context.

---

# Risk vs Policy

Policy defines a rule or governance requirement.

Risk explains why that rule may be needed and what harm it helps reduce.

For example, a source trust policy may require filtering retrieved content by approved source class. The associated risk is that untrusted retrieved content may introduce unsupported, unsafe or adversarial instructions into the answer generation workflow.

Policies should be linked to evidence when they are used to support claims about risk reduction, compliance or operational suitability.

---

# Risk Evidence

Risk statements need evidence when they affect architecture decisions, suitability claims, governance requirements, operational controls or comparisons between alternatives.

Useful evidence includes:

* evaluation results
* benchmark findings
* provider documentation
* policy definitions
* audit logs
* workflow traces
* incident records
* security reviews
* source references
* human review records

Evidence should identify the assessed entity, context, date, method, observed condition and claim being supported or qualified.
