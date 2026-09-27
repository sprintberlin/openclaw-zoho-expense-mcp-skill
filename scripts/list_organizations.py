#!/usr/bin/env python3
"""List Zoho Expense organizations available through one MCP endpoint."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from mcp_client import McporterError, call_tool
from mcp_endpoint import EndpointResolutionError, EndpointSelector, add_endpoint_arguments


ENDPOINT = EndpointSelector("expense", ("ZOHO_EXPENSE_MCP_URL",))
TOOL = "ZohoExpense_list_organizations"


def positive_int(value):
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def build_parser():
    parser = argparse.ArgumentParser(
        description="List Zoho Expense organizations available through an MCP endpoint."
    )
    parser.add_argument("--json", action="store_true", help="print complete JSON records")
    parser.add_argument(
        "--timeout",
        type=positive_int,
        default=30,
        help="MCP call timeout in seconds (default: 30)",
    )
    add_endpoint_arguments(parser)
    return parser


def _walk_for_rows(node):
    if isinstance(node, list):
        return node
    if isinstance(node, dict):
        for key in ("organizations", "data", "response", "result"):
            if key in node:
                rows = _walk_for_rows(node[key])
                if rows is not None:
                    return rows
    return None


def normalize_organizations(payload):
    rows = _walk_for_rows(payload)
    if rows is None:
        return []
    return [row for row in rows if isinstance(row, dict)]


def fetch_organizations(timeout=30):
    mcp_url = ENDPOINT.get()
    return call_tool(mcp_url, TOOL, {}, timeout=timeout)


def pick(record, *names):
    for name in names:
        value = record.get(name)
        if value not in (None, ""):
            return str(value)
    return "-"


def print_table(rows):
    if not rows:
        print("No organizations found.")
        return

    table = [
        [
            pick(row, "organization_id", "organizationId", "id"),
            pick(row, "name", "organization_name"),
            pick(row, "currency_code", "currencyCode", "currency"),
            pick(row, "country", "country_code"),
        ]
        for row in rows
    ]
    headers = ["Organization ID", "Name", "Currency", "Country"]
    widths = [
        max(len(headers[index]), *(len(row[index]) for row in table))
        for index in range(len(headers))
    ]
    print(" | ".join(value.ljust(widths[index]) for index, value in enumerate(headers)))
    print("-+-".join("-" * width for width in widths))
    for row in table:
        print(" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)))
    print(f"\n{len(rows)} organization(s)")


def main(argv=None):
    args = build_parser().parse_args(argv)
    ENDPOINT.configure(args)
    try:
        rows = normalize_organizations(fetch_organizations(timeout=args.timeout))
    except (EndpointResolutionError, McporterError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        print_table(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
