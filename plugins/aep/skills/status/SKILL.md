---
name: status
description: Show where every AEP work item is in the process, the traceability matrix, open high-severity records, stale reviews, and the single next action. Use when the human asks where things are, what to do next, or how the process works here.
---
# /aep:status

Read-only. Do not change files.

1. If `process/config.json` does not exist, say the repo is not framed and suggest `/aep:frame`. Stop.
2. Gather:
   - current branch, and whether the tree is clean,
   - **foundation stage**: status of `docs/product/problem.md`, `docs/product/constraints.md` (and open questions in each), ADR-001 status, and whether `process/config.json` has a `stack`. The first missing item is the project's stage: Problem → Constraints → Platform (propose) → Platform (apply) → Features,
   - `python3 scripts/process/traceability.py --matrix`,
   - for each `docs/specs/SPEC-*/`: spec status, test-plan status, whether a `test(SPEC-nnn)` commit exists (`git log --all --oneline --grep "test(SPEC-nnn)"`), whether its branch exists and is merged into `develop`,
   - open records with severity critical or high,
   - review-matrix rows older than 30 days per lens,
   - architecture docs still `status: draft`,
   - must-have capabilities in problem.md with no spec yet.
3. Work out each spec's stage: Specify (spec draft) → Plan tests (spec approved, plan missing or draft) → Test first (plan approved, no test commit) → Implement (tests red) → Review (tests green, no review this branch) → PR → Merged.
4. Report:
   - the foundation stage in one line, with what it is waiting on (if not yet at Features, this is the main message),
   - `| Spec | Capability | Title | Stage | Waiting on |` where Waiting on is "human: approve spec", "agent: /aep:implement" and so on,
   - traceability errors, if any,
   - open critical or high records,
   - **Next action**: one command, and who runs it.

If the human seems new to the process, end with the flow:
- Foundations (once): `/aep:frame → /aep:problem → /aep:constraints → /aep:approve problem, constraints → /aep:platform → /aep:approve adr ADR-001 → /aep:platform apply`
- Each feature: `/aep:spec → /aep:approve spec → /aep:test-plan → /aep:approve test-plan → /aep:tests → /aep:implement → /aep:review → /aep:pr → human merges`
