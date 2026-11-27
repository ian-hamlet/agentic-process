---
name: approve
description: Record a human approval of an AEP spec, test plan, ADR or foundation document. Human checkpoint; only a human runs it.
argument-hint: "spec SPEC-nnn | test-plan SPEC-nnn | adr ADR-nnn | doc <path>"
disable-model-invocation: true
---
# /aep:approve — human checkpoint

This skill exists so approvals are explicit, recorded in the file and in git history, and never made by an agent on its own. It runs only because a human typed it.

## 1. Find the file
- `spec SPEC-nnn` → `docs/specs/SPEC-nnn-*/spec.md`
- `test-plan SPEC-nnn` → `docs/specs/SPEC-nnn-*/test-plan.md`
- `adr ADR-nnn` → `docs/architecture/adr/ADR-nnn-*.md`
- `doc <path>` → that file (vision, overview, invariants, threat model)

If the argument is missing or ambiguous, ask which file.

## 2. Pre-approval checks
Run them and show the results. If any fails, list the problems and stop; the human fixes them (or asks you to) and runs `/aep:approve` again.

| Target | Checks |
|---|---|
| spec | Open questions empty; at least one REQ and AC; every AC is Given / When / Then; Security section answered; the current branch is `feat/SPEC-nnn-…` |
| test-plan | The spec is approved; `python3 scripts/process/traceability.py` shows no C01 or C03 errors for this spec; every row has a level, technique and concrete data |
| adr | At least two options with pros and cons; a decision and consequences |
| doc | No `[placeholder]` brackets left |

## 3. Confirm with the human
Show a five-line summary of what is being approved (for a spec: REQ count, AC count, out-of-scope items, trust boundary yes/no). Ask with AskUserQuestion:
- "Approve" — record approval
- "Not yet" — stop without changes

Also ask roughly how many minutes they spent reviewing (options: 5, 15, 30, 60; Other allowed). This feeds the metrics.

## 4. Record
1. In the frontmatter set `status: approved` (`accepted` for an ADR), `approved_by:` the output of `git config user.name`, `approved_on:` today's date (YYYY-MM-DD), and for a spec `human_min_spec:` or a test plan `human_min_tests:` the minutes given.
2. Commit on the current branch: `docs(<ID>): approve <target>`. If the current branch is `develop` or `main` (for foundation docs), create `chore/approve-<short-name>` first.
3. Say what comes next:
   - spec → `/aep:test-plan SPEC-nnn`
   - test plan → `/aep:tests SPEC-nnn`
   - ADR or doc → continue where you were.
