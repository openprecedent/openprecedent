---
name: harness-gap-closure
description: Use when a repeated agent workflow mistake, user reminder, or self-detected failure reveals that the local harness should have prevented the problem. Guides Codex to diagnose the harness gap, create or link the issue, add the guardrail, and add regression protection.
---

# Harness Gap Closure

Use this skill when a failure should have been prevented by the repository's local harness rather than left to user correction or memory.

Typical triggers:

- the user says a mistake should have been caught by the harness
- the same workflow failure has happened more than once
- a push, PR, review, branch, or issue-scoped workflow mistake exposes a missing local guardrail
- Codex recognizes that a repeated workaround should become a reusable harness rule

Do not use this skill for one-off product bugs that do not imply a harness deficiency.

## Goal

Turn repeated workflow failures into issue-scoped harness hardening work with a complete loop:

1. identify the harness gap
2. anchor it in a GitHub issue and local task twin
3. implement the local guardrail or workflow fix
4. add regression protection where practical
5. update the repository guidance so later sessions reuse the fix

## Workflow

1. Confirm that the problem is a harness gap, not just a one-off mistake.
   - Ask: should the local workflow, hook, preflight, skill, or command path have prevented this?
   - If the answer is no, do not use this skill.

2. Look for repetition.
   - If the same class of error has happened before, treat that as sufficient evidence that the harness is incomplete.
   - If it is a new but clearly preventable workflow failure, the skill can still be used.

3. Create or link an explicit GitHub issue before editing implementation.
   - Reuse `.codex/skills/ccpm-codex/` for issue, task, branch, and PR mechanics.
   - Do not patch harness code on a discussion-only branch.

4. State the gap precisely.
   - Record:
   - what failed
   - why the current harness allowed it
   - what local signal could have blocked or clarified it earlier

5. Prefer the smallest reliable guardrail.
   - Typical fixes:
   - pre-push hook checks
   - preflight checks
   - repository-local command wrappers
   - workflow skill instructions
   - fail-fast local validation scripts
   - clearer repository guidance tied to enforced behavior

6. Add regression protection.
   - If the gap is scriptable, add or update automated tests.
   - If the gap is primarily procedural, add the strongest practical local proof or fail-fast behavior.
   - Do not stop at docs-only guidance when the failure can be detected locally.

7. Update guidance where contributors will actually see it.
   - Usually one or more of:
   - `AGENTS.md`
   - `docs/engineering/runtime/tooling-setup.md`
   - `docs/engineering/governance/repository-governance.md`
   - local skill command maps

8. Close the loop in the PR.
   - Explain:
   - the repeated failure mode
   - the new harness behavior
   - the regression coverage

## Expected Outcome

After using this skill, the repository should be stronger in a concrete way:

- the same mistake should be blocked earlier, or
- the workflow should now fail locally with a clear explanation, or
- the repository should provide a standard path that removes the ambiguity

## Read Next

- `.codex/skills/ccpm-codex/SKILL.md`
- [`docs/engineering/runtime/tooling-setup.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/tooling-setup.md)
- [`docs/engineering/governance/repository-governance.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/governance/repository-governance.md)
- [`docs/engineering/governance/harness-capability-analysis.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/governance/harness-capability-analysis.md)
