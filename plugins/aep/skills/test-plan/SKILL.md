---
name: test-plan
description: Write the test plan for an approved AEP spec, mapping every acceptance criterion to named test cases with level, technique and data, then stop for human approval. Use after /aep:approve spec.
argument-hint: "SPEC-nnn"
---
# /aep:test-plan — stage 2 (Plan tests)

The plugin root is `<this skill's base directory>/../..`. The template is `templates/test-plan.md`. Test rules are in `process/PROCESS.md` section 4. Stack conventions are in `profiles/<stack>/profile.md` (`stack` from `process/config.json`).

## 1. Preconditions
- `docs/specs/SPEC-nnn-*/spec.md` has `status: approved`. If not, stop and point to `/aep:approve spec SPEC-nnn`.
- You are on its `feat/SPEC-nnn-…` branch.

## 2. Design the tests
Read the spec, `docs/architecture/invariants.md`, `docs/architecture/overview.md`, the profile's test conventions and the existing test project layout.

For each AC, decide:
- **Level**: unit for domain rules (the default); integration for an adapter talking to something real or a realistic fake (HTTP server, file system); end-to-end only for a critical path through the whole app.
- **Technique**: example (the AC's own values), boundary (at and either side of each limit), negative (each invalid input class), property (an invariant over generated inputs), contract (the shape of an external API).
- **Data**: concrete inputs and the exact expected result.
- **Name**: `AC_nnn_<behaviour_in_words>`, following the profile's convention.

Also plan:
- A property test for each invariant the spec touches.
- Which adapters are faked, and how. Never fake domain logic.
- What is deliberately not tested and why. If the gap matters, file a RISK record.

## 3. Write and check
1. Create `test-plan.md` next to the spec from the template.
2. Run `python3 scripts/process/traceability.py --matrix --spec SPEC-nnn`. Every AC must show "In plan: yes". Fix the plan until there are no C01 or C03 errors for this spec.
3. Commit: `docs(SPEC-nnn): draft test plan`.

## 4. Show and stop
Show the human the test-case table and the "Not tested" list. Point out where you chose fewer tests than they might expect, and why. Tell them to edit the plan or reply with changes, then run `/aep:approve test-plan SPEC-nnn`.

**Stop here.** Do not write tests until the plan is approved.
