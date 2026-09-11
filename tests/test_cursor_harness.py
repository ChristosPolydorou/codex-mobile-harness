from __future__ import annotations

import json
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURSOR_ROOT = ROOT / "cursor"

REQUIRED_CURSOR_ARTIFACTS = {
    "README.md",
    "hooks.fragment.json",
    "model-policy.json",
    "agents/cursor-harness-investigator.md",
    "agents/cursor-harness-planner.md",
    "agents/cursor-harness-executor.md",
    "agents/cursor-harness-hard-executor.md",
    "agents/cursor-harness-verifier.md",
    "skills/cursor-hybrid-harness/SKILL.md",
    "hooks/codex-mobile-harness-session.py",
    "hooks/codex-mobile-harness-model-guard.py",
    "hooks/codex-mobile-harness-git-guard.py",
    "install.py",
    "verify.py",
}

AGENT_CONTRACTS = {
    "investigator": {
        "file": "agents/cursor-harness-investigator.md",
        "model": "gpt-5.6-terra[effort=high]",
        "marker": "[cursor-harness-role:investigator]",
        "read_only": True,
    },
    "planner": {
        "file": "agents/cursor-harness-planner.md",
        "model": "claude-opus-5[effort=high]",
        "marker": "[cursor-harness-role:planner]",
        "read_only": True,
    },
    "executor": {
        "file": "agents/cursor-harness-executor.md",
        "model": "composer-2.5[fast=false]",
        "marker": "[cursor-harness-role:executor]",
        "read_only": False,
    },
    "hard-executor": {
        "file": "agents/cursor-harness-hard-executor.md",
        "model": "grok-4.6[fast=false]",
        "marker": "[cursor-harness-role:executor]",
        "read_only": False,
    },
    "verifier": {
        "file": "agents/cursor-harness-verifier.md",
        "model": "grok-4.6[fast=false]",
        "marker": "[cursor-harness-role:verifier]",
        "read_only": True,
    },
}

HOOK_COMMANDS = {
    "sessionStart": "python3 ~/.cursor/hooks/codex-mobile-harness-session.py",
    "subagentStart": "python3 ~/.cursor/hooks/codex-mobile-harness-model-guard.py",
    "beforeShellExecution": "python3 ~/.cursor/hooks/codex-mobile-harness-git-guard.py",
}


def cursor_path(relative_path: str) -> Path:
    return CURSOR_ROOT / relative_path


def load_cursor_text(relative_path: str) -> str:
    return cursor_path(relative_path).read_text(encoding="utf-8")


def load_hook_fragment() -> dict[str, object]:
    with cursor_path("hooks.fragment.json").open(encoding="utf-8") as source:
        return json.load(source)


def load_frontmatter(relative_path: str) -> dict[str, str]:
    document = load_cursor_text(relative_path)
    match = re.match(r"^---\n(?P<frontmatter>.*?)\n---\n", document, re.DOTALL)
    if match is None:
        raise AssertionError(f"{relative_path} must begin with YAML frontmatter")
    return {
        key: value.strip().strip('"')
        for key, value in re.findall(
            r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.+)$",
            match.group("frontmatter"),
            re.MULTILINE,
        )
    }


def run_hook(relative_path: str, payload: object) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, str(cursor_path(relative_path))],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "returncode": completed.returncode,
        "output": json.loads(completed.stdout),
        "stderr": completed.stderr,
    }


