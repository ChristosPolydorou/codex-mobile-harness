#!/usr/bin/env python3
"""Backup-first, additive installer for the user-scoped Cursor harness."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
CURSOR_SOURCE = ROOT / "cursor"
AGENT_NAMES = (
    "cursor-harness-investigator.md",
    "cursor-harness-planner.md",
    "cursor-harness-executor.md",
    "cursor-harness-hard-executor.md",
    "cursor-harness-verifier.md",
)
HOOK_NAMES = (
    "codex-mobile-harness-session.py",
    "codex-mobile-harness-model-guard.py",
    "codex-mobile-harness-git-guard.py",
)
SKILL_ROOT = Path("skills/cursor-hybrid-harness")
POLICY_RELATIVE = Path("model-policy.json")
POLICY_INSTALL_RELATIVE = Path("codex-mobile-harness/model-policy.json")
MANIFEST_RELATIVE = Path("codex-mobile-harness/manifest.json")
ROLE_FILES = {
    "investigator": "cursor-harness-investigator.md",
    "planner": "cursor-harness-planner.md",
    "executor": "cursor-harness-executor.md",
    "hard_executor": "cursor-harness-hard-executor.md",
    "verifier": "cursor-harness-verifier.md",
}
REQUIRED_ROLE_POOLS = {
    "investigator": "other",
    "planner": "other",
    "executor": "cursor",
    "hard_executor": "cursor",
    "verifier": "cursor",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def source_files(source_root: Path) -> list[Path]:
    cursor = source_root / "cursor"
    skill_files = sorted((cursor / SKILL_ROOT).rglob("*"))
    return [
        *(cursor / "agents" / name for name in AGENT_NAMES),
        cursor / POLICY_RELATIVE,
        cursor / SKILL_ROOT / "SKILL.md",
        *(path for path in skill_files if path.is_file() and path.name != "SKILL.md"),
        *(cursor / "hooks" / name for name in HOOK_NAMES),
        cursor / "hooks.fragment.json",
    ]


def base_model(model: str) -> str:
    return model.split("[", 1)[0].strip().lower()


def load_model_policy(source_root: Path) -> dict[str, object]:
    policy_path = source_root / "cursor" / POLICY_RELATIVE
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    if not isinstance(policy, dict) or policy.get("version") != 1:
        raise ValueError("Cursor model policy must have version 1")
    roles = policy.get("roles")
    prefixes = policy.get("pool_prefixes")
    if not isinstance(roles, dict) or set(roles) != set(REQUIRED_ROLE_POOLS):
        raise ValueError("Cursor model policy roles are incomplete or unexpected")
    if not isinstance(prefixes, dict) or set(prefixes) != {"cursor", "other"}:
        raise ValueError("Cursor model policy pool_prefixes must define cursor and other")
    normalized_prefixes: dict[str, tuple[str, ...]] = {}
    for pool, values in prefixes.items():
        if not isinstance(values, list) or not values or not all(
            isinstance(value, str) and value.strip() for value in values
        ):
            raise ValueError(f"Cursor model policy prefixes are invalid for {pool}")
        normalized_prefixes[pool] = tuple(value.strip().lower() for value in values)
    for role, required_pool in REQUIRED_ROLE_POOLS.items():
        entry = roles[role]
        if not isinstance(entry, dict):
            raise ValueError(f"Cursor model policy role is invalid: {role}")
        model = entry.get("model")
        pool = entry.get("pool")
        if not isinstance(model, str) or not model.strip() or pool != required_pool:
            raise ValueError(f"Cursor model policy role boundary is invalid: {role}")
        if not any(
            base_model(model).startswith(prefix)
            for prefix in normalized_prefixes[pool]
        ):
            raise ValueError(f"Cursor model does not belong to its declared pool: {role}")
    return policy


def validate_source(source_root: Path) -> None:
    missing = [str(path.relative_to(source_root)) for path in source_files(source_root) if not path.is_file()]
    if missing:
        raise ValueError(f"missing Cursor source files: {missing}")
    load_model_policy(source_root)
    fragment = json.loads((source_root / "cursor/hooks.fragment.json").read_text(encoding="utf-8"))
    if set(fragment) != {"sessionStart", "subagentStart", "beforeShellExecution"}:
        raise ValueError("Cursor hook fragment has unexpected events")
    for event, entries in fragment.items():
        if not isinstance(entries, list) or len(entries) != 1:
            raise ValueError(f"Cursor hook fragment requires one entry for {event}")
        if not isinstance(entries[0].get("command"), str):
            raise ValueError(f"Cursor hook fragment command missing for {event}")


def target_files(source_root: Path, cursor_home: Path) -> list[tuple[Path, Path]]:
    cursor = source_root / "cursor"
    pairs = [
        *((cursor / "agents" / name, cursor_home / "agents" / name) for name in AGENT_NAMES),
        (cursor / POLICY_RELATIVE, cursor_home / POLICY_INSTALL_RELATIVE),
        *((cursor / "hooks" / name, cursor_home / "hooks" / name) for name in HOOK_NAMES),
    ]
    for source in sorted((cursor / SKILL_ROOT).rglob("*")):
        if source.is_file():
            pairs.append((source, cursor_home / source.relative_to(cursor)))
    return pairs


def rendered_content(source_root: Path, source: Path, policy: dict[str, object]) -> bytes:
    role_by_filename = {filename: role for role, filename in ROLE_FILES.items()}
    role = role_by_filename.get(source.name) if source.parent.name == "agents" else None
    content = source.read_text(encoding="utf-8") if role else None
    if role is None:
        return source.read_bytes()
    model = policy["roles"][role]["model"]
    rendered, replacements = re.subn(
        r"(?m)^model:\s*[^\n]+$",
        f"model: {model}",
        content,
        count=1,
    )
    if replacements != 1:
        raise ValueError(f"agent template must contain exactly one model line: {source}")
    return rendered.encode("utf-8")


def backup_root(cursor_home: Path) -> Path:
    parent = cursor_home / "backups" / "codex-mobile-harness"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    candidate = parent / stamp
    suffix = 1
    while candidate.exists():
        candidate = parent / f"{stamp}-{suffix}"
        suffix += 1
    return candidate


def backup_file(path: Path, cursor_home: Path, root: Path) -> Path:
    destination = root / path.relative_to(cursor_home)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, destination)
    return destination


def atomic_copy(source: Path, destination: Path) -> None:
    atomic_bytes(destination, source.read_bytes(), executable=source.suffix == ".py")


def atomic_bytes(destination: Path, content: bytes, *, executable: bool = False) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as temporary:
        temporary_path = Path(temporary.name)
        temporary.write(content)
        temporary.flush()
        os.fsync(temporary.fileno())
    os.replace(temporary_path, destination)
    if executable:
        destination.chmod(0o755)


def atomic_text(destination: Path, content: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=destination.parent, delete=False) as temporary:
        temporary_path = Path(temporary.name)
        temporary.write(content)
        temporary.flush()
        os.fsync(temporary.fileno())
    os.replace(temporary_path, destination)


def merge_hooks(source_root: Path, cursor_home: Path) -> tuple[dict[str, object], bool]:
    fragment = json.loads((source_root / "cursor/hooks.fragment.json").read_text(encoding="utf-8"))
    destination = cursor_home / "hooks.json"
    if destination.exists():
        current = json.loads(destination.read_text(encoding="utf-8"))
        if not isinstance(current, dict) or not isinstance(current.get("hooks"), dict):
            raise ValueError("existing ~/.cursor/hooks.json must contain an object hooks field")
        if current.get("version", 1) != 1:
            raise ValueError("existing ~/.cursor/hooks.json has unsupported version")
    else:
        current = {"version": 1, "hooks": {}}
    changed = False
    hooks = current["hooks"]
    for event, desired_entries in fragment.items():
        entries = hooks.setdefault(event, [])
        if not isinstance(entries, list):
            raise ValueError(f"existing hook event {event} is not an array")
        desired = desired_entries[0]
        matching = next((index for index, entry in enumerate(entries) if isinstance(entry, dict) and entry.get("command") == desired["command"]), None)
        if matching is None:
            entries.append(desired)
            changed = True
        elif entries[matching] != desired:
            entries[matching] = desired
            changed = True
    return current, changed


def manifest_payload(source_root: Path, cursor_home: Path) -> dict[str, object]:
    files: dict[str, str] = {}
    for _, destination in target_files(source_root, cursor_home):
        if destination.is_file():
            files[str(destination.relative_to(cursor_home))] = sha256(destination)
    hooks = cursor_home / "hooks.json"
    if hooks.is_file():
        files["hooks.json"] = sha256(hooks)
    return {
        "manifest_version": 1,
        "source_root": str(source_root),
        "files": dict(sorted(files.items())),
    }


def install(cursor_home: Path, source_root: Path = ROOT) -> dict[str, object]:
    cursor_home = Path(cursor_home).expanduser().resolve()
    source_root = Path(source_root).resolve()
    validate_source(source_root)
    policy = load_model_policy(source_root)
    cursor_home.mkdir(parents=True, exist_ok=True)
    changed = False
    backups: list[str] = []
    backup: Path | None = None

    def ensure_backup(path: Path) -> None:
        nonlocal backup
        if backup is None:
            backup = backup_root(cursor_home)
        backups.append(str(backup_file(path, cursor_home, backup)))

    for source, destination in target_files(source_root, cursor_home):
        content = rendered_content(source_root, source, policy)
        if destination.is_file() and destination.read_bytes() == content:
            continue
        if destination.exists():
            ensure_backup(destination)
        atomic_bytes(destination, content, executable=source.suffix == ".py")
        changed = True

    hooks_destination = cursor_home / "hooks.json"
    hooks, hooks_changed = merge_hooks(source_root, cursor_home)
    serialized_hooks = json.dumps(hooks, indent=2) + "\n"
    if not hooks_destination.exists() or hooks_destination.read_text(encoding="utf-8") != serialized_hooks:
        if hooks_destination.exists():
            ensure_backup(hooks_destination)
        atomic_text(hooks_destination, serialized_hooks)
        changed = True

    manifest_destination = cursor_home / MANIFEST_RELATIVE
    payload = manifest_payload(source_root, cursor_home)
    serialized_manifest = json.dumps(payload, indent=2) + "\n"
    if not manifest_destination.exists() or manifest_destination.read_text(encoding="utf-8") != serialized_manifest:
        if manifest_destination.exists():
            ensure_backup(manifest_destination)
        atomic_text(manifest_destination, serialized_manifest)
        changed = True

    return {"changed": changed, "backups": backups, "manifest": str(manifest_destination), "hooks_changed": hooks_changed}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cursor-home", type=Path, default=Path.home() / ".cursor")
    args = parser.parse_args()
    result = install(args.cursor_home)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
