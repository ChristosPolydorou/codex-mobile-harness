from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = {
    "AGENTS.md",
    "README.md",
    ".codex/config.toml",
    ".codex/agents/investigator.toml",
    ".codex/agents/planner.toml",
    ".codex/agents/executor.toml",
    ".codex/agents/verifier.toml",
    "harness/README.md",
    "harness/context/.gitkeep",
    "harness/executions/.gitkeep",
    "harness/plans/.gitkeep",
    "harness/reports/.gitkeep",
    "harness/rules/routing.md",
    "harness/rules/complexity.md",
    "harness/rules/escalation.md",
    "harness/rules/scope-control.md",
    "harness/rules/git-policy.md",
    "harness/rules/verification.md",
    "harness/mobile/android.md",
    "harness/mobile/ios.md",
    "harness/templates/implementation-contract.md",
    "harness/templates/escalation-report.md",
    "harness/templates/investigation-report.md",
    "harness/templates/verification-report.md",
}

SUPPORTED_ROUTED_MODELS = {
    "gpt-5.6-luna",
    "gpt-5.6-terra",
    "gpt-5.6-sol",
    "gpt-6-astra",
}

FORBIDDEN_PLACEHOLDER_PATTERN = re.compile(
    r"\b(?:TBD|TODO|implement later|fill in details)\b", re.IGNORECASE
)
RUNTIME_COMPLETION_FORM_FIELD_PATTERN = re.compile(
    r"^- \[runtime-completion\] [^:]+: <[^>]+> "
    r"<!-- runtime-completion -->$"
)
ROUTED_MODEL_WITH_HIGH_PATTERN = re.compile(r"`?(gpt-[a-z0-9.-]+)`?\s+high\b")

ROLE_FILES = {
    "investigator": ".codex/agents/investigator.toml",
    "planner": ".codex/agents/planner.toml",
    "executor": ".codex/agents/executor.toml",
    "verifier": ".codex/agents/verifier.toml",
}

REQUIRED_CONTRACT_HEADINGS = {
    "Objective",
    "Mode and Complexity",
    "Observed Behavior",
    "Expected Behavior",
    "Root Cause or Design Rationale",
    "Relevant Architecture and Ownership",
    "Constraints",
    "Files In Scope",
    "Files Explicitly Out of Scope",
    "Required Changes",
    "Tests to Add",
    "Tests and Checks to Run",
    "Acceptance Criteria",
    "Non-Goals",
    "Risks",
    "Assumptions",
    "Escalation Conditions",
    "Approval Status",
    "Completion Checklist",
}


def is_runtime_completion_form_field(path: Path, line: str) -> bool:
    return (
        path.parent == ROOT / "harness/templates"
        and RUNTIME_COMPLETION_FORM_FIELD_PATTERN.fullmatch(line) is not None
    )


