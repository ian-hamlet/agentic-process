# Correctness lens

## Triggers
Every change.

## Checklist
- [ ] Each AC is met for all inputs it covers, not only the tested example
- [ ] Error paths return or raise what the spec says; nothing is swallowed silently
- [ ] Null, empty, zero, negative, maximum and duplicate inputs are handled
- [ ] Numeric conversions, rounding, units and time zones are correct and explicit
- [ ] Dates and times use an injected clock, not the system clock directly
- [ ] Resources (files, connections, timers) are disposed on every path
- [ ] Concurrency: shared state is protected; async calls are awaited; cancellation is honoured
- [ ] No invariant in invariants.md is broken or reimplemented outside its sole module
- [ ] No behaviour beyond the spec (check the out-of-scope list)
- [ ] No placeholder logic: default returns, hard-coded values standing in for real behaviour
