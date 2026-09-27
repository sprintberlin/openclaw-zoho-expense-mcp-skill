## Description: <br>
Connects an agent to one or many Zoho Expense organizations through MCP. It provides portable endpoint profiles, organization-aware helper CLIs, least-privilege action profiles, and safe expense workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sprintcx](https://clawhub.ai/user/sprintcx) <br>

### License/Terms of Use: <br>
MIT <br>

## Use Case: <br>
Developers, finance teams, and service providers use this skill to select the correct Zoho Expense account, resolve its organization ID, inspect expenses and reports, and perform controlled Expense operations through mcporter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Zoho Expense MCP endpoint is credential-bearing and could expose employee and receipt data if logged or shared. <br>
Mitigation: Treat endpoints like passwords, prefer profile indirection through environment variables or local URL files, and never commit real profile files. <br>
Risk: Selecting the wrong account or organization can read or change another entity's expenses. <br>
Mitigation: Resolve an explicit profile and organization ID, inspect the live server, and verify the target before writes. <br>
Risk: Write Actions can create expenses, submit reports, approve payouts, or record reimbursements. <br>
Mitigation: Use least privilege, read before writing, keep delete, approve, and reimburse Actions disabled by default, and read results back. <br>

## Reference(s): <br>
- [GitHub source repository](https://github.com/sprintberlin/openclaw-zoho-expense-mcp-skill) <br>
- [Zoho MCP portal](https://mcp.zoho.eu) <br>

## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code, expense records] <br>
**Output Format:** [Markdown guidance with bash, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Expense endpoint and organization ID through environment variables, a named profile, or one-off CLI options.] <br>

## Skill Version(s): <br>
1.0.0 <br>

## Ethical Considerations: <br>
Users must apply their organization's accounting, security, approval, retention, and privacy requirements before relying on generated operations. <br>
