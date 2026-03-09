# OpenClaw Collector Rollout Validation

## Goal

Record the first validated real-environment rollout of the OpenClaw collector for MVP issue `#23`.

## Environment

- repository: `openprecedent/openprecedent`
- collector branch: `codex/roll-out-openclaw-collector`
- sessions root: `~/.openclaw/agents/main/sessions`
- validated scheduler: `cron`

`systemctl --user` was present on the target machine, but the user bus was not reachable from this environment. The validated deployment path therefore uses the documented cron installer instead of the `systemd --user` timer path.

Installed schedule:

```cron
*/5 * * * * cd "/workspace/02-projects/incubation/openprecedent" && ./scripts/run-collector.sh >> "/workspace/02-projects/incubation/openprecedent/runtime/collector.log" 2>&1
```

## Real Rollout Result

The collector was installed into the real target environment and confirmed to run on a schedule.

Validated behaviors:

- the scheduled wrapper resolved the repository-local `.venv/bin/openprecedent` binary without requiring a separate global install
- the collector discovered sessions from the real OpenClaw `sessions.json` index format
- repeated collector runs advanced the state file and skipped already imported sessions instead of duplicating them
- collected sessions were replayable and evaluable through the existing CLI

## First Collected Session

The first fully validated collected case was:

- `case_id`: `openclaw_d51637888ee44ff29f2791fc`
- `session_id`: `d5163788-8ee4-4ff2-9f27-91fce72599a4`
- `event_count`: `42`
- `decision_count`: `20`
- `status`: `started`
- `precedent_count`: `0`

Observed unsupported OpenClaw session record types:

- `custom`: `1`
- `thinking_level_change`: `1`

High-level replay summary:

1. the user asked about Feishu-related skills
2. the runtime inspected the skills guidance and ran `skillhub search feishu`
3. the user declined installation until a more specific target existed
4. the user asked for raw contents of two local Context Graph documents
5. the runtime read both local markdown files and returned their contents
6. the user asked whether the runtime could read the `openprecedent/openprecedent` GitHub repository page
7. the runtime read the GitHub skill, fetched the repository page, and confirmed it was accessible
8. the user asked how to subscribe to new GitHub PRs
9. the user then shifted into agent-memory and adjacent-market questions
10. the runtime used `skillhub search`, `gh search repos`, and one failed `web_search` attempt while answering those questions

## Issues Found During Rollout

The real rollout exposed three concrete issues that were fixed in this branch:

1. the scheduled wrapper defaulted to `openprecedent` on `PATH`, which failed when only the repository virtualenv was installed
2. the collector assumed `sessions.json` was a list of objects, but the real OpenClaw index is a dictionary keyed by channel/session scope
3. the cron template used `OPENCLAW_SESSIONS_ROOT=$HOME/...`, but cron environment variable assignments do not reliably expand `$HOME`, so scheduled runs imported zero sessions until the template was rendered with an absolute home path

## Acceptance Summary For Issue 23

Issue `#23` required:

- at least one real environment running scheduled collection
- repeated runs that do not duplicate already imported sessions
- validated setup steps documented in-repo
- the first collected-session evaluation report attached or summarized

This rollout satisfies those conditions:

- the collector is installed in the real target environment via cron
- repeated runs skip imported session ids through the collector state file
- the validated setup path and caveats are documented here and in the collector operations guide
- the first collected session and replay/evaluation summary are recorded above

## Follow-Up Work

The rollout proved the capture path works. The next work should focus on quality rather than more collector scaffolding:

- reduce session-message noise from operator policy and transport metadata wrappers (`#47`)
- tighten `clarify` decision extraction on real multi-turn OpenClaw sessions (`#45`)
- extend OpenClaw session modeling for additional real-world record types only where the live collection stream exposes value (`#46`)
