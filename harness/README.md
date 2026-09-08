# Harness artifact lifecycle

The harness records task-specific evidence below `harness/` without changing application sources merely to create process artifacts. Use one stable, lowercase `<task>` slug per request and retain the original date for every artifact in that task's lifecycle.

## Naming convention

```text
harness/context/YYYY-MM-DD-<task>-baseline.md
harness/plans/YYYY-MM-DD-<task>-implementation-contract.md
harness/executions/YYYY-MM-DD-<task>-execution-log.md
harness/reports/YYYY-MM-DD-<task>-investigation.md
harness/reports/YYYY-MM-DD-<task>-escalation.md
harness/reports/YYYY-MM-DD-<task>-verification.md
```

Use hyphenated task names such as `transfer-lifecycle` or `ios-locale-receipt`. Do not reuse a name for unrelated requests; a later attempt should use a new date or a more specific task slug.

## Content authorship, persistence, and lifecycle

| Artifact | Content author | Persistence authority | Purpose and later consumers |
| --- | --- | --- |
| `context/...-baseline.md` | Primary controller | Primary controller during an authorized implementation workflow | Captures instructions, authority, Git state, likely files, and known evidence. Investigator, Planner, Executor, and Verifier consume it. |
| `reports/...-investigation.md` | Investigator returns complete content in its response | Primary controller may persist it only during an authorized implementation workflow; never for terminal investigate-only unless the user separately asks to save it | Read-only evidence, hypotheses, root-cause confidence, and unknowns. Planner consumes it when investigation preceded planning. |
| `plans/...-implementation-contract.md` | Planner returns complete content in its response | Primary controller may persist it only during an authorized implementation workflow; never for terminal plan-only unless the user separately asks to save it | Decision-complete scope, required changes, checks, acceptance criteria, escalation conditions, and approval state. Executor and Verifier consume it for contract-routed work. |
| `executions/...-execution-log.md` | Executor | Executor may write it only within its authorized implementation/execution scope | The bounded change budget, commands, results, files touched, and stops encountered. Verifier consumes it with the task-attributable diff. |
| `reports/...-escalation.md` | Active Investigator, Planner, Executor, or Verifier returns complete content in its response | Primary controller may persist read-only-role content only during an authorized implementation workflow; Executor may write its own authorized record | Records the contradiction or decision needed. The Planner and human approver consume it before a safe resume. |
| `reports/...-verification.md` | Independent Verifier returns complete content in its response | Primary controller may persist it only during an authorized implementation workflow | Requirement-by-requirement results, evidence boundaries, unrun checks, findings, residual risks, and final verdict. |

Investigator, Planner, and Verifier are read-only roles: they author complete artifact content in their response and never persist workspace files themselves. Plan-only and investigate-only return their terminal artifact in conversation and modify no workspace file unless the user separately asks to save it. The baseline, route record, investigation report, approved Implementation Contract, and direct L0/L1 execution record are immutable inputs once handed to a later phase. An execution log may record new facts chronologically, but it does not rewrite earlier evidence. A Verifier reports findings instead of editing implementation or prior artifacts.

Templates describe the evidence a role must record; they are not deferred design work. The validator permits a runtime-form exception only in an actual `harness/templates/*.md` file and only when the complete line uses this convention:

```text
- [runtime-completion] Field name: <value> <!-- runtime-completion -->
```

The marker does not exempt an `AGENTS.md`, README, rule, TOML file, arbitrary template prose, or another non-form line from the unresolved-placeholder check.

## Contract revisions and approval

When the Planner must revise a contract, preserve the old artifact and create a new revision suffix before the extension, for example:

```text
harness/plans/2026-09-07-transfer-lifecycle-implementation-contract-r2.md
```

The revision identifies a new immutable contract. Human approval must name the exact revision and approved scope; approval of an earlier revision does not carry over automatically. Resume only after the required decision and approval are recorded against the current revision.

## Data handling

Generated artifacts can include sensitive local paths, diffs, issue details, logs, API references, or evidence about customer behavior. Store, share, retain, and redact them according to the target repository's data-handling, security, and retention policies. Do not assume that a harness artifact is safe to publish, attach to a ticket, or copy outside the repository.
