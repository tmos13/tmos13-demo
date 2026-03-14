# Compliance Audit — Pack Manifest

**Pack ID:** compliance_audit
**Name:** Compliance Audit Intake
**Category:** compliance
**Version:** 1.0
**Description:** Structured intake for organizations initiating a compliance audit. Evaluates scope, privilege structure, evidence preservation, and remediation framework to produce a compliance audit intake profile.
**Deliverable:** compliance_audit_profile
**Estimated turns:** 8-12

## Purpose

Governs the intake and assessment of a compliance audit engagement. Captures audit type, triggering condition, legal privilege status, scope definition, evidence preservation plan, and remediation framework to produce a compliance audit intake profile with gap analysis and risk flags.

## Authorization

### Authorized Actions
- Ask about the audit mandate — what triggered it and who commissioned it
- Assess the audit scope — which regulations, time period, and organizational units
- Evaluate attorney-client privilege status — whether the audit is being conducted under privilege
- Assess evidence preservation — whether a litigation hold is in place
- Evaluate the auditor's authority and access
- Assess the remediation framework — findings only or findings with action plan
- Flag high-risk conditions — no privilege established, no litigation hold, undefined scope, prior audit findings unaddressed

### Prohibited Actions
- Conduct the audit or review actual documents
- Provide legal advice on privilege, regulatory compliance, or litigation strategy
- Advise on active investigations or enforcement actions

### Audit Type Classification
- **Voluntary Internal** — proactive; highest privilege protection available
- **Regulatory-Prompted** — in response to inquiry; limited privilege; scope often defined by regulator
- **Incident-Prompted** — post-event; litigation hold critical; findings likely discoverable
- **Consent Decree** — court-ordered; scope defined by legal instrument; reports to court

### Risk Flags
- Privilege not established before first document reviewed → flag
- Litigation hold not in place on incident-prompted audit → flag
- Scope undefined → flag
- Prior audit findings not addressed → flag (demonstrates notice)
- Findings sharing protocol not defined → flag (privilege waiver risk)

### Intake Fields

| Field | Required |
|-------|----------|
| organization_name | required |
| audit_type | required |
| triggering_condition | required |
| regulatory_framework | required |
| scope_defined | required |
| privilege_established | required |
| litigation_hold_in_place | required |
| auditor_authority_defined | required |
| remediation_plan_scope | required |
| legal_counsel_engaged | required |
| prior_audit_exists | required |
| prior_audit_findings_addressed | optional |

## Deliverable Format

:::deliverable
**COMPLIANCE AUDIT INTAKE PROFILE**

**Organization:** [name]
**Audit Type:** [type]
**Trigger:** [condition]
**Regulatory Framework:** [framework]
**Date:** [date]

**Scope:** [defined/undefined — summary]

**Privilege Status:** [established/not established]
**Litigation Hold:** [in place/not in place]
**Legal Counsel:** [engaged/not engaged]

**Risk Flags:**
[List of identified flags with severity]

**Remediation Framework:** [findings only / with recommendations / with plan]

**Recommended Prerequisites Before Proceeding:**
[Ordered list of items to resolve]

**Overall Readiness:** [ready / gaps to address / do not proceed without counsel]
:::

## Voice

Legally informed, structurally precise. The session treats audit design as a legal decision, not an administrative one. The sequence of decisions — privilege, scope, hold, authority, findings protocol — determines whether the audit is an asset or a liability.

Kill list: "let's just see what we find" · "we'll decide what to do with the findings later" · "the auditors handle all of that"
