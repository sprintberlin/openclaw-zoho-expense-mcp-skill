# Recommended Zoho Expense MCP Action Profiles

Zoho Expense exposes 184 MCP Actions. Do not enable the entire catalog for a normal agent. Use the recommended **Expense Auditor & Submitter** profile for day-to-day expense capture, report assembly, and status checking.

Names below match the Zoho MCP setup UI and the complete catalog in `ZOHO_EXPENSE_MCP_ACTIONS.md`. Runtime tools usually appear with the `ZohoExpense_` prefix and underscores instead of spaces, for example `ZohoExpense_list_expenses`.

## Profile overview

1. **Expense Auditor & Submitter**: recommended operational profile. Covers receipt capture, expenses, report creation, approval status, category and policy inspection, and read-back verification. No bulk mutations, permanent deletions, or administrative configurations.
2. **Expense Approver / Finance**: for managers and finance users recording reimbursements or reviewing approval queues.
3. **Expense Administrator**: no blanket profile. Configure approval workflows, custom fields, and organization policies individually.

---

## Profile 1: Expense Auditor & Submitter (Recommended)

Select the following Actions in the Zoho MCP setup UI:

### Organizations, Users, Currencies & Taxes

```text
list organizations
get organization
list users
get user
list currencies
get currency
list taxes
get tax
```

### Expenses

```text
list expenses
get expense
create expense
update expense
split expense
add expense comment
list expense comments
add expense documents
mark document as primary
list expense duplicates
skip duplicate expense
create upload receipts
```

### Expense Reports

```text
list expense reports
get expense report
create expense report
update expense report
add expense to report
add expenses to expense report
remove expenses from expense report
add comment to expense report
validate expense report
submit expense report
approval history expense report
get expense report attachment
get expense report receipt
upload expense report attachment
```

### Categories, Customers, Projects & Tags

```text
list expense categories
get expense category
list customers
get customer
list projects
get project
get tags
all tag options
associate expense tags
associate tags to expense report
```

### Analytics & Summary Reads

```text
get expense list analytics
get unreported expense list analytics
get expenses by category analytics
get expenses by merchant analytics
get expenses by user analytics
get expenses by project analytics
get report list analytics
get policy violation details analytics
get expense report budget summary
get expense report reimbursement
```

---

## Profile 2: Expense Approver / Finance (Additions)

Add these Actions only for authorized finance or manager roles:

```text
approve expense report
reject expense report
forward approval expense report
takeback expense report
list advance payments
get advance payment
create advance payment
approve advance payment
reject advance payment
reimburse expense report
get reimbursement details analytics
get pending reimbursement by user analytics
get employee liability summary analytics
```

---

## Safeguards

- Never enable `delete expense`, `delete expense report`, `bulk delete expense reports`, or other destructive delete Actions in standard agent profiles.
- Keep approval (`approve expense report`) and reimbursement (`reimburse expense report`) Actions disabled unless the agent has an explicit, authorized mandate to execute approvals or payouts.
- Submissions (`submit expense report`) and reimbursements trigger downstream financial workflows; always verify records back before triggering them.
