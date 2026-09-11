#!/usr/bin/env python3
"""Verify a Cursor Hybrid Harness installation without changing it."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def load_installer():
    path = Path(__file__).with_name("install.py")
    spec = importlib.util.spec_from_file_location("cursor_harness_install_for_verify", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load installer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify(cursor_home: Path, source_root: Path) -> list[str]:
    installer = load_installer()
    cursor_home = Path(cursor_home).expanduser().resolve()
    source_root = Path(source_root).resolve()
    errors: list[str] = []
    try:
        installer.validate_source(source_root)
        policy = installer.load_model_policy(source_root)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f"source validation failed: {error}"]

    for source, destination in installer.target_files(source_root, cursor_home):
        if not destination.is_file():
            errors.append(f"missing installed file: {destination.relative_to(cursor_home)}")
        elif installer.rendered_content(source_root, source, policy) != destination.read_bytes():
            errors.append(f"hash mismatch: {destination.relative_to(cursor_home)}")

    hooks = cursor_home / "hooks.json"
    if not hooks.is_file():
        errors.append("missing installed hooks.json")
    else:
        try:
            installed = json.loads(hooks.read_text(encoding="utf-8"))
            fragment = json.loads((source_root / "cursor/hooks.fragment.json").read_text(encoding="utf-8"))
            for event, entries in fragment.items():
                actual = installed.get("hooks", {}).get(event, [])
                for desired in entries:
                    if desired not in actual:
                        errors.append(f"missing merged hook: {event}/{desired['command']}")
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(f"hooks verification failed: {error}")

    manifest = cursor_home / installer.MANIFEST_RELATIVE
    if not manifest.is_file():
        errors.append("missing installed manifest")
    else:
        try:
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            expected = installer.manifest_payload(source_root, cursor_home)
            if payload != expected:
                errors.append("installed manifest does not match current hashes")
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(f"manifest verification failed: {error}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cursor-home", type=Path, default=Path.home() / ".cursor")
    args = parser.parse_args()
    errors = verify(args.cursor_home, Path(__file__).resolve().parents[1])
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("Cursor Hybrid Harness installation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
