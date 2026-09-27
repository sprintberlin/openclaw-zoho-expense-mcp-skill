# Zoho Expense MCP Actions

Complete native Zoho Expense MCP action catalog. Snapshot: 17.08.2026.

**Action count:** 184

| Action | Description |
| :--- | :--- |
| activate project | Mark a project as active. |
| activate user | Make an user active. |
| active tag | Mark a reporting tag as active so that you can use it on entities which you allowed. A newly created tag will be in draft state. Use this to mark that tag as ready. |
| active tag option | Mark a reporting tag's option as active. |
| add advance payment attachment | Upload attachments and link them to an advance payment. Allowed file extensions: gif, png, jpeg, jpg, bmp, webp, pdf, xls, xlsx, doc, docx, xml, csv, txt, tif, tiff, msg, eml, dwg, ai, eps, ppt, pptx, odt, ods, odf, rtf, json, zip, rar, 7z, key, numbers, pages, dst, asice. Max size 10240 KB. Max 20 files. |
| add advance payment comment | Add a comment to an advance payment. |
| add comment to expense report | Add a comment to a report, optionally tying the comment to a specific expense line. |
| add expense comment | To add a comment to an expense, pass the organization ID, specify the expense, and include the comment text in the request body. |
| add expense documents | To attach documents to an expense, pass the organization ID and specify the expense. Upload the document files (PDF, JPG, or PNG) in the request body. You can optionally flag one document as the primary document at the time of upload. |
| add expense to report | Attach a single expense to a report. Useful when the caller is operating in the context of an expense rather than a report. |
| add expenses to expense report | Attach one or more existing expenses to a report. |
| all tag options | Get all options for a reporting tag. |
| approval history expense report | Retrieve the complete approval audit trail for a specific report by providing the report ID and the organization ID. The response returns a chronological list of all approval actions taken on the report, including each entry's status transition (previous status to new status), the approver's name and email, any comments left during approval or rejection, and the date and time of each action. |
| approve advance payment | Approve a submitted advance payment. |
| approve expense report | Approve a submitted report by providing the report ID and the organization ID. The report must currently be in "submitted" status, and the user must be an authorized approver in the report's approval workflow. Upon success, the report's status transitions to "approved" and the submitter is notified. |
| approve trip | Approve a submitted trip request. |
| archive expense report | Archive a report. |
| assign role to user | Assign a role to user. |
| associate expense tags | To link tags to an expense, pass the organization ID, specify the expense, and provide an array of tag identifiers in the request body. Tags must already exist in your organization. Use the Tags API to create them before associating. |
| associate tags to expense report | Associate or update tags on a report. |
| autocomplete departments | Returns a paginated list of departments whose name contains `search_text`. Use each item's `id` as the `department_id` when creating or filtering other Zoho Expense resources. OAuth scope: `ZohoExpense.expense.READ`. |
| bulk add expenses | To create multiple expenses in a single request, pass the organization ID and provide an array of expense objects in the request body. Each object must include the amount, currency, date, and category. Additional expense-level fields can be included per object as needed. |
| bulk approve expense reports | Approve multiple submitted reports at once by providing the organization ID and an array of report IDs. All selected reports must currently be in "submitted" status, and the authenticated user must be an authorized approver for each of them. Upon success, all specified reports transition to "approved" status and the respective submitters are notified. |
| bulk archive expense reports | Archive multiple reports in a single request by providing the organization ID and an array of report IDs. Archiving moves completed or older reports out of the active view without deleting them, helping users keep their workspace organized. Archived reports can still be accessed and searched but will no longer appear in the default report listing. |
| bulk change status of expense reports | Apply a generic status change action to multiple reports in a single call. |
| bulk delete expense reports | Permanently delete multiple reports in a single request by providing the organization ID and report IDs. The reports must typically be in "draft" or "rejected" status to be eligible for deletion - reports that have been submitted, approved, or reimbursed cannot be deleted. This action is irreversible and removes the reports from the system. The expenses associated with the report will be listed as unreported expenses in the Expenses module, available to be added to a new report. |
| bulk field update expense reports | Apply the same field updates to multiple reports in a single call (mass edit). |
| bulk field update expenses | To update a single field across multiple expenses at once, pass the organization ID and provide an array of expense identifiers, the field name to update, and the new value. |
| bulk forward approval expense reports | Forward the approval of multiple reports to another approver in a single call. |
| bulk reimburse expense reports | Record reimbursements for multiple approved reports at once by providing the organization ID and an array of report IDs. All selected reports must be in "approved" status and the authenticated user must have reimbursement permissions within the organization. Use the via_online flag to choose the mode. For an offline reimbursement (via_online=false), account_id - the paid-through account from which the amount is paid - is mandatory, while reimbursed_date and reference_number are optional. For an online reimbursement (via_online=true), a payment gateway must be configured for the organization and account_id (the source account linked to the gateway) along with a configured employee bank account for each report are mandatory. |
| bulk reject expense reports | Reject multiple submitted reports in a single request by providing the organization ID and an array of report IDs. The user can include a comment explaining the reason for rejection, which will apply to all the selected reports. All reports must be in "submitted" status and the authenticated user must be an authorized approver. Once rejected, the reports are sent back to their respective submitters for revision. |
| bulk reject expenses in report | Reject multiple expense line items within a report in a single call. |
| bulk reset substatus of expense reports | Reset the substatus field for multiple reports in a single call. |
| bulk submit expense reports | Submit multiple reports for approval in a single request by providing the organization ID and an array of report IDs. The user must select an approver to whom the reports will be submitted and can specify email addresses of recipients to be CCed on the submission notification. All selected reports must be in "draft" or "recalled" status, should have at least one expense attached, and all mandatory fields must be complete before submission can succeed. |
| bulk unarchive expense reports | Restore multiple previously archived reports back to the active list by providing the organization ID and an array of report IDs. Once unarchived, the reports will reappear in the default report listing and resume their previous status. This action is useful when an archived report needs further action or review. |
| cancel reimbursement of expense report | Cancel a previously recorded reimbursement on a report. |
| cancel trip | Cancel a trip. |
| change status of expense report | Apply a generic status change action to a report. |
| close trip | Close an approved trip. |
| create advance payment | Create a new advance payment for an employee. The `currency_id`, `amount`, `date`, and `user_id` fields are required. |
| create currency | Create a currency. |
| create customer | Create a new customer. |
| create expense | To create a new expense, pass the organization ID. Provide the amount, currency, date, and expense category as required fields. You can also include optional details such as merchant name, description, payment mode, project, cost center, tags, and custom fields. |
| create expense category | Create a new expense category. |
| create expense report | Create a new report in your organization by providing the report name, start date, end date, and organization ID - all of which are mandatory. Optionally, you can include a description of the report's purpose, attach existing expenses by passing their expense IDs, associate the report with a customer or project, add custom field values, and apply tags for categorization. The expenses array accepts objects containing the expense_id and an order value to control sequencing within the report. |
| create organization | Create an organization. |
| create project | Create a new project. |
| create tag | Create a reporting tag |
| create tax | Create a tax. |
| create trip | Create a new trip. |
| create upload receipts | Upload receipts for autoscanning. |
| create user | Create a new user. |
| deactivate project | Mark a project as inactive. |
| deactivate user | Make an user inactive. |
| delete advance payment | Delete an existing advance payment. |
| delete advance payment attachment | Remove a file attached to an advance payment. |
| delete advance payment comment | Delete an existing comment on an advance payment. |
| delete comment of expense report | Delete a comment from a report. |
| delete currency | Delete an existing currency. |
| delete customer | Delete an existing customer. |
| delete expense | To delete a single expense, pass the organization ID and specify the expense in the request URL. You cannot delete expenses in the Submitted, Approved, and Reimbursed statuses. |
| delete expense category | Delete an existing expense category. |
| delete expense comment | To delete a comment, pass the organization ID and specify both the expense and the comment. Users can only delete comments they authored. |
| delete expense document | To remove a document from an expense, pass the organization ID and specify both the expense and the document. |
| delete expense report | Permanently delete a report by providing the organization ID and report ID. The report must typically be in "draft" or "rejected" status to be eligible for deletion - reports that have been submitted, approved, or reimbursed cannot be deleted. This action is irreversible and removes the report from the system. The expenses associated with the report will be listed as unreported expenses in the Expenses module, available to be added to a new report. |
| delete expense report attachment | Delete a specific attachment from a report. Set `unassociate=true` to detach the file from the report without deleting it. |
| delete multiple expenses | To delete multiple expenses at once, pass the organization ID and provide an array of expense identifiers in the request body. You cannot delete expenses in the Submitted, Approved, and Reimbursed statuses. |
| delete project | Delete an existing project. |
| delete tag | Delete a reporting tag. If there are any usages of the reporting tag in transactions, custom views or workflows, you will not be able to delete the tag. |
| delete tax | Delete an existing tax. |
| delete trip | Delete a trip request. Approved, Closed and Cancelled trips cannot be deleted. |
| delete user | Delete an existing user. |
| disable expense category | Disable an expense category. |
| enable expense category | Enable an expense category. |
| export expense report | Trigger an asynchronous export of a report. |
| forward approval expense report | Forward the approval of a report to another approver. |
| get ach reimbursements analytics | Use this report to review reimbursements paid to employees through ACH (direct bank transfer) over a period. This report is available only for organisations with Zoho Forte (online reimbursement) enabled - applicable to US (USD) and Canada (CAD) organisations on paid plans. |
| get advance by user analytics | Use this report to see how much advance amount has been issued to each employee over a chosen period. For every user, it shows how many advances were paid out and the total amount advanced, so you can compare advance utilisation across employees and departments. |
| get advance details analytics | Use this report to see the individual advance transactions across your organization. Each row represents one advance paid out during the selected period and shows who the advance was issued to, the date it was paid, the expense report it is attached to and some more details. |
| get advance payment | Retrieve the details of an existing advance payment. |
| get advance payment attachment | Download a file attached to an advance payment. |
| get all tag options | Get the options and its criteria details of a reporting tag. For each page, you can retrieve only 200 options. |
| get currency | Details of an existing currency. |
| get customer | Details of an existing customer. |
| get employee liability analytics | Use this report to see the transaction-level statement behind any user's row in the Employee Liability Summary report. For a chosen user, it shows the opening balance at the start of the period, every expense, advance, and reimbursement transaction recorded within the period, and the closing balance at the end. Use it to reconcile a specific employee's account, explain how their current outstanding balance was arrived at, or audit a particular settlement. |
| get employee liability summary analytics | Use this report to see, at a point in time, the outstanding balances between your company and each employee. For every user, it shows how much the employee owes the company (typically from advances or company-paid expenses that are yet to be settled) and how much the company owes the employee (typically from out-of-pocket expenses awaiting reimbursement). Use it to track open dues across your workforce, plan reimbursement cycles, and identify employees with the largest outstanding balances. |
| get expense | To retrieve the full details of a specific expense, pass the organization ID along with the expense identifier in the request URL. |
| get expense category | Details of an existing expense category. |
| get expense list analytics | Run this analytics to get a list of the expenses incurred by all users for a particular period, including other details such as the expense status, category, amount, etc. You can include additional filters to get more information about the expenses and customise the columns displayed in your analytics. When `group_by` is not specified, expense records are returned under the `expenses` key. When `group_by` is specified, the response returns grouped results under `expense_details_list`, where each item contains a nested `expense` array with the expense records for that group along with group-level summary fields. |
| get expense metadata analytics | Retrieve metadata for expense analytics. Returns available entity fields, supported filters, grouping options, and sort options for the specified entity type. Call this before building rule, select_columns, group_by, or date_filter parameters for any analytics endpoint. |
| get expense report | Fetch the complete details of a specific report by providing the report ID and the organization ID. The response includes the full report metadata, all associated line-item expenses with their amounts, categories, merchants, receipts, tax details, and mileage information. It also returns the complete approval chain (current, next, and previous approver), any reimbursements already recorded, advance payments applied against the report, unreported expenses available to add, and the list of users involved in the workflow. |
| get expense report attachment | Download a specific attachment file associated with a report. |
| get expense report budget summary | Retrieve the budget vs. actual summary for a report. |
| get expense report receipt | Download the receipt file associated with a report. |
| get expense report reimbursement | Retrieve the reimbursement details associated with a report. |
| get expense tax summary analytics | Use this report to understand your tax outgo on expenses, broken down by individual tax. For each tax used during the selected period, it shows the rate at which the tax was applied, the value of expenses it was applied on, and the resulting tax liability. Use it to track tax-wise spending, prepare tax filings, and identify which taxes account for the largest share of your overall tax burden. |
| get expense tax summary details analytics | For a chosen tax, this report lists every expense to which that tax was applied during the selected period - including each expense's date, reference, category, merchant, value, and the tax charged - so you can verify how a tax total was arrived at, or audit the specific expenses contributing to a tax liability. |
| get expense violations by user analytics | This analytics gives information on the expense policy violations made by the users. The number of expenses violated by each employee and the total of the violated expenses will be displayed in the report. |
| get expenses by attendee analytics | Attendees are the users or contact persons who have incurred expenses along with a user. The list of attendees along with their expense share will be generated in this analytics. Also, you can find the number of expenses for which they were attendees. |
| get expenses by category analytics | View how much your employees have incurred for each expense category over a period. Returns one aggregated summary row per category with total amount, foreign currency amount, and expense count. You can also view this analytics in the form of a chart and get insights with just a glance. |
| get expenses by currency analytics | If you have incurred expenses in multiple currencies, you can run this analytics to get currency-wise records in the form of a chart. The total amount spent under each currency and its exchange value in the base currency of the organisation will also be shown in the analytics. |
| get expenses by customer analytics | Get to know about the expenses incurred for individual customers. The number of expenses incurred for each customer and the total amount spent for each customer will be displayed in the chart. |
| get expenses by department analytics | Run this report to know the number of expenses incurred under every department. The total amount of expenses incurred by various departments will also be displayed in the form of a chart. |
| get expenses by merchant analytics | Run this report to know merchant-wise expenses within a specified period. The number of expenses incurred with individual merchants and the total of the expenses incurred will be shown in a chart. |
| get expenses by mileage analytics | To know user-wise records of the mileage expenses incurred in your organisation, you can generate this analytics. The distance travelled and the number of expenses incurred by each user will be listed. You can also view this analytics in the form of a chart. |
| get expenses by project analytics | This analytics generates information about the expenses incurred for all the ongoing and completed projects over a specified period in a chart. |
| get expenses by user analytics | View the number of expenses incurred and the amount spent by each employee during a given period. Also, identify the user who has incurred the most expenses quickly from the chart. |
| get organization | Get the details of an organization. |
| get pending reimbursement by user analytics | Lists the approved expense reports that are still awaiting reimbursement for one employee. |
| get policy violation details analytics | List the individual expense policy violations recorded across reports over a period, showing each violating expense and the report it belongs to. |
| get project | Details of an existing project. |
| get reimbursement analytics metadata | Retrieve metadata for reimbursement analytics. Returns available entity fields, supported filters, grouping options, and sort options for the specified entity type. Call this before building rule, select_columns, group_by, or date_filter parameters. |
| get reimbursement by user analytics | Use this report to see how much your company has reimbursed each employee over a chosen period. For every user, it shows how many reimbursements were paid out and the total amount reimbursed, so you can compare reimbursement spend across employees. |
| get reimbursement details analytics | Use this report to see the full list of reimbursements paid out to employees over a chosen period. Each row represents one reimbursement and shows the expense report it covered, who approved or paid it, the date it was paid, the payment method, and some other details. |
| get report list analytics | Lists submitted expense reports for a period. Supports filters and grouping. When `group_by` is not specified, expense report records are returned under the `expense_reports` key. When `group_by` is specified, the response returns grouped results under `expense_report_details_list`, where each item contains a nested `expense` array with the expense report records for that group along with group-level summary fields. |
| get reports metadata analytics | Retrieve metadata for expense report analytics. Returns available entity fields, supported filters, grouping options, and sort options. Call this before building rule, select_columns, group_by, or date_filter parameters. |
| get tags | Get a list of all reporting tags in the preferred order that you can set. |
| get tax | Details of an existing tax. |
| get tax group | Details of an existing tax group. |
| get time to approve analytics | Run this analytic report to see how long approvals are taking across expense reports, bucketed into time intervals, so you can spot delays. |
| get time to book analytics | Use this report to understand how long it is taking to book travel for trips, so you can track booking turnaround. |
| get trip | Retrieve details of an existing trip. |
| get trip analytics metadata | Retrieve metadata for trip analytics. Returns available entity fields, supported filters, grouping options, and sort options for the specified entity type. Call this before building rule, select_columns, group_by, or date_filter parameters. |
| get trip list analytics | Retrieve a list of trips with various filtering and grouping options. Use this for any request about trip records, trip details, trips in a period, or trip-wise information. When `group_by` is not specified, trip records are returned under the `trips` key. When `group_by` is specified, the response returns grouped results under `trip_details_list`, where each item contains a nested `trip` array with the trip records for that group along with group-level summary fields. |
| get trip option details analytics | Use this report to see the individual trips behind your trip booking turnaround summary. For each trip, it shows the route, the trip start date, and how long it took at each stage of the booking workflow. Use it to drill into trips that fall within a specific travel mode (for example, all flights booked within 12 hours) to investigate why those particular trips were faster or slower than expected. |
| get trip options time summary analytics | Use this report to measure how quickly trip requests are being processed by the travel desk. For each travel mode (flight, hotel, car, train, and so on), the report breaks the booking workflow into three stages and shows how long each stage typically takes and how those timings are spread across short and long turnaround windows. |
| get trip spend summary analytics | Use this report to review how much was spent on each trip over a period, across categories such as per diem allowance, tickets, hotel, and other trip expenses. |
| get trip summary analytics | Use this report to see a summary of trips over a period, grouped by trip completion status, so you can see how trips are progressing. |
| get trip summary by reports analytics | Use this report to see a summary of trips over a period, grouped by expense report status, so you can see how trips are progressing. |
| get unreported expense list analytics | Run this analytics when the user asks for unreported, unsubmitted, or draft expenses - i.e. expenses that have not been added to any expense report yet or have not been submitted for approval. Retrieve a detailed analytics report of such expenses with various filtering and grouping options. When `group_by` is not specified, expense records are returned under the `expenses` key. When `group_by` is specified, the response returns grouped results under `expense_details_list`, where each item contains a nested `expense` array with the expense records for that group along with group-level summary fields. |
| get user | Details of an existing user. |
| get violations by expense report analytics | Lists expense reports that contain policy violations. Returns one row per report with report details and how many violations occurred on that report. |
| inactive tag | Mark a reporting tag as inactive. |
| inactive tag option | Mark a reporting tag's option as inactive. |
| list advance payments | List all advance payments for the organization. |
| list currencies | Details of all existing currencies. |
| list customers | List of all customers. |
| list expense categories | List of all active expense categories. |
| list expense comments | To retrieve all comments on an expense, pass the organization ID and specify the expense. |
| list expense duplicates | To retrieve expenses flagged as potential duplicates in your organization, pass the organization ID. You can optionally filter the results by date range, status, or the employee who submitted the expenses. |
| list expense reports | Retrieve a list of all reports belonging to your organization. You must provide the organization ID. You can narrow down results by filtering on report status (draft, submitted, approved, rejected, reimbursed, or recalled) using the filter_by query parameter. The response returns each report's summary information including report name, number, status, total amounts, submission and approval dates, approver details, policy info, and custom field values. |
| list expenses | To retrieve all expenses in your organization, pass the organization ID. You can narrow down the results using optional filters such as status, category, project, submitted by, and date range. |
| list organizations | Get the list of organizations. |
| list projects | List of all projects. |
| list taxes | Details of all existing taxes. |
| list trips | List all existing trips. |
| list users | Details of all existing users. |
| mark default option | Mark an option as the default option or clear default option for a reporting tag. |
| mark document as primary | To set a document as the primary document for an expense, pass the organization ID and specify both the expense and the document. |
| merge expenses | To merge multiple expenses into one, pass the organization ID. Provide an array of at least two expense identifiers and specify which one should be the primary expense, the one into which the others will be merged. You cannot merge Submitted, Approved, and Reimbursed expenses. |
| recall advance payment | Recall a previously submitted advance payment. |
| reimburse expense report | Record a reimbursement against an approved report by providing the report ID and the organization ID. The report must be in "approved" status and the authenticated user must have reimbursement permissions within the organization. The reimbursement can be recorded offline or paid online. For an offline (manual) reimbursement, account_id - the paid-through account from which the amount is paid - is mandatory; amount (defaults to the report's reimbursable amount), date, reference_number, currency_id, exchange_rate and notes are optional. For an online reimbursement, a payment gateway must be configured for the organization and both account_id (the source account linked to the gateway) and bank_account_id (the employee's bank account to be paid) are mandatory, with the payment authorized using payment_token, or otp together with otp_id. |
| reject advance payment | Reject a submitted advance payment. |
| reject expense in report | Reject a single expense line item within a report. |
| reject expense report | Reject a submitted report by providing the report ID and the organization ID. You can optionally include a comments field in the request body explaining the reason for rejection (e.g., "Purpose is not valid."). The report must be in "submitted" status and the user must be an authorized approver. Once rejected, the report is sent back to the submitter who can then revise and resubmit it. |
| reject trip | Reject a submitted trip request. |
| remove advance payment from expense report | Detach one or more advance payments from a report. |
| remove expenses from expense report | Detach one or more expenses from a report. |
| reorder tags | Reorder the reporting tags in your organization. The order of tags will be followed in transactions and reports. |
| reupload expense report attachment | Replace the contents of an existing attachment, optionally sourcing the new file from a cloud provider. |
| share expense report | Share a report with other users in the organization. |
| skip duplicate expense | To mark an expense as not a duplicate and bypass further duplicate detection, pass the organization ID and specify the expense. |
| split expense | To split an expense, pass the organization ID and specify the expense. Provide an array of split objects, each containing the amount and category. The sum of all split amounts must equal the original expense amount. You can optionally assign different project, cost center, or custom field values to each split. |
| submit advance payment | Submit a draft advance payment to the approver. |
| submit expense report | Submit a draft or recalled report for approval by providing the report ID and the organization ID. The user must select an approver to whom the report will be submitted and can specify email addresses of recipients to be CCed on submission. The report must be in "draft" or "recalled" status, should have at least one expense attached before submission can succeed. |
| takeback expense report | Recall a submitted report. |
| unarchive expense report | Unarchive a report. |
| update advance payment | Update the details of an existing advance payment. Only draft advances can be edited. |
| update currency | Update the details of an existing currency. |
| update customer | Update the details of an existing customer. |
| update expense | To update an expense, pass the organization ID and specify the expense in the request URL. Include only the fields you want to update, such as amount, date, category, merchant name, description, project, cost center, or custom fields. |
| update expense category | Update the details of an existing expense category. |
| update expense report | Update an existing report by providing its report ID and the organization ID. You can optionally update the report name, description, start date, end date, customer or project association, custom field values, and tags. Note that the report must typically be in a draft or recalled state to be editable - reports that have already been submitted or approved cannot be modified without first being recalled. |
| update organization | Update the details of an organization. |
| update project | Update the details of an existing project. |
| update tag | Update a reporting tag |
| update tag criteria | Update the visibility conditions (or filter in some places) of a reporting tag. You can set other tags or location as filters for a tag. Check our help document to know about the requirements of a tag to be associated as a filter to another tag. |
| update tag options | Create, update or delete the options of a reporting tag. Reorder and arrange them in an hierarchical structure as per your organization requirements. **NOTE:** An option cannot be a child option beyond five hierarchical level. The overall children of an option cannot exceed 500 options. |
| update tax | Update the details of an existing tax. |
| update trip | Updates an existing trip with the provided details. Fields not included in the request will retain their current values. |
| update user | Update the details of an existing user. |
| upload expense report attachment | Upload one or more attachments to a report. Supports common file types up to 10 MB each, with a max of 20 files per request. |
| validate expense report | Validate a report before submission. Returns any policy violations, missing-receipt warnings, or other issues that would block submission. |
| void advance payment | Mark an advance payment as fully returned and record the refund details. The returned `date` is required. |
