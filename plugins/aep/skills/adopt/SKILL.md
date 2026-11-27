---
name: adopt
description: Bring existing code under the Agentic Engineering Process - reconstruct the problem definition, constraints and platform decision from the code, apply the stack profile, then write as-built specs and characterization tests. Use after /aep:frame in a repository that already has code.
argument-hint: "[area or feature to adopt, or blank to start]"
disable-model-invocation: true
---
# /aep:adopt — stage 0b

The plugin root is `<this skill's base directory>/../..`. The repo must be framed (`process/config.json` exists); if not, point to `/aep:frame` and stop.

Existing code was written without a problem definition or specs, so nobody knows exactly what it promises. Adoption records what exists **today**, pins it with tests, and files anything that looks wrong. It does not change behaviour.

## 1. Problem, constraints and platform, as built
Do these once, in order, on `chore/aep-adopt` from `develop`:
1. **Problem**: draft `docs/product/problem.md` (`origin: as-built`) from the README, code and any docs, then run the `/aep:problem` interview to correct and complete it. The human may decide the code solves the wrong problem; note that, and keep going.
2. **Constraints**: run `/aep:constraints`. Record constraints the existing code already implies (runtime, OS, external services) and ask whether each is a real constraint or just an accident of the first implementation.
3. **Platform**: draft ADR-001 from `templates/adr-platform.md` describing the platform the code already uses, with the hard-constraint table filled in. If the existing platform fails a hard constraint (for example, a runtime below the client's minimum version), say so in Consequences. The human approves it with `/aep:approve adr ADR-001`; then run `/aep:platform apply`.
4. **Baseline failures**: applying the profile may make the existing code fail its rules (for example, a target-framework minimum). Do not fix them during adoption. File a DEF record per rule broken (`found_by: gate`) and tell the human the first work item is to fix it on its own `fix/DEF-nnn-…` branch, through the normal flow. Warnings that become errors: fix real problems; never suppress one without asking, and record agreed suppressions as DEC records.

Each of the four steps ends with its own human approval; stop after each and say what is next.

## 2. Plan the as-built specs
1. Inventory the code: entry points and commands, modules, external calls, files read and written, configuration and secrets.
2. Group behaviour into candidate specs of at most about 10 ACs each, mapped to capabilities in problem.md.
3. Show the human `| Candidate SPEC | Capability | Behaviour covered | Risk if wrong | Suggested order |`, highest risk first. Ask which to adopt first. Stop.

## 3. Adopt one area
1. From `develop`, create `feat/SPEC-nnn-asbuilt-<slug>` (ID from `next_id.py SPEC`).
2. Write the spec from the template with `origin: as-built`. REQs and ACs describe current behaviour precisely, with concrete values from the code (limits, defaults, formats, messages).
3. Behaviour that looks like a bug: keep the AC describing what the code does now, and file a DEF record linking it. Code that cannot be tested without refactoring: add a RISK record proposing a refactor as a future spec.
4. Run the `requirements-reviewer` agent; apply rewrites that keep the spec faithful to the code; the rest goes under Open questions.
5. Commit `docs(SPEC-nnn): as-built spec`; the human approves with `/aep:approve spec SPEC-nnn`.

Then the normal flow, with characterization tests: `/aep:test-plan`, approval, `/aep:tests` (tests should **pass** against existing code; a failure shows a difference between spec and code: ask the human which is right), skip `/aep:implement` unless a refactor is needed, `/aep:review`, `/aep:pr`.
