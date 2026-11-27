---
name: implement
description: Make the failing AEP tests pass one acceptance criterion at a time using red-green-refactor, committing each step, then run the full local gate. Use after /aep:tests.
argument-hint: "SPEC-nnn"
---
# /aep:implement — stage 4 (Implement)

The plugin root is `<this skill's base directory>/../..`.

## 1. Preconditions
- On `feat/SPEC-nnn-…`, clean working tree.
- A `test(SPEC-nnn): …` commit exists on this branch (`git log --oneline develop..HEAD`) and its tests currently fail. If not, stop and point to `/aep:tests`.
- Read the spec, the test plan, `docs/architecture/invariants.md` and `docs/architecture/overview.md`.

## 2. Rules for this stage
- Make tests pass by changing **source code only**.
- Never change an approved spec, the test plan, or a test's assertions or expected values. If a test looks wrong, stop and explain to the human: which test, why you think it is wrong, and what you propose. If they agree, file a DEC record (`/aep:record decision`) and change it in a separate `test(SPEC-nnn): …` commit that names the DEC.
- Build only what the ACs require. Nothing from the Out of scope list.
- Keep domain logic free of I/O; put I/O behind interfaces as overview.md describes.
- Use the sole implementation that invariants.md names for any sensitive operation; never write a second one.

## 3. Red → green → refactor, one AC at a time
In the order of the test plan, for each AC:
1. **Red**: run only that AC's tests and confirm they fail.
2. **Green**: write the simplest code that makes them pass. Replace the stub for that behaviour.
3. Run the whole fast suite. Nothing else may break.
4. Commit: `feat(SPEC-nnn): AC-nnn <behaviour>`.
5. **Refactor** if the code now has duplication or unclear names; run the fast suite; commit `refactor(SPEC-nnn): <what>`.

## 4. Full local gate
When every AC is green, run, in order: format check, build, all tests (`test_all`), `python3 scripts/process/traceability.py`, `python3 scripts/process/doc_drift.py`, and a search for TODO, FIXME and not-implemented stubs in the source paths. Fix anything that fails, with a commit per fix.

## 5. Report
Show the human:
- `| AC | Commit | Test status |`
- the gate results,
- anything you noticed but did not change (possible defects, design concerns). Offer to file them as records.

Next step: `/aep:review`.
