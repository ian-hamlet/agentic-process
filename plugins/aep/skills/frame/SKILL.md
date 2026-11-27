---
name: frame
description: Set up the Agentic Engineering Process in the current repository - process config, CI gate, git hooks, branch model, foundation documents and a proven walking skeleton. Run once per repository, or with "upgrade" after updating the aep plugin.
argument-hint: "[upgrade]"
disable-model-invocation: true
---
# /aep:frame — stage 0

The plugin root is two directories above this skill's base directory (`<base>/../..`). It holds `process/PROCESS.md`, `templates/`, `scripts/`, `lenses/` and `profiles/`. Read `process/PROCESS.md` sections 5–8 before starting.

If the argument is `upgrade`, skip to **Upgrade** at the end.

## 1. Preconditions
1. Must be a git repository with a clean working tree (`git status --porcelain` empty). If not, stop and tell the human what is uncommitted.
2. If `process/config.json` already exists, this repo is framed: suggest `/aep:frame upgrade` or `/aep:status` and stop.
3. Branches: if `develop` does not exist, create it from `main` (or `master`) with `git branch develop <main>`. Then `git checkout -b chore/aep-frame develop`. All framing commits go on this branch.

## 2. Pick the stack profile
Detect the stack: `*.sln`, `*.slnx` or `*.csproj` → `dotnet`. Only the `dotnet` profile exists in this version. For any other stack, stop and tell the human; offer to draft a new profile in the plugin by following `profiles/dotnet/profile.md` as the model.

Read `profiles/<stack>/profile.md` fully.

## 3. Create the process files
Never overwrite an existing file silently: if a target exists, show what would change and ask.

| From (plugin) | To (project) |
|---|---|
| `scripts/traceability.py`, `doc_drift.py`, `next_id.py` | `scripts/process/` |
| `profiles/<stack>/config.example.json` | `process/config.json` — set `process_version` from the plugin's `.claude-plugin/plugin.json`, real project name in `commands.run`, real source and test paths |
| `templates/RULES.md` | `process/RULES.md` |
| `templates/metrics.csv` | `process/experiments/metrics.csv` |
| (empty dir with `.gitkeep`) | `process/experiments/retros/`, `docs/specs/`, `docs/records/`, `docs/architecture/adr/` |
| `templates/review-matrix.md` | `docs/review-matrix.md` |
| profile files | as listed in the profile's "Files in this profile" table |

Make `.githooks/pre-commit` executable and run `git config core.hooksPath .githooks`. Add to the README a "Development setup" note that each clone must run that command.

Add `.claude/settings.json` (merge if it exists) with permissions that deny reading `.env`, `.env.*` and `secrets/**`, and allow the project's build, test and format commands and read-only git commands.

## 4. Stack setup (dotnet)
Follow the profile: ensure a solution file at the root includes every project; ensure a test project exists with xUnit, coverlet.msbuild, FsCheck.Xunit and NetArchTest.Rules. Run `dotnet build`.

Existing code may now fail the profile's rules. Handle each failure explicitly, never silently:
- **Baseline rules** (the profile's "Baseline rules" table, e.g. D01 target framework): do not fix them inside framing. File a DEF record per rule broken (`found_by: gate`), and tell the human that the first work item is to bring the code up to the baseline on its own `fix/DEF-nnn-…` branch, through the normal flow. Framing stops before step 6 in that case; the walking skeleton is completed on the fix branch.
- **Warnings now treated as errors**: fix real problems; never suppress a warning without asking the human, and record each agreed suppression as a DEC record (`/aep:record decision`).

## 5. Foundation documents
Create from the templates: `docs/vision.md`, `docs/architecture/overview.md`, `docs/architecture/invariants.md`, `docs/architecture/threat-model.md`.

- If code already exists, draft each from the code and the README first, then ask the human to correct it.
- Otherwise, ask the human. Use AskUserQuestion, at most four questions at a time, with concrete options where possible: who it is for and what it must never do; five to ten invariants; the assets worth protecting; the external systems it talks to.
- Leave all four with `status: draft`. The human approves them with `/aep:approve doc <path>` when satisfied.

Write `CLAUDE.md` from `templates/CLAUDE.md` with real commands from `process/config.json`. If a `CLAUDE.md` exists, merge: keep its project facts, adopt the template's structure, and show the human the result.

## 6. Walking skeleton
Add one smoke test that runs real code with no AC ID (for example, the domain project loads, or a pure function returns a known value), plus one architecture test `ARCH_domain_has_no_adapter_dependencies` if the layers exist. Run the full local gate: every command in `process/config.json` plus `traceability.py` and `doc_drift.py`. All must pass.

## 7. Prove each gate fails
For each gate below, make the breaking change, run the matching command, confirm it fails, then revert with `git checkout -- <file>` or by deleting the temporary file. Record the result in a table for the human.

| Gate | Temporary break |
|---|---|
| Format | add badly indented code |
| Build (warnings as errors) | add an unused variable |
| Tests | make the smoke test assert a wrong value |
| Traceability | add a test file whose name mentions `AC_999` |
| Placeholder check | add `// TODO` to a source file and run the CI grep |
| Stop hook | describe it; it runs automatically at the end of an agent turn |

The secret scan runs only in CI; it is proven when the first PR runs.

## 8. Commit and hand over
Commit on `chore/aep-frame`: `chore(process): adopt AEP v<version>`. Do not push.

Tell the human, as a short numbered list:
1. Review the drafts in `docs/` and approve each with `/aep:approve doc <path>`.
2. Push the branch (`git push -u origin chore/aep-frame`) and open a PR into `develop`. Watch the `gate` check run.
3. In GitHub, set branch protection on `develop` and `main`: require a pull request, require the `gate` status check, block force pushes. Agents cannot do this.
4. Merge the PR. Then start the first work item with `/aep:spec <feature>`, or `/aep:adopt` if there is existing code to document first.

## Upgrade
1. Clean tree; branch `chore/aep-upgrade-<version>` from `develop`.
2. Compare `process_version` in `process/config.json` with the plugin version.
3. For `scripts/process/*`, the CI workflow, the git hook and `.editorconfig`, diff the project copy with the plugin copy. Show the human each difference and apply the ones they accept. Keep project-specific edits.
4. Read the plugin's `CHANGELOG.md` entries between the two versions and list any manual steps.
5. Update `process_version`, run the local gate, commit `chore(process): upgrade AEP to v<version>`.
