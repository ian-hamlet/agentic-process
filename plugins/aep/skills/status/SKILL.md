---
name: status
description: Show where every AEP work item is in the process, the traceability matrix, open high-severity records, stale reviews, and the single next action. Use when the human asks where things are, what to do next, or how the process works here.
---
# /aep:status

Read-only. Do not change files.

1. If `process/config.json` does not exist, say the repo is not framed and suggest `/aep:frame`. Stop.
2. Gather:
   - current branch, and whether the tree is clean,
   - `python3 scripts/process/traceability.py --matrix`,
   - for each `docs/specs/SPEC-*/`: spec status, test-plan status, whether a `test(SPEC-nnn)` commit exists (`git log --all --oneline --grep "test(SPEC-nnn)"`), whether its branch exists and is merged into `develop`,
   - open records with severity critical or high,
   - review-matrix rows older than 30 days per lens,
   - foundation docs still `status: draft`.
3. Work out each spec's stage: Specify (spec draft) → Plan tests (spec approved, plan missing or draft) → Test first (plan approved, no test commit) → Implement (tests red) → Review (tests green, no review this branch) → PR → Merged.
4. Report:
   - `| Spec | Title | Stage | Waiting on |` where Waiting on is "human: approve spec", "agent: /aep:implement" and so on,
   - traceability errors, if any,
   - open critical or high records,
   - **Next action**: one command, and who runs it.

If the human seems new to the process, end with the stage flow in one line:
`/aep:spec → /aep:approve spec → /aep:test-plan → /aep:approve test-plan → /aep:tests → /aep:implement → /aep:review → /aep:pr → human merges`.
