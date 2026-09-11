#!/usr/bin/env python3
"""Enforce Cursor/Other pool boundaries for marked routed subagents."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROLE_MARKERS = {
    "investigator": "[cursor-harness-role:investigator]",
    "planner": "[cursor-harness-role:planner]",
    "executor": "[cursor-harness-role:executor]",
    "verifier": "[cursor-harness-role:verifier]",
}
ROLE_POOL_REQUIREMENTS = {
    "investigator": "other",
    "planner": "other",
    "executor": "cursor",
    "verifier": "cursor",
}


def load_policy() -> dict[str, object]:
    cursor_root = Path(__file__).resolve().parents[1]
    candidates = (
        cursor_root / "model-policy.json",
        cursor_root / "codex-mobile-harness" / "model-policy.json",
    )
    for path in candidates:
        if path.is_file():
            policy = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(policy, dict) or policy.get("version") != 1:
                break
            if not isinstance(policy.get("roles"), dict) or not isinstance(
                policy.get("pool_prefixes"), dict
            ):
                break
            return policy
    raise ValueError("Cursor model policy is missing or invalid")


def is_model_in_pool(model: str, pool: str, policy: dict[str, object]) -> bool:
    normalized = model.strip().lower()
    base = normalized.split("[", 1)[0]
    prefixes = policy["pool_prefixes"][pool]
    return any(base.startswith(prefix.lower()) for prefix in prefixes)


def decision(payload: object) -> dict[str, str]:
    if not isinstance(payload, dict):
        return deny("CURSOR_HARNESS_MODEL_MISMATCH: malformed subagent input")
    task = payload.get("task")
    model = payload.get("subagent_model")
    if not isinstance(task, str) or not isinstance(model, str) or not model.strip():
        return deny("CURSOR_HARNESS_MODEL_MISMATCH: missing task or model")

    role = next((name for name, marker in ROLE_MARKERS.items() if marker in task), None)
    if role is None:
        return {"permission": "allow"}

    try:
        policy = load_policy()
        required_pool = ROLE_POOL_REQUIREMENTS[role]
        if policy["roles"][role]["pool"] != required_pool:
            raise ValueError("configured role pool violates the harness boundary")
        in_required_pool = is_model_in_pool(model, required_pool, policy)
    except (OSError, TypeError, ValueError, KeyError, json.JSONDecodeError):
        return deny("CURSOR_HARNESS_MODEL_MISMATCH: model policy unavailable")
    if required_pool not in ROLE_POOL_REQUIREMENTS.values() or not in_required_pool:
        expected = "Cursor Models" if required_pool == "cursor" else "Other Models"
        return deny(
            f"CURSOR_HARNESS_MODEL_MISMATCH: {role} must use {expected}"
        )
    return {"permission": "allow"}


def deny(message: str) -> dict[str, str]:
    return {"permission": "deny", "user_message": message}


def main() -> None:
    try:
        payload = json.load(sys.stdin)
        output = decision(payload)
    except (json.JSONDecodeError, OSError):
        output = deny("CURSOR_HARNESS_MODEL_MISMATCH: invalid hook input")
    print(json.dumps(output))


if __name__ == "__main__":
    main()
