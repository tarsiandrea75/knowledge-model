# Security Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how security is represented in the RAG Knowledge Model.

Security covers the controls, boundaries, threats, mitigations and evidence that determine whether RAG entities can be used without exposing source data, prompts, generated answers, credentials, traces or operational capabilities beyond their intended scope.

The Security Model answers the question:

> **What security concern or control affects a RAG entity, workflow, deployment or artifact, and how should that concern be represented as reusable knowledge?**

---

# Core Principle

Security is first-class knowledge when it affects trust, access, confidentiality, integrity, availability, governance, compliance or operational risk.

It is not only an infrastructure setting.

Security knowledge explains which entities are protected, which controls apply, which threats are mitigated, which policies govern behavior and which evidence supports a security claim.

```text
Component SECURED_BY Policy
Workflow GOVERNED_BY Policy
Tool REQUIRES Provider
Provider SUPPORTS Framework
Evidence SUPPORTS Claim
Policy REFERENCES Reference
```

Representing security explicitly makes RAG systems easier to evaluate, compare, audit and operate across different deployment contexts.

---

# Security Concern

A Security Concern represents a condition that may affect the secure operation of a RAG system.

Security concerns may include:

* unauthorized access to source documents
* prompt injection through retrieved content
* leakage of private data into generated answers
* exposure of credentials through tool invocation
* insecure provider dependency
* missing audit trail for state-changing tools
* insufficient tenant isolation
* stale or untrusted source material
* retrieval over documents outside the user's authorization scope
* unverified generated citations

A security concern should be modeled when it has reusable meaning for selecting, configuring, evaluating or governing RAG entities.

Preferred:

```text
Retriever returns only chunks whose access-control metadata permits the requesting user to read the underlying source document.
```

Avoid:

```text
Make retrieval secure.
```

The avoided statement does not identify the protected asset, control boundary, authorization condition or verification target.

---

# Security Boundary

Every security statement should define a clear boundary.

The boundary identifies:

* the protected entity or artifact
* the actor, workflow, tool or provider that may access it
* the data that crosses the boundary
* the policy that governs access or handling
* the control that enforces the policy
* the evidence that supports the claim

Boundaries are especially important in RAG because source documents, embeddings, prompts, retrieval traces and generated answers may have different security requirements even when they participate in the same workflow.

---

# Protected Asset

A protected asset is any entity, artifact or operational capability whose exposure or modification affects security.

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

Protected assets should be represented structurally when they are reused by claims, evidence, policies, workflows or deployment decisions.

---

# Control Type

Control type describes the primary security mechanism.

Canonical control types include:

```text
Authentication Control
Authorization Control
Access Control
Data Redaction Control
Encryption Control
Network Isolation Control
Tenant Isolation Control
Prompt Injection Mitigation
Source Trust Control
Citation Verification Control
Tool Permission Control
Credential Management Control
Audit Logging Control
Retention Control
Human Approval Control
Other
```

The control type should describe the dominant mechanism, not every downstream benefit.

---

# Threat and Mitigation

A threat describes a security-relevant failure mode or adversarial condition.

A mitigation describes the control or workflow behavior that reduces the likelihood or impact of the threat.

Examples include:

* prompt injection mitigated by source filtering, instruction separation and answer verification
* unauthorized retrieval mitigated by metadata filters and policy enforcement
* credential exposure mitigated by scoped tool permissions and audit logging
* sensitive trace retention mitigated by redaction and retention policies
* provider data exposure mitigated by deployment constraints and provider policy review

Threats and mitigations should be linked to claims and evidence when they support suitability, compliance or operational decisions.

---

# Relationship Use

Security knowledge should use canonical relationships when the association has reusable graph meaning.

Common relationship patterns include:

```text
Component SECURED_BY Policy
Workflow GOVERNED_BY Policy
Tool GOVERNED_BY Policy
Provider GOVERNED_BY Policy
Workflow DEPENDS_ON Provider
Tool REQUIRES Component
Component OBSERVED_BY Tool
Tool LOGGED_BY Component
Evaluation Metric MEASURES Artifact
Evidence SUPPORTS Claim
Policy REFERENCES Reference
```

Relationship targets should use stable identifiers whenever the target concept is represented as an RKM entity.

Plain prose may explain local security behavior, but reusable security controls, dependencies, evidence and governance should be represented structurally.

---

# Security vs Policy

Security describes protected assets, threats, controls and security-relevant behavior.

Policy describes the rule or governance requirement that applies to that behavior.

For example, a security model may describe authorization filtering during retrieval. A policy may require that the authorization filter is enforced for production workflows that retrieve private source documents.

---

# Security vs Observability

Observability records what happened during execution.

Security explains whether the observed behavior satisfied a control, exposed a risk or supported a mitigation.

For example, a retrieval trace may record that a metadata filter was applied. That observation becomes security evidence when it supports a claim that the workflow enforces document-level authorization during retrieval.

---

# Security Evidence

Security claims require evidence when they describe access control, isolation, redaction, auditability, provider behavior, compliance support or mitigation effectiveness.

Useful evidence includes:

* policy definitions
* provider documentation
* audit logs
* validation reports
* evaluation results
* configuration snapshots
* workflow traces
* human review records
* source references

Evidence should identify the entity, workflow, deployment context, policy, control and observation date whenever that information affects interpretation.
