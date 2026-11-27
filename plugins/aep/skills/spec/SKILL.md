---
name: spec
description: Start an AEP work item by writing a spec with clear, testable requirements (REQ) and acceptance criteria (AC) on a new feature branch, then stop for human approval. Use when the human asks for a new feature, change or behaviour.
argument-hint: "<what the feature or change should do>"
---
# /aep:spec — stage 1 (Specify)

The plugin root is `<this skill's base directory>/../..`. The spec template is `templates/spec.md`. Requirement rules are in `process/PROCESS.md` section 3.

## 0. Preconditions
Feature work starts only when the foundations are agreed (rule C15). Check, and if any fails say which and the command that fixes it, then stop:
- `docs/product/problem.md` and `docs/product/constraints.md` have `status: approved` → else `/aep:problem`, `/aep:constraints`
- `docs/architecture/adr/ADR-001-*.md` has `status: accepted` and `process/config.json` has a `stack` → else `/aep:platform`, `/aep:platform apply`

## 1. Branch
1. Working tree must be clean. Switch to `develop`; if it has an upstream, `git pull --ff-only`.
2. Get the ID: `python3 scripts/process/next_id.py SPEC`. Choose a short kebab-case slug.
3. `git checkout -b feat/SPEC-nnn-<slug>`.

## 2. Understand before writing
1. Read `CLAUDE.md`, `docs/product/problem.md`, `docs/product/constraints.md`, `docs/architecture/invariants.md`, `docs/architecture/threat-model.md`, and any spec that covers nearby behaviour (search `docs/specs/`). Identify the capability (CAP-nnn) this spec delivers, and the quality attributes and constraints it must respect; record them in the spec's frontmatter.
2. Read the code the change will touch, enough to know what exists.
3. List what you would otherwise have to guess: inputs and their limits, error behaviour, defaults, what happens on external failure, what is out of scope. Ask the human about the ones that change behaviour, using AskUserQuestion (up to four questions, concrete options, your recommendation first). Do not guess; anything still unknown goes under Open questions.

## 3. Write the spec
Create `docs/specs/SPEC-nnn-<slug>/spec.md` from the template. Reserve IDs with `next_id.py REQ --count N` and `next_id.py AC --count N`.

Each requirement must pass this checklist:
- One behaviour per REQ, phrased "The system shall …".
- Every AC is Given / When / Then with concrete values (numbers, strings, states), and a tester could mark it pass or fail without asking anyone.
- Error and edge behaviour are ACs: invalid, empty, boundary, duplicate, external failure, timeout.
- Quality requirements (performance, reliability, security) have numbers.
- No vague words unless quantified (fast, robust, user-friendly, appropriate, reasonable, efficient ...).
- No implementation detail unless it is a real constraint.
- At most about 10 ACs; otherwise propose splitting into several specs.
- Out of scope is explicit. The Security section says whether a trust boundary moves; if yes, draft the threat-model.md change too.
- If a real design choice exists (two or more reasonable options with different consequences), say so under Design and suggest `/aep:adr`.

## 4. Independent review
Run the `requirements-reviewer` agent with the spec path. Apply rewrites you agree with. Anything that needs the human goes under Open questions. Do not argue with the reviewer in the spec; if you reject a finding, say why in your report to the human.

## 5. Commit and stop
1. Commit: `docs(SPEC-nnn): draft spec`.
2. Show the human:
   - the REQ and AC list as a compact table (`| REQ | AC | Given / When / Then |`),
   - the open questions,
   - reviewer findings you rejected, with reasons.
3. Tell them: edit the file directly or reply with changes; when happy, run `/aep:approve spec SPEC-nnn`.

**Stop here.** Do not write a test plan, tests or code until the spec is approved.
