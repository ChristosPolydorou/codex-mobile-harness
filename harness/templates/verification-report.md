# Verification Report

The independent Verifier completes this report from the original request,
route decision, baseline Git status/diff, task-attributable diff, and exact
command/manual-check results. It also receives the approved Implementation
Contract when the route requires one; otherwise, for a direct L0/L1 route, it
receives the immutable route/execution record plus explicit direct-route change
budget. The Verifier does not verify its own implementation and must preserve
`NOT RUN` and `BLOCKED` evidence exactly.

## Verification Inputs

Record the immutable request, route record, baseline Git status/diff, final
attributable diff, repository authorities/conventions, and exact evidence
supplied. For L2-L5 or another contract-routed change, record the approved
Implementation Contract/version and approval evidence. For L0/L1, record the
immutable route/execution record and direct-route change budget instead.

The minimum direct-route change budget records: original observable request and
acceptance criteria; L0/L1 route/risk-floor/approval outcome; in-scope
files/symbols; current and expected behavior; exact change; MUST, MAY, and OUT
OF SCOPE boundaries; preservation constraints; exact tests and checks; and
escalation conditions.

## Requirement-by-Requirement Results

For every acceptance criterion, record `PASS`, `FAIL`, `BLOCKED`, or `NOT
RUN`; cite the specific evidence and state whether the behavior itself was
exercised or only statically inspected.

## Scope Result

State whether the task-attributable diff matches the approved contract's MUST
budget when a contract was required, or the direct-route change budget for
L0/L1. State whether MAY adaptations remained mechanical/conforming and which
pre-existing dirty work was preserved. List unauthorized scope as a finding.

## Findings

List findings in this exact order, omitting empty groups only after writing
`None found`:

### BLOCKER

None found.

Findings that make requested behavior unsafe, incorrect, or unapprovable.

### MAJOR

None found.

Findings with material regression, contract, security/privacy, data, or
cross-platform risk.

### MINOR

None found.

Findings with bounded correctness, maintainability, or quality impact.

### INFORMATIONAL

None found.

Non-blocking evidence limitations, observations, or follow-up context.

Each finding identifies severity, exact file/symbol or evidence, impact,
reproduction/analysis, and required resolution or accepted residual risk.

## Evidence Table

| Check or observation | Layer/platform/variant | Exact command or method | Result (`PASS`/`FAIL`/`BLOCKED`/`NOT RUN`) | What it directly proves | What it does not prove |
| --- | --- | --- | --- | --- |
| Record one row per check | Record actual target | Record exact command or observation | Record actual result | State direct evidence | State evidence boundary |

## Quality and Platform Review

Record findings or an evidence-backed no-finding result for requested behavior,
repository conventions, nullability, lifecycle, concurrency, navigation/state,
security/privacy, validation/error handling, analytics, accessibility,
localization, cross-platform effects, and meaningful test selection. Include
Android, iOS, and KMP/shared implications separately when applicable.

## Unrun Checks

List every required `NOT RUN` or `BLOCKED` check, why it was not completed,
what it would have proved, and the remaining risk. State `None` only when no
such check exists.

## Residual Risks

List unresolved risks and their owner/acceptance path. Do not describe a
compile, static inspection, build artifact, or another platform's evidence as
runtime, visual, installation, launch, or parity proof.

## Verdict

Choose exactly one verdict:

- `PASS` — acceptance criteria have sufficient faithful evidence and no
  unresolved blocker or major concern remains.
- `PASS WITH CONCERNS` — bounded concerns and explicit residual risks remain.
  At L5, this verdict requires explicit human acceptance before completion;
  record the acceptance evidence here.
- `FAIL` — a blocker, major unresolved contradiction, unauthorized scope, or
  insufficient required evidence prevents completion.

State the rationale, required next action, and whether human acceptance is
still required.
