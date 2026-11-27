# Agentic Engineering Process (AEP) v0.4

This is the normative process: what must happen, who does it, and what enforces it. The reasoning behind it is in [docs/PLAYBOOK.md](../docs/PLAYBOOK.md). Every skill in this plugin implements one step of this document.

## 1. Roles

| Role | Who | Does |
|------|-----|------|
| Human | You | Approves the **spec**, the **test plan** and the **merge**. Nothing else needs you. |
| Implementer | Main Claude session | Writes production code, in TDD steps, on a feature branch |
| test-author | Subagent | Writes failing tests from the approved test plan; never sees the implementation first |
| requirements-reviewer | Subagent, read-only | Checks a spec is clear, complete and testable |
| Reviewers (correctness, tests, security, architecture) | Subagents, read-only, fresh context | Review the diff against one checklist each |

The author of a piece of work never reviews it.

## 2. Work item lifecycle

A work item is one spec. It should fit in about a day of agent time; if it has more than about 10 acceptance criteria, split it.

| # | Stage | Skill | Output | Exit gate | Enforced by |
|---|-------|-------|--------|-----------|-------------|
| 0 | Frame (once per repo) | `/aep:frame` | Config, CI, git hooks, foundation docs, walking skeleton | CI green; each gate shown to fail when broken | Skill checklist |
| 0b | Adopt (once, existing code) | `/aep:adopt` | As-built specs, characterization tests, records | Human approves as-built specs | `/aep:approve` |
| 1 | Specify | `/aep:spec` | `docs/specs/SPEC-nnn-slug/spec.md` on branch `feat/SPEC-nnn-slug` | **Human approves spec** | `/aep:approve spec` |
| 2 | Plan tests | `/aep:test-plan` | `test-plan.md` beside the spec | **Human approves test plan**; every AC covered | `/aep:approve test-plan`, traceability |
| 3 | Test first | `/aep:tests` | Failing tests named after their ACs | Every planned test exists and fails for the right reason | traceability, skill check |
| 4 | Implement | `/aep:implement` | Red → green → refactor commits | All tests pass; full local gate passes | Stop hook, CI |
| 5 | Review | `/aep:review` | Findings filed as records | No open critical/high finding unless accepted as a risk | `/aep:pr` precondition |
| 6 | Pull request | `/aep:pr` | PR into `develop` with traceability and metrics | CI green; **human merges** | Branch protection |
| 7 | Retrospective (per iteration) | `/aep:retro` | Retro notes; proposed process changes | Each change cites a metric or incident | Skill checklist |

A real design choice during stage 1 gets an ADR (`/aep:adr`). A defect, risk or decision at any stage gets a record (`/aep:record`). `/aep:status` shows where every work item is.

## 3. Requirements

- **REQ-nnn** states one behaviour: "The system shall …".
- Each REQ has one or more **AC-nnn** in Given / When / Then form, with concrete values. A tester must be able to say pass or fail without interpretation.
- Vague words (fast, robust, user-friendly, appropriate, etc.) are not allowed unless quantified.
- Error handling and edge cases are ACs, not prose.
- Quality requirements (performance, security, reliability) are REQs with measurable ACs.
- Every spec has an **Out of scope** list and a **Security** section saying whether a trust boundary moves.
- **Open questions** must be empty before approval.
- IDs (SPEC, REQ, AC, ADR, DEF, RISK, DEC) are global to the repo and never reused. Get the next one from `scripts/process/next_id.py`.

## 4. Tests

- The test plan maps every AC to at least one test case, with level (unit, integration, end-to-end), technique (example, boundary, negative, property) and data.
- Test names begin with the AC ID. Use `AC_001_…` in languages that do not allow hyphens in names.
- Tests assert observable behaviour. Assert on a call to a fake only when that call *is* the behaviour (for example, a request sent to an external API).
- Fakes replace adapters (network, disk, clock) only, never domain logic.
- Every invariant in `docs/architecture/invariants.md` that a spec touches has a property-based test.
- Changing the assertion of an approved test needs a DEC record and human agreement.

## 5. Git and CI

| Branch | Purpose | Who writes |
|--------|---------|-----------|
| `main` | Released code | Human merges from `develop` only |
| `develop` | Integration | Human merges PRs only |
| `feat/SPEC-nnn-slug` | One work item | Agent commits |
| `fix/DEF-nnn-slug` | One defect fix | Agent commits |
| `chore/…` | Process and tooling changes | Agent commits |

- Commit messages: `<type>(<ID>): <summary>`. TDD commits are `test:` (red), `feat:` or `fix:` (green), `refactor:`.
- Agents never commit on, push to or merge into `develop` or `main`, and never force push. The plugin's Bash guard hook blocks this.
- Every PR runs the CI gate: format, build with warnings as errors, no placeholders, tests with coverage threshold, traceability, doc drift, vulnerable packages, secret scan.
- A human sets branch protection on `develop` and `main`: require a PR, require the `gate` check, block force pushes.

## 6. Definition of done

- Spec and test plan approved by a human.
- Every AC has a passing test named after it.
- The full local gate and CI pass.
- Triggered reviews ran; no open critical/high record without an accepted risk.
- Spec status set to `done`; metrics row added.
- A human merged the PR.

## 7. Core rules

Project-specific rules go in the project's `process/RULES.md`. These apply to every project.

| ID | Rule | Enforced by |
|----|------|-------------|
| C01 | Every AC in an approved spec appears in its test plan | `traceability.py` (CI) |
| C02 | Every AC in an approved test plan has a test named after it | `traceability.py` (CI) |
| C03 | No test names an AC that does not exist | `traceability.py` (CI) |
| C04 | No AC ID is defined twice | `traceability.py` (CI) |
| C05 | Facts declared in doc frontmatter match the code | `doc_drift.py` (CI) |
| C06 | Build has no warnings | Compiler settings (CI) |
| C07 | No TODO, FIXME or not-implemented stubs in source | CI grep step |
| C08 | Tests pass before the agent finishes a turn that changed code | Stop hook |
| C09 | Agents do not commit to, push to or merge into `develop`/`main`, or force push | Bash guard hook, branch protection |
| C10 | Agents cannot read `.env` files or `secrets/` | Bash guard hook, permissions |
| C11 | No secrets in the repository | gitleaks (CI) |
| C12 | No known-vulnerable dependencies | Package audit (CI) |
| C13 | Spec, test plan and merge are approved by a human | `/aep:approve` (judgment), branch protection |
| C14 | The author does not review its own work | judgment: `/aep:review` uses subagents |

## 8. Project files

```text
CLAUDE.md                        # agent entry point, short
process/config.json              # process version, stack, commands, paths
process/RULES.md                 # project-specific rules and their enforcement
process/experiments/metrics.csv  # one row per merged work item
process/experiments/retros/
docs/vision.md
docs/architecture/overview.md, invariants.md, threat-model.md, adr/ADR-nnn-*.md
docs/specs/SPEC-nnn-slug/spec.md, test-plan.md
docs/records/DEF-nnn.md, RISK-nnn.md, DEC-nnn.md
docs/review-matrix.md
scripts/process/                 # traceability.py, doc_drift.py, next_id.py (copied from the plugin)
.github/workflows/ci.yml
.githooks/pre-commit
```

## 9. Versioning

The plugin is versioned with semantic versions. A project records the version it uses in `process/config.json` (`process_version`). `/aep:frame upgrade` refreshes the copied scripts and CI file and shows the differences. Changes to the process go to the plugin repository as pull requests, each citing the metric or incident behind it.
