# Agentic Engineering Playbook

**Process v0.2 · Draft for team trial**

How to set up a repository, a team of AI agents and automated quality gates so that software built mostly by agents stays secure, well-structured and testable. It applies to any application and any mainstream stack. We will each use it on a small experimental project and compare the results.

- **Status:** Draft, open for comment
- **Date:** 26 November 2026
- **Applies to:** any application, any stack

> Source: https://claude.ai/artifact/VtsnFxZS51UhGCZYJLsfrc (converted to Markdown 27 November 2026)

## Contents

1. [Purpose and use](#1-purpose-and-how-to-use-this-document)
2. [Why agents need a different process](#2-why-agent-driven-projects-need-a-different-process)
3. [Principles](#3-principles)
4. [The process model](#4-the-process-model)
5. [Setting up the repository](#5-setting-up-the-repository)
6. [Setting up the agents](#6-setting-up-the-agents)
7. [Minimum quality bars](#7-minimum-quality-bars)
8. [Running an experiment](#8-running-an-experiment)
9. [Pooling results](#9-pooling-results)
10. [Open questions](#10-open-questions-for-the-team)
- [Appendix: Templates](#appendix-templates)

---

## 1. Purpose and how to use this document

AI coding agents can now write most of the code in a project. The engineering problem has moved: writing code is cheap, but making sure it is correct, secure and maintainable is not. This playbook describes a process for that, and the repository and agent setup that make the process run without anyone having to remember it.

> In our experiments the **process is the product**. Each application is a test bench. We hold the applications to a high standard for code quality, security, architecture and testability because that is how we find out whether the process works.

- **Everyone** reads sections 2 to 4 once. They explain why the process looks the way it does.
- **To start a project**, work through section 5 (repository) and section 6 (agents), then check against section 7. The appendix has files to copy.
- **To run the experiment**, follow section 8 and record metrics as you go.
- **At the end**, section 9 explains how we combine results and update the playbook.

The examples use Claude Code because that is the tool we have most experience with. Every idea here maps onto other agent tools: an entry instruction file, subagents with restricted tools, lifecycle hooks and reusable commands.

## 2. Why agent-driven projects need a different process

Agents work quickly, read whatever documentation they find as current truth, and confidently produce code that looks finished. Traditional processes assume code is written slowly by people who remember the context, so they lean on memory, conventions and goodwill. With agents, those assumptions break. The patterns below come from experience on a previous production project, and they are widely reported elsewhere.

### Failure: what tends to go wrong

- **Process stays as prose.** Good practices are written down and then not enforced. Within weeks they are followed less and less.
- **Docs drift, and agents trust them.** A standards file names an algorithm or a folder that changed months ago, and the agent follows it.
- **Too much context.** Long guides cost tokens on every task and bury the few rules that matter.
- **Tests come after the code.** Manual testing gives false confidence, and placeholder code ships.
- **Plausible placeholders.** Stubs, default returns and wrong conversions that compile and look right.
- **Security reviewed late.** Design-level flaws are found after release, when they are expensive to fix.
- **Facts stored twice.** Versions, schema numbers and config values copied into several files go out of step.
- **The author reviews its own work.** The same agent shares its own blind spots.

### Works: what tends to help

- **Automated gates from day one.** Linters, type checks, tests and scanners that run on every change.
- **Stable IDs that link everything.** Acceptance criteria, decisions and defects have IDs that appear in tests and code, so any line can be traced to its reason.
- **Several narrow reviews.** Separate reviewers for security, correctness, tests and so on each find issues the others miss. Agreement between them raises confidence.
- **Invariants written down.** A short list of rules that must never break, for example "money is never a float".
- **Decisions and accepted risks as records.** Reasons are kept, so nobody, human or agent, reverses a decision without knowing why it was made.
- **A review coverage matrix.** Shows at a glance which kinds of review have not been run lately.

Two ideas tie these together: **a rule nobody enforces gets followed less and less, and a fact stored twice eventually disagrees with itself.** The rest of this playbook turns these lessons into a repository and an agent setup that enforce themselves.

## 3. Principles

| ID | Principle | Detail |
|----|-----------|--------|
| P1 | **Every rule is either enforced or labelled as judgment.** | Each rule in `RULES.md` names the lint, hook, CI job or test that enforces it. If nothing can enforce it, it is marked "judgment" and appears in a review checklist. |
| P2 | **One fact, one place.** | Each fact has a single source in code or config. A document that repeats it declares it in frontmatter, and CI checks the two match. |
| P3 | **Tests come before implementation, and a human approves the test list.** | Reviewing a list of test names is the cheapest point at which a human can catch a misunderstanding. |
| P4 | **Security is designed at the start.** | A threat model exists before the first feature and is updated whenever a change moves a trust boundary. |
| P5 | **The author never reviews its own work.** | Reviewers are separate agents in fresh context, each with one focus and a checklist. |
| P6 | **Keep the agent's starting context small.** | A short entry file holds invariants, commands and links. Detail is loaded only when a task needs it. |
| P7 | **Decisions are records.** | Architecture choices, accepted risks and won't-fix defects each get a short file with a stable ID and the reasoning. |
| P8 | **If it is not measured, we cannot compare it.** | Every work item records a small fixed set of numbers. |

## 4. The process model

Work moves through nine stages. Stages 1 and 9 happen once per project or iteration; stages 2 to 8 repeat for each work item. A work item should take no more than about a day of agent time. If it looks bigger, split it.

| # | Stage | Output | Exit criterion | Led by |
|---|-------|--------|----------------|--------|
| 1 | **Frame** (once per project) | Vision, invariants, threat model v1, first ADR, walking skeleton | One trivial test passes through the full CI pipeline before any feature code exists | Both |
| 2 | **Specify** | Spec with numbered acceptance criteria (`AC-nnn`), edge cases, out-of-scope list | Human approves the spec | Human approves |
| 3 | **Design** | ADR if a real choice is being made; threat-model update if a trust boundary moves | ADR accepted, or "no design decision" noted in the spec | Agent drafts |
| 4 | **Test first** | Failing tests named after their ACs, written by the test-author agent | Human approves the test list; every AC has a test; new tests fail for the right reason | Human approves |
| 5 | **Implement** | Code on a branch or worktree | New tests pass and no existing test breaks | Agent |
| 6 | **Automated gate** | Hook and CI results | Format, lint, types, tests, coverage, security scans, traceability and doc-drift checks all pass | Machine |
| 7 | **Focused review** | Review reports; findings filed as records | No open Critical or High finding, unless it is recorded as an accepted risk | Agent reviewers |
| 8 | **Accept and merge** | Merged change, changelog entry, metrics row | Human accepts the merge | Human |
| 9 | **Retrospective** | Retro notes; proposed changes to `process/` | Each proposed change cites the metric or incident behind it | Both |

### Three human checkpoints

Humans approve the **spec**, the **test list** and the **merge**. Everything else can be delegated. These are the points where a person's understanding of the problem adds the most for the least time.

### Gate before review

Agent reviewers should not spend effort on what a linter or test can catch. Running the automated gate first keeps review findings about design, security and correctness. When a reviewer does find something a tool could have caught, add that tool or rule, so the same finding never needs a reviewer again.

## 5. Setting up the repository

One repository holds both the process deliverables and the application. Work through the steps in order. Do not write feature code until step 8 is done.

### 5.1 Layout

```text
repo/
├── CLAUDE.md                  # agent entry point, at most ~150 lines
├── README.md                  # for humans: what this is, how to run it
├── process/                   # PROCESS DELIVERABLES (application-independent)
│   ├── PROCESS.md             # stages, gates and roles from this playbook
│   ├── RULES.md               # every rule and what enforces it
│   ├── templates/             # spec, ADR, record, review report, retro
│   ├── lenses/                # one checklist per review focus
│   ├── experiments/
│   │   ├── hypotheses.md
│   │   ├── metrics.csv        # one row per work item
│   │   └── retros/
│   └── CHANGELOG.md           # the process is versioned too
├── .claude/
│   ├── settings.json          # committed permissions and hooks
│   ├── agents/                # test author, reviewers, red team
│   └── skills/                # /spec, /adr, /record, /review, /retro
├── docs/
│   ├── product/               # vision.md, specs/SPEC-nnn-*.md
│   ├── architecture/          # overview.md, invariants.md,
│   │                          # threat-model.md, adr/ADR-nnn-*.md
│   ├── records/               # DEF-, RISK-, DEC- files, one per record
│   └── review-matrix.md       # when each review focus last ran
├── app/
│   ├── src/                   # domain/ (pure) · application/ · adapters/
│   └── tests/                 # unit/ · integration/ · e2e/
├── scripts/                   # traceability, doc-drift, version bump
└── .github/workflows/ci.yml   # the automated gate
```

Keep `process/` independent of the application: nothing in it should mention the app's domain. That lets us compare it across experiments and later lift it into a shared template.

### 5.2 Setup steps

1. **Create the repository and protect the main branch.**
   Create the layout above. Turn on branch protection for `main`: require the CI checks to pass, require a pull request, and block force pushes. Agents work on branches; only a human merges.
2. **Choose the stack and record it as ADR-001.**
   Prefer a stack with strict static types, fast tests and mature security tooling. Write down why in `docs/architecture/adr/ADR-001-stack.md`. Section 5.3 lists tools for common stacks.
3. **Set up the toolchain with strict settings.**
   Formatter, linter with no warnings allowed, strict type checker, test runner with coverage, property-based testing library. Fail on warnings from the start. Loosening later is easy; tightening later means fixing everything at once.
4. **Write the foundation documents.**
   - `vision.md`: who it is for, what it does, what it will never do.
   - `invariants.md`: five to ten rules that must never break, and which module is the only allowed implementation of each sensitive operation.
   - `threat-model.md`: assets, actors, trust boundaries, and threats per boundary (STRIDE is a good prompt). Keep it to a page or two.
   - `overview.md`: layers and allowed dependency directions.
5. **Add the traceability and doc-drift scripts.**
   Traceability fails CI when an acceptance criterion has no test naming it, or a test names an AC that does not exist. Doc-drift fails CI when a fact declared in a document's frontmatter does not match the code. Both are short scripts; see Appendix H.
6. **Build the CI pipeline.**
   In order, fastest first: format check, lint, type check, unit tests with coverage threshold, architecture rules, traceability, doc-drift, dependency audit, static security analysis, secret scan, integration tests, build from clean. Every job is required for merge.
7. **Install git hooks.**
   Use lefthook or pre-commit to run format, lint, type check and secret scan before every commit. These apply to people as well as agents, so nobody can bypass the fast checks by working outside the agent.
8. **Prove it with a walking skeleton.**
   Write one trivial end-to-end slice (for example a health check or a no-op command) with one test, and push it through the whole pipeline. Deliberately break each gate once (a lint error, a failing test, a fake secret, an untested AC) and confirm CI goes red. Only then start on features.

### 5.3 Tooling by stack

Suggestions, not requirements. Pick one per row and record it in ADR-001.

| Concern | TypeScript | Python | Go |
|---------|------------|--------|----|
| Format | Prettier or Biome | Ruff format | gofmt |
| Lint | ESLint with typescript-eslint strict | Ruff | golangci-lint |
| Types | `tsc --strict` | mypy `--strict` or pyright | compiler |
| Tests and coverage | Vitest | pytest with pytest-cov | `go test -cover` |
| Property-based tests | fast-check | Hypothesis | rapid |
| Architecture rules | dependency-cruiser | import-linter | go-arch-lint |
| Dependency audit | npm audit, osv-scanner | pip-audit, osv-scanner | govulncheck |
| Static security analysis | Semgrep or CodeQL | Semgrep or CodeQL | Semgrep or CodeQL |
| Secret scanning | gitleaks | gitleaks | gitleaks |
| Mutation testing (optional) | Stryker | mutmut | gremlins |

*Mutation testing is the best check that tests assert real behaviour rather than mocks. It is slow, so run it nightly or before a release rather than on every change.*

### 5.4 Records instead of trackers

Defects, accepted risks and decisions live as separate markdown files in `docs/records/`, each with YAML frontmatter: ID, type, status, severity, who found it, and links (Appendix C). Agents can search them, scripts can build an index from them, and git history shows how each one changed. Avoid a single large tracker file; it grows until no agent can read it.

### 5.5 Repository checklist

- [ ] Main branch protected; CI required; force push blocked
- [ ] ADR-001 records the stack and why
- [ ] Formatter, linter, strict types and coverage threshold all fail the build
- [ ] vision, invariants, threat model and architecture overview written
- [ ] Traceability and doc-drift scripts run in CI
- [ ] Dependency audit, static analysis and secret scan run in CI
- [ ] Git hooks installed and documented in README
- [ ] Walking skeleton passes; each gate proven to fail when broken

## 6. Setting up the agents

Treat agents as a small team with defined roles, restricted tools and clear outputs. The main session implements. Everything else runs as a subagent in its own fresh context, so it does not inherit the implementer's assumptions.

### 6.1 The entry file

`CLAUDE.md` (or the equivalent for your tool) is the only document an agent is sure to read. Keep it short and factual: what the project is, the invariants, the commands, where things live, the definition of done, and what the agent must never do. Link to everything else. A paragraph of explanation belongs in `docs/`, not here. Template in Appendix A.

When an agent makes the same mistake twice, add a line to `CLAUDE.md`, or better, a rule with enforcement in `RULES.md`. Keep these lessons in the repository rather than in personal notes or tool memory, so everyone's agents get them.

### 6.2 The agent roster

Each agent is a file in `.claude/agents/` with a name, a description saying when to use it, a tool list and a prompt. Reviewers get read-only tools. Start with the core roles and add optional ones when the application needs them.

| Agent | When it runs | Tools | Output |
|-------|--------------|-------|--------|
| **Implementer** (main session) | Stage 5 | Full, within permissions | Code that makes the failing tests pass |
| **test-author** | Stage 4, from the approved spec | Read, search, write tests | Failing tests named after ACs, plus edge-case and property tests |
| **security-reviewer** | Changes to auth, input handling, data access, crypto, secrets, external calls | Read, search | Findings with severity, location and failure scenario |
| **correctness-reviewer** | Every change | Read, search | Logic errors, unhandled cases, invariant breaks |
| **test-reviewer** | Every change | Read, search, run tests | Weak assertions, tests of mocks, missing edge cases, untested ACs |
| **architecture-reviewer** | New modules, new dependencies, cross-layer changes | Read, search | Layering breaks, duplicated logic, missing ADRs |
| **docs-keeper** | Before merge | Read, search, edit `docs/` | Docs updated to match the change; drift fixed |
| **red-team** | Once per iteration | Read, search, run tests | Attempts to break invariants and abuse the system, written as failing tests |

Optional, when relevant: **privacy-reviewer** (personal data, logging, retention), **accessibility-reviewer** (any UI), **performance-reviewer** (hot paths, queries), **dependency-reviewer** (new packages, licences, supply chain), **api-reviewer** (public interfaces, compatibility).

The test author is separate from the implementer on purpose. Tests written by the agent that wrote the code tend to check what the code does rather than what the spec asked for.

Each reviewer prompt is short. It points to its checklist in `process/lenses/`, which holds the detail. That keeps the agent file stable while the checklist evolves. Examples in Appendices D and E.

### 6.3 Choosing which reviews run

Each lens checklist starts with its triggers: file paths, layers or topics. A `/review` skill reads the diff, works out which lenses apply, runs those reviewers in parallel and files the findings as records. Before each release, run every lens once and update `docs/review-matrix.md` with the date and finding counts.

### 6.4 Where context lives

| Kind of information | Where | Loaded |
|---------------------|-------|--------|
| Invariants, commands, definition of done, prohibitions | `CLAUDE.md` | Every session |
| What to build | `docs/product/specs/` | When working on that spec |
| Why things are the way they are | ADRs, records | When the agent searches for them |
| How to review for X | `process/lenses/X.md` | By that reviewer only |
| How to do a repeated workflow | `.claude/skills/` | When the skill is invoked |
| Rules that tools enforce | Tool config; listed in `RULES.md` | Never needed in context; the tool reports it |

The last row matters most. A rule that a tool enforces does not need to be in the agent's context at all, because the tool says so when it is broken.

### 6.5 Hooks and permissions

Hooks run commands at fixed points in the agent's work, so checks happen without anyone asking. Commit them in `.claude/settings.json` so the whole team gets the same behaviour.

| Hook | What it runs | Effect |
|------|--------------|--------|
| `PostToolUse` on Edit / Write | Formatter and linter | Style problems fixed while the agent still has the context |
| `Stop` | Fast test suite and type check | On failure (exit code 2) the output goes back to the agent, so it cannot finish with failing tests |
| `PreToolUse` on Bash | A script that rejects risky commands | Blocks things like force pushes, piping downloads into a shell, or deleting outside the repo |
| Permissions `deny` | `.env*`, `secrets/**`, key files | Agents cannot read secrets even by accident |
| Permissions `allow` | Test, lint, build and read-only git commands | Fewer prompts for safe, routine commands |

Configuration example in Appendix F.

### 6.6 Skills for repeated workflows

Turn each repeated workflow into a skill so it runs the same way every time:

- `/spec` drafts a spec from the template with the next free AC numbers.
- `/adr` starts a decision record with options considered.
- `/record` files a defect, risk or decision with the next free ID.
- `/review` picks the triggered lenses for the current diff and runs them in parallel.
- `/retro` collects the iteration's metrics and drafts the retrospective.

### 6.7 Parallel work

Give each work item its own branch, and run parallel agents in separate git worktrees so they cannot edit the same files. Reviewers can always run in parallel because they do not write. Keep parallel implementation to work items that touch different modules; merging two agents' changes to the same module costs more than it saves.

### 6.8 Choosing models

Use the most capable model for the implementer, the security reviewer and the red team, where mistakes are costly. Faster models are usually fine for formatting docs, filing records and summarising metrics. Record which model each role used in `hypotheses.md`, because it affects the results.

### 6.9 Agent failure modes to watch for

- **Plausible placeholders**: code that compiles but does not do the job. Tests on real outputs and a lint rule against `TODO` in `src/` catch these.
- **Stale documentation treated as truth**: the drift check and a short entry file reduce this.
- **Reporting success without running tests**: the `Stop` hook enforces it.
- **Tests that test the mock**: the test reviewer and mutation testing catch these.
- **Duplicated logic**, especially for sensitive operations: `invariants.md` names the one allowed implementation.
- **Changing the spec to fit the code**: specs are only edited with human approval, and `CLAUDE.md` forbids editing ACs to make tests pass.
- **Quiet scope creep**: the spec's out-of-scope list and a review of diff size help.

## 7. Minimum quality bars

Every project meets these from the first commit. Each row says what enforces it.

| Area | Minimum | Enforced by |
|------|---------|-------------|
| **Code quality** | Strict types; formatter; linter with no warnings; no debug printing; function complexity limit; no `TODO` in `src/` | Linter and type checker in hooks and CI |
| **Testability** | Domain logic has no I/O and is unit-tested; adapters sit behind interfaces; coverage floor on the domain layer (we suggest 85% of lines and branches); property-based tests for each invariant | Coverage threshold in CI; traceability script; test reviewer |
| **Security** | Threat model before the first feature; input validated at every boundary; authorisation checked on every data access; secrets only from the environment; no secrets in logs | Static analysis, secret scan and dependency audit in CI; security reviewer on triggered changes |
| **Architecture** | Layered or hexagonal structure with dependency direction checked; invariants listed; every significant choice has an ADR | Architecture rules tool in CI; architecture reviewer |
| **Documentation** | Specs and records hold current truth; no fact repeated without frontmatter declaration | Doc-drift and link checks in CI; docs-keeper agent |
| **Operations** | Version from one source; changelog per merge; reproducible build from a clean checkout | Version-bump script; CI builds from scratch |

## 8. Running an experiment

### 8.1 Choose a project

Pick something you can finish in about three weeks part-time. It needs real rules to protect, a security boundary and untrusted input, or the practices have nothing to prove. Ideally each person picks a different kind of software, so we learn whether the process holds up across them. Some examples:

| Project | What it does | Stresses |
|---------|--------------|----------|
| Shared expense splitter | Groups record shared costs; the app works out who owes whom. | Money rounding invariants, property-based tests, per-group authorisation |
| Room or desk booking | Members book shared spaces in time slots. | Concurrency and double-booking, time zones, role-based permissions |
| Webhook relay | Receives signed webhooks, verifies them and forwards them with retries. | Signature checks, replay protection, rate limiting, hostile input |
| Data reconciliation CLI | Compares two CSV exports and reports mismatches. | Pure logic, malformed files, very large inputs, a non-web contrast case |

### 8.2 Optionally, vary one thing

Everyone runs the same base process. If you want, change exactly one variable and record it in `hypotheses.md`. For example: let the implementer write its own tests; run every lens on every change; skip human approval of the test list; use a different model for reviewers.

### 8.3 Shared hypotheses

| ID | Hypothesis | Evidence |
|----|------------|----------|
| H1 | Writing tests first, with a human-approved test list, reduces defects found after merge. | Escaped defects per work item |
| H2 | Automated gates catch routine problems, so review findings are mostly about design and security. | Share of review findings a tool could have caught |
| H3 | Focused reviewers in fresh context find issues the implementer missed. | Findings per lens; overlap between lenses |
| H4 | Drift and traceability checks keep docs accurate with little effort. | Drift failures, time to fix, docs found wrong at the end |
| H5 | Human time concentrates in the three checkpoints and stays small. | Human minutes per checkpoint and per work item |

### 8.4 Metrics

Add one row to `process/experiments/metrics.csv` per work item when it merges. Keep the columns identical across experiments.

```csv
work_item,date_merged,acs,tests_added,agent_sessions,gate_failures,review_findings_crit,review_findings_high,review_findings_med,review_findings_low,findings_tool_catchable,escaped_defects,human_min_spec,human_min_tests,human_min_merge,human_min_other,notes
```

- **Escaped defects**: problems found after merge in this work item's code. Update the row when one is found.
- **Findings tool-catchable**: each one is a candidate rule for `RULES.md`.
- **Human minutes**: rough estimates are fine.

### 8.5 Timeline

| When | What |
|------|------|
| Days 1–2 | **Frame and set up.** Sections 5 and 6 in full, ending with a walking skeleton that has proved every gate fails when broken. |
| Week 1 | **Iteration 1.** Two or three work items through stages 2 to 8. Short retro. |
| Week 2 | **Iteration 2.** Two or three work items, at least one moving a trust boundary. Apply process changes from the first retro and log them in `process/CHANGELOG.md`. |
| Week 3 | **Iteration 3 and close.** Final work items, then every lens and a red-team pass over the whole codebase. Check every document against the code by hand to find drift the scripts missed. Final retro. |

## 9. Pooling results

- **Weekly 30-minute sync.** Bring your metrics rows and the most surprising agent behaviour of the week.
- **Final retro per experiment** using Appendix G. For each hypothesis, say whether the evidence supports it, contradicts it, or is unclear.
- **Process changes go back as pull requests** to the shared playbook, each citing the metric or incident behind it. A change only one experiment needed stays local. A change two or more experiments needed independently goes into the next version.
- **One combined write-up** comparing the experiments.

## 10. Open questions for the team

1. Records as markdown in the repo (better for agents) or as issues in a tracker (better for people)? This playbook assumes markdown.
2. Same stack for everyone, to make comparison easier, or different stacks, to test that the process is independent of the stack?
3. How many experiments, and who runs which?
4. Is three weeks part-time realistic?
5. Which optional review lenses should be standard?

---

## Appendix: Templates

Copy these into your repository and adjust them. Bracketed parts are for you to fill in. Commands assume a Node project; replace them for your stack.

### Appendix A. CLAUDE.md

```markdown
# [Project name]

[One sentence: what it does and for whom.]
This repo is a process experiment. Follow process/PROCESS.md.

## Invariants (never violate)
- [Invariant 1]
- [Invariant 2]
- Only [module] may [sensitive operation]. Never reimplement it.

## Commands
- Install:     [cmd]
- Test (fast): [cmd]      Test (all): [cmd]
- Lint+types:  [cmd]      Traceability: scripts/traceability.py

## Where things live
- Specs + acceptance criteria: docs/product/specs/
- Decisions: docs/architecture/adr/   Threat model: docs/architecture/threat-model.md
- Defects/risks/decisions: docs/records/   Rules: process/RULES.md

## Definition of done
- Every AC in the spec has a passing test named after it.
- Format, lint, types, tests, traceability and drift checks pass.
- Triggered reviews run; findings filed as records.

## Never
- Commit, push or merge without explicit human instruction.
- Leave placeholders, TODOs or stubbed logic in app/src/.
- Edit a spec's acceptance criteria to make a test pass.
- Read .env or anything under secrets/.
```

### Appendix B. Spec with acceptance criteria

`docs/product/specs/SPEC-004-[name].md`

```markdown
---
id: SPEC-004
title: [Feature name]
status: draft        # draft | approved | done
approved_by:
---
## Problem
[What the user needs and why.]

## Acceptance criteria
- AC-041: Given [context], when [action], then [result].
- AC-042: ...

## Edge cases
- [Empty input, limits, concurrency, permissions, malformed data...]

## Out of scope
- [Things the agent must not add.]

## Security
- Trust boundary moved? [yes/no] If yes, update threat-model.md.
```

### Appendix C. Record

`docs/records/DEF-007.md`

```markdown
---
id: DEF-007               # DEF | RISK | DEC
type: defect
status: open              # open | fixed | accepted | wont-fix
severity: high            # critical | high | medium | low
found_by: review:security # review:<lens> | gate | test | human | production
found_in: SPEC-004
escaped: false            # true if found after merge
links: [AC-041, ADR-003]
---
## What happens
## Why it matters
## Resolution (or reasoning for accepting it)
```

### Appendix D. Reviewer and test-author agents

`.claude/agents/security-reviewer.md`

```markdown
---
name: security-reviewer
description: Reviews a change for security issues. Use after any change that touches authentication, authorisation, input parsing, data access, crypto, secrets or outbound calls.
tools: Read, Grep, Glob
---
You are reviewing a change you did not write. Do not edit files.

1. Read docs/architecture/threat-model.md and invariants.md.
2. Apply every item in process/lenses/security.md to the diff.
3. Skip anything already tracked in docs/records/.
4. For each finding give: severity, file:line, a concrete failure
   scenario (input and result), and a fix or a reason to accept it.
5. Say which findings a lint rule or test could have caught.
Report "no findings" if there are none. Do not pad the report.
```

`.claude/agents/test-author.md`

```markdown
---
name: test-author
description: Writes failing tests from an approved spec before implementation. Use at the test-first stage of every work item.
tools: Read, Grep, Glob, Write, Edit
---
You write tests from the spec, not from the code. Only create or
edit files under app/tests/.

1. Read the spec named in the request. It must have status: approved.
2. For each AC, write at least one test whose name starts with its ID,
   e.g. "AC-041 settles a group to zero".
3. Add edge-case tests from the spec's edge-case list, and a
   property-based test for any invariant the feature touches.
4. Assert on observable behaviour, never on calls to mocks.
5. Run the tests and confirm each new one fails for the expected
   reason (missing behaviour, not a syntax or import error).
6. Finish with a plain list of test names for human approval.
```

### Appendix E. Review lens checklist

`process/lenses/security.md`

```markdown
# Security lens

## Triggers
Paths: app/src/adapters/http/**, app/src/auth/**, app/src/**/crypto*
Topics: login, sessions, permissions, file or network input,
        secrets, outbound requests, serialisation

## Checklist
- [ ] Every entry point validates input type, size and format
- [ ] Every data access checks the caller may access that record
      (no access by guessable ID alone)
- [ ] Queries, commands and templates are parameterised
- [ ] Secrets come from the environment; none in code, logs or errors
- [ ] Crypto uses a vetted library with safe defaults; no custom crypto
- [ ] Tokens expire and are checked for replay where it matters
- [ ] Outbound requests cannot be pointed at internal addresses
- [ ] Error messages shown to users reveal no internals
- [ ] Rate limits on anything that can be abused or is expensive
- [ ] New dependencies are maintained, licensed and audited
- [ ] Threat model updated if a trust boundary moved
```

### Appendix F. Hooks and permissions

`.claude/settings.json`

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run test:*)",
      "Bash(npm run lint:*)",
      "Bash(git status)",
      "Bash(git diff:*)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Bash(git push --force:*)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "npm run -s lint:fix" }]
      }
    ],
    "Stop": [
      {
        "hooks": [{ "type": "command", "command": "npm run -s test:fast || exit 2" }]
      }
    ]
  }
}
```

### Appendix G. Retrospective

`process/experiments/retros/iteration-[n].md`

```markdown
# Iteration [n] retro, [date]

## Numbers (from metrics.csv)
Work items: · Gate failures: · Findings C/H/M/L: · Escaped: · Human min:

## Hypotheses
- H1: supports / contradicts / unclear. Evidence:
- H2 ... H5

## What the agents did that surprised us

## Rules to add (each with what will enforce it)

## Process changes proposed (each citing a metric or incident)
```

### Appendix H. Traceability and doc-drift scripts

Minimal versions in Python, which works alongside any stack. Extend them as needed.

`scripts/traceability.py`

```python
#!/usr/bin/env python3
"""Fail if an AC has no test, or a test names an AC that doesn't exist."""
import pathlib, re, sys

AC = re.compile(r"\bAC-\d{3}\b")

def ids(root):
    return {m for p in pathlib.Path(root).rglob("*") if p.is_file()
            for m in AC.findall(p.read_text(errors="ignore"))}

specs, tests = ids("docs/product/specs"), ids("app/tests")
for ac in sorted(specs - tests):
    print(f"No test names {ac}")
for ac in sorted(tests - specs):
    print(f"Test names unknown {ac}")
sys.exit(1 if specs ^ tests else 0)
```

`scripts/doc_drift.py` (needs PyYAML)

```python
#!/usr/bin/env python3
"""Fail if a fact declared in a doc's frontmatter disagrees with the code.

Declare facts in frontmatter like:
facts:
  schema_version:
    value: 3
    source: app/src/db/schema.ts
    pattern: 'SCHEMA_VERSION = (\d+)'
"""
import pathlib, re, sys, yaml

failures = 0
for doc in pathlib.Path("docs").rglob("*.md"):
    text = doc.read_text()
    if not text.startswith("---"):
        continue
    meta = yaml.safe_load(text.split("---")[1]) or {}
    for name, fact in (meta.get("facts") or {}).items():
        source = pathlib.Path(fact["source"]).read_text()
        match = re.search(fact["pattern"], source)
        actual = match.group(1) if match else None
        if str(fact["value"]) != actual:
            print(f"{doc}: {name} is {fact['value']!r} in the doc, "
                  f"{actual!r} in {fact['source']}")
            failures += 1
sys.exit(1 if failures else 0)
```

### Appendix I. RULES.md

`process/RULES.md`

```markdown
| ID  | Rule                                          | Enforced by                   |
|-----|-----------------------------------------------|-------------------------------|
| R01 | No debug printing in app/src/                 | linter (error)                |
| R02 | Every AC has a test named after it            | scripts/traceability.py in CI |
| R03 | Domain layer never imports adapters           | architecture rules tool in CI |
| R04 | No secrets in the repository                  | gitleaks in hook and CI       |
| R05 | Version defined only in the package manifest  | scripts/doc_drift.py in CI    |
| R06 | No TODO or placeholder in app/src/            | linter (error)                |
| R07 | Errors shown to users never include internals | judgment: security lens       |
```

---

*Agentic Engineering Playbook, process v0.2. Propose changes through the process in section 9.*
