---
status: draft          # draft | approved
origin: new            # new | as-built (reconstructed from existing code)
approved_by:
approved_on:
human_min:             # rough minutes the human spent on this document
---
# Problem definition: [working name]

This document says what problem we are solving and what success looks like. It deliberately says nothing about technology: platform and implementation are decided later (ADR-001), from this document and docs/product/constraints.md.

## Problem statement
[One paragraph: who has what problem, what it costs them today, and why it is worth solving now.]

## Users and stakeholders
| Who | What they need | How they are affected today |
|-----|----------------|-----------------------------|
| [user group] | | |

## Outcomes
How we will know it worked. Each outcome is measurable.

| ID | Outcome | Measure | Target |
|----|---------|---------|--------|
| OUT-1 | [e.g. users see a problem within minutes rather than days] | [time from event to alert] | [≤ 5 minutes] |

## Capabilities
What the solution must be able to do, at the level of a feature list. Each capability is later detailed by one or more specs (`capability: CAP-nnn` in the spec).

| ID | Capability | Why it matters | Priority |
|----|-----------|----------------|----------|
| CAP-001 | [the solution can ...] | [outcome it serves] | must / should / could |

## Out of scope
- [Things this solution will not do. These bound every spec.]

## Quality attributes
How well it must work. Each has a concrete scenario and a target, so it can be tested and used to compare platforms.

| ID | Attribute | Scenario | Target |
|----|-----------|----------|--------|
| QA-001 | [availability / performance / security / usability / maintainability ...] | [when ..., the system ...] | [number] |

## Domain rules
Rules of the problem domain that must always hold, whatever the implementation. They seed docs/architecture/invariants.md.
- [e.g. a reading is never attributed to the wrong device]

## Information and assets
| Information | Sensitivity | Why it matters |
|-------------|-------------|----------------|
| [credentials, personal data, measurements ...] | [secret / personal / internal / public] | [harm if lost, leaked or altered] |

## Assumptions
- [Things taken as true without proof. Each is a risk if wrong.]

## Constraints raised so far
Anything said about how it must be built (a language, a client standard, where it runs) is noted here and moved into docs/product/constraints.md by `/aep:constraints`.
- [e.g. client runs everything on Azure]

## Open questions
[Must be empty before approval.]
- [ ] [Question, and who can answer it]