class HarnessContractTests(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        missing = sorted(path for path in REQUIRED_FILES if not (ROOT / path).is_file())
        self.assertEqual([], missing)

    def test_project_config_uses_safe_defaults(self) -> None:
        with (ROOT / ".codex/config.toml").open("rb") as source:
            config = tomllib.load(source)
        self.assertEqual("high", config["plan_mode_reasoning_effort"])
        self.assertTrue(config["agents"]["enabled"])
        self.assertEqual(4, config["agents"]["max_concurrent_threads_per_session"])
        self.assertEqual("gpt-5.6-luna", config["agents"]["default_subagent_model"])
        self.assertEqual("high", config["agents"]["default_subagent_reasoning_effort"])

    def test_custom_agent_schema_and_names(self) -> None:
        for expected_name, relative_path in ROLE_FILES.items():
            with self.subTest(role=expected_name):
                with (ROOT / relative_path).open("rb") as source:
                    role = tomllib.load(source)
                self.assertEqual(expected_name, role["name"])
                self.assertTrue(role["description"].strip())
                self.assertTrue(role["developer_instructions"].strip())

    def test_roles_are_not_model_pinned(self) -> None:
        for relative_path in ROLE_FILES.values():
            with (ROOT / relative_path).open("rb") as source:
                role = tomllib.load(source)
            self.assertNotIn("model", role)
            self.assertNotIn("model_reasoning_effort", role)

    def test_router_contains_exact_model_boundaries(self) -> None:
        router = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        required_phrases = {
            "gpt-6-astra",
            "gpt-5.6-sol",
            "gpt-5.6-terra",
            "gpt-5.6-luna",
            "Planner ceiling",
            "Executor allowlist",
            "plan-only",
            "investigate-only",
            "human approval",
            "independent Verifier",
        }
        missing = sorted(phrase for phrase in required_phrases if phrase not in router)
        self.assertEqual([], missing)

    def test_rule_links_from_agents_file_exist(self) -> None:
        router = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        links = re.findall(r"\[[^]]+\]\((harness/[^)]+\.md)\)", router)
        self.assertGreaterEqual(len(links), 8)
        missing = sorted(link for link in links if not (ROOT / link).is_file())
        self.assertEqual([], missing)

    def test_implementation_contract_has_every_required_heading(self) -> None:
        template = (ROOT / "harness/templates/implementation-contract.md").read_text(
            encoding="utf-8"
        )
        headings = {
            line.removeprefix("## ").strip()
            for line in template.splitlines()
            if line.startswith("## ")
        }
        self.assertEqual(set(), REQUIRED_CONTRACT_HEADINGS - headings)

    def test_mobile_gates_cover_critical_platform_risks(self) -> None:
        android = (ROOT / "harness/mobile/android.md").read_text(encoding="utf-8")
        ios = (ROOT / "harness/mobile/ios.md").read_text(encoding="utf-8")
        for phrase in ("StateFlow", "Compose", "Room", "WorkManager", "permissions", "R8"):
            self.assertIn(phrase, android)
        for phrase in ("MainActor", "SwiftUI", "Keychain", "entitlements", "signing", "SwiftData"):
            self.assertIn(phrase, ios)

    def test_mobile_approval_gates_preserve_router_specific_triggers(self) -> None:
        android = " ".join(
            (ROOT / "harness/mobile/android.md").read_text(encoding="utf-8").split()
        )
        ios = " ".join(
            (ROOT / "harness/mobile/ios.md").read_text(encoding="utf-8").split()
        )
        for phrase in (
            "permissions",
            "Services",
            "receivers",
            "deep links",
            "background execution",
            "signing",
            "R8/ProGuard",
            "DI boundary",
            "Regardless of its L3",
        ):
            self.assertIn(phrase, android)
        for phrase in (
            "entitlements",
            "signing",
            "capabilities",
            "Keychain",
            "background modes",
            "deep links",
            "actor isolation",
            "persistence migration",
            "Regardless of its L3",
        ):
            self.assertIn(phrase, ios)

    def test_verification_inputs_support_direct_l0_l1_routes(self) -> None:
        verification = (ROOT / "harness/rules/verification.md").read_text(
            encoding="utf-8"
        )
        template = (ROOT / "harness/templates/verification-report.md").read_text(
            encoding="utf-8"
        )
        for document in (verification, template):
            normalized_document = " ".join(document.split())
            for phrase in (
                "L0/L1",
                "immutable route/execution record",
                "direct-route change budget",
                "in-scope files/symbols",
                "tests and checks",
            ):
                self.assertIn(phrase, normalized_document)

    def test_investigation_template_has_investigate_only_terminal_choice(self) -> None:
        template = (ROOT / "harness/templates/investigation-report.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "NONE — investigate-only request complete; stop after this report", template
        )

    def test_verification_status_vocabulary_is_explicit(self) -> None:
        verification = (ROOT / "harness/rules/verification.md").read_text(
            encoding="utf-8"
        )
        template = (ROOT / "harness/templates/verification-report.md").read_text(
            encoding="utf-8"
        )
        for document in (verification, template):
            for status in ("PASS", "FAIL", "BLOCKED", "NOT RUN"):
                self.assertIn(status, document)

    def test_validator_is_self_contained_and_does_not_read_task_reports(self) -> None:
        validator_source = Path(__file__).read_text(encoding="utf-8")
        ignored_session_directory = ".super" + "powers/"
        self.assertNotIn(ignored_session_directory, validator_source)

    def test_harness_gitkeep_placeholders_are_zero_bytes(self) -> None:
        placeholders = sorted((ROOT / "harness").rglob(".gitkeep"))
        self.assertEqual(4, len(placeholders))
        self.assertTrue(all(path.stat().st_size == 0 for path in placeholders))

    def test_direct_l0_l1_inputs_are_accepted_by_all_execution_consumers(self) -> None:
        required_direct_route_inputs = (
            "immutable direct L0/L1 route/execution record",
            "direct-route change budget",
        )
        for relative_path in (
            ".codex/agents/executor.toml",
            ".codex/agents/verifier.toml",
            "harness/rules/scope-control.md",
        ):
            with self.subTest(document=relative_path):
                document = (ROOT / relative_path).read_text(encoding="utf-8")
                for phrase in required_direct_route_inputs:
                    self.assertIn(phrase, document)

        scope_control = (ROOT / "harness/rules/scope-control.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "primary router/controller prepares the direct-route record and budget before spawning the Executor",
            " ".join(scope_control.split()),
        )

    def test_investigator_and_verifier_match_canonical_report_templates(self) -> None:
        investigator = (ROOT / ".codex/agents/investigator.toml").read_text(
            encoding="utf-8"
        )
        for contract_only_section in (
            "Files Explicitly Out of Scope",
            "Tests to Add",
            "Approval Status",
            "Completion Checklist",
        ):
            with self.subTest(section=contract_only_section):
                self.assertNotIn(contract_only_section, investigator)

        verifier = (ROOT / ".codex/agents/verifier.toml").read_text(encoding="utf-8")
        for severity in ("BLOCKER", "MAJOR", "MINOR", "INFORMATIONAL"):
            self.assertIn(severity, verifier)
        for noncanonical_severity in ("critical", "high", "medium", "low"):
            self.assertNotIn(f"severity ({noncanonical_severity}", verifier.lower())

        verification_template = (ROOT / "harness/templates/verification-report.md").read_text(
            encoding="utf-8"
        )
        for heading in ("BLOCKER", "MAJOR", "MINOR", "INFORMATIONAL"):
            self.assertIn(f"### {heading}\n\nNone found", verification_template)

    def test_terminal_route_records_define_all_roles_and_explicit_none_fields(self) -> None:
        for relative_path in ("AGENTS.md", "harness/rules/routing.md"):
            with self.subTest(document=relative_path):
                document = " ".join(
                    (ROOT / relative_path).read_text(encoding="utf-8").split()
                )
                for field in (
                    "investigator model",
                    "planner model",
                    "executor model",
                    "verifier model",
                ):
                    self.assertIn(field, document)
                self.assertIn("none", document)

        routing = " ".join(
            (ROOT / "harness/rules/routing.md").read_text(encoding="utf-8").split()
        )
        for phrase in (
            "L0/L1 plan-only: Investigator `none`; Planner `gpt-5.6-luna` high; Executor `none`; Verifier `none`",
            "L0/L1 investigate-only: Investigator `gpt-5.6-luna` high; Planner `none`; Executor `none`; Verifier `none`",
            "L3 plan-only: Investigator `none`; Planner `gpt-5.6-sol` high; Executor `none`; Verifier `none`",
            "L4/L5 investigate-only: Investigator `gpt-6-astra` high; Planner `none`; Executor `none`; Verifier `none`",
            "Plan-only never spawns an Executor or Verifier",
            "Investigate-only never spawns a Planner, Executor, or Verifier",
        ):
            self.assertIn(phrase, routing)

    def test_readme_documents_required_setup_and_modes(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for phrase in (
            "Plan only",
            "Investigate only",
            "human approval",
            "python3 -m unittest -v tests/test_harness_contract.py",
            ".codex/agents/*.toml",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, readme)

    def test_read_only_role_persistence_rule_is_consistent_across_policy(self) -> None:
        required_rule = (
            "Read-only Investigator, Planner, and Verifier author and return complete "
            "artifact or escalation content in their response; they never write "
            "repository files.",
            "The primary controller may persist returned content only during an "
            "authorized implementation workflow and only within approved scope.",
            "Plan-only and investigate-only remain conversation-output-only and modify "
            "no workspace file unless the user separately asks to save the result.",
            "Executor may write only authorized implementation/execution records within "
            "its workspace-write scope.",
            "Escalation content may be authored by any active role, not only Executor.",
        )
        for relative_path in (
            "AGENTS.md",
            "harness/rules/escalation.md",
            "harness/templates/escalation-report.md",
        ):
            with self.subTest(document=relative_path):
                document = " ".join(
                    (ROOT / relative_path).read_text(encoding="utf-8").split()
                )
                for statement in required_rule:
                    self.assertIn(statement, document)

    def test_harness_authored_content_has_no_unresolved_placeholders(self) -> None:
        """Scan shipped policy, excluding validator literals and marked form inputs."""
        scan_paths = [ROOT / "AGENTS.md", ROOT / "README.md"]
        scan_paths.extend((ROOT / ".codex").rglob("*.toml"))
        scan_paths.extend((ROOT / "harness").rglob("*.md"))

        findings = []
        for path in scan_paths:
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if (
                    not is_runtime_completion_form_field(path, line)
                    and FORBIDDEN_PLACEHOLDER_PATTERN.search(line)
                ):
                    findings.append(f"{path.relative_to(ROOT)}:{line_number}: {line}")

        self.assertEqual([], findings)

    def test_custom_agents_have_no_functional_markdown_role_files(self) -> None:
        agent_markdown_files = sorted(
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / ".codex/agents").glob("*.md")
            if path.is_file()
        )
        self.assertEqual([], agent_markdown_files)

    def test_routing_documents_use_supported_models_at_high_effort(self) -> None:
        for relative_path in ("AGENTS.md", "harness/rules/routing.md"):
            with self.subTest(document=relative_path):
                document = (ROOT / relative_path).read_text(encoding="utf-8")
                routed_models = re.findall(r"gpt-[a-z0-9.-]+", document)
                high_effort_models = ROUTED_MODEL_WITH_HIGH_PATTERN.findall(document)
                self.assertTrue(routed_models)
                self.assertTrue(set(routed_models).issubset(SUPPORTED_ROUTED_MODELS))
                self.assertEqual(routed_models, high_effort_models)

    def test_runtime_completion_marker_requires_template_form_field(self) -> None:
        original_read_text = Path.read_text
        invalid_root_placeholder = "TBD <!-- runtime-completion -->\n"
        invalid_template_placeholder = "TBD <!-- runtime-completion -->\n"
        valid_template_form_field = (
            "- [runtime-completion] Runtime evidence: <TODO> "
            "<!-- runtime-completion -->\n"
        )

        def read_text_with_marker(
            target_path: Path, replacement: str
        ) -> callable:
            def read_text(path: Path, *args, **kwargs) -> str:
                if path == target_path:
                    return replacement
                return original_read_text(path, *args, **kwargs)

            return read_text

        with patch.object(
            Path,
            "read_text",
            new=read_text_with_marker(ROOT / "README.md", invalid_root_placeholder),
        ):
            with self.assertRaises(AssertionError):
                self.test_harness_authored_content_has_no_unresolved_placeholders()

        with patch.object(
            Path,
            "read_text",
            new=read_text_with_marker(
                ROOT / "harness/templates/investigation-report.md",
                invalid_template_placeholder,
            ),
        ):
            with self.assertRaises(AssertionError):
                self.test_harness_authored_content_has_no_unresolved_placeholders()

        with patch.object(
            Path,
            "read_text",
            new=read_text_with_marker(
                ROOT / "harness/templates/investigation-report.md",
                valid_template_form_field,
            ),
        ):
            self.test_harness_authored_content_has_no_unresolved_placeholders()

    def test_each_routed_model_occurrence_requires_high_effort(self) -> None:
        weakened_matrix = "\n".join(
            (
                "| L0 | no Planner | `gpt-5.6-luna` high | `gpt-5.6-luna` high |",
                "| L1 | no Planner | `gpt-5.6-luna` high | `gpt-5.6-luna` high |",
                "| L2 | `gpt-5.6-terra` high | `gpt-5.6-luna` high | `gpt-5.6-terra` high |",
                "| L3 | `gpt-5.6-sol` high | `gpt-5.6-luna` high or `gpt-5.6-terra` high | `gpt-5.6-terra` high |",
                "| L4 | `gpt-6-astra` high | `gpt-5.6-terra` high | `gpt-5.6-sol` high |",
                "| L5 | `gpt-6-astra` high | `gpt-5.6-terra` high | `gpt-5.6-sol` high or `gpt-6-astra` |",
            )
        )

        routed_models = re.findall(r"gpt-[a-z0-9.-]+", weakened_matrix)
        high_effort_models = ROUTED_MODEL_WITH_HIGH_PATTERN.findall(weakened_matrix)
        self.assertNotEqual(routed_models, high_effort_models)
        self.assertEqual("gpt-6-astra", routed_models[-1])
        self.assertNotIn("gpt-6-astra", high_effort_models[-1:])


if __name__ == "__main__":
    unittest.main()
