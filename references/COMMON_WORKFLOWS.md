# Common Zoho Expense workflows

Use these procedures after the live MCP server and organization are confirmed. Names below are setup Action names. Runtime tools use `ZohoExpense_` and underscores.

## Capture an expense from a receipt

1. Call `create upload receipts` or `add expense documents` with the receipt file.
2. Read the created or matched expense with `get expense`.
3. If the amount, currency, date, merchant, or category is wrong, update only those fields with `update expense`.
4. Read the expense back and compare amount, currency, date, category, and merchant before continuing.

## Build and validate a report

1. List unreported expenses with `list expenses` or `get unreported expense list analytics`.
2. Create the report with `create expense report`, or attach existing expenses with `add expenses to expense report`.
3. Call `validate expense report` before any submit.
4. Read `get expense report` and confirm report number, dates, totals, and attached expense IDs.

Do not call `submit expense report` unless the task explicitly asks to submit and the validation result has no blocking violations.

## Check approval and reimbursement state

1. Read `get expense report` for status, approver, and totals.
2. Read `approval history expense report` when the question is about who approved or rejected it.
3. Read `get expense report reimbursement` or `get pending reimbursement by user analytics` for payout state.

Recording a reimbursement with `reimburse expense report` changes paid state. Require an explicit task and read the report back afterwards.
