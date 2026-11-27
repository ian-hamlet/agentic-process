# Getting started with AEP

AEP (Agentic Engineering Process) is a way of building software where AI agents write most of the code and humans make the decisions. It is packaged as a Claude Code plugin, `aep`. You install it once per machine, switch it on in a repository, and its commands take each change through the same steps: **clear requirements, an agreed test plan, failing tests, code written test-first, independent reviews, and a pull request that passes CI**. The rules that matter are enforced by git hooks, Claude Code hooks and CI, not left to memory.

## What you decide

You make three decisions per piece of work. Agents do the rest.

1. **Approve the spec.** Are these requirements and acceptance criteria what I want?
2. **Approve the test plan.** Would these tests prove it?
3. **Merge the pull request.** Is the evidence good enough?

## How it works in a project

You drive the process from the Claude Code panel in VS Code with `/aep:` commands, and every command produces or updates a document in the repository.

- `/aep:spec "<what you want>"` creates a branch and drafts `docs/specs/SPEC-001-…/spec.md`. A separate reviewer agent checks the requirements are testable. It asks you about anything it would otherwise have to guess, then stops.
- You read the spec, edit it or ask for changes, and run `/aep:approve spec SPEC-001`. This records your name and the date in the file and commits it.
- `/aep:test-plan` writes `test-plan.md` next to the spec, and stops again for `/aep:approve test-plan`.
- `/aep:tests` has an independent agent write failing tests. `/aep:implement` makes them pass one acceptance criterion at a time, with a commit at each step. `/aep:review` runs four reviewers and files what they find in `docs/records/`. `/aep:pr` opens the pull request with a requirement-to-test table for you to merge.

Each stage refuses to start until the previous approval is in the file. If you are ever unsure where things are, `/aep:status` says which stage each piece of work is at and what to run next.

```text
/aep:spec → /aep:approve spec → /aep:test-plan → /aep:approve test-plan
          → /aep:tests → /aep:implement → /aep:review → /aep:pr → you merge
```

Everything is plain Markdown in git, so documents are reviewed, versioned and merged like code.

| Document | Where | Created by |
|----------|-------|-----------|
| Vision, architecture, invariants, threat model | `docs/`, `docs/architecture/` | `/aep:frame` (asks you questions) |
| Spec and test plan, one folder per piece of work | `docs/specs/SPEC-nnn-…/` | `/aep:spec`, `/aep:test-plan` |
| Design decisions | `docs/architecture/adr/` | `/aep:adr` |
| Defects, risks, decisions | `docs/records/` | `/aep:review`, `/aep:record` |
| Metrics and retrospectives | `process/experiments/` | `/aep:pr`, `/aep:retro` |

## Starting a new project

1. **Set up your machine** once: [SETUP.md](SETUP.md), sections 1 (macOS) or 2 (Windows), then 3 to 5. This installs .NET 10, git, the GitHub CLI and the plugin.
2. **Create the repository** with a `develop` branch and protect `main` and `develop`: SETUP.md section 6.
3. **Open it in VS Code** and, in the Claude Code panel, run `/aep:frame`. It asks for the project name and the kind of application, creates the .NET 10 solution and test project, CI workflow, git hooks and foundation documents on a `chore/aep-frame` branch, and shows that each check fails when broken. Approve the foundation documents, push, open the pull request, merge it.
4. **Start your first feature** with `/aep:spec "<what you want>"` and follow the flow above.

## The two repositories today

| Repository | What it is | State |
|------------|-----------|-------|
| [agentic-process](https://github.com/ian-hamlet/agentic-process) | The `aep` plugin: process, commands, agents, templates, hooks, .NET profile | v0.5.0 on `develop`; public; protected |
| [eddi-monitor](https://github.com/ian-hamlet/eddi-monitor) | First trial project; code written by an agent before the process existed | Not yet framed; public; protected |

## Good to know

- The process itself is in [plugins/aep/process/PROCESS.md](plugins/aep/process/PROCESS.md) (two pages). The reasoning behind it is in [plugins/aep/docs/PLAYBOOK.md](plugins/aep/docs/PLAYBOOK.md).
- Only the .NET stack is supported so far, with .NET 10 as the minimum.
- Not yet tried end to end: the commands have not been run on a real project, and the Windows setup has not been tried on a Windows machine. Expect rough edges and report them as issues or pull requests on agentic-process.
