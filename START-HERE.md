# Start here: a new project with AEP

A printable checklist for starting a project with the Agentic Engineering Process (AEP). Work top to bottom. For background, see GETTING-STARTED.md; for installing tools, see SETUP.md.

**The idea in one line:** define the problem, then the constraints, then choose the platform. After that, every feature goes spec → test plan → tests → code → review → pull request. Claude does the work and stops whenever a decision is yours.

---

## 1. Check your machine (2 minutes)

Run these in a terminal. If any fails, fix it with SETUP.md (macOS section 1, Windows section 2).

| Check | Expect |
|-------|--------|
| `dotnet --list-sdks` | a 10.x line |
| `gh auth status` | Logged in to github.com |
| `python3 -c "import yaml"` (Windows: `python`) | no output |
| `gitleaks version` | a version number |
| `code --version` | a version number |

---

## 2. Create the repository (5 minutes)

Replace `NAME` with the project name. Public lets branch protection work on GitHub Free; choose private if the client's information is confidential (branch protection then needs a paid plan).

```bash
cd ~/development
gh repo create ian-hamlet/NAME --public --add-readme --clone
cd NAME
git checkout -b develop
git push -u origin develop
```

Protect `main` and `develop` (every change then goes through a pull request, including yours):

```bash
for b in main develop; do
gh api -X PUT repos/ian-hamlet/NAME/branches/$b/protection --input - >/dev/null <<'EOF' && echo "$b protected"
{"required_status_checks": null, "enforce_admins": true,
 "required_pull_request_reviews": {"required_approving_review_count": 0},
 "restrictions": null, "allow_force_pushes": false, "allow_deletions": false}
EOF
done
```

Open it: `code .`

---

## 3. Make sure the plugin is there (1 minute)

In VS Code, open the **Claude Code** panel and type `/aep:`. You should see `frame`, `problem`, `status` and others.

If not, type these, then start a new Claude Code session:

```text
/plugin marketplace add ~/development/agentic-process
/plugin install aep@agentic-process
```

To pick up the latest process first: `cd ~/development/agentic-process && git pull`.

---

## 4. Run the process

Type the command in the Claude Code panel. **You** columns are your jobs.

| Step | Type | Claude does | You |
|------|------|-------------|-----|
| 1 | `/aep:frame` | Installs the process: config, checks, hooks, CI. No technology yet. | Push the branch it names, open the PR on GitHub, merge it |
| 2 | `/aep:problem` | Interviews you, writes `docs/product/problem.md` | Answer; read the file; correct it |
| 3 | `/aep:constraints` | Interviews you about how it must be built, writes `constraints.md` | Answer; find out unknowns from the client |
| 4 | `/aep:approve problem` then `/aep:approve constraints` | Checks completeness, records your approval | Confirm |
| 5 | `/aep:platform` | Compares 2–3 platforms against your constraints, writes ADR-001 | Read the comparison; change the decision if you disagree |
| 6 | `/aep:approve adr ADR-001` then `/aep:platform apply` | Installs the stack, skeleton project, full CI | Push, open PR, merge when CI is green |
| 7 | `/aep:spec "<a must-have capability>"` | Drafts requirements with Given/When/Then criteria | Read, correct, then `/aep:approve spec SPEC-001` |
| 8 | `/aep:test-plan` | Maps every criterion to named tests | Read, then `/aep:approve test-plan SPEC-001` |
| 9 | `/aep:tests`, `/aep:implement`, `/aep:review` | Failing tests, then code one criterion at a time, then four reviewers | Watch; answer questions |
| 10 | `/aep:pr` | Opens the pull request with a requirement-to-test table | Check CI is green, review, merge |

Repeat steps 7–10 for each capability.

**Lost?** Type `/aep:status`. It reads the documents in the repo and tells you where you are and what to type next. The repo itself is the memory: nothing depends on remembering a previous session.

---

## 5. Think about these before `/aep:problem`

Jot down rough answers; the interview goes faster and better. No technology at this stage.

**The problem**
- Who has the problem? What happens today, and what does it cost them?
- Why solve it now?

**Outcomes**
- How will you know it worked? Put a number on it (time saved, errors avoided, delay reduced).

**Capabilities**
- The five to ten things it must be able to do. Which are must, should, could?
- What will it deliberately **not** do?

**Quality**
- How fast, how reliable, how secure, how easy to change does it need to be? Think of a concrete situation for each ("when 100 readings arrive at once, ...").

**Rules of the domain**
- What must always be true, whatever the code does? ("a reading is never assigned to the wrong device")

**Information**
- What data does it hold or touch? How sensitive is it (secrets, personal data)?

## 6. Think about these before `/aep:constraints`

Ask the client where you don't know. "Don't know" is fine; guessing is not.

- **Where it runs**: cloud (which), servers, desktop, phone, browser, device?
- **OS and CPU**: Windows, macOS, Linux; Intel/AMD or ARM?
- **Client standards**: required languages and minimum versions (e.g. .NET 10 or later)? Banned ones?
- **Existing systems**: what must it connect to (sign-in, APIs, databases)?
- **Data**: where may it be stored, for how long, under which rules (e.g. GDPR)?
- **Security and compliance**: certifications, audits, penetration tests?
- **Operations**: who runs it, who supports it, what availability is promised?
- **Licensing and cost**: open-source rules, hosting budget?
- **People**: who will maintain it, and what do they know?
- **Delivery**: deadlines, test environments, approvals?

---

## 7. Ground rules

- **Read before you approve.** Approvals are the point where your judgment matters most; they are recorded with your name.
- **Do not skip stages.** Claude will refuse to write a spec before the platform is decided, or code before the tests.
- **Every change is a pull request**, and only you merge.
- **Note surprises** about what the agents did; they feed the retrospective (`/aep:retro`) and improve the process.
- **Rough times count.** When asked how long a review took, a guess is fine; the numbers let us compare projects.
- **A good first problem** is small (about three weeks part-time), has real rules to protect, and takes input you cannot trust.
