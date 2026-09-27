"""Credential-free tests for the Zoho Expense helper CLIs."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch


REPOSITORY = Path(__file__).resolve().parents[1]


def load_script(name):
    path = REPOSITORY / "scripts" / name
    spec = importlib.util.spec_from_file_location(f"{path.stem}_under_test", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ExpenseHelperCliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.organizations = load_script("list_organizations.py")
        cls.records = load_script("list_records.py")

    def run_script(self, script, *arguments):
        env = os.environ.copy()
        env.pop("ZOHO_EXPENSE_MCP_URL", None)
        env.pop("ZOHO_EXPENSE_ORGANIZATION_ID", None)
        env.pop("ZOHO_ORGANIZATION_ID", None)
        env.pop("ZOHO_MCP_PROFILE", None)
        return subprocess.run(
            [sys.executable, str(REPOSITORY / "scripts" / script), *arguments],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )

    def test_help_needs_no_credentials(self):
        for script in ("list_organizations.py", "list_records.py"):
            with self.subTest(script=script):
                result = self.run_script(script, "--help")
                self.assertEqual(result.returncode, 0)
                self.assertIn("usage:", result.stdout)
                self.assertEqual(result.stderr, "")

    def test_unknown_and_missing_options_use_exit_code_2(self):
        cases = (
            ("list_organizations.py", ("--unknown",)),
            ("list_records.py", ()),
            ("list_records.py", ("expenses", "--unknown")),
            ("list_records.py", ("expenses", "--query")),
            ("list_records.py", ("expenses", "--query", "organization_id=1")),
        )
        for script, arguments in cases:
            with self.subTest(script=script, arguments=arguments):
                result = self.run_script(script, *arguments)
                self.assertEqual(result.returncode, 2)
                self.assertIn("usage:", result.stderr)

    def test_expense_limit_bounds_first_request_and_result(self):
        rows = [{"expense_id": str(index), "merchant_name": f"Merchant-{index}"} for index in range(1, 5)]
        calls = []

        def fake_page(resource, organization_id, extra_query=None, page=1, per_page=100, timeout=30):
            calls.append(
                {
                    "resource": resource,
                    "organization_id": organization_id,
                    "extra_query": extra_query,
                    "page": page,
                    "per_page": per_page,
                    "timeout": timeout,
                }
            )
            return rows, {"has_more_page": True}

        with patch.object(self.records, "query_page", side_effect=fake_page):
            result = self.records.query_all(
                "expenses",
                "123456789",
                extra_query={"status": "unreported"},
                per_page=100,
                max_records=3,
                timeout=17,
            )

        self.assertEqual(
            calls,
            [
                {
                    "resource": "expenses",
                    "organization_id": "123456789",
                    "extra_query": {"status": "unreported"},
                    "page": 1,
                    "per_page": 3,
                    "timeout": 17,
                }
            ],
        )
        self.assertEqual(len(result), 3)

    def test_organization_normalization(self):
        payload = {
            "organizations": [
                {"organization_id": "1", "name": "Acme"},
                {"organization_id": "2", "name": "Beta"},
            ]
        }
        rows = self.organizations.normalize_organizations(payload)
        self.assertEqual([row["name"] for row in rows], ["Acme", "Beta"])


if __name__ == "__main__":
    unittest.main()
