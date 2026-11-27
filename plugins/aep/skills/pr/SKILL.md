---
name: pr
description: Finish an AEP work item - check it is done, add the metrics row, push the feature branch and open a pull request into develop for a human to merge. Use after /aep:review.
argument-hint: "[SPEC-nnn]"
disable-model-invocation: true
---
# /aep:pr — stage 6 (Pull request)

Agents never merge. This skill prepares everything so the human's merge decision is quick and well informed.

## 1. Check the definition of done
On `feat/SPEC-nnn-…` or `fix/DEF-nnn-…`. Stop and report if any check fails:
- Spec and test plan have `status: approved`.
- No record in `docs/records/` with `found_in: SPEC-nnn`, `status: open` and severity `critical` or `high`.
- Full local gate passes (format, build, all tests, traceability, doc drift, no placeholders).
- `git status` is clean.

## 2. Close the work item
1. Set the spec's and test plan's `status: done`.
2. Append a row to `process/experiments/metrics.csv`. Fill what you can compute:
   - `acs`: ACs in the spec; `tests_added`: tests whose names carry this spec's AC IDs
   - review findings by severity and `findings_tool_catchable`: from this spec's records
   - `human_min_spec`, `human_min_tests`: from the frontmatter
   - `process_version`: from `process/config.json`; `date_merged`: leave blank (set at merge)
   - `agent_sessions`, `gate_failures`: ask the human for a rough number, or leave blank
3. Commit: `docs(SPEC-nnn): close work item`.

## 3. Push and open the PR
1. `git push -u origin <branch>`.
2. Build the PR body:
   - **Summary**: the spec's goal, in two sentences.
   - **Requirements**: `| REQ | AC | Test |` from `python3 scripts/process/traceability.py --matrix --spec SPEC-nnn`.
   - **Commits**: `git log --oneline develop..HEAD`, which shows red → green → refactor.
   - **Review**: lenses run, findings by severity, records filed and their status.
   - **Reviewer checklist** for the human:
     - [ ] The tests express what I approved in the spec
     - [ ] No test was weakened after the red-phase commit
     - [ ] CI `gate` is green
     - [ ] Any accepted risks are acceptable
3. If `gh` is installed and authenticated: `gh pr create --base develop --head <branch> --title "SPEC-nnn: <title>" --body-file <tmpfile>`. Otherwise print the body and the compare URL (`https://github.com/<owner>/<repo>/compare/develop...<branch>`, from `git remote get-url origin`) for the human to open.

## 4. Hand over
Tell the human:
1. Wait for the `gate` check; if it fails, run `/aep:status` and ask for a fix on this branch.
2. Review using the checklist, then merge with a merge commit (keeps the TDD history visible) and delete the branch.
3. Note the minutes the review took in the metrics row (`human_min_merge`) and set `date_merged` in the next work item, or ask Claude to do it.
