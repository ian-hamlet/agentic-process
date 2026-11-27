---
name: approve
description: Record a human approval of an AEP problem definition, constraints, spec, test plan, ADR or architecture document. Human checkpoint; only a human runs it.
argument-hint: "problem | constraints | spec SPEC-nnn | test-plan SPEC-nnn | adr ADR-nnn | doc <path>"
disable-model-invocation: true
---
# /aep:approve — human checkpoint

This skill exists so approvals are explicit, recorded in the file and in git history, and never made by an agent on its own. It runs only because a human typed it.

## 1. Find the file
- `problem` → `docs/product/problem.md`
- `constraints` → `docs/product/constraints.md`
- `spec SPEC-nnn` → `docs/specs/SPEC-nnn-*/spec.md`
- `test-plan SPEC-nnn` → `docs/specs/SPEC-nnn-*/test-plan.md`
- `adr ADR-nnn` → `docs/architecture/adr/ADR-nnn-*.md`
- `doc <path>` → that file (overview, invariants, threat model)

If the argument is missing or ambiguous, ask which file.

## 2. Pre-approval checks
Run them and show the results. If any fails, list the problems and stop; the human fixes them (or asks you to) and runs `/aep:approve` again.

| Target | Checks |
|---|---|
| problem | Open questions empty; problem statement, at least one outcome with a target, at least one must-have capability, out-of-scope list, quality attributes with targets; no technology named outside "Constraints raised so far" |
| constraints | All ten categories answered; every constraint has source, hard/soft and how verified; no open question about a possible hard constraint; if `confidential: true`, the repository is private |
| spec | Open questions empty; at least one REQ and AC; every AC is Given / When / Then; Security section answered; the current branch is `feat/SPEC-nnn-…` |
| test-plan | The spec is approved; `python3 scripts/process/traceability.py` shows no C01 or C03 errors for this spec; every row has a level, technique and concrete data |
| adr | At least two options with pros and cons; a decision and consequences. For ADR-001 (platform): problem and constraints approved; every hard constraint has pass or fail for every candidate; the chosen option passes all of them |
| doc | No `[placeholder]` brackets left |

## 3. Confirm with the human
Show a five-line summary of what is being approved (for a problem: capability and quality-attribute counts; for constraints: hard and soft counts; for a spec: REQ count, AC count, out-of-scope items, trust boundary yes/no; for ADR-001: the chosen platform). Ask with AskUserQuestion:
- "Approve" — record approval
- "Not yet" — stop without changes

Also ask roughly how many minutes they spent reviewing (options: 5, 15, 30, 60; Other allowed). This feeds the metrics.

## 4. Record
1. In the frontmatter set `status: approved` (`accepted` for an ADR), `approved_by:` the output of `git config user.name`, `approved_on:` today's date (YYYY-MM-DD), and the minutes given in `human_min` (problem, constraints), `human_min_spec` (spec) or `human_min_tests` (test plan).
2. Commit on the current branch: `docs(<ID>): approve <target>`. If the current branch is `develop` or `main` (for foundation docs), create `chore/approve-<short-name>` first.
3. Say what comes next:
   - problem → `/aep:constraints` if constraints are not yet approved, otherwise `/aep:platform`
   - constraints → `/aep:platform` (once the problem is approved too)
   - ADR-001 → `/aep:platform apply`
   - spec → `/aep:test-plan SPEC-nnn`
   - test plan → `/aep:tests SPEC-nnn`
   - ADR or doc → continue where you were.
