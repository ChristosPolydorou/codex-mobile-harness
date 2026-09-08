# Implementation Contract

This is the Planner's decision-complete handoff to the Executor. It consumes
the route record and, where applicable, investigation evidence. Complete every
field with repository-specific evidence before execution. A contract may not
leave a design choice to the Executor, offer alternatives such as "use X or
Y", hide an architecture choice, use broad wording such as "as appropriate",
or name an unspecified test. Only the Planner may revise this artifact.

## Objective

State the requested observable outcome and the acceptance boundary.

## Mode and Complexity

Record the route decision verbatim: mode (`implement`, `plan-only`, or
`investigate-only`), L0-L5 complexity, every risk floor and its triggering
fact, routed models/effort, approval requirement, and next artifact.

## Observed Behavior

Record confirmed current behavior, including the reproduction or trace that
establishes it. For planned work without a defect, state the confirmed current
absence of the requested behavior.

## Expected Behavior

Specify the observable success behavior, failure/recovery behavior, and every
affected platform or variant.

## Root Cause or Design Rationale

State the confirmed root cause; if no defect is being fixed, state the single
approved design rationale. Separate confirmed evidence from a bounded
assumption and link it to the relevant investigation evidence.

## Relevant Architecture and Ownership

Name the current owners of data, state, UI, navigation, persistence, network,
and platform behavior that the change crosses. Cite the applicable repository,
Template, SDD/API/design/security authorities and any deliberate platform
boundary.

## Constraints

List preserved contracts and protections: existing architecture, validation,
error handling, analytics, accessibility, localization, session behavior,
privacy/PII handling, generated boundaries, dependencies, and dirty-work
preservation. State every applicable platform gate and human-approval limit.

## Files In Scope

List each exact repository-relative path and its purpose in this contract.

## Files Explicitly Out of Scope

List adjacent files, modules, platforms, generated outputs, configuration, and
cleanup work that must not change. State why each remains outside this contract.

## Required Changes

Create one complete repeated block for every implementation step. Steps are
ordered and contain no design alternatives, placeholders, hidden choices,
broad "as appropriate" language, or unspecified verification.

### Step [number]: [single completed action]

- **File:** exact repository-relative path.
- **Symbols:** exact class, function, composable, view, reducer, route, or
  configuration key; write `new symbol: <name>` only when the approved design
  creates it.
- **Current behavior:** evidence-backed current behavior at this location.
- **Exact change:** exact code/data/control-flow change, including ownership
  and platform differences where relevant.
- **Reason:** direct link to the objective and root cause/design rationale.
- **Expected result:** observable result after this individual step.
- **Dependencies on other steps:** earlier step numbers, external approved
  contract, or `none`.

Repeat the block until the contract contains every required edit. Do not leave
example brackets in an approved contract.

## Tests to Add

For each new or changed test, name its exact file, test name, setup/input,
assertions, failure mode it prevents, and why the selected layer exercises the
risk. State `None` only with a concrete technical reason and the compensating
check in the next section.

## Tests and Checks to Run

List each exact command or directly observed manual check, its expected
behavior, and the risk it covers. Include required platform/build variants,
lint/static checks, focused regression tests, and runtime/device/simulator or
visual checks when their evidence is required. Mark unavailable required checks
as `BLOCKED` or unselected checks as `NOT RUN`; never imply they passed.

## Acceptance Criteria

List independently verifiable, requirement-by-requirement outcomes. Include
negative assertions for behavior that must remain unchanged.

## Non-Goals

List prohibited redesigns, migrations, refactors, dependency changes, and
platform expansions not authorized by this contract.

## Risks

Identify concrete behavior, lifecycle, data, security/privacy, accessibility,
localization, and cross-platform risks, plus the specific mitigation/evidence
for each.

## Assumptions

List only assumptions that remain after investigation, their evidence,
confidence, impact if false, and the exact escalation trigger. Do not convert
an undecided design choice into an assumption.

## Escalation Conditions

Map each expected stop condition to the `PLAN_DISCREPANCY`, `SCOPE_EXPANSION`,
`RISK_ESCALATION`, `VERIFICATION_CONTRADICTION`, `ENVIRONMENT_BLOCKER`, or
`USER_DECISION_REQUIRED` category. State the safe stopping point and whether
Planner revision or human approval is required before resuming.

## Approval Status

Use exactly one status:

- `NOT REQUIRED` — record why no L4/L5 or high-risk gate applies.
- `PENDING HUMAN APPROVAL` — record the exact scope/architecture/risk awaiting
  decision and stop before implementation.
- `APPROVED` — record the approver identity, approval timestamp or durable
  evidence link, and the exact scope/architecture approved.

Human approval covers only the written contract; it never authorizes later
expansion.

## Completion Checklist

- [ ] Contract is current against the live repository and its authority cited.
- [ ] Every required change has a complete repeated step block.
- [ ] Scope and non-goals exclude unrelated dirty work and unsupported changes.
- [ ] Tests and checks are exact, risk-faithful, and no evidence layer is
  overstated.
- [ ] Approval status has the required evidence before execution.
- [ ] Executor change budget is derivable as MUST, MAY, and OUT OF SCOPE.
- [ ] Independent Verifier inputs and acceptance criteria are complete.
