# Cursor Hybrid Harness v1 — Approved Design

## Status

Approved for implementation on 2026-09-11 in the continuation of `Codex
Harness Design`. The approved direction is hybrid: model-pool orchestration
applies to every local Cursor coding Agent chat, while the complete mobile
risk policy applies only to Android, iOS, and Kotlin Multiplatform work.

## Goal

Add a user-scoped Cursor companion to Codex Mobile Harness v1. Cursor Models
must perform all implementation. L2-L5 tasks must first be planned and
instructed by an Other Model. Existing Team, User, project, and `AGENTS.md`
instructions remain the authority for implementation logic.

## Scope

The installation applies to local Cursor Agent chats for the current macOS
user. It adds uniquely named user subagents, one automatically discoverable
skill, and additive hooks under `~/.cursor/`.

It does not edit:

- Cursor Team Rules or administrator model policy;
- existing Cursor User Rules stored in Customize;
- any project's `.cursor/rules`, `.cursor/agents`, hooks, or `AGENTS.md`;
- Cursor `settings.json`, `mcp.json`, extensions, plans, or internal databases;
- the existing Codex and VS Code Codex harness installation.

Cursor Tab and Inline Edit are outside the orchestration guarantee. Cloud and
remote agents do not receive local user files automatically; they require a
separate project, Team, or managed distribution decision.

## Authority

The router controls only workflow roles and model-pool selection. It must not
replace implementation rules. Apply authority in this order:

1. enforced Team and Enterprise policy;
2. the current user request;
3. the closest project rules and `AGENTS.md` instructions;
4. product, SDD, API, design, security, and release contracts;
5. live implementation and tests;
6. this generic orchestration policy.

If an authority conflict changes architecture, risk, or scope, stop and report
it rather than silently choosing a different implementation.

## Pipeline

```text
Local Cursor coding Agent chat
  -> session hook injects the routing contract
  -> controller inspects authority, repository, and Git state
  -> classifies mode and L0-L5 complexity
  -> optional read-only Other Model Investigator
  -> L2-L5 Other Model Planner
  -> decision-complete Implementation Contract
  -> Cursor Model Executor
  -> independent Cursor Model Verifier
  -> evidence-backed result or escalation
```

L0-L1 skip the Other Model Planner by default but still use a pinned Cursor
Model Executor. L2-L5 require the Planner. L4-L5 and every applicable mobile
high-risk gate require explicit human approval of the written contract before
the Executor starts.

## Cursor Model Policy

The exact v1 agents are deliberately few. Their model and pool selections are
defined in the editable `cursor/model-policy.json` source file; the installer
renders each agent's `model:` frontmatter from that file and installs a copy at
`~/.cursor/codex-mobile-harness/model-policy.json`.

| Role | Levels | Cursor subagent | Model |
| --- | --- | --- | --- |
| Investigator | when root cause or ownership is unknown | `cursor-harness-investigator` | `gpt-5.6-terra[effort=high]` |
| Planner | L2-L5 | `cursor-harness-planner` | `claude-opus-5[effort=high]` |
| Executor | L0-L3 default | `cursor-harness-executor` | `composer-2.5[fast=false]` |
| Hard executor | difficult L3, L4-L5 | `cursor-harness-hard-executor` | `grok-4.6[fast=false]` |
| Verifier | every behavior change | `cursor-harness-verifier` | `grok-4.6[fast=false]` |

`composer-2.5` and `grok-4.6` draw from Cursor Models. The Planner and
Investigator draw from Other Models. The Verifier is read-only but intentionally
draws from Cursor Models so verification stays within the enabled Cursor pool.
The hard executor is chosen for broad multi-file implementation, integration
difficulty, or a contract whose implementation requires stronger repository
reasoning; it is not chosen merely because planning was difficult.

