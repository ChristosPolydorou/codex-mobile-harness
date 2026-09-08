# Codex Mobile Harness v1

Codex Mobile Harness is a project-local operating policy for Android, iOS, and Kotlin Multiplatform work. It routes a request to a bounded investigation, planning, implementation, and independent verification path while leaving the mobile repository's own authority in charge.

## Prerequisites

- A current Codex client that supports project custom agents and multi-agent tools.
- Python 3.11+ when running the static harness validation. Python is not a runtime dependency of the mobile application.
- A clear understanding of repository-specific authority before installation: the user request, closest `AGENTS.md`, product/SDD/API/design/security contracts, and live code/tests take precedence over this generic harness.

Account access and available models can differ between Codex installations. Confirm the routed model is available before dispatching work.

## Source-package validation

Run this only from a clone of this harness repository. It validates the source
package, including its `tests/` directory; it is not a target-install command.

```bash
# Harness repository root
python3 -m unittest -v tests/test_harness_contract.py
```

## Install into a mobile repository

From the target mobile repository root, merge `AGENTS.md`, `.codex/`, and
`harness/`. This is a merge operation, not a replacement operation. Do not
replace the target root `README.md`, and do not copy this source repository's
`tests/` directory into the target:

1. Read the target repository's existing `AGENTS.md`, `.codex/config.toml`, and local instructions first.
2. Merge the harness policy with an existing `AGENTS.md`; preserve all existing repository-specific instructions and resolve any conflict in favor of the closer repository authority.
3. Merge the top-level `plan_mode_reasoning_effort = "high"` and the `[agents]` settings into an existing `.codex/config.toml`; preserve unrelated project settings rather than replacing the file.
4. Copy the remaining `.codex/agents/` role files and `harness/` resources without deleting existing project assets.
5. Do not copy this source repository's root `README.md` or `tests/` directory.

## Target-install validation

Run the following from the target mobile repository root after the merge. It
uses only installed policy/resources, parses the merged TOML, and validates
every harness link in the installed `AGENTS.md`; it does not assume that the
source-package test suite exists in the target.

```bash
# Target mobile repository root
python3 - <<'PY'
import re
import tomllib
from pathlib import Path

root = Path.cwd()
required = [
    "AGENTS.md",
    ".codex/config.toml",
    ".codex/agents/investigator.toml",
    ".codex/agents/planner.toml",
    ".codex/agents/executor.toml",
    ".codex/agents/verifier.toml",
    "harness/rules/routing.md",
    "harness/rules/scope-control.md",
    "harness/rules/verification.md",
    "harness/templates/implementation-contract.md",
    "harness/templates/investigation-report.md",
    "harness/templates/verification-report.md",
]
missing = [path for path in required if not (root / path).is_file()]
assert not missing, f"Missing installed harness files: {missing}"

with (root / ".codex/config.toml").open("rb") as source:
    config = tomllib.load(source)
assert config["plan_mode_reasoning_effort"] == "high"
assert config["agents"]["enabled"] is True
assert config["agents"]["default_subagent_reasoning_effort"] == "high"

agents = (root / "AGENTS.md").read_text(encoding="utf-8")
links = re.findall(r"\[[^]]+\]\((harness/[^)]+\.md)\)", agents)
missing_links = [link for link in links if not (root / link).is_file()]
assert links and not missing_links, f"Broken installed harness links: {missing_links}"
print("Installed Codex Mobile Harness policy, TOML, and links: PASS")
PY
```

The supported custom-role format is TOML: `.codex/agents/*.toml`, not `.codex/agents/*.md`. The role files describe the role; model selection belongs to the route record and explicit spawn. Every explicit spawn setting must state both a supported `model` and `reasoning effort: high`.

## Choose a prompt path

State the desired mode in the prompt. The router inspects authority, repository state, likely files, and platform risk before confirming a route.

| Path | Use when | Example prompt | Expected artifact/route |
| --- | --- | --- | --- |
| Direct L0/L1 | A mechanical or one-owner, understood change has no higher risk floor. | `Implement: Correct the typo in the Android empty-state string and run the focused checks.` | Bounded direct change budget, Executor, and proportional deterministic checks or independent Verifier. |
| Normal complex implementation | The work touches multiple files, behavior owners, or has uncertain cause. | `Implement: Trace and fix the Android lifecycle race that leaves the transfer confirmation stale after returning to the app.` | Investigator when needed, Planner, Implementation Contract, Executor, independent Verifier. |
| Plan only | You need a decision-complete implementation plan but no changes. | `Plan only: Add a saved-payment toggle to the KMP bill-payments flow, including platform and API implications.` | Planner returns the complete Implementation Contract in conversation and, when required, an approval request; stop with no workspace write. |
| Investigate only | You need evidence and root-cause confidence but no fix. | `Investigate only: Determine why the iOS transfer receipt sometimes displays the previous locale after an in-app language change.` | Investigator returns the complete read-only report in conversation; stop with no workspace write. |

