# Changelog

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
