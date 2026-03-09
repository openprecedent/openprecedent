# Feishu PR Notifications

## Goal

Send a Feishu bot notification whenever a pull request becomes ready for review.

This repository uses a GitHub Actions based notification flow:

1. GitHub pull request event occurs
2. workflow formats a short message
3. workflow posts to a Feishu bot webhook

This is preferred over having a coding agent actively send notifications because PR review is an event-driven repository concern, not a session-scoped agent concern.

## Current Trigger Scope

The first implementation notifies on:

- `pull_request.opened`
- `pull_request.reopened`
- `pull_request.ready_for_review`

Draft pull requests are ignored.

## Required Secret

Configure this repository secret in GitHub:

- `FEISHU_WEBHOOK_URL`

Path:

1. GitHub repository
2. `Settings`
3. `Secrets and variables`
4. `Actions`
5. `New repository secret`

## Message Shape

The current message includes:

- repository name
- PR number
- PR title
- author
- action type
- source and target branch
- PR link

## Future Improvements

Possible later extensions:

- notify again when all required checks pass
- notify only for PRs targeting `main`
- include CI status summary
- support richer Feishu card messages
- include a repository-specific review handbook link in the message
