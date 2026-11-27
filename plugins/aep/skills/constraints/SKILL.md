---
name: constraints
description: Enquire about and record the target constraints - where the solution runs, OS and CPU, client technology standards, existing systems, data, security, operations, licensing, people and delivery - with source, hard or soft, and how each is verified, then stop for approval. Use once a problem definition exists, before choosing a platform.
argument-hint: "[client or organisation, optional]"
---
# /aep:constraints — stage 2 (Target constraints)

The plugin root is `<this skill's base directory>/../..`. Template: `templates/constraints.md`.

Constraints are requirements on **how** the solution may be built, set by the client, regulation or our organisation. They are gathered once the problem is understood (so questions can be specific), and before the platform is chosen (so the choice can satisfy them).

## 1. Preconditions
- `docs/product/problem.md` exists. It may still be a draft: constraints can be gathered while the problem is refined. If it does not exist, point to `/aep:problem` and stop.
- Work on the same `chore/aep-problem` branch if it is still open, otherwise create `chore/aep-constraints` from `develop`.

## 2. Confidentiality check
Ask whether any constraint is confidential to the client. If yes, check the repository's visibility (`gh repo view --json visibility`). If it is public, stop and tell the human: confidential constraints must not be committed to a public repository. Offer to record them in a private location and keep only a non-confidential summary here.

## 3. Enquire
Start from "Constraints raised so far" in problem.md. Then go through the ten categories in the template, in rounds of up to four questions (AskUserQuestion with typical options plus "No constraint" and "Don't know"). Make the questions specific to this problem; for example, if a capability involves collecting data from devices, ask what devices and networks are involved.

For each constraint, establish:
- **Source**: who requires it, and the document or person behind it.
- **Hard or soft**: would breaking it rule a solution out (hard), or only make it less attractive (soft)?
- **How verified**: the rule, CI check, test or review that will show it is met.

"Don't know" on something that could rule platforms in or out becomes an open question with the person who can answer. Do not guess client standards.

## 4. Write and commit
1. `docs/product/constraints.md` from the template; IDs from `python3 scripts/process/next_id.py CON --count N`. Every category answered, even with "No constraint".
2. Move the items from "Constraints raised so far" in problem.md into this file, and leave a pointer there.
3. Commit `docs(constraints): draft target constraints`.

## 5. Stop
Show the human the constraints table, highlight the hard ones, and list open questions with who should answer each. Tell them:
- resolve open questions (unknown hard constraints block approval),
- `/aep:approve constraints` when complete,
- then `/aep:platform` to choose the platform.

**Stop here.** Do not compare or choose platforms in this stage.
