# Complexity classification

Classify after inspecting the request, authority, live repository, likely
files, contracts, and Git state. Select the highest applicable level and record
the facts that triggered it. A precise prompt may lower ambiguity; it cannot
lower a deterministic risk floor.

| Level | Inclusion test | Exclusions | Example | Minimum route |
| --- | --- | --- | --- | --- |
| L0 Mechanical | One obvious resource, copy, spacing, or fixture change with no behavior effect. | Any API, state, lifecycle, security, build, or architecture effect. | Correct one string resource or test fixture value. | Direct Executor and deterministic checks, or Verifier. |
| L1 Localized | One understood behavior owner and a small change. | Public contract, migration, security, persistence, and cross-module decisions. | Correct a local validation branch with focused tests. | Direct Executor and independent Verifier. |
| L2 Moderate | Several related files, contained state change, known API mapping, local build configuration, or precise multi-step work without an architecture choice. | Uncertain root cause, public interface adjustment, multi-module coordination, or a risk floor above L2. | Add a known API field through mapper, UI state, and tests. | Planner, Executor, independent Verifier. |
| L3 Complex | Uncertain root cause; concurrency, lifecycle, or navigation interaction; multi-module coordination; public interface adjustment; or broad test impact without new architecture. | New subsystem/pattern, migrations, DI/module-boundary changes, or critical-risk work. | Trace a rotation/navigation race across shared modules. | Investigator when needed, Planner, Executor, independent Verifier. |
| L4 Architectural | New subsystem or pattern, ownership redesign, framework/UI migration, database migration, DI/module-boundary change, background execution, authentication, or cryptography change. | Destructive/irreversible migration, plausible data or credential loss, and other L5 triggers. | Replace a screen stack or introduce a new secure-auth flow. | Planner, explicit human approval, Executor, independent Verifier. |
| L5 Critical | Payment, transfer, OTP, session, or PII risk; destructive or irreversible migration; signing/entitlement/release risk; cross-platform security boundary; or high-blast-radius architecture. | None once triggered. | Change payment authorization, release signing, or a destructive account-data migration. | Investigator/Planner, explicit human approval, Executor, independent Verifier. |

## Deterministic floors

- Security, authentication, payment, persistence migration, signing,
  entitlements, and a new dependency are at least L4.
- A destructive migration or plausible data or credential loss is L5.
- Concurrency plus lifecycle or navigation is at least L3.
- Apply the L5 floor over every lower classification. If multiple tests apply,
  record all triggers and use the highest result.
