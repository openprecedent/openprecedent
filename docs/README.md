# Docs

Repository documentation is organized by function:

- `product/`: strategy and MVP product definition
- `architecture/`: system design and object model
- `research/`: market and competitive analysis
- `engineering/`: implementation and operational documentation

Directory entrypoints:

- [Product docs](/root/.config/superpowers/worktrees/openprecedent/codex-issue-265-doc-chronology/docs/product/README.md)
- [Architecture docs](/root/.config/superpowers/worktrees/openprecedent/codex-issue-265-doc-chronology/docs/architecture/README.md)
- [Research notes](/root/.config/superpowers/worktrees/openprecedent/codex-issue-265-doc-chronology/docs/research/README.md)
- [Engineering docs](/root/.config/superpowers/worktrees/openprecedent/codex-issue-265-doc-chronology/docs/engineering/README.md)

Engineering documentation is further organized by concern:

- `engineering/cli/`: Rust public CLI design, implementation, and usage
- `engineering/runtime/`: runtime boundaries, startup flows, tooling, and collector operations
- `engineering/validation/`: live validation, rollout validation, and replay-quality evidence
- `engineering/governance/`: harness policy, review rules, and repository workflow guidance

## Documentation Conventions

OpenPrecedent documentation should be organized primarily by topic tree, not by date-prefixed filenames alone.

Repository-wide rules:

- use a directory-level `README.md` when a doc category needs a recommended reading path, chronology cues, or canonical-vs-historical guidance
- keep canonical current docs in stable topic locations such as `docs/product/` or `docs/architecture/`
- mark drafts, historical notes, archived rounds, or superseded material explicitly in document metadata or directory indexes rather than expecting readers to infer status from filenames
- include explicit date metadata when chronology matters for the document set, especially for research notes, evolving discussion docs, or historical drafts
- keep English and Chinese entrypoints aligned when parallel documentation trees exist

For the repository-level chronology and entrypoint guidance, see:

- [Documentation governance](/root/.config/superpowers/worktrees/openprecedent/codex-issue-265-doc-chronology/docs/engineering/governance/documentation-governance.md)
