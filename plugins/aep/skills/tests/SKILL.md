---
name: tests
description: Write the failing tests for an approved AEP test plan (the red phase of TDD), using the independent test-author agent, and commit them. Use after /aep:approve test-plan.
argument-hint: "SPEC-nnn"
---
# /aep:tests — stage 3 (Test first)

The plugin root is `<this skill's base directory>/../..`. Stack conventions are in `profiles/<stack>/profile.md`.

## 1. Preconditions
- The spec and test plan in `docs/specs/SPEC-nnn-*/` both have `status: approved`. If not, stop and say which approval is missing.
- You are on the `feat/SPEC-nnn-…` branch with a clean working tree.

## 2. Delegate to test-author
Launch the `test-author` agent. Give it: the spec path, the test-plan path, the test directory from `process/config.json`, and the profile's test conventions section (paste it). The test author must not see an implementation first: do not write production code before it finishes.

## 3. Make the tests compile (compiled languages only)
If the test author lists missing types or methods, add **compile-only stubs** in source: the exact signatures, with bodies that throw a not-implemented exception. No logic. These are removed in `/aep:implement`; CI's placeholder check (C07) keeps the branch from merging until then.

## 4. Verify the red phase
1. Run the fast test command from `process/config.json`.
2. Every new test must **fail**, and fail for the right reason: an assertion failure or the not-implemented stub. A compile error, a wrong import or a test that already passes is a problem. A test that passes already means either the behaviour exists or the test checks nothing; investigate and report it.
3. Run `python3 scripts/process/traceability.py --matrix --spec SPEC-nnn`. Every AC must have at least one test, and the names must match the plan.

## 5. Commit and report
1. Commit tests and stubs together: `test(SPEC-nnn): failing tests for AC-nnn..AC-nnn`. The `test(` prefix tells the Stop hook that failing tests are expected.
2. Show the human: `| Test | AC | Fails with |`, plus any differences from the plan and why.
3. Next step: `/aep:implement SPEC-nnn`. The human may look at the test code first; it is the executable form of the spec they approved.
