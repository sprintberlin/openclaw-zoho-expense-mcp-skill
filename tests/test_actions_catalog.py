"""Tests for the Expense actions catalog, profiles, and lookup CLI."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

REPOSITORY = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPOSITORY / "references" / "actions.jsonl"
PROFILES_PATH = REPOSITORY / "references" / "profiles.json"
WORKFLOWS = REPOSITORY / "references" / "COMMON_WORKFLOWS.md"
LOOKUP_SCRIPT = REPOSITORY / "scripts" / "lookup_actions.py"

sys.path.insert(0, str(REPOSITORY / "scripts"))
import lookup_actions  # noqa: E402
import import_actions  # noqa: E402


class ActionsCatalogAndLookupTests(unittest.TestCase):
    def test_catalog_file_is_valid_jsonl(self):
        self.assertTrue(CATALOG_PATH.exists(), f"missing {CATALOG_PATH}")
        lines = [
            line.strip()
            for line in CATALOG_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(lines), 184)
        keys = set()
        for idx, line in enumerate(lines, start=1):
            data = json.loads(line)
            for required in ("key", "name", "summary", "description", "added"):
                self.assertIn(required, data)
                self.assertTrue(str(data[required]).strip())
            self.assertNotIn(data["key"], keys, f"duplicate key {data['key']} at line {idx}")
            keys.add(data["key"])
        self.assertIn("create_expense_report", keys)
        self.assertIn("list_expenses", keys)
        self.assertIn("reimburse_expense_report", keys)

    def test_catalog_keys_match_runtime_tool_names(self):
        for line in CATALOG_PATH.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            self.assertEqual(record["key"], record["name"].replace(" ", "_"))

    def test_profiles_file_is_valid_and_consistent(self):
        self.assertTrue(PROFILES_PATH.exists(), f"missing {PROFILES_PATH}")
        data = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
        self.assertEqual(data.get("version"), 1)
        self.assertEqual(data.get("service"), "expense")
        result = subprocess.run(
            [sys.executable, str(LOOKUP_SCRIPT), "--validate"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Validation OK", result.stdout)

    def test_lookup_cli_profiles_listing(self):
        result = subprocess.run(
            [sys.executable, str(LOOKUP_SCRIPT), "--profiles"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("expense-viewer", result.stdout)
        self.assertIn("expense-submitter", result.stdout)
        self.assertIn("expense-approver", result.stdout)
        self.assertIn("expense-admin", result.stdout)

    def test_lookup_cli_task_inspection(self):
        result = subprocess.run(
            [sys.executable, str(LOOKUP_SCRIPT), "--task", "build-expense-report", "--names-only"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("create expense report", result.stdout)
        self.assertIn("validate expense report", result.stdout)

    def test_lookup_cli_search_names_only(self):
        result = subprocess.run(
            [sys.executable, str(LOOKUP_SCRIPT), "--search", "receipt", "--names-only"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("create upload receipts", result.stdout)

    def test_all_profiles_fit_within_300_action_limit(self):
        data = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
        profiles = data["profiles"]
        counts = {
            profile_id: len(lookup_actions.resolve_profile_actions(profile_id, profiles))
            for profile_id in ("expense-viewer", "expense-submitter", "expense-approver", "expense-admin")
        }
        self.assertEqual(counts["expense-viewer"], 72)
        self.assertEqual(counts["expense-submitter"], 104)
        self.assertEqual(counts["expense-approver"], 121)
        self.assertEqual(counts["expense-admin"], 163)
        self.assertLessEqual(counts["expense-admin"], 300)

    def test_viewer_is_read_only(self):
        data = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
        actions = lookup_actions.resolve_profile_actions("expense-viewer", data["profiles"])
        self.assertIn("list_expenses", actions)
        self.assertIn("get_expense_report", actions)
        for action in actions:
            self.assertFalse(
                action.startswith(("create_", "update_", "delete_", "bulk_", "add_", "submit_", "approve_", "reject_", "reimburse_")),
                f"viewer must stay read-only: {action}",
            )

    def test_submitter_covers_core_expense_workflow_without_deletes(self):
        data = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
        actions = lookup_actions.resolve_profile_actions("expense-submitter", data["profiles"])
        for required in (
            "list_expenses",
            "get_expense",
            "create_expense",
            "update_expense",
            "list_expense_reports",
            "get_expense_report",
            "create_expense_report",
            "update_expense_report",
            "validate_expense_report",
            "submit_expense_report",
        ):
            self.assertIn(required, actions)
        for denied in (
            "delete_expense",
            "delete_expense_report",
            "bulk_delete_expense_reports",
            "approve_expense_report",
            "reimburse_expense_report",
        ):
            self.assertNotIn(denied, actions)

    def test_approver_has_finance_actions(self):
        data = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
        actions = lookup_actions.resolve_profile_actions("expense-approver", data["profiles"])
        for required in (
            "approve_expense_report",
            "reject_expense_report",
            "forward_approval_expense_report",
            "reimburse_expense_report",
        ):
            self.assertIn(required, actions)
        self.assertNotIn("bulk_delete_expense_reports", actions)

    def test_admin_covers_setup_without_bulk_delete(self):
        data = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
        actions = lookup_actions.resolve_profile_actions("expense-admin", data["profiles"])
        for required in ("create_user", "update_organization", "create_expense_category", "update_tax"):
            self.assertIn(required, actions)
        self.assertNotIn("bulk_delete_expense_reports", actions)
        self.assertNotIn("delete_user", actions)

    def test_workflow_actions_exist_in_catalog(self):
        catalog = {
            json.loads(line)["key"]
            for line in CATALOG_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        prefixes = (
            "list ",
            "get ",
            "create ",
            "update ",
            "add ",
            "remove ",
            "validate ",
            "submit ",
            "approve ",
            "reject ",
            "reimburse ",
            "forward ",
            "takeback ",
            "skip ",
            "split ",
        )
        names = {
            span.replace(" ", "_")
            for span in re.findall(r"`([^`]+)`", WORKFLOWS.read_text(encoding="utf-8"))
            if not span.startswith("ZohoExpense_") and span.startswith(prefixes)
        }
        missing = sorted(names - catalog)
        self.assertEqual(missing, [])

    def test_importer_parses_two_line_and_one_line_dumps(self):
        sample = (
            "Zoho Expense\n"
            "Tools linked to your MCP Server\n"
            "Search Tools\n"
            "list expenses\n"
            "To retrieve all expenses in your organization, pass the organization ID.\n"
            "listExpenseDuplicate To retrieve expenses flagged as duplicates.\n"
        )
        parsed = import_actions.parse_dump(sample)
        keys = {entry["key"]: entry for entry in parsed}
        self.assertIn("list_expenses", keys)
        self.assertIn("listExpenseDuplicate", keys)
        self.assertEqual(
            keys["list_expenses"]["description"],
            "To retrieve all expenses in your organization, pass the organization ID.",
        )


if __name__ == "__main__":
    unittest.main()
