# Threat Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how threats are represented in the RAG Knowledge Model.

Threats describe adversarial, accidental or environmental conditions that may compromise confidentiality, integrity, availability, trust, safety, governance or operational suitability in a RAG context.

The Threat Model answers the question:

> **What condition can harm a RAG entity, workflow, artifact or deployment, what boundary exposes it, and how should that threat connect to controls, policies, claims and evidence?**

---

# Core Principle

A threat is structured knowledge when it affects security, safety, governance, evaluation, deployment or operational trust.

It is not only a warning.

A threat identifies the exposed boundary, triggering condition, affected asset, likely impact, mitigation, security control, governing policy and evidence context.

```text
Component SECURED_BY Policy
Workflow GOVERNED_BY Policy
Tool GOVERNED_BY Policy
Provider MONITORED_BY Tool
Technique MITIGATES Problem
Evidence SUPPORTS Claim
Evidence REFERENCES Reference
```

RKM currently represents threats as embedded structured fragments inside security controls, risks, policies, claims, evidence and related domain models. A threat should become a first-class identity-backed entity only after shared identity support, registry support, relationship guidance and schema support exist for that entity type.

---

# Threat

A threat is a condition or actor behavior that can cause harm when it crosses or exploits a boundary in a RAG system.

RAG threats may involve:

* prompt injection through retrieved content
* unauthorized retrieval from private source documents
* leakage of sensitive data into generated answers
* citation manipulation or unsupported citation claims
* credential exposure through tool invocation
* provider dependency failure or policy conflict
* poisoned source material entering an index
* tenant isolation failure in shared infrastructure
* stale content being treated as authoritative
* incomplete audit evidence for state-changing workflows

A threat should be scoped to a concrete boundary and asset.

Preferred:

```text
Untrusted retrieved content may contain instructions that conflict with the system prompt when the workflow inserts source passages into the generation context without instruction separation or source trust filtering.
```

Avoid:

```text
Prompt injection is dangerous.
```

The avoided statement names a concern but does not identify the exposed workflow, protected asset, boundary, triggering condition or mitigation target.

---

# Threat Boundary

Every threat should define the boundary where exposure occurs.

The boundary identifies:

* the exposed entity, workflow, tool, provider, dataset or artifact
* the protected asset or operational capability
* the actor, source, provider or system component involved
* the data or instruction crossing the boundary
* the RAG stage where the exposure occurs
* the security control or policy that should reduce the exposure
* the evidence that supports the threat assessment

Threat boundaries prevent RKM from treating local deployment hazards as universal properties of a technique, provider or component.

For example, prompt injection is a threat for workflows that insert untrusted retrieved content into prompts. It is not the same exposure for a static benchmark that evaluates retrieval only and never invokes a generator.

---

# Threat Type

Threat type describes the dominant source of harm or exposure.

Canonical threat types include:

```text
Prompt Injection Threat
Unauthorized Access Threat
Data Leakage Threat
Source Poisoning Threat
Citation Integrity Threat
Credential Exposure Threat
Tenant Isolation Threat
Provider Dependency Threat
Auditability Threat
Freshness Threat
Tool Invocation Threat
Availability Threat
Governance Threat
Other
```

The threat type should describe the primary exposure, not every downstream consequence.

For example, a retrieved document that contains malicious instructions is a `Prompt Injection Threat` when the main harm is instruction override during generation. It may also create governance or citation concerns, but those secondary effects should be modeled separately when they have reusable meaning.

---

# Protected Asset

A protected asset is the entity, artifact, data item or operational capability that may be harmed or exposed by the threat.

Common protected assets include:

* source document
* parsed document
* chunk
* embedding vector
* metadata filter
* retrieval result
* prompt
* generated answer
* citation set
* trace record
* evaluation result
* tool credential
* provider configuration
* operational capability

The protected asset should be explicit when the threat informs security controls, policy requirements, evaluation design, deployment decisions or claims about suitability.

---

# Likelihood and Impact

Threat assessment may include likelihood and impact when there is enough context.

Likelihood describes how probable the threat is under the stated boundary and assumptions.

