# Cursor Hybrid Harness v1

This source package is the user-scoped Cursor companion to Codex Mobile
Harness v1. It routes every local Cursor coding Agent chat through the hybrid
workflow while preserving the implementation authority already supplied by
Team policy, the current user request, project rules and `AGENTS.md`, product
and security contracts, and the live repository.

## Model policy and cost control

`model-policy.json` is the single editable source of truth for all five role
models and the Cursor/Other pool prefixes. The current policy uses:

- Other Models: Terra for optional investigation and Claude Opus for L2-L5 planning;
- Cursor Models: Composer 2.5 for normal execution and Grok 4.6 for hard execution and verification.

The Verifier remains read-only, but it now uses Cursor Grok 4.6. To adopt a
new model or change the cost/speed balance, edit only `cursor/model-policy.json`
in this repository, rerun the installer, run the verifier, restart Cursor, and
open a fresh local Agent chat. The installer renders the `model:` frontmatter
from that policy and installs an auditable copy at
`~/.cursor/codex-mobile-harness/model-policy.json`.

## Source validation and installation

Validate this source package before installing it. The installer validates the
required source files, parses the existing user hook configuration, backs up an
owned file before changing it, copies only uniquely named harness files, and
records installed hashes in its owned manifest. It merges the three hook
entries additively and idempotently; it does not remove, reorder, or replace
unrelated hooks.

Install only for the current macOS user by targeting `~/.cursor`. The package
does not modify Cursor Team Rules, existing User Rules, `settings.json`, MCP
configuration, extensions, plans, databases, project `.cursor` files, or
project repositories. It applies to local Cursor coding Agent chats only;
Cursor Tab, Inline Edit, cloud agents, and remote agents are outside this
local-only boundary.

## Parent model and authority

Select Composer 2.5 in Cursor's main model picker once so the parent
controller conversation uses the Cursor Models pool. Cursor persists that
selection. This package cannot rewrite the model picker or administrator model
policy. If an administrator blocks a pinned model or Cursor substitutes a
fallback, report the mismatch and do not allow an Other Model to implement or
verify.

With only Cursor Grok 4.6 and Composer 2.5 enabled, L0-L1 execution and all
Cursor execution/verification are available. L2-L5, `plan-only`, and an
investigation route also need at least one enabled Other Model matching the
policy (currently Claude Opus 5 for planning; Terra is used when investigation
is needed). Auto may remain disabled.

## Cursor setup

1. Open Cursor Settings → Models. Keep Cursor Grok 4.6 and Composer 2.5
   enabled, and keep Auto disabled if you want deterministic routing.
2. Enable Claude Opus 5 under Other Models for the current Planner policy. Also
   enable GPT-5.6 Terra if you want the optional Investigator route, or change
   those entries in `cursor/model-policy.json` to Other Models you already
   allow.
3. In the main Agent model picker, select Composer 2.5 for the parent
   controller. The subagent frontmatter controls the role-specific models.
4. Restart Cursor or open a new local Agent chat. The `sessionStart` hook will
   inject the route contract and current policy path.
5. For an L2-L5 request, verify the visible route is Other Planner →
   Implementation Contract → Cursor Executor → Cursor Verifier. If Cursor
   falls back because a model is unavailable, the model guard stops the marked
   dispatch instead of silently crossing pools.

The router controls workflow roles and model-pool selection, never
implementation logic. Team and Enterprise policy remains first; then the
current user request, existing Cursor User Rules, closest project rules and
`AGENTS.md`, product and security contracts, live implementation and tests,
and this generic policy.
Stop and report an authority conflict that changes architecture, risk, or
scope.

## Runtime verification

Run source tests before installation, then use the verifier to compare the
installed hashes, validate the merged hooks, and exercise hook fixtures. A
fresh interactive local Cursor Agent chat, after restarting Cursor or opening
a new chat, is a separate runtime observation. Report it as `NOT RUN` until it
has actually been observed.

The package hooks are intentionally narrow:

- `sessionStart` supplies advisory routing and authority context. It is
  fail-open so a context-injection failure does not stop a conversation.
- `subagentStart` checks marked Investigator/Planner/Executor/Verifier
  dispatches against their required model pools.
- `beforeShellExecution` fail-closed blocks `git commit`, `git push`,
  `git reset --hard`, and `git clean` while allowing ordinary inspection and
  non-destructive commands.
