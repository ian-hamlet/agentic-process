# Setting up a machine for AEP

There are two setup routes: **macOS on Apple Silicon** (section 1) and **Windows on Intel/AMD x64** (section 2). Everything after that is the same on both. Each step has a check; run it before moving on. Allow about 30 minutes.

## Baseline

| Requirement | Version |
|-------------|---------|
| .NET SDK | 10 or later. Projects must target `net10.0` or later; the build fails otherwise (rule D01). |
| Python | 3.9 or later, with PyYAML |
| git | Any recent version. On Windows, Git for Windows (Claude Code and the git hooks use its `sh`). |
| GitHub CLI (`gh`) | Any recent version |
| VS Code | Recent, with the C# Dev Kit and Claude Code extensions |

---

## 1. macOS (Apple Silicon)

Open **Terminal**.

| Step | Command | Check |
|------|---------|-------|
| Homebrew | Install from https://brew.sh | `brew --version` |
| git | `brew install git` | `git --version` |
| GitHub CLI | `brew install gh` | `gh --version` |
| .NET 10 SDK | `brew install --cask dotnet-sdk` | `dotnet --list-sdks` shows 10.x |
| PyYAML | `python3 -m pip install --user pyyaml` | `python3 -c "import yaml"` |
| gitleaks | `brew install gitleaks` | `gitleaks version` |
| VS Code | `brew install --cask visual-studio-code` | `code --version` |
| Extensions | `code --install-extension ms-dotnettools.csdevkit` then `code --install-extension anthropic.claude-code` | `code --list-extensions` |

**If `dotnet` says "bad CPU type"**, an Intel (x64) SDK is installed. Remove it, then install the cask above:

```bash
sudo rm -rf /usr/local/share/dotnet /etc/paths.d/dotnet
brew install --cask dotnet-sdk
# open a new terminal
dotnet --list-sdks
```

---

## 2. Windows (Intel/AMD x64)

Open **PowerShell** (not as administrator unless a step asks). `winget` is built into Windows 10 and 11.

| Step | Command | Check (in a new terminal) |
|------|---------|---------------------------|
| Git for Windows | `winget install --id Git.Git -e` | `git --version` |
| GitHub CLI | `winget install --id GitHub.cli -e` | `gh --version` |
| .NET 10 SDK | `winget install --id Microsoft.DotNet.SDK.10 -e` | `dotnet --list-sdks` shows 10.x |
| Python | `winget install --id Python.Python.3.12 -e` | `python --version` |
| PyYAML | `python -m pip install --user pyyaml` | `python -c "import yaml"` |
| gitleaks | `winget install --id Gitleaks.Gitleaks -e` | `gitleaks version` |
| VS Code | `winget install --id Microsoft.VisualStudioCode -e` | `code --version` |
| Extensions | `code --install-extension ms-dotnettools.csdevkit` then `code --install-extension anthropic.claude-code` | `code --list-extensions` |

Windows notes:

- **Close and reopen the terminal** after installing, so the new commands are on the PATH.
- **Python is `python`, not `python3`**, on Windows. The AEP hooks and git hooks find whichever works, so nothing needs changing. If `python` opens the Microsoft Store, turn off the "App execution aliases" for python in Settings → Apps → Advanced app settings.
- **Line endings**: AEP projects include a `.gitattributes` that keeps LF line endings in every checkout, so format checks agree with macOS and CI. No git setting is needed.
- **Claude Code** on Windows uses Git for Windows' bash to run commands and hooks, which is why Git for Windows is required.

---

## 3. Identity (both)

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
gh auth login          # GitHub.com → HTTPS → log in with a web browser
gh auth status         # check
```

## 4. The AEP plugin repository

Once, by its owner:

```bash
cd ~/development/agentic-process
gh repo create <owner>/agentic-process --private --source . --remote origin
git push -u origin main develop
```

Everyone else (macOS path shown; on Windows use e.g. `C:\dev\agentic-process`):

```bash
git clone https://github.com/<owner>/agentic-process.git ~/development/agentic-process
```

A private repository must be shared with each team member (GitHub → Settings → Collaborators, or an organisation team).

## 5. Install the plugin in Claude Code (both)

In a Claude Code session (the VS Code panel or a terminal):

```text
/plugin marketplace add ~/development/agentic-process
/plugin install aep@agentic-process
```

On Windows, give the Windows path of the clone, e.g. `/plugin marketplace add C:\dev\agentic-process`.

Restart the session, then type `/aep:` and check that the skills appear. To update later: `git pull` in the plugin repository, then `/plugin marketplace update agentic-process`.

## 6. Branch protection for each project repository

Agents never merge; GitHub enforces that through branch protection. On GitHub Free, branch protection works only on **public** repositories. A private repository needs GitHub Pro, Team or Enterprise.

For each of `develop` and `main` (the `gate` check exists once CI has run, but it can be named in advance). In Git Bash or macOS Terminal:

```bash
gh api -X PUT repos/<owner>/<repo>/branches/develop/protection --input - <<'EOF'
{
  "required_status_checks": { "strict": true, "contexts": ["gate"] },
  "enforce_admins": false,
  "required_pull_request_reviews": { "required_approving_review_count": 0 },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

`required_approving_review_count` is 0 because on a one-person project you cannot approve your own pull request; the PR is still required, and you still merge it yourself. Alternatively use the web page: repository → Settings → Branches → Add rule.

## 7. Start a project

In the project repository, with a clean working tree:

```bash
git checkout develop || git checkout -b develop
git push -u origin develop
```

Then in Claude Code: `/aep:frame`, and `/aep:adopt` if the project already has code. `/aep:status` always says what to do next.
