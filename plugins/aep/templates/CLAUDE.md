# [Project name]

[One sentence: the problem it solves and for whom, from docs/product/problem.md.]
This repo follows the Agentic Engineering Process (AEP) v[version]. The process is defined by the `aep` plugin: start work with `/aep:status`.
Problem first: docs/product/problem.md and constraints.md come before platform (ADR-001), which comes before features.

## Invariants (never violate)
See docs/architecture/invariants.md. The short form:
- [INV-1 in one line]
- [INV-2 in one line]

## Commands
Build, test and format commands are set by `/aep:platform apply`; until then they read "set by /aep:platform".
- Build:        [commands.build]
- Test (fast):  [commands.test_fast]
- Test (all):   [commands.test_all]
- Format:       [commands.format_fix]   (check: [commands.format_check])
- Traceability: python3 scripts/process/traceability.py --matrix
- Doc drift:    python3 scripts/process/doc_drift.py
- Next ID:      python3 scripts/process/next_id.py AC

## Where things live
- Problem and target constraints: docs/product/problem.md, constraints.md
- Platform decision: docs/architecture/adr/ADR-001-platform.md
- Specs and test plans: docs/specs/SPEC-nnn-slug/
- Architecture, invariants, threat model, ADRs: docs/architecture/
- Defects, risks, decisions: docs/records/
- Project rules: process/RULES.md   Process config: process/config.json

## Definition of done
- Spec and test plan approved by a human (status: approved).
- Every AC has a passing test whose name starts with its ID (AC_001_...).
- Build, format, tests, traceability and drift checks pass.
- Triggered reviews ran; findings filed as records.

## Never
- Commit on, push to or merge into develop or main. Work on feat/, fix/ or chore/ branches.
- Start a stage before the previous human approval (problem and constraints → platform → spec → test plan → tests).
- Choose or change technology outside ADR-001, or break a hard constraint in constraints.md.
- Change an approved spec's ACs or an approved test's assertion to make code pass.
- Leave TODO, FIXME or not-implemented stubs in source.
- Read .env files or anything under secrets/.
