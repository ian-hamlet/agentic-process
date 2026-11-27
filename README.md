# Agentic Engineering Process (AEP)

A portable, versioned engineering process for building software mostly with AI agents, packaged as a Claude Code plugin called `aep`. Install it in any repository, and its skills walk each change through:

**testable requirements → approved test plan → failing tests → TDD implementation → independent reviews → CI-gated pull request**

Hooks and CI enforce the important rules, so the process does not depend on anyone remembering it.

**New here?** Read [GETTING-STARTED.md](GETTING-STARTED.md) (one page), then [SETUP.md](SETUP.md) for macOS or Windows.

## What a human does

You make three decisions per work item. Everything else is delegated.

| Checkpoint | You run | You are deciding |
|------------|---------|------------------|
| Spec | `/aep:approve spec SPEC-nnn` | These requirements and acceptance criteria are what I want |
| Test plan | `/aep:approve test-plan SPEC-nnn` | These tests would prove it |
| Merge | Merge the PR in GitHub | The evidence is good enough to integrate |

## The flow

```text
/aep:spec "<feature>"            agent drafts REQs + Given/When/Then ACs on feat/SPEC-nnn-slug; reviewer agent checks testability
/aep:approve spec SPEC-nnn       YOU approve
/aep:test-plan SPEC-nnn          agent maps every AC to named tests (level, technique, data)
/aep:approve test-plan SPEC-nnn  YOU approve
/aep:tests SPEC-nnn              independent test-author agent writes failing tests → commit "test(...)"  (red)
/aep:implement SPEC-nnn          one AC at a time: green → refactor, a commit each; full local gate
/aep:review                      correctness, tests, security, architecture reviewers in parallel; findings → records
/aep:pr                          checks done-ness, adds metrics row, pushes, opens PR into develop
                                 YOU merge when CI "gate" is green
```

`/aep:status` tells you where every work item is and what to run next. `/aep:record`, `/aep:adr` and `/aep:retro` cover defects, risks, decisions, design choices and retrospectives.

## Install in a project

The plugin is installed from this repository, which is also a plugin marketplace.

From a local clone (good while you are changing the process):

```text
/plugin marketplace add ~/development/agentic-process
/plugin install aep@agentic-process
```

From GitHub, once this repository is pushed:

```text
/plugin marketplace add <owner>/agentic-process
/plugin install aep@agentic-process
```

To make every clone of a project pick it up, commit this to the project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "agentic-process": { "source": { "source": "github", "repo": "<owner>/agentic-process" } }
  },
  "enabledPlugins": { "aep@agentic-process": true }
}
```

Then, in the project:

1. `/aep:frame`: adds the process config, CI workflow, git hooks, foundation docs and a walking skeleton on a `chore/aep-frame` branch, and proves each gate fails when broken.
2. `/aep:adopt`, if the repository already has code: writes as-built specs and characterization tests.
3. `/aep:spec "<first feature>"`.

## What is in the plugin

```text
plugins/aep/
├── .claude-plugin/plugin.json   # name and version
├── process/PROCESS.md           # the normative process: stages, rules, enforcement
├── docs/PLAYBOOK.md             # the reasoning behind it (read once)
├── skills/                      # /aep:frame, adopt, spec, approve, test-plan, tests,
│                                #   implement, review, pr, record, adr, status, retro
├── agents/                      # requirements-reviewer, test-author, correctness-,
│                                #   test-, security-, architecture-reviewer
├── lenses/                      # one review checklist per focus
├── hooks/                       # guard.py (blocks risky git/shell/secret access), stop_gate.py (tests before finishing)
├── templates/                   # spec, test plan, ADR, record, CLAUDE.md, invariants, threat model, ...
├── scripts/                     # traceability.py, doc_drift.py, next_id.py (copied into projects for CI)
└── profiles/dotnet/             # stack profile: config, strict build props, CI workflow, git hook, VS Code tasks
```

## Shared and per-project

| Lives in the plugin (shared, versioned) | Lives in each project (created by the skills) |
|---|---|
| Process, skills, agents, lenses, templates, hooks, stack profiles | `CLAUDE.md`, `process/config.json`, `process/RULES.md` |
| | `docs/specs/SPEC-nnn-*/spec.md` and `test-plan.md` |
| | `docs/architecture/` (vision, overview, invariants, threat model, ADRs) |
| | `docs/records/` (DEF, RISK, DEC), `docs/review-matrix.md` |
| | `scripts/process/`, `.github/workflows/ci.yml`, `.githooks/` |
| | `process/experiments/metrics.csv`, retros |

## Changing the process

The process is versioned like code (see [CHANGELOG.md](CHANGELOG.md)). Propose changes as pull requests to this repository, each citing the metric or incident behind it. A change that two or more projects needed goes into the next version. Projects pick it up with `/aep:frame upgrade`.

## Requirements

See [SETUP.md](SETUP.md) for step-by-step setup on macOS (Apple Silicon) and Windows (x64).

- Claude Code with plugin support
- Python 3.9 or later (traceability, drift and hook scripts); PyYAML for the drift check
- git (Git for Windows on Windows), and a GitHub repository for CI
- For the .NET profile: the .NET 10 SDK or later; projects must target `net10.0`+ (rule D01)
