# Agentic Engineering Process (AEP) v0.6

This is the normative process: what must happen, who does it, and what enforces it. The reasoning behind it is in [docs/PLAYBOOK.md](../docs/PLAYBOOK.md). Every skill in this plugin implements one step of this document.

**Problem first.** The problem and its constraints are defined and approved before any platform is chosen, and the platform is chosen before any feature is built. Implementation is secondary to the problem definition.

## 1. Roles

| Role | Who | Does |
|------|-----|------|
| Human | You | Approves the **problem**, the **constraints**, the **platform**, each **spec** and **test plan**, and every **merge** |
| Implementer | Main Claude session | Writes production code, in TDD steps, on a feature branch |
| test-author | Subagent | Writes failing tests from the approved test plan; never sees the implementation first |
| requirements-reviewer | Subagent, read-only | Checks problem definitions and specs are clear, complete and testable |
| Reviewers (correctness, tests, security, architecture) | Subagents, read-only, fresh context | Review the diff against one checklist each |

The author of a piece of work never reviews it.

## 2. Foundations (once per project)

| # | Stage | Skill | Output | Exit gate |
|---|-------|-------|--------|-----------|
| 0 | Frame | `/aep:frame` | Process files, branch model, core CI gate and git hook (no platform) | Core gate green |
| 0b | Adopt (existing code only) | `/aep:adopt` | As-built problem, constraints and ADR-001, then as-built specs | Human approvals as below |
| 1 | Define the problem | `/aep:problem` | `docs/product/problem.md`: statement, users, outcomes, capabilities (CAP), quality attributes (QA), domain rules, information assets; draft invariants and threat-model assets | **Human approves problem** |
| 2 | Target constraints | `/aep:constraints` | `docs/product/constraints.md`: CON entries across ten categories, each with source, hard/soft, how verified | **Human approves constraints** |
| 3 | Choose the platform | `/aep:platform` | ADR-001: candidates, hard-constraint pass/fail, weighted scoring, decision | **Human accepts ADR-001** |
| 4 | Apply the platform | `/aep:platform apply` | Stack profile installed: build tools, full CI gate, project skeleton, architecture overview, trust boundaries; each gate proven to fail when broken | Full gate green |

Constraints may be gathered while the problem is still being refined, but both are approved before the platform is chosen. If the chosen platform has no AEP stack profile, writing one (in the plugin repository) is the next piece of work.

## 3. Feature work (repeats)

A work item is one spec delivering (part of) one capability. It should fit in about a day of agent time; more than about 10 acceptance criteria means split it.

| # | Stage | Skill | Output | Exit gate | Enforced by |
|---|-------|-------|--------|-----------|-------------|
| 5 | Specify | `/aep:spec` | `docs/specs/SPEC-nnn-slug/spec.md` on `feat/SPEC-nnn-slug` | **Human approves spec** | `/aep:approve spec` |
| 6 | Plan tests | `/aep:test-plan` | `test-plan.md` beside the spec | **Human approves test plan**; every AC covered | `/aep:approve test-plan`, traceability |
| 7 | Test first | `/aep:tests` | Failing tests named after their ACs | Every planned test exists and fails for the right reason | traceability, skill check |
| 8 | Implement | `/aep:implement` | Red → green → refactor commits | All tests pass; full local gate passes | Stop hook, CI |
| 9 | Review | `/aep:review` | Findings filed as records | No open critical/high finding unless accepted as a risk | `/aep:pr` precondition |
| 10 | Pull request | `/aep:pr` | PR into `develop` with traceability and metrics | CI green; **human merges** | Branch protection |
| 11 | Retrospective (per iteration) | `/aep:retro` | Retro notes; proposed process changes | Each change cites a metric or incident | Skill checklist |

A design choice during a spec gets an ADR (`/aep:adr`). A defect, risk or decision at any stage gets a record (`/aep:record`). `/aep:status` shows where the project and every work item are.

## 4. Requirements

**Problem level** (`problem.md`): outcomes and quality attributes have measurable targets; capabilities are distinct and prioritised (must / should / could); out of scope is explicit; no technology is named. Technology requirements are constraints, not problem statements.

**Constraint level** (`constraints.md`): every category is answered; each constraint has a source, is hard or soft, and says how it will be verified. Unknown hard constraints block approval.

**Spec level** (`spec.md`):
- Names the capability it delivers, and the quality attributes and constraints it must respect.
- **REQ-nnn** states one behaviour: "The system shall …".
- Each REQ has one or more **AC-nnn** in Given / When / Then form with concrete values. A tester must be able to say pass or fail without interpretation.
- Vague words (fast, robust, user-friendly, appropriate, etc.) are not allowed unless quantified.
- Error handling and edge cases are ACs, not prose.
- Every spec has an **Out of scope** list and a **Security** section saying whether a trust boundary moves.
- **Open questions** must be empty before approval.

IDs (CAP, QA, CON, SPEC, REQ, AC, ADR, DEF, RISK, DEC) are global to the repo and never reused. Get the next one from `scripts/process/next_id.py`.

