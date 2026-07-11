# Policy Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how policies are represented in the RAG Knowledge Model.

Policies are rules, constraints, governance requirements and operational guardrails that shape how RAG entities may be selected, configured, invoked, evaluated or deployed.

The Policy Model answers the question:

> **What rule or constraint governs a RAG entity, workflow, tool, provider or artifact, and how should that governance be represented as reusable knowledge?**

---

# Core Principle

A policy is first-class knowledge when it affects trust, safety, compliance, reproducibility, access, cost or operational behavior.

It is not only an implementation setting.

A policy explains why an entity can be used, how it must be used and what constraints apply to its behavior.

```text
Tool GOVERNED_BY Policy
Workflow GOVERNED_BY Policy
Provider GOVERNED_BY Policy
Component SECURED_BY Policy
Policy REFERENCES Reference
Policy SUPPORTS Evaluation Metric
```

Representing policies explicitly makes RAG systems easier to audit, compare, govern and export as graph knowledge.

---

# Policy

A Policy represents a rule or constraint that applies to one or more RAG entities or process artifacts.

A policy may describe:

* access control
* data handling
* source trust requirements
* citation requirements
* retention limits
* safety constraints
* privacy requirements
* provider usage constraints
* cost limits
* evaluation gates
* human approval requirements
* logging and audit requirements

A policy should be modeled when it has reusable semantic meaning beyond a single local configuration file.

Preferred:

```text
Generated answers must cite at least one retrieved source document when the workflow produces compliance guidance.
```

Avoid:

```text
Use safe settings.
```

The avoided statement does not identify the rule, governed behavior, scope or verification condition.

---

# Policy Boundary

Every policy should have a clear boundary.

The boundary identifies:

* what behavior or entity is governed
* when the policy applies
* who or what enforces the policy
* what evidence or reference defines the policy
* what outcome indicates compliance
* what happens when the policy is violated

Policies with unclear boundaries are difficult to enforce, evaluate or cite as evidence.

---

# Policy Type

Policy type describes the primary governance role of the policy.

Canonical policy types include:

```text
Access Policy
Data Handling Policy
Privacy Policy
Security Policy
Source Trust Policy
Citation Policy
Retention Policy
Cost Policy
Evaluation Policy
Human Review Policy
Provider Policy
Operational Policy
Compliance Policy
Other
```

The policy type should describe the dominant governance function, not every downstream effect.

---

# Scope

Policy scope describes where the policy applies.

Common policy scopes include:

* entity
* workflow
* workflow step
* tool invocation
* provider dependency
* dataset use
* artifact lifecycle
* evaluation result
* deployment environment
* user group
* jurisdiction

Scope should be explicit when the same policy applies differently across contexts.

For example, a retention policy for execution traces may apply to production monitoring artifacts but not to public benchmark datasets.

---

# Requirement

A policy requirement is a specific condition that must be satisfied.

Requirements should be stated in verifiable terms whenever possible.

Examples include:

* retrieved content must include source identifiers
* generated answers must preserve citation links
* personally identifying information must not be stored in traces
* a tool that changes external state must require authorization
* a workflow must fail closed when source trust cannot be established
* evaluation runs must record dataset version and metric configuration

Requirements may be mandatory, recommended, conditional or prohibited.

The requirement level should be explicit when it affects enforcement or interpretation.

---

# Enforcement

Enforcement describes how the policy is applied.

Enforcement may be:

* manual review
* automated validation
* runtime guardrail
* workflow gate
* access control rule
* provider contract
* deployment configuration
* evaluation threshold
* audit review

RKM should distinguish between a policy requirement and its enforcement mechanism.

For example, a citation policy may require source-backed answers, while a workflow step enforces that policy by rejecting answers without source references.

---

# Compliance Evidence

Compliance evidence records why a policy requirement is believed to be satisfied, violated or not applicable.

Evidence may include:

* validation results
* evaluation reports
* audit logs
* configuration snapshots
* source documentation
* provider documentation
* benchmark results
* human review records

Compliance evidence should reference the policy, governed entity and observation context when that information is available.

---

# Relationship Use

Policies should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Tool GOVERNED_BY Policy
Workflow GOVERNED_BY Policy
Provider GOVERNED_BY Policy
Component SECURED_BY Policy
Policy REQUIRES Component
Policy DEPENDS_ON Provider
Policy REFERENCES Reference
Policy SUPPORTS Evaluation Metric
Evaluation Metric MEASURES Policy
Evidence SUPPORTS Claim
```

Relationship targets should use stable identifiers whenever the target concept is represented as an RKM entity.

Plain prose may explain local policy intent, but reusable governance, enforcement, dependency and evidence relationships should be represented structurally.

---

# Policy vs Metadata

Metadata describes the repository document.

Policy describes governance knowledge about the represented concept or process.

For example, `metadata.reviewState` records the review status of an RKM file. A policy may define that generated answers in a production workflow require human review before publication.

The first is document metadata. The second is domain knowledge.

---

# Policy vs Claim

A policy defines a rule or constraint.

A claim asserts something about an entity or behavior.

Example:

```text
Policy: Answers must include citations when generated from retrieved policy documents.
Claim: A workflow satisfies the citation policy for a named evaluation dataset.
Evidence: Evaluation results show citation coverage for the workflow under a specified protocol.
```

The policy should not be treated as evidence by itself. Evidence supports claims about whether the policy exists, applies or was satisfied.

---

# Policy vs Guardrail

A guardrail is an enforcement mechanism or runtime control.

A policy is the rule that the guardrail implements or supports.

For example, a prompt injection filter may be a guardrail. The policy may state that untrusted retrieved text must not modify system instructions.

Representing this distinction helps RKM compare governance intent separately from implementation mechanism.

---

# Modeling Guidance

Policy knowledge should be represented structurally when it affects entity selection, workflow design, operational risk or evidence-backed claims.

A complete policy representation should identify:

* policy type
* governed scope
* requirements
* requirement level
* enforcement mechanism
* applicable context
* exceptions
* evidence and references
* related claims

Do not encode durable policy knowledge only as prose when it affects graph export, evaluation, compliance or operational behavior.

---

# Summary

Policies describe the governance constraints that shape RAG systems.

In RKM, policies connect tools, workflows, providers, components, artifacts, claims, evidence and references into auditable structured knowledge.

Policy modeling should preserve the distinction between rules, enforcement mechanisms, compliance evidence and claims about compliance.
