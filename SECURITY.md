# Security Policy

## Scope

OpenPrecedent is still in an early stage. Security expectations should still be treated seriously, especially for:

- event payload handling
- secrets in repository configuration
- webhook integrations
- future storage of case data and artifacts

## Reporting

Do not open public GitHub issues for sensitive vulnerabilities.

For now, report security concerns privately to the repository maintainer through a private channel you already use with the project owner.

## Early Security Rules

- never commit secrets
- use repository secrets for webhook credentials
- prefer least-privilege tokens and webhooks
- redact sensitive payload fields before long-term storage where possible
