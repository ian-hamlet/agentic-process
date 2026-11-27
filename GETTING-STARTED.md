# Getting started with AEP

AEP (Agentic Engineering Process) is a way of building software where AI agents do most of the work and humans make the decisions. It is packaged as a Claude Code plugin, `aep`. It puts the **problem first**: before any technology is chosen, it helps you define the problem and record the client's target constraints. Only then does it compare platforms and record the choice. After that, every feature goes through the same steps: **clear requirements, an agreed test plan, failing tests, code written test-first, independent reviews, and a pull request that passes CI**. The rules that matter are enforced by git hooks, Claude Code hooks and CI, not left to memory.

## What you decide

**Once per project:**
1. **The problem.** Is this the right problem, with the right outcomes and priorities?
2. **The constraints.** Are these the client's real requirements on how it is built?
3. **The platform.** Is this the right technology, given the problem and constraints?

**For each feature:**
1. **The spec.** Are these requirements and acceptance criteria what I want?
2. **The test plan.** Would these tests prove it?
3. **The merge.** Is the evidence good enough?

Agents do everything else.

## How it works in a project

You drive the process from the Claude Code panel in VS Code with `/aep:` commands. Each command interviews you where it needs your knowledge, writes or updates a Markdown document in the repository, commits it on a branch, and **stops** where a decision is yours. You read the document, edit it or ask for changes, and record your decision with `/aep:approve …`, which writes your name and the date into the file. The next stage will not start until that approval is there. `/aep:status` always tells you where the project is and what to run next.

```text
Foundations, once:
/aep:frame          install the process (no technology yet)
/aep:problem        interview → docs/product/problem.md             → /aep:approve problem
/aep:constraints    interview → docs/product/constraints.md         → /aep:approve constraints
/aep:platform       compare options → docs/architecture/adr/ADR-001 → /aep:approve adr ADR-001
/aep:platform apply install the chosen stack, CI gate and skeleton

Each feature:
/aep:spec "<capability>"  → /aep:approve spec SPEC-nnn
/aep:test-plan            → /aep:approve test-plan SPEC-nnn
/aep:tests → /aep:implement → /aep:review → /aep:pr → you merge
```

**When are constraints asked about?** After the problem has been described, so the questions can be specific, and before the platform is compared, so the choice can satisfy them. `/aep:constraints` goes through ten areas: where it runs, OS and CPU, client technology standards, existing systems, data, security, operations, licensing, people and delivery. For each constraint it records who requires it, whether it is hard or soft, and how it will be checked. Anything technical you mention while defining the problem (for example "the client is all Azure") is parked for this step rather than lost.

| Document | Where | Created by |
|----------|-------|-----------|
| Problem: outcomes, capabilities (CAP), quality attributes (QA) | `docs/product/problem.md` | `/aep:problem` |
| Target constraints (CON) | `docs/product/constraints.md` | `/aep:constraints` |
| Platform decision and other design decisions | `docs/architecture/adr/` | `/aep:platform`, `/aep:adr` |
| Architecture, invariants, threat model | `docs/architecture/` | `/aep:problem`, `/aep:platform apply` |
| Spec and test plan, one folder per feature | `docs/specs/SPEC-nnn-…/` | `/aep:spec`, `/aep:test-plan` |
| Defects, risks, decisions | `docs/records/` | `/aep:review`, `/aep:record` |
| Metrics and retrospectives | `process/experiments/` | `/aep:pr`, `/aep:retro` |

Everything is plain Markdown in git, so documents are reviewed, versioned and merged like code. Each spec names the capability it delivers, so you can trace from the problem to the tests.

## Starting a new project

A printable step-by-step version, with questions to think about beforehand, is in [START-HERE.md](START-HERE.md).

1. **Set up your machine** once: [SETUP.md](SETUP.md), section 1 (macOS) or 2 (Windows), then 3 to 5.
2. **Create the repository** with a `develop` branch and protect `main` and `develop`: SETUP.md section 6. If the client's constraints will be confidential, make the repository private (and use a paid GitHub plan for branch protection).
3. **Open it in VS Code** and, in the Claude Code panel, run `/aep:frame`. Push the branch, open the pull request, merge it.
4. Run `/aep:problem`, then `/aep:constraints`, then `/aep:platform`, approving each as you go.
5. Start the first feature with `/aep:spec "<a must-have capability>"`.

## Where the process lives

[agentic-process](https://github.com/ian-hamlet/agentic-process) holds the `aep` plugin: process, commands, agents, templates, hooks and stack profiles. Each project is its own repository and uses the plugin.

## Good to know

- The process itself is in [plugins/aep/process/PROCESS.md](plugins/aep/process/PROCESS.md). The reasoning behind it is in [plugins/aep/docs/PLAYBOOK.md](plugins/aep/docs/PLAYBOOK.md).
- Stack profiles available: .NET only, so far ([catalogue](plugins/aep/profiles/README.md)). If the platform decision picks something else, writing that profile becomes the next piece of work.
- Not yet tried end to end: the commands have not been run on a real project, and the Windows setup has not been tried on a Windows machine. Expect rough edges and report them as issues or pull requests on agentic-process.
