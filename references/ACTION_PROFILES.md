# Zoho Expense MCP Action Profiles & Task Recipes

The machine-readable source of truth is [`references/profiles.json`](profiles.json), validated against [`references/actions.jsonl`](actions.jsonl). Use `scripts/lookup_actions.py` for copy-ready lists.

## The 300-Action Server Limit

A Zoho MCP server accepts at most 300 selected Actions per connection. Zoho Expense currently exposes 184 Actions, so every profile fits on one server. Use the smallest matching profile anyway so the session tool catalog and permissions stay narrow.

| Profile | Resolved Actions | Fits one MCP server |
|---|---:|---|
| `expense-viewer` | 72 | yes |
| `expense-submitter` (inherits `expense-viewer`) | 104 | yes |
| `expense-approver` (inherits `expense-submitter`) | 121 | yes |
| `expense-admin` (inherits `expense-approver`) | 163 | yes |

## Role Profiles

```bash
python3 scripts/lookup_actions.py --profiles
python3 scripts/lookup_actions.py --profile expense-viewer --names-only
python3 scripts/lookup_actions.py --profile expense-submitter --names-only
python3 scripts/lookup_actions.py --profile expense-approver --names-only
python3 scripts/lookup_actions.py --profile expense-admin --names-only
```

### 1. Expense Viewer & Auditor (`expense-viewer`) - 72 Actions

Read-only inspection of expenses, reports, receipts, advances, trips, categories, projects, users, taxes, approval history, reimbursement state, policy violations, and analytics. No create, update, approval, reimbursement, or delete Actions.

### 2. Expense Submitter & Drafter (`expense-submitter`) - 104 Actions resolved

Inherits `expense-viewer` and adds receipt capture, expense creation and updates, report assembly and validation, comments, tags, attachments, advance requests, trips, and report submission. It cannot approve, reject, reimburse, or delete records.

### 3. Expense Approver & Finance (`expense-approver`) - 121 Actions resolved

Inherits `expense-submitter` and adds approval, rejection, forwarding, reimbursement, advance decisions, and related finance transitions. Permanent deletion stays excluded.

### 4. Expense Administrator (`expense-admin`) - 163 Actions resolved

Inherits `expense-approver` and adds configuration for users, projects, customers, currencies, taxes, categories, tags, organization settings, archiving, and non-destructive bulk updates. Destructive delete Actions and bulk delete remain excluded.

## Task Recipes

```bash
python3 scripts/lookup_actions.py --tasks
python3 scripts/lookup_actions.py --task receipt-capture --names-only
python3 scripts/lookup_actions.py --task build-expense-report --names-only
python3 scripts/lookup_actions.py --task submit-and-track-report --names-only
python3 scripts/lookup_actions.py --task reimbursement-settlement --names-only
```

- `receipt-capture`: upload or scan a receipt, create or correct an expense, inspect duplicates, and verify details
- `build-expense-report`: find unreported expenses, create or update a report, attach expenses, validate it, and read it back
- `submit-and-track-report`: validate and submit a report, inspect approval history, add a comment, or recall it
- `reimbursement-settlement`: inspect reimbursement and advance state, record an authorized reimbursement, and verify liabilities

## Safeguards

- Do not add `delete expense`, `delete expense report`, `bulk delete expense reports`, or other destructive delete Actions to normal profiles.
- Keep approval and reimbursement Actions out of `expense-submitter`; they require the explicitly authorized `expense-approver` role.
- Submissions and reimbursements trigger downstream financial workflows. Validate and read the resulting state back.
- The catalog describes potentially available Actions. Confirm the selected Actions on the live MCP server with `mcporter list`.
