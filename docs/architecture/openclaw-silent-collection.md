# OpenClaw Silent Collection

## Goal

The MVP silent collection path should capture real OpenClaw execution trajectories without changing the user's workflow and without parsing gateway log lines.

## Source of Truth

OpenClaw session transcripts under `~/.openclaw/agents/main/sessions/` are the primary source of truth for silent collection.

Why:

- They are structured JSONL trajectories, not plain-text logs.
- They preserve message, tool, and model-level activity.
- They can be imported after a session without changing OpenClaw runtime behavior.

## Collection Contract

OpenPrecedent imports two artifacts from the OpenClaw session directory:

- `sessions.json`
  - session index and metadata
  - used for discovery and selecting the latest session
- `*.jsonl`
  - per-session transcript
  - used for trajectory import

## Event Mapping

The current importer maps transcript records into OpenPrecedent events as follows:

- `type=session` -> `case.started`
- `type=checkpoint` -> `checkpoint.saved`
- `type=model_change` -> `model.completed`
- `message.role=user` -> `message.user`
- `message.role=assistant` text/summary -> `message.agent`
- `assistant.content[type=toolCall]` -> `tool.called`
- `assistant.content[type=toolCall name=exec_command]` -> `command.started`
- `assistant.content[type=toolCall name=exec_command]` with read-only commands such as `cat`, `sed`, `head`, `tail`, `rg`, or `grep` -> `file.read`
- `assistant.content[type=toolCall name=apply_patch]` -> `file.write`
- `assistant.content[type=toolCall name=view_image]` -> `file.read`
- `message.role=toolResult` -> `tool.completed`
- `message.role=toolResult toolName=exec_command` -> `command.completed`

This is intentionally trajectory-first. We do not parse gateway stdout/stderr logs in MVP.

## CLI

The current CLI entry points are:

- `openprecedent runtime list-openclaw-sessions`
- `openprecedent runtime import-openclaw-session --latest --case-id <id>`
- `openprecedent runtime import-openclaw-session --session-id <id> --case-id <id>`
- `openprecedent runtime import-openclaw-session --session-file <path> --case-id <id>`
- `openprecedent runtime collect-openclaw-sessions`

## Automated Collection

For background collection, use:

- `openprecedent runtime collect-openclaw-sessions --limit 1`

This command:

- reads the session index
- imports the latest unseen session transcript
- writes a local collector state file
- skips sessions that were already collected

This is the intended MVP path for cron-based silent collection.

Operational assets now live in:

- `scripts/run-collector.sh`
- `scripts/install-collector-assets.sh`
- `deploy/systemd/openprecedent-collector.service`
- `deploy/systemd/openprecedent-collector.timer`
- `deploy/cron/openprecedent-collector.cron`
- `docs/engineering/openclaw-collector-operations.md`

## MVP Boundary

This is an import-based silent collector, not a live hook into OpenClaw internals.

That is acceptable for MVP because it proves the key product requirement:

- real user-agent trajectories can be captured with no workflow change
- trajectories can be replayed, explained, and reused as precedents

Future work can add file watching or direct runtime emission if needed.
