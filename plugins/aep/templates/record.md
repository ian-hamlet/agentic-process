---
id: DEF-nnn               # DEF | RISK | DEC
type: defect              # defect | risk | decision
status: open              # open | fixed | accepted | wont-fix
severity: medium          # critical | high | medium | low
found_by: review:correctness   # review:<lens> | gate | test | human | production
found_in: SPEC-nnn
escaped: false            # true if found after merge
tool_catchable: false     # true if a lint rule or test could have caught it
links: []
date: [YYYY-MM-DD]
---
# DEF-nnn: [One-line summary]

## What happens
[Concrete scenario: input or state, and the wrong result. file:line.]

## Why it matters
[Impact on users, data, security or maintainability.]

## Resolution
[The fix and the test that proves it, or the reasoning for accepting it and who accepted it.]
