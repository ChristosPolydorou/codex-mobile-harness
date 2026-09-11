---
name: cursor-hybrid-harness
description: Route local Cursor coding work through pinned Other-Model planning and Cursor-Model execution.
---

# Cursor Hybrid Harness

Use this skill for every local Cursor coding Agent chat. It controls role flow
and model pools only; it never replaces Team and Enterprise policy, the current user request, existing Cursor User Rules, project rules, AGENTS.md, or product,
security, and source authority. Read [routing](references/routing.md) before
dispatching any role. The role-model source of truth is
`cursor/model-policy.json`; future model changes require editing that file and
rerunning the user-scoped installer.

For Android, iOS, or Kotlin Multiplatform work only, also read
[mobile](references/mobile.md) and load `~/.agents/skills/mobile-template-engineering/v1`. Do not load mobile gates for unrelated work.

Classify the mode and L0-L5 complexity, then emit the visible route record and
use the exact marked dispatch recipe. `plan-only` and `investigate-only` are
terminal modes: Plan-only never spawns an Executor or Verifier. Investigate-only never spawns a Planner, Executor, or Verifier.
