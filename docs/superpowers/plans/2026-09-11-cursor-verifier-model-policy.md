# Cursor Verifier and Model Policy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the Cursor verifier to Grok 4.6 and centralize all Cursor harness role-model selections in one editable policy file.

**Architecture:** `cursor/model-policy.json` becomes the source of truth for role models and pool prefixes. The installer validates that policy, renders each user-agent frontmatter model from it, installs an auditable copy under `~/.cursor/codex-mobile-harness/`, and makes the model guard read the same policy at runtime. The Cursor verifier remains read-only but uses the Cursor Models pool, while Investigator and Planner remain Other Models.

**Tech Stack:** Markdown custom subagents, JSON policy, Python standard library installer/hooks/verifier, `unittest`.

**Spec:** `docs/specs/cursor-hybrid-harness-v1.md`

## Global Constraints

- Cursor Models are the only Executor and Verifier pool: Composer 2.5 by default, Grok 4.6 for hard execution and verification.
- Other Models are reserved for Investigator and Planner; L2-L5 still require an Other-Model Planner and Implementation Contract.
- Existing Cursor Team/User/project rules, settings, MCP configuration, and repositories remain untouched.
- Mobile gates remain limited to Android, iOS, and Kotlin Multiplatform work.
- The installer remains additive, backup-first, idempotent, and user-scoped.
- No new dependencies; no `git commit`, `git push`, `git reset --hard`, or `git clean`.

---

### Task 1: Lock the configurable policy contract with tests

**Files:**
- Modify: `tests/test_cursor_harness.py`
- Create: `cursor/model-policy.json`

**Interfaces:**
- Consumes: the existing five Cursor role files and model-pool guard behavior.
- Produces: `model-policy.json` with `roles` and `pool_prefixes` consumed by the installer and hooks.

- [ ] **Step 1: Write failing tests** for the verifier's Cursor Grok pin, policy role/pool constraints, and a future-policy override that changes an installed agent from the single policy file.
- [ ] **Step 2: Run the focused Cursor suite** and confirm failure because the policy file and policy-driven rendering do not exist yet.
- [ ] **Step 3: Add the policy** with current defaults: Investigator `gpt-5.6-terra[effort=high]`, Planner `claude-opus-5[effort=high]`, Executor `composer-2.5[fast=false]`, Hard Executor `grok-4.6[fast=false]`, Verifier `grok-4.6[fast=false]`.
- [ ] **Step 4: Run the focused suite** and confirm the policy-only assertions pass while installer-dependent assertions remain red.

### Task 2: Make installation and model guarding policy-driven

**Files:**
- Modify: `cursor/install.py`
- Modify: `cursor/verify.py`
- Modify: `cursor/hooks/codex-mobile-harness-model-guard.py`
- Modify: `cursor/hooks/codex-mobile-harness-session.py`

**Interfaces:**
- Consumes: `cursor/model-policy.json` and existing role Markdown templates.
- Produces: rendered user agents, installed policy manifest entry, policy-aware hook decisions, and dynamic session context.

- [ ] **Step 1: Extend source validation** to parse policy version, role names, allowed pools, model strings, and pool prefixes.
- [ ] **Step 2: Render only each agent's `model:` frontmatter** from policy while preserving all prompt text and existing user files.
- [ ] **Step 3: Install the policy copy** at `~/.cursor/codex-mobile-harness/model-policy.json`, include it in hashes/backups, and make verification compare rendered bytes.
- [ ] **Step 4: Update model guard rules** so Investigator/Planner require Other prefixes and Executor/Verifier require Cursor prefixes; malformed or missing policy input denies marked dispatches.
- [ ] **Step 5: Update session context** to report the configured role models and future override location.
- [ ] **Step 6: Run the focused suite** to confirm GREEN.

### Task 3: Update routing documentation and setup guidance

**Files:**
- Modify: `cursor/README.md`
- Modify: `cursor/skills/cursor-hybrid-harness/references/routing.md`
- Modify: `cursor/skills/cursor-hybrid-harness/SKILL.md`
- Modify: `cursor/skills/cursor-hybrid-harness/references/mobile.md`
- Modify: `docs/specs/cursor-hybrid-harness-v1.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: the policy-driven runtime behavior from Tasks 1-2.
- Produces: one-file model change instructions, current Cursor setup steps, and accurate Cursor/Other pool boundaries.

- [ ] **Step 1: Replace static verifier-Other claims** with Cursor Grok verifier claims and identify `cursor/model-policy.json` as the only model-selection edit point.
- [ ] **Step 2: Document the user's current settings**: Composer/Grok alone support L0-L1 and Cursor execution/verification; at least one enabled Other Model is required for L2-L5 planning.
- [ ] **Step 3: Document the exact refresh procedure**: edit policy, run installer, verify, restart Cursor, open a fresh local Agent chat, and inspect the route/model.
- [ ] **Step 4: Run the complete source suite** and scan docs for stale verifier-pool claims.

### Task 4: Reinstall and verify the user-scoped Cursor package

**Files:**
- Target only: `/Users/christos_polydorou/.cursor/agents/`, `/Users/christos_polydorou/.cursor/hooks/`, `/Users/christos_polydorou/.cursor/skills/cursor-hybrid-harness/`, `/Users/christos_polydorou/.cursor/hooks.json`, `/Users/christos_polydorou/.cursor/codex-mobile-harness/`

**Interfaces:**
- Consumes: the policy-driven source package and existing user-scoped Cursor installation.
- Produces: updated installed agents, hooks, skill, policy copy, manifest, and verification evidence.

- [ ] **Step 1: Run the installer** with Python 3.11+ and inspect the backup/changed report.
- [ ] **Step 2: Run the installer a second time** and require `changed: false`.
- [ ] **Step 3: Run `cursor/verify.py`**, hook fixtures, focused tests, full tests, compile check, and diff check.
- [ ] **Step 4: Compare settings/MCP hashes and confirm existing rules remain outside the install target.**
- [ ] **Step 5: Report fresh interactive Cursor dispatch as NOT RUN** until the user restarts Cursor and opens a new local Agent chat.
