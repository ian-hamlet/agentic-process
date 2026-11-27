---
id: SPEC-nnn
title: [Short feature name]
status: draft          # draft | approved | done
origin: new            # new | as-built (describes existing behaviour)
capability: CAP-nnn    # from docs/product/problem.md
quality: []            # QA-nnn this spec must meet
constraints: []        # CON-nnn this spec must respect
owner: [human name]
approved_by:
approved_on:
human_min_spec:        # rough minutes the human spent reviewing
branch: feat/SPEC-nnn-slug
---
# SPEC-nnn: [Short feature name]

## Goal
[One or two sentences: what problem this solves and for whom. No solution detail.]

## Context
[What exists today that this builds on. Links to related specs, ADRs, records.]

## Requirements

### REQ-nnn: The system shall [one observable behaviour].
Rationale: [why this is needed]

- **AC-nnn**: Given [precondition with concrete values], when [action], then [observable result with concrete values].
- **AC-nnn**: Given [...], when [invalid or edge input], then [exact error behaviour].

### REQ-nnn: The system shall [quality requirement, e.g. respond within 200 ms at the 95th percentile for 50 concurrent users].
Rationale: [why]

- **AC-nnn**: Given [...], when [...], then [measurable result].

## Edge cases considered
[Each edge case below must be covered by an AC above. List the AC that covers it.]
- [Empty input] → AC-nnn
- [Limit / boundary] → AC-nnn
- [Malformed data] → AC-nnn

## Out of scope
- [Things the agent must not build in this work item.]

## Security and privacy
- Trust boundary moved: [yes / no]. [If yes: which one, and the threat-model.md update.]
- Personal or secret data handled: [none / what, and where it is stored or logged].

## Design
[Link an ADR, or write "No design decision needed".]

## Open questions
[Must be empty before approval.]
- [ ] [Question for the human]
