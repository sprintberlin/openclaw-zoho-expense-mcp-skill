# Common Zoho Expense workflows

## Preconditions

1. Resolve the exact endpoint, profile, and organization.
2. Run `mcporter list` against the selected endpoint.
3. Inspect the live Action schema.
4. Use `headers.X-ORG-ID` when required by the live schema.
5. Read every changed record back.

## Capture an expense from a receipt

1. Search existing expenses and duplicates.
2. Use `create upload receipts` for receipt autoscanning or `add expense documents` for an existing expense.
3. Read the created or matched expense with `get expense`.
4. Correct only verified fields with `update expense`.
5. Verify amount, currency, date, merchant, category, tax, payment mode, and receipt.

## Build a travel expense report

1. List candidate expenses with `list expenses` or `get unreported expense list analytics`.
2. Filter by status, date range, merchant, customer, or project.
3. Exclude placeholder amounts, missing-amount markers, duplicates, and expenses already assigned to another report.
4. Confirm report name, purpose, start date, end date, and expense order.
5. Create an argument file:

```json
{
  "headers": {
    "X-ORG-ID": "<ORGANIZATION_ID>"
  },
  "body": {
    "report_name": "Travel Expenses London 2026-06",
    "description": "Client meeting Acme Corp",
    "start_date": "2026-06-20",
    "end_date": "2026-06-24",
    "expenses": [
      {"expense_id": "<EXPENSE_ID_1>", "order": 1},
      {"expense_id": "<EXPENSE_ID_2>", "order": 2}
    ]
  }
}
```

6. Match field names to the live schema:
   - Report text: `description` or `purpose`.
   - Expenses: `expenses` as an array of objects.
   - Legacy expenses: `expense_ids` as an array of strings.
   - Never use a comma-separated string.
7. Call `ZohoExpense_create_expense_report`.
8. Read `report_id`, `report_number`, and `status` from the response.
9. Call `ZohoExpense_validate_expense_report`.
10. Read the report with `ZohoExpense_get_expense_report`.
11. Verify dates, expense IDs, expense count, totals, converted totals, and `draft` status.

Mixed expense currencies are valid. Verify organization-currency conversion and exchange rates in the read-back.

## Add expenses to an existing report

1. Read the target report.
2. Require `draft` or `recalled` status.
3. Verify every expense is unreported and belongs to the same organization.
4. Call `add expenses to expense report` with an array matching the live schema.
5. Read the report back and verify the attached expense IDs and totals.

## Submit a report

1. Require an explicit submission instruction.
2. Read and validate the report.
3. Require `draft` or `recalled` status, at least one expense, no blocking violation, and the required approver selection.
4. Create an argument file:

```json
{
  "headers": {
    "X-ORG-ID": "<ORGANIZATION_ID>"
  },
  "path_variables": {
    "report_id": "<REPORT_ID>"
  }
}
```

5. Add approver and CC fields exactly as required by the live schema.
6. Call `ZohoExpense_submit_expense_report`.
7. Read the report back and verify `submitted` status, approver, totals, and attached expense IDs.

## Approval and reimbursement

1. Require explicit authority for `approve expense report`, `reject expense report`, `forward approval expense report`, or `reimburse expense report`.
2. Read the report, approval history, and reimbursement state.
3. Execute one authorized transition.
4. Read the report and reimbursement state back.
5. Verify status, actor, amount, currency, and timestamp.

## Lifecycle

```text
expense: unreported -> report: draft -> submitted -> approved -> reimbursed
                         recalled <----+
```
