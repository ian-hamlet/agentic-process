# Tests lens

## Triggers
Every change.

## Checklist
- [ ] Every AC has a test whose name starts with its ID, and the test checks what the AC says
- [ ] Every row in the approved test plan exists with the planned name, level and technique
- [ ] Assertions check observable results with specific values, not just "not null" or "no exception"
- [ ] No test asserts that a domain method was called; fakes stand in for adapters only
- [ ] Negative and boundary cases from the spec's edge-case list are tested
- [ ] Invariants touched by the change have property-based tests
- [ ] Tests are deterministic: no real clock, network, randomness without a seed, or order dependence
- [ ] No skipped, ignored or commented-out tests
- [ ] Test names describe behaviour, so a failure message explains what broke
- [ ] An approved test's assertion was not weakened (compare with the red-phase `test(...)` commit)
