# HarnessHub Real-Project Validation Report

## Question

Can OpenPrecedent lineage and harness practice materially improve real Codex development work in HarnessHub?

## What Was Run

- multiple issue-scoped HarnessHub development rounds were executed with runtime decision-lineage invocations recorded at `initial_planning`, `before_file_write`, and selected repair points
- repeated observation and sanitized archival were performed against the shared runtime invocation log
- a systematic diagnosis was performed on the shared runtime database, runtime workflow scripts, and retrieval implementation after `matched_case_ids` remained empty across repeated HarnessHub rounds

## Observed Result

- OpenPrecedent is already effective as:
  - cross-session research instrumentation
  - issue-scoped scope-discipline support
  - a durable decision externalization layer during HarnessHub development
- OpenPrecedent is not yet validated as an effective precedent-hit layer for HarnessHub runtime use
- the strongest immediate reason is structural: the shared runtime database currently contains no searchable HarnessHub history
  - `cases = 0`
  - `decisions = 0`
  - `events = 0`
- the current Codex runtime workflow records invocation logs but does not continuously ingest completed external-project Codex rounds into searchable runtime cases
- even after that pipeline gap is fixed, the current brief matcher still ranks primarily by lexical token overlap, so semantically related but differently worded HarnessHub issues will remain easy to miss

## Interpretation

The current evidence does not show that precedent retrieval has failed on real HarnessHub work.
It shows that the retrieval layer has not yet been given the minimum searchable history it needs to operate.

The problem decomposes into three layers:

1. pipeline gap
   - completed HarnessHub rounds are not yet converted into searchable runtime cases and decisions
2. retrieval quality gap
   - the current matcher still relies mainly on lexical overlap
3. sample volume gap
   - even after the first two layers improve, the study will still need more imported HarnessHub rounds

This means issue `#131` has already produced useful evidence, but the chain from real development history to reusable matched precedent is still incomplete.

## Confidence Change

- confidence increased that OpenPrecedent can already help real external development as a research harness and decision externalization layer
- confidence did not yet increase for real precedent-hit usefulness, because the searchable-history loop remains unbuilt
- confidence increased that the next research work should focus on building and validating that loop rather than immediately redesigning retrieval in the abstract

## Follow-Up

Minimal follow-up issue chain:

- `#152` Export completed HarnessHub Codex rounds as importable searchable-history artifacts
- `#153` Import exported HarnessHub rounds into the shared runtime and extract decisions
- `#154` Validate non-empty `matched_case_ids` for a later HarnessHub runtime query
- `#155` Improve HarnessHub decision-lineage matching beyond lexical overlap

Target end-state for this issue chain:

- completed HarnessHub development rounds become searchable runtime cases
- later HarnessHub runtime queries return non-empty `matched_case_ids`
- the matched cases are strong enough to influence a real later development decision
