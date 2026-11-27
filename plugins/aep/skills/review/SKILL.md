---
name: review
description: Run focused, independent AEP reviews (correctness, tests, security, architecture) on the current branch's changes in parallel, file findings as records and update the review matrix. Use after /aep:implement, or with "all" before a release.
argument-hint: "[all]"
---
# /aep:review — stage 5 (Focused review)

The plugin root is `<this skill's base directory>/../..`. Checklists are in `lenses/`.

## 1. Scope
1. Integration branch from `process/config.json` (default `develop`). Diff range: `<integration>...HEAD`. With `all`, review the whole source tree instead of a diff.
2. Find the spec: from the branch name `feat/SPEC-nnn-…` → `docs/specs/SPEC-nnn-*/`.
3. Run the full local gate first (same as `/aep:implement` step 4). Reviewers should not spend effort on what tools catch. If the gate fails, stop and fix that first.

## 2. Choose lenses
Read the Triggers section of each file in `lenses/`.
- Always: `correctness`, `tests`.
- `security` if any changed path or topic matches its triggers.
- `architecture` if the diff adds projects, folders, namespaces or packages, edits project files, or touches more than one layer.
- With `all`: every lens.

Tell the human which lenses run and why, in one line each.

## 3. Run reviewers in parallel
Launch one agent per lens in a single message so they run in parallel: `correctness-reviewer`, `test-reviewer`, `security-reviewer`, `architecture-reviewer`. Give each: the diff range, the spec and test-plan paths, and the absolute path of its lens file. They work in fresh context and cannot see this conversation, so give them everything they need in the prompt.

## 4. Consolidate
1. Merge findings. Where two lenses report the same problem, keep one and note both lenses: agreement raises confidence.
2. Check each finding yourself against the code. Drop ones you can show are wrong, and say why in the report.
3. For each remaining finding of **medium or above**, file a record from `templates/record.md` in `docs/records/` (DEF for a defect, RISK for a risk), with `found_by: review:<lens>`, `found_in: SPEC-nnn`, `tool_catchable` as the reviewer said, and the ID from `next_id.py`. Low findings go in the report only.
4. For each tool-catchable finding, propose a rule for `process/RULES.md` with the tool that would enforce it.
5. Add one row per lens to the top of the table in `docs/review-matrix.md`: date, branch, lens, counts by severity.
6. Commit: `docs(SPEC-nnn): review findings`.

## 5. Report and next step
Show `| ID | Severity | Lens | Summary | file:line |`.

- **Critical or high** findings must be fixed before the PR. Fix each one test-first: add a failing test that shows the defect (`test(SPEC-nnn): DEF-nnn …`), fix it (`fix(SPEC-nnn): DEF-nnn …`), set the record's status to `fixed`. Or the human accepts it as a risk: change it to a RISK record with `status: accepted` and their reasoning.
- Medium and low: ask the human whether to fix now or leave open.
- When no critical or high record for this spec is open: `/aep:pr`.
