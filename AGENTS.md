# Codex Mobile Harness v1

## Authority and entry conditions

Apply authority in this order: **user request -> closest applicable repository
instructions -> product/SDD/API/design/security contracts -> live
implementation/tests -> this generic harness**. This harness does not replace
more-specific repository authority.

Before any edit or delegation, inspect applicable instructions, repository
structure, likely files, contracts, and Git state. Classify the explicit mode
(`implement`, `plan-only`, or `investigate-only`) and L0-L5 complexity, then
emit a visible route record with: `mode`, `complexity`, `risk floors`, `planner
model`, `investigator model`, `executor model`, `verifier model`, `approval
requirement`, and `next artifact`. Every record names all four role models;
write `none` for each inactive role.

Use the focused rules: [routing](harness/rules/routing.md),
[complexity](harness/rules/complexity.md), [scope control](harness/rules/scope-control.md),
[escalation](harness/rules/escalation.md), [Git policy](harness/rules/git-policy.md),
and [verification](harness/rules/verification.md). Apply platform gates for
[Android](harness/mobile/android.md) and [iOS/KMP](harness/mobile/ios.md). Use
the [Implementation Contract](harness/templates/implementation-contract.md),
[investigation report](harness/templates/investigation-report.md),
[escalation report](harness/templates/escalation-report.md), and
[verification report](harness/templates/verification-report.md) as the phase
artifacts.

## Roles, models, and approval

Dispatch only the named custom roles (`investigator`, `planner`, `executor`,
`verifier`) with the routed model and `high` effort. Where applicable, enforce:
Investigator -> Planner -> Implementation Contract -> Executor -> independent
Verifier. An Investigator is read-only; a Planner writes no implementation; an
Executor follows the approved contract without redesign or scope improvisation;
and an independent Verifier never verifies its own implementation. Do not make
unsupported completion claims.

Read-only Investigator, Planner, and Verifier author and return complete
artifact or escalation content in their response; they never write repository
files. The primary controller may persist returned content only during an
authorized implementation workflow and only within approved scope. Plan-only
and investigate-only remain conversation-output-only and modify no workspace
file unless the user separately asks to save the result. Executor may write
only authorized implementation/execution records within its workspace-write
scope. Escalation content may be authored by any active role, not only
Executor.

| Level | Investigator | Planner | Executor | Verifier |
| --- | --- | --- | --- | --- |
| L0 | `none`, or `gpt-5.6-luna` high when investigation is required | `none` | `gpt-5.6-luna` high | deterministic checks or `gpt-5.6-luna` high |
| L1 | `none`, or `gpt-5.6-luna` high when investigation is required | `none` by default | `gpt-5.6-luna` high | `gpt-5.6-luna` high |
| L2 | `none`, or `gpt-5.6-terra` high when investigation is required | `gpt-5.6-terra` high | `gpt-5.6-luna` high | `gpt-5.6-terra` high |
| L3 | `none`, or `gpt-5.6-sol` high when investigation is required | `gpt-5.6-sol` high | `gpt-5.6-luna` high or `gpt-5.6-terra` high | `gpt-5.6-terra` high |
| L4 | `none`, or `gpt-6-astra` high when investigation is required | `gpt-6-astra` high -> human approval | `gpt-5.6-terra` high | `gpt-5.6-sol` high |
| L5 | `none`, or `gpt-6-astra` high when investigation is required | `gpt-6-astra` high -> human approval | `gpt-5.6-terra` high | `gpt-5.6-sol` high, or `gpt-6-astra` high only for exceptional critical review |

Planner ceiling: `gpt-6-astra` high reasoning. Do not route planning to
`xhigh`, `max`, or `ultra`.

Executor allowlist: only `gpt-5.6-luna` high and `gpt-5.6-terra` high.
If Sol or Astra appears necessary to implement, return to planning because the
contract is insufficiently decomposed.

L2-L5 require a decision-complete Implementation Contract; L4/L5 and every
listed high-risk gate require explicit human approval before implementation.
Human approval covers only the written scope and architecture, never later
expansion. `plan-only` stops after the Implementation Contract and approval
request. `investigate-only` uses a read-only Investigator and stops after the
investigation report. Before executing an existing plan, verify that its
contract is current, complete, approved when necessary, and matches the live
repository.

For terminal modes, use the level ladder without changing the implementation
matrix: plan-only routes Planner `gpt-5.6-luna` high at L0/L1,
`gpt-5.6-terra` high at L2, `gpt-5.6-sol` high at L3, and `gpt-6-astra` high
at L4/L5; its Investigator, Executor, and Verifier fields are `none`.
Investigate-only routes Investigator on that same ladder; its Planner,
Executor, and Verifier fields are `none`. Plan-only never spawns an Executor
or Verifier. Investigate-only never spawns a Planner, Executor, or Verifier.

All behavior changes require an independent Verifier; L0 requires proportional
deterministic verification. AGENTS.md is orchestration policy, not a
cryptographic sandbox. Actual permissions, repository protections, CI, and
human review remain necessary.
