# Investigation Report

This is a read-only Investigator artifact. It distinguishes facts from
hypotheses and ends before application files are changed.

## Request and Mode

Record the original request, acceptance question, `investigate-only` route (or
the investigation phase of an implementation route), complexity, risk floors,
and applicable authority.

## Reproduction Status

Record `REPRODUCED`, `NOT REPRODUCED`, `NOT APPLICABLE`, or `BLOCKED`; include
the exact reproduction steps, environment/variant, observed output, and any
blocker.

## Facts

List only directly observed facts. Every fact cites an exact file/symbol,
command output, trace, test, log, or direct runtime observation.

## Execution Path

Trace the input/event through ownership, state, navigation, persistence,
network, and platform side effects relevant to the request. Mark branches not
observed as unknown rather than inferred.

## Hypotheses and Evidence

For each hypothesis, state its confidence and the evidence **for** and
**against** it. A hypothesis is not a recommendation or a substitute for a
confirmed root cause.

## Root Cause

State `CONFIRMED`, `MOST LIKELY`, or `UNKNOWN`; give the supporting evidence,
the failing boundary, and what observation would change the conclusion.

## Confidence

Record `HIGH`, `MEDIUM`, or `LOW`, explain why, and name the remaining evidence
needed to increase confidence.

## Unknowns

List unresolved ownership, contract, environment, runtime, device/simulator,
or cross-platform facts and their impact on a safe implementation.

## Relevant Files and Symbols

List exact repository-relative paths and symbols, their responsibility, and
whether they were inspected, executed, or only identified by reference.

## Platform Implications

State Android, iOS, KMP/shared, and variant implications separately. Identify
which are confirmed and which need platform-specific evidence.

## Application File Change Confirmation

Confirm that no application, build, dependency, generated, or configuration
file changed during investigation. If any write was required to reproduce,
stop and issue an escalation report instead of claiming a read-only
investigation.

## Recommended Next Artifact

Name exactly one of: `NONE — investigate-only request complete; stop after this report`; decision-complete Implementation Contract; escalation report; or human
decision request. The `NONE` terminal choice is required when the original mode
is `investigate-only` and no blocker/decision remains. For every non-terminal
choice, state the facts that make that next artifact safe.
