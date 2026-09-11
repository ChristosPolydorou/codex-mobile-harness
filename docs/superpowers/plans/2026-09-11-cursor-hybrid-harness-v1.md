# Cursor Hybrid Harness v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Version, install, and verify a user-scoped Cursor orchestration layer that reserves implementation for Cursor Models, uses Other Models to plan L2-L5 work, preserves existing Cursor rules, and activates the full mobile harness only for Android/iOS/KMP tasks.

**Architecture:** A concise `sessionStart` hook injects the router into local Cursor Agent chats. Five pinned user subagents implement the role/model boundaries, an automatically discoverable skill holds detailed routing policy, and deterministic hooks guard marked subagent dispatches and forbidden Git commands. A standard-library Python installer performs a backup-first additive merge into `~/.cursor`, and a verifier checks the installed hashes and behavior.

**Tech Stack:** Cursor Markdown subagents and skills, Cursor hooks JSON, Python 3 standard library, `unittest`.

**Spec:** `docs/specs/cursor-hybrid-harness-v1.md`

## Global Constraints

- Apply orchestration to every local Cursor coding Agent chat; apply mobile gates only to Android, iOS, and KMP work.
- Cursor Models are the only Executors: `composer-2.5[fast=false]` by default and `grok-4.6[fast=false]` for hard execution.
- L2-L5 use `claude-opus-5[effort=high]` as the Other Model Planner before implementation.
- The read-only Verifier uses `grok-4.6[fast=false]`; all role selections are sourced from `cursor/model-policy.json`.
- Existing Team, User, project, `AGENTS.md`, product, security, and source authority remains in force; the harness controls role flow, not implementation logic.
- Do not modify Cursor settings, MCP configuration, internal databases, existing User Rules, project rules, or project repositories.
- Merge `~/.cursor/hooks.json` additively and idempotently; back up every owned target before replacing changed content.
- Keep `git commit`, `git push`, `git reset --hard`, and `git clean` blocked by the Cursor hook.
- Do not commit or push during this execution; leave a verified working-tree diff for the user.

---

### Task 1: Define executable Cursor package contracts

**Files:**
- Create: `tests/test_cursor_harness.py`
- Create: `cursor/README.md`
- Create: `cursor/hooks.fragment.json`

**Interfaces:**
- Produces fixture loaders and assertions used to validate all later Cursor package files.
- Consumes the approved model matrix and preservation boundaries from the spec.

- [ ] **Step 1: Write failing structural and model-policy tests**

  Add `unittest` cases requiring the five agent files, the orchestration skill,
  three hook scripts, installer, verifier, and hook fragment. Assert exact
  model pins, role markers, read-only flags, mobile-policy reference, terminal
  modes, and unique hook commands.

- [ ] **Step 2: Run the focused tests and verify RED**

  Run `/opt/homebrew/bin/python3 -m unittest -v tests/test_cursor_harness.py`.
  Expected: failures naming the missing `cursor/` artifacts.

- [ ] **Step 3: Add the package overview and canonical hook fragment**

  Document source validation, user installation, Composer parent-model setup,
  authority preservation, local-only boundary, and runtime verification. Define
  one entry each for `sessionStart`, `subagentStart`, and
  `beforeShellExecution` in the JSON fragment.

- [ ] **Step 4: Re-run the focused tests**

  Expected: structure still fails only for not-yet-created agent, skill, script,
  installer, and verifier files; the fragment-specific assertions pass.

- [ ] **Step 5: Record the diff without staging or committing**

  Run `git diff --check` and record the task evidence in the SDD ledger.

### Task 2: Add pinned Cursor subagents and the hybrid routing skill

**Files:**
- Create: `cursor/agents/cursor-harness-investigator.md`
- Create: `cursor/agents/cursor-harness-planner.md`
- Create: `cursor/agents/cursor-harness-executor.md`
- Create: `cursor/agents/cursor-harness-hard-executor.md`
- Create: `cursor/agents/cursor-harness-verifier.md`
- Create: `cursor/skills/cursor-hybrid-harness/SKILL.md`
- Create: `cursor/skills/cursor-hybrid-harness/references/routing.md`
- Create: `cursor/skills/cursor-hybrid-harness/references/mobile.md`
- Test: `tests/test_cursor_harness.py`

**Interfaces:**
- Consumes the exact subagent names, model pins, and task markers from Task 1.
- Produces the role endpoints and detailed policy loaded by the session hook.

- [ ] **Step 1: Run a baseline pressure scenario without the skill**

  Give a fresh subagent three prompts: an L1 edit, an L3 multi-module change,
  and an L5 payment/security change. Record whether it consistently delegates
  implementation to Cursor Models, plans L2-L5 with Other Models, preserves
  local rules, and stops for L5 approval. This is the required RED evidence for
  the new process skill.

- [ ] **Step 2: Create the minimal role files**

  Load the role models from `cursor/model-policy.json`. Investigator, Planner,
  and Verifier are read-only. Executor descriptions require the exact executor dispatch marker,
  an approved contract or direct L0/L1 budget, preservation of dirty work, no
  redesign, proportional tests, and escalation on material discrepancies.

- [ ] **Step 3: Create the skill and focused references**

  Keep `SKILL.md` concise and discovery-oriented. Put the model matrix,
  complexity routing, mode behavior, authority, artifact handoffs, and stop
  conditions in `references/routing.md`; put only Android/iOS/KMP activation
  and the installed canonical mobile-policy path in `references/mobile.md`.