def load_module(relative_path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, cursor_path(relative_path))
    if spec is None or spec.loader is None:
        raise AssertionError(f"unable to load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CursorHarnessContractTests(unittest.TestCase):
    def test_required_cursor_artifacts_exist(self) -> None:
        missing = sorted(
            relative_path
            for relative_path in REQUIRED_CURSOR_ARTIFACTS
            if not cursor_path(relative_path).is_file()
        )
        self.assertEqual([], missing)

    def test_agents_pin_the_approved_models_and_roles(self) -> None:
        for role, contract in AGENT_CONTRACTS.items():
            with self.subTest(role=role):
                path = cursor_path(contract["file"])
                if not path.is_file():
                    self.skipTest(f"awaiting {contract['file']}")
                frontmatter = load_frontmatter(contract["file"])
                self.assertEqual(f"cursor-harness-{role}", frontmatter.get("name"))
                self.assertEqual(contract["model"], frontmatter.get("model"))
                self.assertEqual(
                    str(contract["read_only"]).lower(), frontmatter.get("readonly")
                )
                self.assertIn(contract["marker"], load_cursor_text(contract["file"]))

    def test_model_policy_is_the_single_source_for_role_models_and_pools(self) -> None:
        policy = json.loads(load_cursor_text("model-policy.json"))
        self.assertEqual(1, policy["version"])
        expected = {
            "investigator": ("gpt-5.6-terra[effort=high]", "other"),
            "planner": ("claude-opus-5[effort=high]", "other"),
            "executor": ("composer-2.5[fast=false]", "cursor"),
            "hard_executor": ("grok-4.6[fast=false]", "cursor"),
            "verifier": ("grok-4.6[fast=false]", "cursor"),
        }
        for role, (model, pool) in expected.items():
            with self.subTest(role=role):
                self.assertEqual(model, policy["roles"][role]["model"])
                self.assertEqual(pool, policy["roles"][role]["pool"])
                agent_role = "hard-executor" if role == "hard_executor" else role
                frontmatter = load_frontmatter(
                    AGENT_CONTRACTS[agent_role]["file"]
                )
                self.assertEqual(model, frontmatter["model"])
        self.assertIn("composer-", policy["pool_prefixes"]["cursor"])
        self.assertIn("grok-", policy["pool_prefixes"]["cursor"])

    def test_model_policy_override_changes_installed_agent_without_template_edit(
        self,
    ) -> None:
        installer = load_module("install.py", "cursor_harness_policy_install")
        with tempfile.TemporaryDirectory() as temporary:
            source_root = Path(temporary) / "source"
            shutil.copytree(CURSOR_ROOT, source_root / "cursor")
            policy_path = source_root / "cursor" / "model-policy.json"
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["roles"]["verifier"]["model"] = "composer-2.5[fast=false]"
            policy_path.write_text(json.dumps(policy, indent=2) + "\n", encoding="utf-8")

            cursor_home = Path(temporary) / ".cursor"
            installer.install(cursor_home, source_root)
            installed = (cursor_home / "agents" / "cursor-harness-verifier.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("model: composer-2.5[fast=false]", installed)

    def test_skill_preserves_authority_and_activates_mobile_policy_only_for_mobile_work(
        self,
    ) -> None:
        relative_path = "skills/cursor-hybrid-harness/SKILL.md"
        if not cursor_path(relative_path).is_file():
            self.skipTest(f"awaiting {relative_path}")
        skill = load_cursor_text(relative_path)
        for phrase in (
            "Team and Enterprise policy",
            "current user request",
            "existing Cursor User Rules",
            "AGENTS.md",
            "~/.agents/skills/mobile-template-engineering/v1",
            "Android",
            "iOS",
            "Kotlin Multiplatform",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill)

    def test_skill_defines_terminal_modes_without_executor_or_verifier_dispatch(
        self,
    ) -> None:
        relative_path = "skills/cursor-hybrid-harness/SKILL.md"
        if not cursor_path(relative_path).is_file():
            self.skipTest(f"awaiting {relative_path}")
        skill = load_cursor_text(relative_path)
        for phrase in (
            "plan-only",
            "investigate-only",
            "Plan-only never spawns an Executor or Verifier",
            "Investigate-only never spawns a Planner, Executor, or Verifier",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill)

    def test_hook_fragment_has_one_unique_command_for_each_required_event(self) -> None:
        relative_path = "hooks.fragment.json"
        if not cursor_path(relative_path).is_file():
            self.skipTest(f"awaiting {relative_path}")
        fragment = load_hook_fragment()
        self.assertEqual(set(HOOK_COMMANDS), set(fragment))
        commands = []
        for event, expected_command in HOOK_COMMANDS.items():
            with self.subTest(event=event):
                entries = fragment[event]
                self.assertIsInstance(entries, list)
                self.assertEqual(1, len(entries))
                self.assertEqual(expected_command, entries[0]["command"])
                commands.append(entries[0]["command"])
        self.assertEqual(len(commands), len(set(commands)))

    def test_model_guard_enforces_marked_pool_boundaries_and_leaves_unmarked_alone(
        self,
    ) -> None:
        guard = "hooks/codex-mobile-harness-model-guard.py"
        if not cursor_path(guard).is_file():
            self.skipTest(f"awaiting {guard}")
        cases = (
            ({"task": "[cursor-harness-role:executor] implement", "subagent_model": "composer-2.5"}, "allow"),
            ({"task": "[cursor-harness-role:executor] implement", "subagent_model": "claude-opus-5"}, "deny"),
            ({"task": "[cursor-harness-role:planner] plan", "subagent_model": "claude-opus-5"}, "allow"),
            ({"task": "[cursor-harness-role:planner] plan", "subagent_model": "grok-4.6"}, "deny"),
            ({"task": "[cursor-harness-role:verifier] verify", "subagent_model": "grok-4.6"}, "allow"),
            ({"task": "[cursor-harness-role:verifier] verify", "subagent_model": "claude-opus-5"}, "deny"),
            ({"task": "ordinary built-in work", "subagent_model": "claude-opus-5"}, "allow"),
            ({"task": "[cursor-harness-role:executor] implement"}, "deny"),
        )
        for payload, expected in cases:
            with self.subTest(payload=payload):
                result = run_hook(guard, payload)
                self.assertEqual(0, result["returncode"])
                self.assertEqual(expected, result["output"]["permission"])

    def test_git_guard_blocks_destructive_history_commands_and_allows_inspection(
        self,
    ) -> None:
        guard = "hooks/codex-mobile-harness-git-guard.py"
        if not cursor_path(guard).is_file():
            self.skipTest(f"awaiting {guard}")
        forbidden = (
            "git commit -m change",
            "git push origin main",
            "git -C /tmp/repo reset --hard HEAD",
            "cd /tmp/repo && git clean -fd",
            "env git push",
        )
        allowed = ("git status --short", "git diff --check", "git log -1")
        for command in forbidden:
            with self.subTest(command=command):
                result = run_hook(guard, {"command": command})
                self.assertEqual("deny", result["output"]["permission"])
        for command in allowed:
            with self.subTest(command=command):
                result = run_hook(guard, {"command": command})
                self.assertEqual("allow", result["output"]["permission"])
        malformed = run_hook(guard, {"cwd": "/tmp"})
        self.assertEqual("deny", malformed["output"]["permission"])

    def test_session_hook_emits_routing_context(self) -> None:
        hook = "hooks/codex-mobile-harness-session.py"
        if not cursor_path(hook).is_file():
            self.skipTest(f"awaiting {hook}")
        result = run_hook(hook, {})
        self.assertEqual(0, result["returncode"])
        context = result["output"]["additional_context"]
        self.assertIn("cursor-hybrid-harness", context)
        self.assertIn("Cursor Models", context)
        self.assertIn("Other Models", context)
        self.assertIn("verifier=grok-4.6[fast=false]", context)
        self.assertIn("cursor/model-policy.json", context)

    def test_installer_merges_idempotently_backs_up_changes_and_preserves_unrelated_files(
        self,
    ) -> None:
        installer_path = "install.py"
        verifier_path = "verify.py"
        if not cursor_path(installer_path).is_file() or not cursor_path(verifier_path).is_file():
            self.skipTest("awaiting installer and verifier")
        installer = load_module(installer_path, "cursor_harness_install")
        verifier = load_module(verifier_path, "cursor_harness_verify")
        with tempfile.TemporaryDirectory() as temporary:
            cursor_home = Path(temporary) / ".cursor"
            cursor_home.mkdir()
            unrelated = {"command": "./hooks/unrelated.py"}
            (cursor_home / "hooks.json").write_text(
                json.dumps({"version": 1, "hooks": {"sessionStart": [unrelated]}}),
                encoding="utf-8",
            )
            settings = cursor_home / "settings.json"
            settings.write_text('{"preserve": true}\n', encoding="utf-8")
            first = installer.install(cursor_home, ROOT)
            self.assertTrue(first["changed"])
            merged = json.loads((cursor_home / "hooks.json").read_text(encoding="utf-8"))
            self.assertIn(unrelated, merged["hooks"]["sessionStart"])
            self.assertEqual([], verifier.verify(cursor_home, ROOT))
            backup_root = cursor_home / "backups" / "codex-mobile-harness"
            backup_count = len(tuple(backup_root.rglob("*")))
            second = installer.install(cursor_home, ROOT)
            self.assertFalse(second["changed"])
            self.assertEqual(backup_count, len(tuple(backup_root.rglob("*"))))
            self.assertEqual('{"preserve": true}\n', settings.read_text(encoding="utf-8"))

    def test_install_module_is_self_contained_and_manifest_has_hashes(self) -> None:
        installer_path = "install.py"
        if not cursor_path(installer_path).is_file():
            self.skipTest(f"awaiting {installer_path}")
        installer = load_module(installer_path, "cursor_harness_install_manifest")
        self.assertTrue(callable(installer.install))
        self.assertTrue(callable(installer.sha256))


if __name__ == "__main__":
    unittest.main()
