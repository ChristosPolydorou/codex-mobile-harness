# Escalation Report

Any active role uses this artifact to provide the Planner or human with a
recoverable, evidence-backed decision point before unapproved expansion.

## Authorship and persistence

Read-only Investigator, Planner, and Verifier author and return complete
artifact or escalation content in their response; they never write repository
files. The primary controller may persist returned content only during an
authorized implementation workflow and only within approved scope. Plan-only
and investigate-only remain conversation-output-only and modify no workspace
file unless the user separately asks to save the result. Executor may write
only authorized implementation/execution records within its workspace-write
scope. Escalation content may be authored by any active role, not only
Executor.

## Category

Use one or more exact categories: `PLAN_DISCREPANCY`, `SCOPE_EXPANSION`,
`RISK_ESCALATION`, `VERIFICATION_CONTRADICTION`, `ENVIRONMENT_BLOCKER`, or
`USER_DECISION_REQUIRED`.

## Current Route and Approval State

Record mode, L0-L5 level, triggered risk floors, routed roles, contract
version, and current approval status.

## Halt Point

State the last completed safe step, the exact operation not started, and why
continuing would exceed the approved contract or evidence.

## Observed Fact and Evidence

Provide the concrete observed fact with exact file/symbol, command result,
trace, reproduction, or direct observation. Do not substitute a suspicion for
evidence.

## Conflicting Assumption

Quote the specific Implementation Contract assumption, required-change step,
or route decision that conflicts with the observed fact.

## Required Scope or Risk Change

State the smallest newly required file, module, API, dependency, platform,
security/privacy, lifecycle/concurrency, persistence, or architecture change;
include the new minimum complexity and approval implication.

## Files Already Changed

List exact paths and task-attributable hunks completed before the halt, or
state `None`. Identify any pre-existing user work encountered and preserved.

## Checks Already Run

List each exact command/manual check, `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN`,
and its literal result. Never treat an unrun or blocked check as passing.

## Safe State and Rollback Note

Describe the current safe repository state, whether the partial change is
coherent, and the narrow recoverable rollback guidance. Never reset, clean, or
overwrite unrelated user work.

## Planner or Human Decision Requested

Ask for one concrete decision: Planner contract revision, human approval of
specified L4/L5 scope, or product/architecture selection. Explain why the
Executor cannot choose it.

## Resume Conditions

List the required revised contract, approval evidence, environment access, or
test outcome. State the exact safe step from which the existing Executor may
resume after reclassification where required.
