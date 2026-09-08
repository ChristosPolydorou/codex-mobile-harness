# Scope control

Before edits, the Executor must use either an approved Implementation Contract
for contract-routed work or an immutable direct L0/L1 route/execution record
plus an explicit direct-route change budget. The primary router/controller
prepares the direct-route record and budget before spawning the Executor. The
applicable authority must state this mandatory change budget:

```text
MUST: files, symbols, behaviors, tests, and acceptance criteria required by the contract.
MAY: trivial codebase-conformity adaptations that do not change architecture or public behavior.
OUT OF SCOPE: named files/subsystems plus unrelated cleanup, modernization, formatting, dependency updates, and speculative fixes.
```

Inspect and preserve pre-existing dirty hunks. The task-attributable diff may
contain only MUST work and necessary MAY adaptations. Any additionally required
file, public API change, dependency, behavior change, or cross-platform
divergence not already listed and approved in the applicable MUST budget is a
stop and escalation; it cannot be absorbed into MAY. The Executor may fix only
a mechanical compile or test error unambiguously caused by its in-scope edit and
still inside the approved authority. All other errors, overlapping dirty work,
failed assumptions, or requirements that exceed the budget require an
escalation report. Independent verification remains required at the level
selected by the route record.
