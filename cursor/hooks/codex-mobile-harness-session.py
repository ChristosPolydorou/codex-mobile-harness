#!/usr/bin/env python3
"""Inject the concise Cursor Hybrid Harness contract at session start."""

from __future__ import annotations

import json
from pathlib import Path
import sys


BASE_ROUTING_CONTEXT = """Use the cursor-hybrid-harness skill for every local Cursor coding Agent chat.
The router controls role flow and model pools only; existing Team and Enterprise policy,
the current user request, existing Cursor User Rules, the closest project rules and
AGENTS.md, product/security/source contracts, and live code/tests remain authoritative.
Emit CURSOR_HARNESS_ROUTE before dispatch. L0-L1 use a marked Cursor-Model Executor.
L2-L5 require a marked Other-Model Planner and decision-complete Implementation Contract,
then a marked Cursor-Model Executor and independent marked Cursor-Model Verifier. Cursor Models
are the implementation and verification pool; Other Models plan and investigate.
Plan-only and investigate-only stop at their terminal artifact. For Android, iOS, or KMP,
load the canonical ~/.agents/skills/mobile-template-engineering/v1 risk and approval
policy; adapt only its Codex-specific model names to the Cursor Hybrid model matrix.
Never let an Other Model implement. Stop on model, authority, scope, safety, approval,
or verification mismatch; do not improvise."""


def load_policy_context() -> str:
    cursor_root = Path(__file__).resolve().parents[1]
    candidates = (
        cursor_root / "model-policy.json",
        cursor_root / "codex-mobile-harness" / "model-policy.json",
    )
    try:
        for path in candidates:
            if path.is_file():
                policy = json.loads(path.read_text(encoding="utf-8"))
                roles = policy["roles"]
                role_summary = ", ".join(
                    f"{role}={roles[role]['model']} ({roles[role]['pool']})"
                    for role in (
                        "investigator",
                        "planner",
                        "executor",
                        "hard_executor",
                        "verifier",
                    )
                )
                return (
                    f"\nCurrent role models come from {path}: {role_summary}. "
                    "Edit the source cursor/model-policy.json and rerun the installer to change them."
                )
    except (OSError, TypeError, KeyError, ValueError, json.JSONDecodeError):
        pass
    return "\nCURSOR_HARNESS_MODEL_POLICY_UNAVAILABLE: stop marked dispatches and repair the installation."


def main() -> None:
    # Cursor supplies JSON on stdin. Context injection is advisory and fail-open;
    # malformed lifecycle input must not prevent a session from opening.
    try:
        json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        pass
    print(json.dumps({"additional_context": BASE_ROUTING_CONTEXT + load_policy_context()}))


if __name__ == "__main__":
    main()
