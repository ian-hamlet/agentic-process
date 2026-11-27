---
spec: SPEC-nnn
status: draft          # draft | approved | done
approved_by:
approved_on:
human_min_tests:       # rough minutes the human spent reviewing
---
# Test plan for SPEC-nnn: [title]

## Approach
[Which test levels are used and why. Example: domain rules as unit tests; the HTTP adapter as integration tests against a fake server; no end-to-end tests because ...]

## Test cases
Every AC in the spec appears at least once. Test names start with the AC ID.

| AC | Test name | Level | Technique | Inputs / data | Expected result |
|----|-----------|-------|-----------|---------------|-----------------|
| AC-nnn | AC_nnn_[behaviour_in_words] | unit | example | [concrete values] | [concrete result] |
| AC-nnn | AC_nnn_[rejects_...] | unit | negative | [invalid value] | [exact error] |
| AC-nnn | AC_nnn_[boundary_...] | unit | boundary | [limit, limit+1] | [result at each] |

Techniques: example, boundary, negative, property, contract, performance.

## Properties and invariants
| Invariant (from invariants.md) | Property tested | Generator |
|--------------------------------|-----------------|-----------|
| [INV-n] | [for all valid inputs, ...] | [how inputs are generated] |

## Test doubles and data
- Faked: [adapters only: clock, HTTP client, file system ...] and how.
- Real: [everything else].
- Fixtures: [files or builders, where they live].

## Not tested, and why
- [Item]: [reason, and the risk record if the gap matters]

## Exit criteria
- Every test above exists and passes.
- Coverage on changed domain code meets the threshold in process/config.json.
- No skipped or ignored tests.