With only Composer 2.5 and Grok 4.6 enabled, L0-L1 and Cursor-side execution
and verification work. L2-L5, `plan-only`, and any investigation route also
require at least one enabled Other Model matching the policy. Auto is not
required.

If a Team administrator blocks a pinned model or Cursor substitutes a fallback,
the workflow must report the model mismatch. It may select another installed
agent only when that agent satisfies the same pool boundary. It must not let an
Other Model implement.

For the parent/controller conversation itself to use the Cursor Models pool,
the user selects Composer 2.5 in the main Cursor model picker once; Cursor
persists that selection. The files in this package cannot safely rewrite the
account's model picker or administrator policy.

## Modes and Complexity

- `implement`: use the full applicable pipeline.
- `plan-only`: return the plan or Implementation Contract and stop. Do not
  invoke an Executor or Verifier.
- `investigate-only`: use the read-only Investigator and stop after the report.

The L0-L5 meanings and deterministic risk floors remain those in the canonical
Codex Mobile Harness. For non-mobile coding, use the same general signals:
mechanical scope, ownership, interfaces, architecture, concurrency, persistence,
security, release risk, rollback difficulty, and root-cause uncertainty.

For Android, iOS, Swift, Kotlin, Compose, Android Views, SwiftUI, UIKit, Gradle
mobile, Xcode, or KMP tasks, the Cursor skill must also load the installed
`~/.agents/skills/mobile-template-engineering/v1` policy and the applicable
Android/iOS gates. Those gates raise complexity and approval requirements but
never apply to unrelated web, backend, documentation, or scripting work.

## Dispatch Contract

Every routed subagent task starts with one exact marker:

- `[cursor-harness-role:investigator]`
- `[cursor-harness-role:planner]`
- `[cursor-harness-role:executor]`
- `[cursor-harness-role:verifier]`

The model guard denies a marked Executor or Verifier task when Cursor reports a
model outside the Cursor Models allowlist. It denies a marked Planner or
Investigator task when Cursor reports a Cursor Model. Unmarked built-in or
unrelated subagents remain untouched so the harness does not break Cursor's own
Explore, Bash, or Browser workers.

## Installation and Preservation

The installer must:

1. validate its source package before writing;
2. parse existing `~/.cursor/hooks.json` before modifying it;
3. back up every owned target that would change;
4. copy only uniquely named harness files;
5. merge hook entries idempotently without reordering or removing unrelated
   entries;
6. record installed hashes in an owned manifest;
7. leave rules, settings, MCP configuration, and project files unchanged.

The hook set contains:

- `sessionStart`: injects the concise routing and authority contract;
- `subagentStart`: validates marked Investigator, Planner, Executor, and
  Verifier model-pool boundaries;
- `beforeShellExecution`: blocks `git commit`, `git push`,
  `git reset --hard`, and `git clean` while allowing ordinary read-only Git
  inspection and non-destructive commands.

The Git guard is fail-closed. The session context hook is advisory and
fail-open: losing context must not prevent Cursor from opening a conversation.

## Verification

Source tests must cover:

- required files and valid frontmatter;
- exact pinned model and read-only/write role boundaries;
- L0-L5 routing and terminal modes;
- mobile-only activation of platform gates;
- model-guard allow/deny behavior;
- forbidden and allowed Git command behavior;
- additive, idempotent hook merging;
- backups, manifest hashes, and preservation of unrelated Cursor files.

Installed verification must compare hashes, validate merged hook entries, run
hook fixtures, and confirm existing rule/settings hashes are unchanged. A fresh
interactive Cursor Agent chat is a separate runtime check and must be reported
as `NOT RUN` until actually observed.

## Boundaries

Cursor instructions and subagent pins are not a cryptographic sandbox. Cursor
may override a pinned model because of Team policy, plan availability, or
runtime limitations. The model guard detects marked dispatch mismatches, but a
controller can still ignore an instruction or omit a marker. Repository
protections, CI, review, and human approval remain necessary.