## 5. Tests

- The test plan maps every AC to at least one test case, with level (unit, integration, end-to-end), technique (example, boundary, negative, property) and data.
- Test names begin with the AC ID. Use `AC_001_…` in languages that do not allow hyphens in names.
- Tests assert observable behaviour. Assert on a call to a fake only when that call *is* the behaviour (for example, a request sent to an external API).
- Fakes replace adapters (network, disk, clock) only, never domain logic.
- Every invariant in `docs/architecture/invariants.md` that a spec touches has a property-based test.
- Changing the assertion of an approved test needs a DEC record and human agreement.

## 6. Git and CI

| Branch | Purpose | Who writes |
|--------|---------|-----------|
| `main` | Released code | Human merges from `develop` only |
| `develop` | Integration | Human merges PRs only |
| `feat/SPEC-nnn-slug` | One work item | Agent commits |
| `fix/DEF-nnn-slug` | One defect fix | Agent commits |
| `chore/…` | Process, foundations and tooling | Agent commits |

- Commit messages: `<type>(<ID>): <summary>`. TDD commits are `test:` (red), `feat:` or `fix:` (green), `refactor:`.
- Agents never commit on, push to or merge into `develop` or `main`, and never force push. The plugin's guard hook blocks this; branch protection (admins included) enforces it on GitHub.
- Before a platform is chosen, CI runs the **core gate**: traceability, doc drift, secret scan. After `/aep:platform apply`, the stack profile's gate adds format, build with warnings as errors, no placeholders, tests with coverage threshold and vulnerable packages.
- Once the gate has passed once, branch protection requires the `gate` check.

## 7. Definition of done (feature work)

- Spec and test plan approved by a human.
- Every AC has a passing test named after it.
- The full local gate and CI pass.
- Triggered reviews ran; no open critical/high record without an accepted risk.
- Spec status set to `done`; metrics row added.
- A human merged the PR.

## 8. Core rules

Stack profiles add their own rules (for .NET: D01–D03). Project-specific rules go in the project's `process/RULES.md`.

| ID | Rule | Enforced by |
|----|------|-------------|
| C01 | Every AC in an approved spec appears in its test plan | `traceability.py` (CI) |
| C02 | Every AC in an approved test plan has a test named after it | `traceability.py` (CI) |
| C03 | No test names an AC that does not exist | `traceability.py` (CI) |
| C04 | No AC ID is defined twice | `traceability.py` (CI) |
| C05 | Facts declared in doc frontmatter match the code | `doc_drift.py` (CI) |
| C06 | Build has no warnings | Stack profile compiler settings (CI) |
| C07 | No TODO, FIXME or not-implemented stubs in source | Stack profile CI step |
| C08 | Tests pass before the agent finishes a turn that changed code | Stop hook |
| C09 | Agents do not commit to, push to or merge into `develop`/`main`, or force push | Guard hook, branch protection |
| C10 | Agents cannot read `.env` files or `secrets/` | Guard hook, permissions |
| C11 | No secrets in the repository | gitleaks (CI, pre-commit) |
| C12 | No known-vulnerable dependencies | Stack profile package audit (CI) |
| C13 | Problem, constraints, platform, spec, test plan and merge are approved by a human | `/aep:approve` (judgment), branch protection |
| C14 | The author does not review its own work | judgment: `/aep:review` uses subagents |
| C15 | No feature spec before the problem and constraints are approved and ADR-001 is accepted and applied | `/aep:spec` precondition |
| C16 | The platform satisfies every hard constraint, and changes keep it so | ADR-001 hard-constraint table (`/aep:approve`); judgment: architecture lens |

## 9. Project files

```text
CLAUDE.md                        # agent entry point, short
process/config.json              # process version, stack (null until platform applied), commands, paths
process/RULES.md                 # project-specific rules and their enforcement
process/experiments/metrics.csv  # one row per merged work item
process/experiments/retros/
docs/product/problem.md          # the problem: outcomes, CAP, QA, domain rules, assets
docs/product/constraints.md      # CON: target constraints
docs/architecture/adr/ADR-001-platform.md, ADR-nnn-*.md
docs/architecture/overview.md, invariants.md, threat-model.md
docs/specs/SPEC-nnn-slug/spec.md, test-plan.md
docs/records/DEF-nnn.md, RISK-nnn.md, DEC-nnn.md
docs/review-matrix.md
scripts/process/                 # traceability.py, doc_drift.py, next_id.py (copied from the plugin)
.github/workflows/ci.yml         # core gate, replaced by the stack profile's gate
.githooks/pre-commit
.gitattributes
```

## 10. Versioning

The plugin is versioned with semantic versions. A project records the version it uses in `process/config.json` (`process_version`). `/aep:frame upgrade` refreshes the copied scripts and CI files and shows the differences. Changes to the process go to the plugin repository as pull requests, each citing the metric or incident behind it.
