---
id: ADR-001
title: Platform selection
status: proposed       # proposed | accepted | superseded by ADR-nnn
date: [YYYY-MM-DD]
approved_by:
profile: [aep profile to apply, e.g. dotnet, or "none yet"]
related: [docs/product/problem.md, docs/product/constraints.md]
---
# ADR-001: Platform selection

## Context
[Two or three sentences: what the solution must do (from problem.md) and the constraints that most shape the choice (from constraints.md).]

## Candidates
| Option | Runtime and language | Where it runs | Architecture style | AEP profile |
|--------|---------------------|---------------|--------------------|-------------|
| A | | | | exists / missing |
| B | | | | |

## Hard constraints
An option that fails any hard constraint is out.

| Constraint | A | B |
|-----------|---|---|
| CON-nnn [short text] | pass / fail: [why] | |

## Quality attributes and other factors
Weight 1–3 from the priority in problem.md; score 1–5 per option with a one-line reason.

| Factor | Weight | A | B |
|--------|--------|---|---|
| QA-nnn [short text] | | | |
| Soft constraints | | | |
| Team skills | | | |
| Cost to build and run | | | |
| AEP profile available | | | |
| **Weighted total** | | | |

## Decision
[The option chosen, the runtime version, where it runs, and the architecture style, in two or three sentences.]

## Consequences
- Profile settings driven by constraints: [e.g. minimum .NET version 10 from CON-003]
- [What becomes easier]
- [What becomes harder, and any RISK record]
- [If no AEP profile exists: the profile to write before feature work starts]
