# Security Control Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how security controls are represented in the RAG Knowledge Model.

Security controls describe reusable mechanisms that protect assets, reduce threats, enforce policies or verify secure behavior across RAG entities, workflows, tools, providers and deployments.

The Security Control Model answers the question:

> **What control protects a RAG asset or boundary, which threat does it address, and what evidence shows that the control applies?**

---

# Core Principle

A security control is structured knowledge when it affects whether a RAG entity, workflow or artifact can be trusted, governed, deployed or compared.

It is not only a configuration setting or operational checklist item.

A security control captures the protected asset, boundary, threat, mitigation, applicability condition, verification method, related policy, claim, evidence and reference.

```text
Component SECURED_BY Policy
Workflow GOVERNED_BY Policy
Tool GOVERNED_BY Policy
Tool OBSERVED_BY Component
Evaluation Metric MEASURES Artifact
Evidence SUPPORTS Claim
Policy REFERENCES Reference
```

Representing controls explicitly makes security knowledge reusable across architecture documentation, schemas, validation, evaluation and graph export.

---

# Security Control Fragment

RKM currently represents security controls as embedded structured fragments.

The reusable schema is `schema/definitions/security-control.schema.json`.

This definition intentionally omits first-class identity, metadata, description and top-level relationships. A standalone Security Control entity should be introduced only after shared identity support, entity type registry support and relationship guidance exist for that entity type.

An embedded security control fragment may appear inside entities, workflows, deployments, tool contracts, policies or evidence records when the control has reusable semantic value within that containing document.

Examples include:

* authorization filtering for retrieval over private documents
* prompt injection mitigation at the retrieval-to-generation boundary
* citation verification before an answer is returned
* scoped credentials for tool invocation
* tenant isolation in a hosted vector database
* audit logging for state-changing agent tools
* retention limits for traces that contain sensitive source material

---

# Control Type

Control type describes the primary mechanism represented by the control.

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

The control type should identify the dominant security mechanism.

For example, a workflow step that checks whether retrieved chunks are visible to the requesting user is an `Authorization Control`, even if the same workflow also emits logs and returns citations.

---

# Boundary

Every security control should define the boundary where it applies.

The boundary identifies:

* the source and target of the interaction
* the asset, artifact or capability crossing the boundary
* the RAG stages where the boundary is relevant
* the actor, tool, provider, workflow step or deployment context involved
* the policy that governs the boundary
* the verification method used to show that the control applies

Common boundary types include:

* entity boundary
* workflow boundary
* workflow step boundary
* tool invocation boundary
* provider boundary
* deployment boundary
* dataset boundary
* artifact boundary
* user boundary
* tenant boundary
* network boundary

Boundaries should be explicit because the same control may protect different assets in different contexts.

---

# Protected Asset

A protected asset is any entity, artifact, data item or operational capability whose exposure, modification or misuse has security impact.

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

Protected assets should be represented structurally when claims, evidence, policies, workflows or deployment decisions depend on them.

---

# Threat and Mitigation

A threat describes a security-relevant failure mode or adversarial condition.

A mitigation describes how the control reduces likelihood, impact or exposure.

Examples include:

* unauthorized retrieval mitigated by metadata filters and policy enforcement
* prompt injection mitigated by source filtering, instruction separation and answer verification
* credential exposure mitigated by scoped tool permissions and audit logging
* sensitive trace retention mitigated by redaction and retention controls
* insecure provider dependency mitigated by provider policy review and deployment constraints

Threats and mitigations should remain separate.

The threat explains what can go wrong. The mitigation explains what the control does about it.

---

# Applicability

Applicability describes when the control is relevant.

Applicability may depend on:

* deployment environment
* data sensitivity
* user role
* tenant boundary
* provider dependency
* workflow stage
* tool side effect
* regulatory or governance requirement
* source trust level

Applicability should be explicit when a control applies only under certain conditions.

For example, a human approval control may be required for state-changing tools in production but not for read-only retrieval in a local benchmark.

---

# Verification

Verification describes how RKM consumers know that the control exists, applies or is effective.

Verification may include:

* policy review
* configuration inspection
* automated test
* audit log review
* provider documentation
* benchmark or evaluation result
* runtime observation
* human review

Verification should link to claims and evidence when it supports security, governance, compliance or operational suitability.

Evidence should describe what was observed, where it was observed and which control statement the observation supports.

---

# Relationship Use

Security control knowledge should use canonical relationships when the association has reusable graph meaning.

Common relationship patterns include:

```text
Component SECURED_BY Policy
Workflow GOVERNED_BY Policy
Tool GOVERNED_BY Policy
Provider GOVERNED_BY Policy
Workflow DEPENDS_ON Provider
Tool REQUIRES Component
Tool OBSERVED_BY Component
Tool LOGGED_BY Component
Evaluation Metric MEASURES Artifact
Evidence SUPPORTS Claim
Policy REFERENCES Reference
```

Relationship targets should use stable identifiers whenever the target concept is represented as an RKM entity.

Plain prose may explain local control behavior, but reusable security, governance, dependency, observation and evidence knowledge should be represented structurally.

---

# Security Control vs Policy

A security control is a mechanism or boundary behavior.

A policy is a rule or governance requirement.

For example, a policy may require document-level authorization during retrieval. A security control describes how the retriever enforces that requirement and how the enforcement can be verified.

---

# Security Control vs Security Concern

A security concern describes the risk or condition that matters.

A security control describes the mechanism that protects against the concern.

For example, prompt injection through retrieved content is a security concern. Source trust filtering and answer verification are security controls that may mitigate that concern.

---

# Modeling Guidance

Use embedded security control fragments when the control is part of another first-class RKM entity or process description.

Do not model Security Control as a standalone entity until the identity model, entity type registry and schema registry explicitly support that entity type.

Prefer structured fields over prose when the control has reusable meaning for graph export, validation, evaluation, governance or comparison.

Use claims and evidence for assertions about control effectiveness, compliance, provider behavior or operational enforcement.