- [ ] **Step 4: Re-run the same pressure scenario with the skill**

  Require a visible route, Other Model planning for L2-L5, a marked Cursor
  Executor handoff, preserved project authority, and an L5 approval stop.
  Capture any new rationalization and tighten only the wording that allowed it.

- [ ] **Step 5: Run the focused contract tests**

  Run `/opt/homebrew/bin/python3 -m unittest -v tests/test_cursor_harness.py`.
  Expected: agent and skill tests pass; hook-script and installer tests remain
  RED until Task 3.

- [ ] **Step 6: Record the diff without staging or committing**

  Run `git diff --check` and record evidence in the ledger.

### Task 3: Implement deterministic hooks and backup-first installer

**Files:**
- Create: `cursor/hooks/codex-mobile-harness-session.py`
- Create: `cursor/hooks/codex-mobile-harness-model-guard.py`
- Create: `cursor/hooks/codex-mobile-harness-git-guard.py`
- Create: `cursor/install.py`
- Create: `cursor/verify.py`
- Modify: `tests/test_cursor_harness.py`

**Interfaces:**
- Consumes `cursor/hooks.fragment.json`, the exact agent/skill source tree, and
  task markers from Task 2.
- Produces `install(cursor_home, source_root) -> dict` and
  `verify(cursor_home, source_root) -> list[str]` for tests and CLI entrypoints.

- [ ] **Step 1: Add failing behavioral tests**

  Test allowed/denied Planner and Executor model combinations, forbidden Git
  commands including shell prefixes and option placement, allowed read-only Git
  commands, malformed hook input, idempotent hook merging, changed-file backup,
  unrelated-hook preservation, unrelated-file hash preservation, and installed
  manifest verification.

- [ ] **Step 2: Run the focused tests and verify RED**

  Run `/opt/homebrew/bin/python3 -m unittest -v tests/test_cursor_harness.py`.
  Expected: behavioral failures caused by missing functions and scripts.

- [ ] **Step 3: Implement the three hook programs**

  Use only the Python standard library. The session hook reads stdin and emits
  `additional_context`; the model guard reads `task` and `subagent_model` and
  emits `allow` or `deny`; the Git guard reads `command` and emits `allow` or
  `deny`. Invalid input to the security guards must return a denial.

- [ ] **Step 4: Implement additive installation**

  Validate the source, parse the existing hooks document, create a timestamped
  backup for every changed owned target, copy owned files atomically, merge each
  hook once, and write a manifest containing source and installed SHA-256
  hashes. Never enumerate or rewrite project repositories or Cursor databases.

- [ ] **Step 5: Implement installed verification**

  Confirm required hashes, hook entries, frontmatter model pins, executable
  hook behavior, and the manifest. Return explicit error strings and a nonzero
  CLI exit for every mismatch.

- [ ] **Step 6: Run focused tests to GREEN**

  Run `/opt/homebrew/bin/python3 -m unittest -v tests/test_cursor_harness.py`.
  Expected: all Cursor package tests pass.

- [ ] **Step 7: Run the complete source suite**

  Run `/opt/homebrew/bin/python3 -m unittest discover -s tests -v` and
  `git diff --check`. Expected: both the original 24 contracts and all Cursor
  contracts pass with no whitespace errors.

- [ ] **Step 8: Record the diff without staging or committing**

  Record test counts and the task-attributable diff in the ledger.

### Task 4: Install and verify the user-scoped Cursor harness

**Files:**
- Create or update owned files under `~/.cursor/agents/`,
  `~/.cursor/skills/cursor-hybrid-harness/`, `~/.cursor/hooks/`, and
  `~/.cursor/codex-mobile-harness/`
- Additively modify: `~/.cursor/hooks.json`
- Preserve: Cursor settings, MCP configuration, existing rules, project rules,
  existing agents/skills/hooks, plans, databases, and extensions

**Interfaces:**
- Consumes the verified package and installer from Task 3.
- Produces an installed manifest and verification report for the current user.

- [ ] **Step 1: Capture the pre-installation baseline**

  Record the file inventory and SHA-256 hashes of existing `hooks.json`, owned
  target collisions, Cursor settings, user-skill entrypoints, and representative
  existing project rule trees. Do not read or print secrets from MCP or internal
  databases.

- [ ] **Step 2: Run the installer against a temporary Cursor home**

  Install twice into a temporary fixture containing unrelated hooks, rules,
  settings, and agents. Verify idempotence, backups, and byte-for-byte
  preservation of unrelated content.

- [ ] **Step 3: Install into the real user Cursor home**

  Run `/opt/homebrew/bin/python3 cursor/install.py --cursor-home
  /Users/christos_polydorou/.cursor`. This is the only authorized external write
  scope. Do not change project repositories.

- [ ] **Step 4: Verify the real installation**

  Run `/opt/homebrew/bin/python3 cursor/verify.py --cursor-home
  /Users/christos_polydorou/.cursor`, execute all three hooks with deterministic
  fixtures, and compare the preserved baseline hashes.

- [ ] **Step 5: Record the runtime boundary**

  Report source tests and installed checks as `PASS`, mismatches as `FAIL`,
  environment limits as `BLOCKED`, and a fresh interactive Cursor Agent routing
  observation as `NOT RUN` unless it was actually performed. Document the
  one-time Composer 2.5 parent-model selection and Cursor restart/new-chat step.

- [ ] **Step 6: Leave the source branch uncommitted**

  Present the verified working-tree diff and exact optional `git add`,
  `git commit`, and `git push` commands for the user; do not run them.
