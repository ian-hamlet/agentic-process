---
name: retro
description: Draft an AEP iteration retrospective from metrics, records, review matrix and git history, judge the process hypotheses, and propose evidence-backed process changes. Use at the end of each iteration.
argument-hint: "[iteration number]"
disable-model-invocation: true
---
# /aep:retro — stage 7

The plugin root is `<this skill's base directory>/../..`. The template is `templates/retro.md`.

1. Find the previous retro in `process/experiments/retros/`; this iteration covers everything since its date (or since the start).
2. Gather: metrics rows in that window, records created or closed, review-matrix rows, `git log develop` merges, any changes to `process/` and `CLAUDE.md`.
3. Fill the numbers table. Do not invent missing numbers; show them as blank and say so.
4. For H1–H5, give a verdict only where the numbers support one; otherwise "unclear" and what data would settle it.
5. Ask the human, with AskUserQuestion or a short list: what surprised them about the agents' behaviour, and where the process felt slow or pointless.
6. Propose changes. Each one cites a metric or incident, and says whether it is **local** (this project's `CLAUDE.md`, `RULES.md`, config) or **upstream** (the aep plugin, for every project). Prefer changes that add enforcement over changes that add prose.
7. Write `process/experiments/retros/iteration-<n>.md`. Commit on a `chore/retro-<n>` branch.
8. For upstream changes, draft the text of an issue or PR for the agentic-process repository for the human to submit.
