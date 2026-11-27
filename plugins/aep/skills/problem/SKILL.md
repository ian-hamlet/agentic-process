---
name: problem
description: Define the problem before any technology - problem statement, users, measurable outcomes, capabilities, quality attributes, domain rules and information assets - by interviewing the human, then stop for approval. Use right after /aep:frame, or when the human describes a new problem to solve.
argument-hint: "[short description of the problem, optional]"
---
# /aep:problem — stage 1 (Define the problem)

The plugin root is `<this skill's base directory>/../..`. Templates: `templates/problem.md`, `templates/invariants.md`, `templates/threat-model.md`.

The implementation is secondary to the problem. This stage produces a problem definition with **no technology in it**. If the human names a language, framework, cloud or device, write it under "Constraints raised so far" for `/aep:constraints`, and carry on with the problem.

## 1. Preconditions
- The repo is framed (`process/config.json` exists); otherwise point to `/aep:frame` and stop.
- Clean working tree. From `develop`, create `chore/aep-problem`. If `docs/product/problem.md` already exists, this is a revision: say so and work on the existing file.

## 2. Interview
Work in short rounds; use AskUserQuestion where there are sensible options, free text otherwise. At most four questions per round. Summarise what you heard after each round, so the human can correct it.

1. **Problem and people**: who has the problem, what it costs them today, why now.
2. **Outcomes**: how we would know it worked. Push for numbers ("faster" → "how fast, measured how?").
3. **Capabilities**: what the solution must be able to do, as a short list. Ask for priority (must / should / could) and what is explicitly out of scope.
4. **Quality attributes**: for the ones that matter (availability, performance, security, usability, maintainability, cost), a concrete scenario and target each.
5. **Domain rules**: what must always be true in this domain, whatever the implementation.
6. **Information**: what data the solution holds or touches, and how sensitive it is.

Do not invent answers. Unknowns go under Open questions, with who can answer.

## 3. Write
1. `docs/product/problem.md` from the template. IDs: `OUT-n` for outcomes; `CAP-nnn`, `QA-nnn` from `python3 scripts/process/next_id.py CAP --count N` (and `QA`).
2. `docs/architecture/invariants.md` from the template, seeded from the domain rules (implementation column left for later), `status: draft`.
3. `docs/architecture/threat-model.md` from the template, with Assets and Actors filled from the information table; trust boundaries wait for the platform decision. `status: draft`.

## 4. Independent check
Run the `requirements-reviewer` agent on `docs/product/problem.md`, telling it this is a problem definition, not a spec: check that outcomes and quality attributes are measurable, capabilities are distinct and testable in principle, out-of-scope is explicit, and no technology choices have crept in. Apply the rewrites you agree with; anything needing the human goes under Open questions.

## 5. Commit and stop
1. Commit `docs(problem): draft problem definition`.
2. Show the human: the problem statement, the capability table, the quality-attribute table, open questions, and the constraints raised so far.
3. Tell them: edit the file or reply with changes. Then two things, in either order:
   - `/aep:constraints` to capture target constraints (it can start while the problem is still being refined),
   - `/aep:approve problem` when the problem definition is right.

**Stop here.** No platform discussion, no specs, no code.
