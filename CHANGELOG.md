# Changelog

## 0.6.0 — 2026-11-27

**Problem first.** The problem and its target constraints are defined and approved before any platform is chosen; the platform is chosen, as ADR-001, before any feature is built.

- New skills: `/aep:problem` (problem statement, outcomes, capabilities CAP, quality attributes QA, domain rules, information assets), `/aep:constraints` (CON entries across ten categories, each with source, hard/soft and how verified; confidentiality check against repository visibility), `/aep:platform` (candidates compared against hard constraints and weighted quality attributes in ADR-001; `apply` installs the chosen stack profile, skeleton and architecture documents).
- `/aep:frame` is now platform-independent: it installs the process, a core CI gate (traceability, doc drift, secret scan), a core pre-commit hook and `.gitattributes`. It no longer creates foundation documents or a project skeleton.
- `/aep:adopt` reconstructs problem, constraints and ADR-001 from existing code before writing as-built specs; baseline failures from the stack profile become DEF records.
- `/aep:spec` refuses to start before problem and constraints are approved and ADR-001 is accepted and applied (rule C15). Specs name their capability, quality attributes and constraints.
- New rules C15, C16. `next_id.py` supports CAP, QA, CON.
- Stack profiles have a catalogue (`profiles/README.md`) and a "Suits" section; the .NET minimum version is a default that ADR-001 sets from constraints. D02 (line endings) moved to the core.
- `vision.md` replaced by `docs/product/problem.md`.
- GETTING-STARTED.md: one-page overview of the process, the documents it creates, and how to start a new project.
- SETUP.md section 6: create a repository with `gh`, and branch protection as used in practice (admins included, `gate` check added after the first green CI run).
- Upgrading from 0.5.0: projects framed with 0.5.0 have no problem or constraints documents; run `/aep:problem` and `/aep:constraints`, then record the existing platform as ADR-001 (`/aep:platform`).

## 0.5.0 — 2026-11-27

- **Rule D03**: projects pin the .NET 10 SDK in `global.json` (`rollForward: latestFeature`), so machines with newer SDKs (e.g. 11) build exactly as CI does. CI reads the SDK version from the same file instead of its own setting.
- SETUP.md: macOS installs `dotnet-sdk@10`; newer SDKs may sit alongside.
- Upgrading from 0.4.0: run `/aep:frame upgrade`.

## 0.4.0 — 2026-11-27

- **.NET baseline rule D01**: every project must target .NET 10 or later. Enforced by an MSBuild target in the profile's `Directory.Build.props`, so builds below the baseline fail locally and in CI. CI uses the .NET 10 SDK.
- **Rule D02**: `.gitattributes` keeps LF line endings so format checks agree on macOS, Windows and CI.
- `/aep:frame` no longer fixes baseline failures in existing code during framing; it files a DEF record and makes the upgrade the first work item.
- **Windows support**: hooks and the git pre-commit hook find `python3`, `python` or `py`; VS Code tasks have Windows variants; SETUP.md has macOS and Windows sections.
- Upgrading from 0.3.0: run `/aep:frame upgrade`.

## 0.3.0 — 2026-11-27

First packaged version, derived from the Agentic Engineering Playbook v0.2.

- `PROCESS.md`: a short normative process split out of the playbook, with core rules C01–C14 and what enforces each.
- Requirements as REQ ("The system shall …") with Given / When / Then ACs; a separate, human-approved test plan per spec.
- Specs and test plans live together in `docs/specs/SPEC-nnn-slug/` (the playbook had `docs/product/specs/`).
- Branch model: `main` (release), `develop` (integration), `feat/`, `fix/`, `chore/` branches. Agents never commit to, push to or merge into `develop` or `main`.
- Skills: frame, adopt, spec, approve, test-plan, tests, implement, review, pr, record, adr, status, retro.
- Agents: requirements-reviewer (new), test-author, correctness-, test-, security-, architecture-reviewer.
- Hooks: Bash/file guard, Stop gate that runs fast tests when code changed (skips the red phase).
- Scripts: traceability (spec ↔ test plan ↔ tests, with `--matrix`), doc drift, next ID.
- `.NET` stack profile with GitHub Actions gate.
- `/aep:adopt` for repositories that already have code (the playbook assumed new projects only).
