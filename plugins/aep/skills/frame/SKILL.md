---
name: frame
description: Set up the Agentic Engineering Process in the current repository before any technology is chosen - process config, branch model, platform-independent CI gate and git hook, guard rails and CLAUDE.md. Run once per repository, or with "upgrade" after updating the aep plugin.
argument-hint: "[upgrade]"
disable-model-invocation: true
---
# /aep:frame — stage 0

The plugin root is two directories above this skill's base directory (`<base>/../..`). It holds `process/PROCESS.md`, `templates/`, `scripts/`, `lenses/` and `profiles/`. Read `process/PROCESS.md` sections 2 and 5–8 before starting.

Framing installs the **process**, not a platform. No language, framework or project structure is chosen here: that happens in `/aep:platform`, after the problem and constraints are defined. If the argument is `upgrade`, skip to **Upgrade** at the end.

## 1. Preconditions
1. A git repository with a clean working tree (`git status --porcelain` empty). If not, stop and say what is uncommitted.
2. If `process/config.json` already exists, the repo is framed: suggest `/aep:frame upgrade` or `/aep:status` and stop.
3. Branches: if `develop` does not exist, create it from `main` (or `master`) with `git branch develop <main>`. Then `git checkout -b chore/aep-frame develop`. All framing commits go on this branch.
4. Note whether the repository already contains application code. If it does, framing still installs only the process; `/aep:adopt` then documents the existing code.

## 2. Create the process files
Never overwrite an existing file silently: if a target exists, show what would change and ask.

| From (plugin) | To (project) |
|---|---|
| `scripts/traceability.py`, `doc_drift.py`, `next_id.py` | `scripts/process/` |
| `templates/config.json` | `process/config.json`, with `process_version` from the plugin's `.claude-plugin/plugin.json` |
| `templates/RULES.md` | `process/RULES.md` |
| `templates/metrics.csv` | `process/experiments/metrics.csv` |
| (empty dir with `.gitkeep`) | `process/experiments/retros/`, `docs/product/`, `docs/specs/`, `docs/records/`, `docs/architecture/adr/` |
| `templates/review-matrix.md` | `docs/review-matrix.md` |
| `templates/ci-core.yml` | `.github/workflows/ci.yml` |
| `templates/pre-commit-core` | `.githooks/pre-commit` (executable) |
| `templates/gitattributes` | `.gitattributes`, then `git add --renormalize .` |

Run `git config core.hooksPath .githooks`. Add a "Development setup" note to the README saying each clone must run that command, and linking to the plugin's SETUP.md.

Add `.claude/settings.json` (merge if it exists) with permissions that deny reading `.env`, `.env.*` and `secrets/**`, and allow read-only git commands and `python3 scripts/process/*`.

Write `CLAUDE.md` from `templates/CLAUDE.md`. Commands not yet known say "set by /aep:platform". If a `CLAUDE.md` exists, merge: keep its project facts, adopt the template's structure, and show the human the result.

## 3. Prove the core gates
Run `python3 scripts/process/traceability.py` and `python3 scripts/process/doc_drift.py`; both must pass. Then prove traceability fails: add a temporary file under `tests/` mentioning `AC_999`, run it, confirm the failure, delete the file. The secret scan is proven when CI first runs on the PR. Show the results as a table.

## 4. Commit and hand over
Commit `chore(process): adopt AEP v<version>`. Do not push.

Tell the human, as a short numbered list:
1. Push the branch (`git push -u origin chore/aep-frame`), open a PR into `develop`, watch the `gate` check, and merge it.
2. If branch protection is not yet set on `develop` and `main`, set it (SETUP.md section 6).
3. Next: `/aep:problem` to define the problem, or `/aep:adopt` if the repository already has code.

## Upgrade
1. Clean tree; branch `chore/aep-upgrade-<version>` from `develop`.
2. Compare `process_version` in `process/config.json` with the plugin version.
3. Diff the project copies with the plugin copies: `scripts/process/*`, `.gitattributes`, and either the core files (`ci-core.yml`, `pre-commit-core`) or, if a stack is set, the profile's files. Show the human each difference and apply the ones they accept. Keep project-specific edits.
4. Read the plugin's `CHANGELOG.md` entries between the two versions and list any manual steps.
5. Update `process_version`, run the local gate, commit `chore(process): upgrade AEP to v<version>`.
