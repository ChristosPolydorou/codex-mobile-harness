# Codex Mobile Harness v1 — Approved Design

## Status

Approved for implementation on 2026-09-07 in the referenced conversation `Codex Harness Design` (`6a9e806d-7620-83eb-84bd-90548ba1a9d5`).

This document freezes the approved v1 behavior so the implementation plan and the eventual harness do not depend on chat history.

## Goal

Create a project-local Codex harness for Android, iOS, and Kotlin Multiplatform work that spends high-end reasoning on investigation and planning, constrains implementation to cheaper models, and requires independent verification before completion.

## Pipeline

```text
User prompt
  -> deterministic mode and risk routing
  -> optional Investigator
  -> optional Planner
  -> Implementation Contract
  -> Executor
  -> independent Verifier
  -> PASS or explicit escalation
```

L0 and L1 work may go directly to a constrained Executor. L2 through L5 work requires a Planner. Difficult or uncertain bugs may use an Investigator before planning. The Verifier must be independent of the Executor.

## Hard Laws

1. The Planner investigates, decides, decomposes, and writes an Implementation Contract; it does not implement.
2. The Executor follows an approved contract; it does not redesign or silently widen scope.
3. An unexpected repository fact, required extra scope, or failed assumption causes a stop and escalation, not improvisation.
4. Architectural, migration, authentication, security, persistence, signing, entitlement, and other high-risk work requires human approval before implementation.
5. Completion requires an independent Verifier verdict and proportionate evidence.
6. Plan-only mode stops after the plan or Implementation Contract.
7. Investigate-only mode remains read-only and stops after evidence, root cause, confidence, and unknowns are reported.

## Model Policy

All routed roles use `high` reasoning.

| Complexity | Planner | Executor | Verifier |
|---|---|---|---|
| L0 Mechanical | none | `gpt-5.6-luna` | deterministic checks or `gpt-5.6-luna` |
| L1 Localized | none by default | `gpt-5.6-luna` | `gpt-5.6-luna` |
| L2 Moderate | `gpt-5.6-terra` | `gpt-5.6-luna` | `gpt-5.6-terra` |
| L3 Complex | `gpt-5.6-sol` | `gpt-5.6-luna` or `gpt-5.6-terra` | `gpt-5.6-terra` |
| L4 Architectural | `gpt-6-astra` | `gpt-5.6-terra` | `gpt-5.6-sol` |
| L5 Critical | `gpt-6-astra` | `gpt-5.6-terra` | `gpt-6-astra` only when critical review justifies it; otherwise `gpt-5.6-sol` |

Hard boundaries:

- Planner ceiling: `gpt-6-astra` with `high` reasoning. Do not route planning to `xhigh`, `max`, or `ultra`.
- Executor floor: `gpt-5.6-luna` with `high` reasoning.
- Executor allowlist: only `gpt-5.6-luna` and `gpt-5.6-terra`, both at `high`.
- Executor selection is based on implementation difficulty after planning, not on planning difficulty.
- If Sol or Astra appears necessary to implement, the contract is insufficiently decomposed and must return to planning.

## Routing Inputs

The router assesses:

- explicit user mode (`implement`, `plan-only`, or `investigate-only`);
- ambiguity and missing product decisions;
- number of modules, files, and public interfaces likely affected;
- architectural and state-ownership impact;
- concurrency, lifecycle, navigation, and background-work impact;
- API, persistence, migration, authentication, authorization, cryptography, privacy, and PII impact;
- build system, dependency, entitlement, signing, and deployment impact;
- reproduction or root-cause uncertainty;
- rollback difficulty and blast radius;
- Android, iOS, and KMP platform parity requirements.

Deterministic risk floors override a lower heuristic score. Precise user instructions can reduce ambiguity, but cannot lower a security, migration, data-loss, or architecture risk floor.

## Human Approval Gate

Implementation must pause for explicit human approval when any of the following is true:

- route is L4 or L5;
- a new subsystem or architectural pattern is proposed;
- an architecture replacement, framework migration, or UI-stack migration is proposed;
- authentication, authorization, cryptography, Keychain/Keystore, payment, transfer, OTP, session, or PII behavior changes;
- database schema, persistence format, destructive migration, or data retention changes;
- Android permissions, services, receivers, deep links, background execution, signing, R8/ProGuard, or dependency injection boundaries change;
- iOS entitlements, signing, capabilities, Keychain, background modes, deep links, actor isolation, or persistence migration changes;
- public API or cross-module contract changes beyond the user's explicit request;
- a new dependency is required.

Approval applies to the written architecture and scope, not as blanket permission for later scope expansion.

## Implementation Contract

The Planner must produce a contract with these sections:

1. Objective
2. Mode and complexity
3. Observed behavior
4. Expected behavior
5. Root cause or design rationale
6. Relevant architecture and ownership
7. Constraints
8. Files in scope
9. Files explicitly out of scope
10. Required changes, per file and symbol
11. Tests to add
12. Tests and checks to run
13. Acceptance criteria
14. Non-goals
15. Risks
16. Assumptions
17. Escalation conditions
18. Approval status
19. Completion checklist

The contract is incomplete if an Executor still needs to choose between architectural alternatives.

## Verifier Contract

The Verifier receives the original request, route decision, approved Implementation Contract, pre-existing repository state, task-attributable diff, and exact check results. It remains read-only and returns one of:

- `PASS`
- `PASS WITH CONCERNS`
- `FAIL`

`PASS WITH CONCERNS` is not sufficient for security-, migration-, authentication-, payment-, signing-, or data-sensitive L5 completion unless the human explicitly accepts the concerns.

The Verifier checks requirement coverage, scope adherence, implementation correctness, platform lifecycle/concurrency/state risks, security/privacy regressions, accessibility/localization preservation, test relevance, and whether evidence supports the completion claim.

## Codex Configuration Constraint

Current Codex custom agents are project-local TOML files under `.codex/agents/`. Although the original request referred to `.codex/agents/*.md`, v1 must use `.toml` because that is the supported runtime format. Markdown remains appropriate for routing rules, platform policy, templates, plans, and reports.

## Non-Goals

- No separate Python or server orchestrator in v1.
- No automatic merging, committing, pushing, or deployment.
- No dependency additions.
- No replacement of repository-specific `AGENTS.md`, SDD, API, security, or design authority.
- No claim that prompt instructions are an OS-level security boundary.
- No silent implementation of architecture or high-risk decisions.
