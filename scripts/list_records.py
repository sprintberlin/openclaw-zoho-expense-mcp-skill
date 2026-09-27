#!/usr/bin/env python3
"""List common Zoho Expense record types with pagination and account routing."""

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


ENDPOINT = EndpointSelector(
    "expense",
    ("ZOHO_EXPENSE_MCP_URL",),
    require_organization_id=True,
)

RESOURCES = {
    "expenses": {
        "tool": "ZohoExpense_list_expenses",
        "response_key": "expenses",
        "columns": (
            ("expense_id", "ID"),
            ("date", "Date"),
            ("user_name", "Employee"),
            ("merchant_name", "Merchant"),
            ("category_name", "Category"),
            ("amount", "Amount"),
            ("currency_code", "Currency"),
            ("status", "Status"),
        ),
    },
    "reports": {
        "tool": "ZohoExpense_list_expense_reports",
        "response_key": "expense_reports",
        "columns": (
            ("report_id", "ID"),
            ("report_number", "Report"),
            ("report_name", "Name"),
            ("user_name", "Submitter"),
            ("total", "Total"),
            ("currency_code", "Currency"),
            ("status", "Status"),
        ),
    },
    "advances": {
        "tool": "ZohoExpense_list_advance_payments",
        "response_key": "advance_payments",
        "columns": (
            ("advance_id", "ID"),
            ("user_name", "Employee"),
            ("date", "Date"),
            ("amount", "Amount"),
            ("currency_code", "Currency"),
            ("status", "Status"),
        ),
    },
    "projects": {
        "tool": "ZohoExpense_list_projects",
        "response_key": "projects",
        "columns": (
            ("project_id", "ID"),
            ("project_name", "Project"),
            ("customer_name", "Customer"),
            ("status", "Status"),
        ),
    },
    "users": {
        "tool": "ZohoExpense_list_users",
        "response_key": "users",
        "columns": (
            ("user_id", "ID"),
            ("name", "Name"),
            ("email", "Email"),
            ("status", "Status"),
        ),
    },
}

_RESERVED_QUERY_KEYS = {"organization_id", "page", "per_page"}


def positive_int(value):
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def query_pair(value):
    key, separator, raw = value.partition("=")
    key = key.strip()
    if not separator or not key:
        raise argparse.ArgumentTypeError("must use KEY=VALUE")
    if key in _RESERVED_QUERY_KEYS:
        raise argparse.ArgumentTypeError(
            f"{key} is managed by the helper and cannot be overridden"
        )
    return key, raw


def build_parser():
    parser = argparse.ArgumentParser(
        description="List expenses, reports, advances, projects, or users from Zoho Expense."
    )
    parser.add_argument("resource", choices=sorted(RESOURCES))
    parser.add_argument(
        "--query",
        type=query_pair,
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="additional live Action query parameter; repeat as needed",
    )
    parser.add_argument("--json", action="store_true", help="print complete JSON records")
    parser.add_argument("--limit", type=positive_int, help="return at most this many records")
    parser.add_argument(
        "--page-size",
        type=positive_int,
        default=100,
        help="page size (default: 100)",
    )
    parser.add_argument(
        "--timeout",
        type=positive_int,
        default=30,
        help="MCP call timeout in seconds (default: 30)",
    )
    add_endpoint_arguments(parser, include_organization_id=True)
    return parser


def _walk_for_rows(node, response_key):
    if isinstance(node, list):
        return node
    if isinstance(node, dict):
        if response_key in node and isinstance(node[response_key], list):
            return node[response_key]
        for key in ("data", "response", "result"):
            if key in node:
                rows = _walk_for_rows(node[key], response_key)
                if rows is not None:
                    return rows
    return None


def normalize_page(payload, response_key):
    rows = _walk_for_rows(payload, response_key)
    if rows is None:
        rows = []
    rows = [row for row in rows if isinstance(row, dict)]

    page_context = {}
    if isinstance(payload, dict):
        page_context = payload.get("page_context") or payload.get("pageContext") or {}
        if not page_context and isinstance(payload.get("data"), dict):
            page_context = (
                payload["data"].get("page_context")
                or payload["data"].get("pageContext")
                or {}
            )
    return rows, page_context if isinstance(page_context, dict) else {}


def query_page(resource, organization_id, extra_query=None, page=1, per_page=100, timeout=30):
    config = RESOURCES[resource]
    query_params = {
        "organization_id": organization_id,
        "page": page,
        "per_page": per_page,
    }
    query_params.update(extra_query or {})
    payload = call_tool(
        ENDPOINT.get(),
        config["tool"],
        {"query_params": query_params},
        timeout=timeout,
    )
    return normalize_page(payload, config["response_key"])


def query_all(resource, organization_id, extra_query=None, per_page=100, max_records=None, timeout=30):
    records = []
    page = 1

    while True:
        request_limit = per_page
        if max_records is not None:
            remaining = max_records - len(records)
            if remaining <= 0:
                break
            request_limit = min(request_limit, remaining)

        rows, page_context = query_page(
            resource,
            organization_id,
            extra_query=extra_query,
            page=page,
            per_page=request_limit,
            timeout=timeout,
        )
        records.extend(rows)
        if max_records is not None and len(records) >= max_records:
            break

        has_more = page_context.get("has_more_page")
        if has_more is None:
            has_more = page_context.get("hasMorePage")
        if has_more is False or len(rows) < request_limit or not rows:
            break
        page += 1

    if max_records is not None:
        records = records[:max_records]
    return records


def display_value(value):
    if value in (None, ""):
        return "-"
    if isinstance(value, dict):
        return str(value.get("name") or value.get("value") or value)
    if isinstance(value, list):
        return ", ".join(display_value(item) for item in value)
    return str(value)


def print_table(resource, rows):
    if not rows:
        print(f"No {resource} found.")
        return

    columns = RESOURCES[resource]["columns"]
    table = [
        [display_value(row.get(field)) for field, _label in columns]
        for row in rows
    ]
    headers = [label for _field, label in columns]
    widths = []
    for index, header in enumerate(headers):
        value_width = max(len(row[index]) for row in table)
        widths.append(min(max(len(header), value_width), 40))

    def crop(value, width):
        return value if len(value) <= width else value[: max(0, width - 3)] + "..."

    print(" | ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    print("-+-".join("-" * width for width in widths))
    for row in table:
        print(
            " | ".join(
                crop(value, widths[index]).ljust(widths[index])
                for index, value in enumerate(row)
            )
        )
    print(f"\n{len(rows)} {resource}")


def main(argv=None):
    args = build_parser().parse_args(argv)
    ENDPOINT.configure(args)
    extra_query = dict(args.query)

    try:
        organization_id = ENDPOINT.organization_id()
        rows = query_all(
            args.resource,
            organization_id,
            extra_query=extra_query,
            per_page=args.page_size,
            max_records=args.limit,
            timeout=args.timeout,
        )
    except (EndpointResolutionError, McporterError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        print_table(args.resource, rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
