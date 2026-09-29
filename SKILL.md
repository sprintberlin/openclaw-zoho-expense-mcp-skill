---
name: "zoho-expense-mcp"
description: "Zoho Expense MCP endpoint setup, multi-account routing, organization selection, action profiles, helper CLIs, and safe expense and reimbursement workflows."
---

# Zoho Expense MCP

Use Zoho Expense through an MCP endpoint from `mcp.zoho.eu`. This skill is the canonical home for Expense-specific action documentation, least-privilege profiles, portable account routing, and helper CLIs.

Source: [sprintberlin/openclaw-zoho-expense-mcp-skill](https://github.com/sprintberlin/openclaw-zoho-expense-mcp-skill)

## Requirements

- A Zoho Expense MCP endpoint from `mcp.zoho.eu`
- `mcporter`
- Endpoint configuration via `ZOHO_EXPENSE_MCP_URL`, `--profile`, or `--mcp-url`
- A Zoho Expense organization ID for organization-scoped calls

Treat the endpoint as a credential. Never print it, commit it, or copy it into tickets, prompts, or chats.

## First setup

1. Create or open a Zoho Expense connection at `mcp.zoho.eu`.
2. Select only required Actions. Resolve the exact list from the JSON catalog:

```bash
python3 scripts/lookup_actions.py --profiles
python3 scripts/lookup_actions.py --profile expense-viewer --names-only
python3 scripts/lookup_actions.py --profile expense-submitter --names-only
python3 scripts/lookup_actions.py --profile expense-approver --names-only
python3 scripts/lookup_actions.py --profile expense-admin --names-only
python3 scripts/lookup_actions.py --task build-expense-report --names-only
```

3. Search the catalog when a profile or task lacks a required Action:

```bash
python3 scripts/lookup_actions.py --search "receipt"
python3 scripts/lookup_actions.py --action create_expense_report
```

4. Configure one endpoint with `ZOHO_EXPENSE_MCP_URL`, or named accounts using [references/MULTI_ACCOUNT.md](references/MULTI_ACCOUNT.md).
5. Configure the organization ID with `ZOHO_EXPENSE_ORGANIZATION_ID` or the selected profile's `organization_id`.
6. Inspect the selected live server with `mcporter list "$ZOHO_EXPENSE_MCP_URL"`; finish only after the required Actions are present.

The catalog describes possible Actions, not what one MCP server has enabled. Runtime names normally use `ZohoExpense_` plus the setup Action name with spaces converted to underscores, for example `ZohoExpense_list_expenses`.

## Endpoint and organization selection

For one account, set `ZOHO_EXPENSE_MCP_URL` and `ZOHO_EXPENSE_ORGANIZATION_ID`. For multiple accounts, pass `--profile NAME` to a bundled helper. Profiles default to `~/.config/zoho-mcp/profiles.json` and can reference an environment variable, a local URL file, or a direct URL.

Endpoint resolution order:

1. `--mcp-url`
2. `--profile`, `ZOHO_EXPENSE_MCP_PROFILE`, or `ZOHO_MCP_PROFILE`
3. `ZOHO_EXPENSE_MCP_URL`

Organization resolution order:

1. `--organization-id`
2. selected profile's `organization_id`
3. `ZOHO_EXPENSE_ORGANIZATION_ID`
4. `ZOHO_ORGANIZATION_ID`

One-off `--mcp-url` can expose the credential in shell history or process listings. Prefer a profile backed by an injected environment variable or `url_file`.

## Safe workflow

1. Resolve the exact account and organization before reading data. Never reuse an endpoint or organization ID from another customer.
2. Inspect the live Actions and the selected Action schema before the first call.
3. Read the target expense, receipt, report, advance, trip, user, or setting before changing it.
4. Use the organization ID returned by `list organizations`; never infer it from names or transfer one between profiles.
5. Send only intended fields, then read the affected record back and compare IDs, amount, currency, date, category, merchant, status, submitter, and approver.
6. Keep delete, bulk mutation, submit, approve, reject, reimbursement, workflow, and administrative Actions disabled unless the task explicitly requires them.
7. Treat report submission, approval, reimbursement, comments that notify users, and report sharing as external actions requiring the active approval policy.

## Bundled helpers

List organizations without requiring an organization ID:

```bash
python3 scripts/list_organizations.py --profile acme
```

List organization-scoped records:

```bash
python3 scripts/list_records.py expenses --profile acme --limit 20
python3 scripts/list_records.py reports --profile acme --query filter_by=Status.Unreported --json
python3 scripts/list_records.py advances --profile acme --json
```

Supported resources are `expenses`, `reports`, `advances`, `projects`, and `users`. `--query KEY=VALUE` can be repeated and must match the live Action schema. Pagination is automatic.

All helpers accept `--mcp-url`, `--profile`, `--profiles-file`, and `--timeout`. Organization-scoped helpers also accept `--organization-id`. Run `--help` without credentials. Unknown or incomplete options exit with status 2.

## Direct mcporter calls

Zoho Expense live schemas may represent the organization scope as the `X-ORG-ID` header instead of an `organization_id` query parameter. Inspect the live Action schema and follow it exactly. A common call shape is:

```bash
cat > /tmp/expense_records.json <<'JSON'
{
  "headers": {
    "X-ORG-ID": "<ORGANIZATION_ID>"
  }
}
JSON
mcporter call "$ZOHO_EXPENSE_MCP_URL.ZohoExpense_list_expenses" --args "$(< /tmp/expense_records.json)"
```

Use the schema shown by the live MCP server when it differs. Write nested arguments to a temporary JSON file instead of fragile shell quoting.

## Expense safeguards

- Confirm amount, currency, date, category, merchant, employee, payment mode, tax, project, customer, and receipt before creating or updating an expense.
- Search duplicates before creating an expense, then verify the created record.
- Never fabricate expense IDs, report IDs, organization IDs, user IDs, category IDs, tax IDs, project IDs, account IDs, or approver IDs.
- Submitting, approving, rejecting, or reimbursing a report changes financial and workflow state. Require an explicit task and verify the resulting state.
- Delete and bulk-delete Actions are destructive. Keep them out of normal profiles unless the task explicitly requires a correction.
- Receipt and attachment Actions transfer sensitive binary data. Verify the transferred file by reading it back; use a confirmed REST upload workflow when MCP does not support the binary operation.

## Report skill defects and contribute

Contributions are explicitly welcome from humans and agents. An Expense task is complete only after serving the user and filing or linking every reproducible skill defect found.

- **Issue**: For schema mismatches, broken helpers or workflows, incorrect parameters, or missing profile Actions. File via GitHub CLI: `gh issue create --repo sprintberlin/openclaw-zoho-expense-mcp-skill --title "bug: ..." --body "..."`.
- **Pull request**: Preferred when you can fix and verify the defect. Follow the standard branch, test, and PR workflow.
- See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules and `gh` workflows.

Do not file skill issues for endpoint/auth/profile setup, rate limits, transient service failures, timeouts, organization-specific custom fields, or unsupported Expense operations. Never include MCP URLs, tokens, record content, employee data, receipts, or customer data.

## References

- [Action catalog](references/actions.jsonl): 184 Zoho Expense Actions in machine-readable JSONL
- [Profiles and task recipes](references/profiles.json): least-privilege profiles and task recipes
- [Catalog format](references/CATALOG_FORMAT.md): architecture and CLI query documentation
- [Action profiles overview](references/ACTION_PROFILES.md): human-readable role and recipe reference
- [Common workflows](references/COMMON_WORKFLOWS.md): ordered procedures for frequent Expense tasks
- [Multi-account profiles](references/MULTI_ACCOUNT.md): portable routing for CRM, People, Books, and Expense
- [Contributing guide](CONTRIBUTING.md): issue and pull request workflows for humans and agents

Query the catalog with `scripts/lookup_actions.py` instead of loading `actions.jsonl` into context.

## Troubleshooting

- **No endpoint configured**: set `ZOHO_EXPENSE_MCP_URL`, select `--profile`, or pass `--mcp-url`; never print the value.
- **No organization ID configured**: use `--organization-id`, profile `organization_id`, or `ZOHO_EXPENSE_ORGANIZATION_ID`.
- **Profile not found or wrong app**: verify `--profiles-file`, profile name, and `services.expense`.
- **Action missing**: inspect the live server; enabling an Action in documentation does not enable it remotely.
- **OAuth scope error**: reconnect the affected Expense connection. Never switch to another customer's endpoint.
- **Organization scope error**: inspect whether the Action expects `headers.X-ORG-ID` or `query_params.organization_id` and use the live schema.
- **Unexpected amount or status**: stop, read the saved record, and compare organization currency, policy rules, report state, and approval history before another write.
