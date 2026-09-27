# Zoho Expense MCP

Connect your agent to Zoho Expense through the Model Context Protocol (MCP). This skill provides everything needed to select an organization, inspect expenses and reports, and perform controlled Expense operations using `mcporter`.

This repository contains the public source for the ClawHub skill `@sprintcx/zoho-expense-mcp`.

## What This Skill Includes

- Agent Skill instructions in `SKILL.md`
- Recommended least-privilege Action profiles
- Complete catalog of 184 known Zoho Expense MCP Actions
- Direct GitHub issue and pull request contribution workflow for humans and agents
- ClawHub release card metadata in `skill-card.md`
- Ready-to-use Python helpers for organizations, expenses, reports, advances, projects, and users
- Multi-account profile support for single-org and multi-tenant setups
- Security-conscious `mcporter` calls without shell expansion

## Requirements

| Requirement | Details |
|---|---|
| Zoho Expense MCP Server | A configured endpoint from [mcp.zoho.eu](https://mcp.zoho.eu) |
| mcporter | MCP client CLI, bundled with OpenClaw; elsewhere `npm i -g mcporter` |
| Endpoint selection | `ZOHO_EXPENSE_MCP_URL` for one account; named profiles or `--mcp-url` for multiple accounts |
| Organization ID | `ZOHO_EXPENSE_ORGANIZATION_ID` or profile `organization_id` for scoped calls |

### Single-account setup

```bash
export ZOHO_EXPENSE_MCP_URL="https://your-org-zoho-expense-xxxxx.zohomcp.eu/mcp/YOUR_TOKEN/message"
export ZOHO_EXPENSE_ORGANIZATION_ID="123456789"
```

To verify without printing credentials:

```bash
if [ -n "$ZOHO_EXPENSE_MCP_URL" ]; then echo "ZOHO_EXPENSE_MCP_URL is set"; else echo "ZOHO_EXPENSE_MCP_URL is not set"; fi
```

### Multiple organizations and customer accounts

Use one shared profile file instead of changing global environment variables:

```json
{
  "version": 1,
  "profiles": {
    "acme": {
      "services": {
        "expense": {
          "env": "ACME_EXPENSE_MCP_URL",
          "organization_id": "123456789"
        }
      }
    }
  }
}
```

```bash
python3 scripts/list_records.py expenses --profile acme
```

The default file is `~/.config/zoho-mcp/profiles.json`. Full format: [`references/MULTI_ACCOUNT.md`](references/MULTI_ACCOUNT.md).

## Quick Start

```bash
# List available tools on the configured MCP server
mcporter list "$ZOHO_EXPENSE_MCP_URL"

# List organizations
python3 scripts/list_organizations.py

# List expenses
python3 scripts/list_records.py expenses --limit 20
```

## Python Scripts

- `scripts/list_organizations.py`: List accessible Zoho Expense organizations.
- `scripts/list_records.py`: Query expenses, reports, advances, projects, or users.
- `scripts/mcp_endpoint.py`: Shared endpoint, profile, and organization resolver.
- `scripts/mcp_client.py`: Shell-free `mcporter` client wrapper.

## Repository Files

- `CONTRIBUTING.md`: Direct GitHub issue and pull request workflow.
- `SKILL.md`: Agent Skill instructions.
- `references/ACTION_PROFILES.md`: Least-privilege Expense Action profiles.
- `references/COMMON_WORKFLOWS.md`: Frequent Expense workflows.
- `references/ZOHO_EXPENSE_MCP_ACTIONS.md`: Complete catalog of 184 known Actions.
- `references/MULTI_ACCOUNT.md`: Portable endpoint profiles.
- `tests/`: Credential-free helper and resolver tests.

## Security Notes

The bundled scripts call `mcporter` directly through `subprocess.run([...])` without shell expansion. Expense records, employee data, and receipts are sensitive. Load only required records and never copy their contents into chats, logs, or repositories.

## Contributing

Bug reports, documentation corrections, missing profile Actions, and pull requests are welcome. Agents using this skill must file or link reproducible skill defects as part of completing the task. Use the normal GitHub CLI workflow described in [`CONTRIBUTING.md`](CONTRIBUTING.md); never include MCP URLs, tokens, customer identifiers, personal data, receipts, or expense records.

## Publish

```bash
clawhub skill publish . \
  --slug zoho-expense-mcp \
  --name "Zoho Expense MCP" \
  --owner sprintcx \
  --version 1.0.0 \
  --source-repo sprintberlin/openclaw-zoho-expense-mcp-skill \
  --source-ref main \
  --source-path . \
  --changelog "Initial public Expense MCP skill with portable account profiles"
```
