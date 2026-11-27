---
name: record
description: File an AEP record - a defect (DEF), risk (RISK) or decision (DEC) - with the next free ID in docs/records/. Use whenever a bug, risk, accepted trade-off or process decision should be kept.
argument-hint: "defect|risk|decision <one-line summary>"
---
# /aep:record

The plugin root is `<this skill's base directory>/../..`. The template is `templates/record.md`.

1. Type → prefix: defect → DEF, risk → RISK, decision → DEC. ID from `python3 scripts/process/next_id.py <PREFIX>`.
2. Create `docs/records/<ID>.md` from the template. Fill:
   - `severity`: ask the human if it is not obvious (critical: data loss, security breach or crash in normal use; high: wrong result in normal use; medium: wrong result in an edge case; low: cosmetic or maintainability).
   - `found_by`, `found_in` (current SPEC from the branch name if any), `escaped: true` if the code is already merged into `develop`, `tool_catchable`, `links`, `date`.
   - The three sections, with a concrete scenario and file:line.
   - A decision (DEC) records who decided, what, and why, and the alternatives rejected.
3. If on a feature branch, commit `docs(<ID>): <summary>`. On `develop` or `main`, leave it uncommitted and tell the human.
4. For an escaped defect, suggest fixing it on `fix/<ID>-<slug>` with the normal flow: a failing test first, then the fix.