Impact describes the harm if the threat occurs.

Both values should be scoped. A high-impact credential exposure threat in a production agent may be irrelevant to a read-only local benchmark, while a low-likelihood provider outage may matter for a workflow with strict availability requirements.

When likelihood or impact is uncertain, the assessment should be represented as a claim with confidence and evidence rather than as an unconditional fact.

---

# Mitigation

A mitigation is a technique, policy, security control, workflow step, component, evaluation method or operational practice that reduces threat likelihood, impact or uncertainty.

Mitigations may include:

* source trust filtering
* instruction separation
* citation verification
* document-level authorization
* scoped tool credentials
* human approval for state-changing tools
* tenant isolation
* provider policy review
* audit logging
* retention limits
* freshness monitoring
* fallback routing

Mitigation should remain separate from the threat so RKM can compare alternatives and preserve tradeoffs.

Examples:

```text
Technique MITIGATES Problem
Workflow GOVERNED_BY Policy
Component SECURED_BY Policy
Tool LOGGED_BY Component
Evaluation Metric MEASURES Artifact
Evidence SUPPORTS Claim
```

A mitigation should not imply that a threat is eliminated unless evidence supports that stronger claim.

---

# Relationship Use

Threat knowledge should use canonical relationships when the association has reusable graph meaning.

Threat itself is not currently a registered first-class entity type. Until identity and registry support exists, threats should be represented through structured fields, security controls, policies, risks, problems, claims, evidence and documented concepts.

Useful relationship patterns include:

```text
Workflow GOVERNED_BY Policy
Tool GOVERNED_BY Policy
Component SECURED_BY Policy
Provider MONITORED_BY Tool
Tool LOGGED_BY Component
Technique MITIGATES Problem
Workflow HAS_LIMITATION Limitation
Evidence SUPPORTS Claim
Evidence REFERENCES Reference
```

Plain prose may explain local threat context, but reusable threat exposure, mitigation, evidence and governance should be represented structurally whenever possible.

---

# Threat vs Risk

A threat is a condition or behavior that can cause harm.

A risk is exposure to a possible negative outcome under specific conditions.

For example, prompt injection through retrieved content is a threat. A workflow has risk when it inserts untrusted retrieved content into the generation prompt without controls that isolate source content from instructions.

Threats explain what may act against the system. Risks explain how exposed a specific entity, workflow or deployment is to harm.

---

# Threat vs Problem

A problem is a recurring challenge, failure mode or requirement gap.

A threat is security-relevant or trust-relevant harm potential at a boundary.

For example, unsupported generated answers are a problem. Citation manipulation is a threat when an actor or source condition can cause the workflow to present misleading citation support.

Problems can motivate techniques and evaluation. Threats motivate controls, policies, monitoring, evidence requirements and deployment constraints.

---

# Threat vs Security Control

A security control is the mechanism that protects an asset, governs a boundary or reduces exposure.

A threat is the condition that makes the control necessary.

For example, document-level authorization is a security control. Unauthorized retrieval is a threat that the control mitigates when private source documents are indexed or retrieved.

The security control should describe enforcement and verification. The threat should describe the exposed boundary, asset, triggering condition and possible harm.

---

# Evidence

Threat statements should be supported by evidence when they affect governance, deployment, suitability or comparative claims.

Useful evidence includes:

* incident reports
* security analyses
* provider documentation
* policy documents
* benchmark results
* evaluation traces
* audit logs
* configuration reviews
* human review records

Evidence should identify what was observed, which boundary was assessed and which claim about the threat or mitigation it supports.

---

# Schema Representation

Threats are currently represented as embedded fragments rather than standalone entity documents.

The reusable security control definition includes embedded threat structure in `schema/definitions/security-control.schema.json`.

Threat fields inside schemas should preserve:

* threat type
* statement
* protected asset
* boundary
* triggering condition
* likely impact
* mitigation
* related controls or policies
* supporting claims, evidence and references

A standalone threat schema should not be introduced until `Threat` is added to shared identity support, the entity type registry and relationship guidance.