`Plan only` and `Investigate only` are explicit terminal modes. Do not treat either as authorization to implement a follow-up change or to save an artifact. The Planner or Investigator authors complete artifact content in its response; the primary controller may persist that content only during an authorized implementation workflow. A terminal plan-only or investigate-only request modifies no workspace file unless the user separately asks to save the returned artifact.

Each terminal route record names Investigator, Planner, Executor, and Verifier
models, using `none` for inactive roles. Plan-only uses the Planner ladder
L0/L1 Luna High, L2 Terra High, L3 Sol High, and L4/L5 Astra High; it never
spawns an Executor or Verifier. Investigate-only uses that same ladder for the
Investigator and never spawns a Planner, Executor, or Verifier.

## Complexity, approval, and escalation

L0 and L1 normally use the direct path. L2 and L3 require a decision-complete Implementation Contract before implementation. L4 and L5, and every listed platform or high-risk gate, require **human approval** before the Executor starts.

Approval is revision-specific. The approver must identify the exact Implementation Contract filename and revision, the approved scope and architecture, and the evidence/timestamp. For example, approval of `harness/plans/2026-09-07-transfer-lifecycle-implementation-contract-r2.md` does not approve a later `-r3` revision or any newly discovered scope. A scope, risk-floor, or architecture change returns work to the Planner and requires a new approval decision when the revised contract requires it.

An active role stops and authors escalation-report content in its response when live evidence contradicts the contract, scope must expand, a risk floor rises, verification contradicts the claim, the environment blocks required evidence, or a product decision remains. The primary controller may persist a read-only role's returned content only during an authorized implementation workflow. The Planner alone revises a contract. After a decision or revised contract exists, resume from the existing execution context with that artifact rather than treating the old approval as blanket permission.

## End-to-end examples

For the Android lifecycle example above, the router records the mode and risk floors before work. Because lifecycle and state ownership may be involved, it routes at least L3: an Investigator returns evidence in its response if the cause is uncertain; the Planner returns a contract using the L3 planner route; the primary controller may persist those returned artifacts as part of the authorized implementation workflow; the Executor makes only the approved change and may write its authorized implementation/execution records within its workspace-write scope; and a separate Verifier returns its review in a response. If inspection shows a permissions, background-execution, persistence, DI-boundary, or other L4/L5 gate, the path stops for human approval before implementation.

For the iOS investigate-only example, the Investigator remains read-only, traces retained localization state and the SwiftUI/UI boundary, and returns the complete investigation report in conversation. It records unavailable simulator or device evidence as `NOT RUN` or `BLOCKED` as appropriate, then stops without modifying a workspace file. A later fix is a new implementation request and is routed again; the report is saved only if the user separately asks to save it.

## Operational artifacts

During an authorized implementation workflow, the primary controller may persist returned role artifacts beneath `harness/`; the Executor may write its authorized implementation/execution records under its workspace-write scope. See [the artifact lifecycle guide](harness/README.md) for exact names, authorship, persistence authority, revision handling, and data-handling requirements.

```text
harness/context/     baseline repository and authority evidence
harness/plans/       Implementation Contracts
harness/executions/  bounded implementation execution logs
harness/reports/     investigation, escalation, and verification reports
```

These artifacts make the route record, approval state, execution boundary, and evidence reviewable. Preserve the applicable baseline, investigation, approved contract, and route/execution record as immutable inputs to later phases.

## Configuration precedence and limitations

Configuration resolves in this order: user request; the closest applicable repository instructions; product, SDD, API, design, and security contracts; live implementation and tests; then this harness. The harness is not an architecture replacement and must not override project-specific policies.

Routing is instruction-driven, not a security boundary. Sandbox permissions, repository protections, CI, secrets management, code review, and human approval remain separate controls. Recheck this documentation whenever Codex configuration or custom-agent support changes, and revalidate the merged project configuration rather than assuming account or model behavior is identical across installations.
