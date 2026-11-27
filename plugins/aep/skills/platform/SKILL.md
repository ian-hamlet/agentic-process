---
name: platform
description: Choose the implementation platform from the approved problem definition and target constraints - compare candidates in ADR-001 for human acceptance - and then, with "apply", install the chosen stack profile, CI gate, skeleton and architecture documents. Use after /aep:approve problem and /aep:approve constraints.
argument-hint: "[apply]"
---
# /aep:platform — stage 3 (Platform selection)

The plugin root is `<this skill's base directory>/../..`. Templates: `templates/adr-platform.md`, `templates/overview.md`. Available stack profiles: `profiles/README.md` (the catalogue) and each `profiles/<name>/profile.md`.

Without an argument this skill **proposes** the platform. With `apply` it **applies** an accepted decision.

## Propose

### 1. Preconditions
- `docs/product/problem.md` and `docs/product/constraints.md` both have `status: approved`. If not, say which approval is missing and stop.
- If `docs/architecture/adr/ADR-001-*.md` exists and is accepted, skip to **Apply**.
- From `develop`, create `chore/aep-platform`.

### 2. Candidates
Read problem.md, constraints.md and the profile catalogue. Choose two or three realistic candidates. Include at least one that has an AEP profile if any could fit; include a candidate without a profile if it is clearly better. A candidate is a runtime and language, where it runs, and an architecture style (for example: .NET 10 console app on Windows x64; Python 3.12 service in a Linux container; TypeScript web app in the browser).

### 3. Compare
1. **Hard constraints**: pass or fail per candidate, with the reason. Any fail removes it.
2. **Quality attributes and other factors**: weight from the problem's priorities (1–3), score 1–5 with a one-line reason each. Include soft constraints, team skills, cost, and whether an AEP profile exists.
3. Where a fact is missing (for example the client's hosting costs), ask the human rather than guess.

### 4. Write ADR-001 and stop
1. `docs/architecture/adr/ADR-001-platform.md` from the template, `status: proposed`, with your recommendation under Decision and `profile:` set.
2. In Consequences, list the profile settings that constraints drive (for example, a minimum runtime version).
3. Commit `docs(ADR-001): propose platform`.
4. Show the human the hard-constraint table and the scored table, and your recommendation in two sentences. Tell them to change the Decision if they disagree, then `/aep:approve adr ADR-001`, then `/aep:platform apply`.

**Stop here.**

## Apply

### 1. Preconditions
- ADR-001 has `status: accepted`. You are on `chore/aep-platform` (or create it from `develop`), clean tree.
- If ADR-001's `profile:` has no folder under `profiles/`, stop. Tell the human that writing the profile is the next piece of work, done in the agentic-process plugin repository using `profiles/dotnet/` as the model, and offer to draft the issue text describing what the profile needs (tools per row of the profile's Tools table, CI workflow, rules for the constraints).

### 2. Install the profile
Read `profiles/<profile>/profile.md` fully, then:
1. Copy the files in its "Files in this profile" table. The profile's CI workflow and pre-commit hook replace the core ones that `/aep:frame` installed (they include the core steps).
2. In `process/config.json` set `stack` and `commands` from the profile's `config.example.json`, and real source and test paths.
3. Apply the constraint-driven settings named in ADR-001's Consequences (for example, the minimum runtime version property in the profile's build settings).
4. Ask the human for the project name and kind of application (console, web API, service, library, desktop) if ADR-001 does not say. Create the minimal structure the profile describes: one source project and one test project, building against the decided version. **No application logic**: behaviour arrives only through specs.

### 3. Architecture documents
- `docs/architecture/overview.md` from the template: layers and allowed dependencies for the chosen architecture style; components as created.
- `docs/architecture/threat-model.md`: add the trust boundaries the platform creates (for example: app ↔ external API, app ↔ local files) and threats per boundary.
- `docs/architecture/invariants.md`: fill the "sole implementation" column where a module is now known; otherwise leave it for the first spec that touches it.

### 4. Walking skeleton and proof
1. Add one smoke test with no AC ID, and one architecture test if the profile provides the tool. Run the full local gate (every command in config plus `traceability.py` and `doc_drift.py`): all must pass.
2. Prove each gate fails when broken, as listed in the profile (format, build warning, failing test, unknown AC, placeholder), reverting each break. Show the results as a table.
3. Update `CLAUDE.md`'s Commands section from `process/config.json`.

### 5. Commit and hand over
Commit `chore(platform): apply <profile> profile per ADR-001`. Tell the human:
1. Push the branch and open a PR into `develop`; watch the `gate` check.
2. Once it is green, require the `gate` check in branch protection (SETUP.md section 6).
3. Merge, then start feature work with `/aep:spec "<capability>"`, beginning with a must-have capability from problem.md.
