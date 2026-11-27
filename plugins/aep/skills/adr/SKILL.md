---
name: adr
description: Draft an architecture decision record (ADR) comparing real options for a design choice, for human acceptance. Use when a spec involves a choice between reasonable designs, libraries or structures with different consequences.
argument-hint: "<the decision to make>"
---
# /aep:adr

The plugin root is `<this skill's base directory>/../..`. The template is `templates/adr.md`.

1. ID from `python3 scripts/process/next_id.py ADR`. File: `docs/architecture/adr/ADR-nnn-<slug>.md`.
2. Read `docs/architecture/overview.md`, existing ADRs and the related spec.
3. Write the context as the forces the decision must satisfy (requirements, constraints, invariants), not as a preferred answer.
4. Compare at least two real options, including "do the simplest thing" where it applies. Be specific about consequences for testability, security and future change.
5. Recommend one option under Decision, leave `status: proposed`.
6. Link the ADR from the spec's Design section. Commit `docs(ADR-nnn): propose <decision>`.
7. Tell the human to review it and run `/aep:approve adr ADR-nnn`. If they choose a different option, update Decision and Consequences first.
