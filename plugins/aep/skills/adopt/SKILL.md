---
name: adopt
description: Bring existing code under the Agentic Engineering Process by writing as-built specs and characterization tests for behaviour that already exists. Use after /aep:frame in a repository that already has code without specs.
argument-hint: "[area or feature to adopt, or blank to propose a plan]"
disable-model-invocation: true
---
# /aep:adopt — stage 0b

The plugin root is `<this skill's base directory>/../..`. Templates are in `templates/`. The repo must be framed (`process/config.json` exists); if not, tell the human to run `/aep:frame` first.

Existing code was written without specs, so nobody knows exactly what it promises. Adoption records what it does **today**, pins that with tests, and files anything that looks wrong. It does not change behaviour.

## 1. Plan (when no argument is given)
1. Inventory the code: entry points and commands, modules, external calls, files read and written, configuration and secrets.
2. Group behaviour into candidate specs of at most about 10 ACs each. Example grouping for a CLI: argument parsing; each command; each external API; each file format.
3. Show the human a table: `| Candidate SPEC | Behaviour covered | Risk if wrong | Suggested order |`, highest risk first. Ask which to adopt first. Stop.

## 2. Adopt one area
1. From `develop`, create branch `feat/SPEC-nnn-asbuilt-<slug>` (ID from `python3 scripts/process/next_id.py SPEC`).
2. Write `docs/specs/SPEC-nnn-<slug>/spec.md` from the template with `origin: as-built`. REQs and ACs describe current behaviour precisely, with concrete values taken from the code (limits, defaults, formats, error messages). Reserve AC IDs with `next_id.py AC --count N`.
3. For behaviour that looks like a bug, keep the AC describing what the code does now, and file a DEF record (`/aep:record defect`) linking it. Do not fix it here.
4. Where behaviour is unclear or the code cannot be tested without refactoring (I/O mixed into logic, static clocks, hard-coded URLs), add an open question or a RISK record proposing a refactor as a future spec.
5. Run the `requirements-reviewer` agent on the spec. Apply its rewrites that keep the spec faithful to the code; put the rest under Open questions.
6. Commit `docs(SPEC-nnn): as-built spec`. Tell the human to review it and run `/aep:approve spec SPEC-nnn`. Stop.

## 3. After approval
The rest is the normal flow, with one difference: tests are **characterization** tests, so they should pass immediately against existing code.
- `/aep:test-plan SPEC-nnn`, then approval.
- `/aep:tests SPEC-nnn`: a test that fails reveals a difference between the as-built spec and the code. Stop and ask the human which is right; file a DEF record if the code is wrong.
- Skip `/aep:implement` unless a refactor is needed to make code testable; such a refactor must keep all tests green.
- `/aep:review`, then `/aep:pr`.
