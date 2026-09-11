# Hybrid routing contract

## Authority and first inspection

Apply authority in this order: enforced Team and Enterprise policy; current
user request; closest project rules and `AGENTS.md`; product, SDD, API, design,
security, and release contracts; live implementation and tests; then this
generic orchestration policy. Existing Cursor User Rules remain in force. The
router controls workflow roles and model pools, never implementation logic.

Before any dispatch or edit, inspect applicable authority, repository
structure, likely files, contracts, and current Git state. Preserve unrelated
dirty work. If an authority conflict changes architecture, risk, or scope,
stop and report it; do not silently choose a new direction.

## Visible route record

For every request, first publish:

```text
CURSOR_HARNESS_ROUTE
mode: implement | plan-only | investigate-only
complexity: L0 | L1 | L2 | L3 | L4 | L5
risk_floors: <applicable floors or none>
investigator: <agent/model or none>
planner: <agent/model or none>
executor: <agent/model or none>
verifier: <agent/model or none>
approval: required | not-required
next_artifact: <report, Implementation Contract, implementation, or verification report>
```

Classify L0-L5 from mechanical scope, ownership, interfaces, architecture,
concurrency, persistence, security, release risk, rollback difficulty, and
root-cause uncertainty. Apply any mobile risk floor after loading the mobile
reference.

## Policy-driven model-pool matrix

The editable source of truth is `cursor/model-policy.json`. Change that file
and rerun the installer when selecting a different model or adopting a new
Cursor release; do not hand-edit the installed agent frontmatter. The current
defaults are:

| Role | Dispatch endpoint | Model | Use |
| --- | --- | --- | --- |
| Investigator | `cursor-harness-investigator` | `gpt-5.6-terra[effort=high]` | Read-only when ownership or root cause is unknown |
| Planner | `cursor-harness-planner` | `claude-opus-5[effort=high]` | Required for L2-L5 |
| Executor | `cursor-harness-executor` | `composer-2.5[fast=false]` | Default L0-L3 implementation |
| Hard executor | `cursor-harness-hard-executor` | `grok-4.6[fast=false]` | Broad multi-file, integration-difficult, or L4-L5 implementation |
| Verifier | `cursor-harness-verifier` | `grok-4.6[fast=false]` | Independent read-only review of every behavior change |

Investigator and Planner are Other Models and are read-only. Executor, Hard
executor, and Verifier are Cursor Models; the Verifier is still read-only even
though it uses the Cursor pool. L0-L1 skip the Planner by default, but always
use a pinned Cursor Model Executor. L2-L5 always use the Other Model Planner
before implementation. The hard executor is not selected merely because
planning was difficult.

## Positive dispatch recipe and exact markers

Every routed subagent prompt begins with exactly one role marker as its first
line. Do not use an unmarked replacement for a routed role.

```text
[cursor-harness-role:investigator]
[cursor-harness-role:planner]
[cursor-harness-role:executor]
[cursor-harness-role:verifier]
```

For `implement`:

1. Dispatch the marked, read-only Investigator only when root cause or
   ownership is unknown; retain its report.
2. At L2-L5, dispatch the marked Other Model Planner and require a
   decision-complete Implementation Contract. At L0-L1, record the direct,
   minimal change budget instead.
3. At L4-L5, and for every applicable high-risk gate, stop for explicit human
   approval of the written contract before any Executor dispatch.
4. Dispatch the exact marked Cursor Model Executor, choosing the Hard executor
   only for the allowed difficulty criteria. Give it the approved contract or
   direct L0/L1 budget, authority, dirty-work boundary, and verification scope.
5. For every behavior change, dispatch an independent marked Cursor Model
   Verifier with the contract, final task-attributable diff, and evidence.

No role may infer that a general recommendation permits a pool violation. If
Cursor reports a fallback model, Team policy blocks a pin, or a marked role is
in the wrong model pool, stop and report `CURSOR_HARNESS_MODEL_MISMATCH`. Select
another installed endpoint only if it satisfies the same role and pool boundary.
Never let an Other Model implement.

## Artifacts and terminal modes

Investigator returns an evidence-backed investigation report. Planner returns
a decision-complete Implementation Contract with scope, non-goals, ownership,
approach, ordered changes, verification, risks, and approval status. Executor
returns the task-attributable diff and proportional test evidence. Verifier
returns PASS, FAIL, BLOCKED, or NOT RUN evidence, including remaining limits.

`plan-only` dispatches the Planner on the level ladder, returns the plan or
Implementation Contract, and stops. Plan-only never spawns an Executor or
Verifier. `investigate-only` dispatches the read-only Investigator, returns its
report, and stops. Investigate-only never spawns a Planner, Executor, or
Verifier. Neither terminal mode edits the workspace unless the user separately
authorizes saving its output.

L2-L5 plans must be current and decision-complete. L4-L5 approval covers only
the written scope and architecture; a later expansion requires another stop and
approval. Never weaken validation, error handling, security, privacy,
accessibility, localization, analytics, or platform protections as a workaround.
