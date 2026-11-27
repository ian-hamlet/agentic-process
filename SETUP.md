# Setting up a machine for AEP

Written for macOS on Apple Silicon. Each step has a check command; run it before moving on. Allow about 30 minutes.

## 1. Tools

| Tool | Why | Install | Check |
|------|-----|---------|-------|
| Homebrew | Installs the rest | https://brew.sh | `brew --version` |
| git | Version control | `brew install git` (or Xcode tools) | `git --version` |
| GitHub CLI | Create repos, open PRs, set branch protection | `brew install gh` | `gh --version` |
| .NET SDK (Arm64) | Build and test .NET projects | Installer from https://dotnet.microsoft.com/download (choose **Arm64**) | `dotnet --list-sdks` |
| Python 3.9+ | Traceability, drift and hook scripts | Included with macOS | `python3 --version` |
| PyYAML | Doc-drift check | `python3 -m pip install --user pyyaml` | `python3 -c "import yaml"` |
| gitleaks | Secret scan in the pre-commit hook (CI has its own) | `brew install gitleaks` | `gitleaks version` |
| VS Code | Editor | https://code.visualstudio.com | `code --version` |
| VS Code extensions | C#, Claude Code | `code --install-extension ms-dotnettools.csdevkit` and `code --install-extension anthropic.claude-code` | `code --list-extensions` |
| Claude Code CLI (optional) | Run Claude in a terminal; `claude plugin validate` | See https://docs.claude.com/en/docs/claude-code/setup | `claude --version` |

### .NET on Apple Silicon

If `dotnet --version` says **bad CPU type**, the Intel (x64) SDK is installed. Remove it and install the Arm64 one:

```bash
sudo rm -rf /usr/local/share/dotnet /etc/paths.d/dotnet
# then run the Arm64 installer from https://dotnet.microsoft.com/download
# open a new terminal, then:
dotnet --list-sdks
```

Which .NET version a project uses is the project's decision (record it as ADR-001). .NET 8 support ended on 10 November 2026; .NET 10 is the current long-term-support release.

## 2. Identity

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
gh auth login          # GitHub.com → HTTPS → log in with a web browser
gh auth status         # check
```

## 3. The AEP plugin repository (once, by its owner)

```bash
cd ~/development/agentic-process
gh repo create <owner>/agentic-process --private --source . --remote origin
git push -u origin main
git push -u origin develop
```

Everyone else clones it:

```bash
git clone https://github.com/<owner>/agentic-process.git ~/development/agentic-process
```

## 4. Install the plugin in Claude Code

In a Claude Code session (VS Code panel or terminal):

```text
/plugin marketplace add ~/development/agentic-process
/plugin install aep@agentic-process
```

Restart the session, then type `/aep:` and check that the skills appear. To update later: `git pull` in the plugin repo, then `/plugin marketplace update agentic-process`.

## 5. Branch protection for each project repository

Agents never merge; GitHub enforces that through branch protection. On GitHub Free, branch protection works only on **public** repositories. A private repository needs GitHub Pro, Team or Enterprise.

For each of `develop` and `main` (the `gate` check exists once CI has run, but it can be named in advance):

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

`required_approving_review_count` is 0 because on a one-person project you cannot approve your own pull request; the PR is still required, and you still merge it yourself.

## 6. Start a project

In the project repository, with a clean working tree:

```bash
git checkout develop || git checkout -b develop
git push -u origin develop
```

Then in Claude Code: `/aep:frame`, and `/aep:adopt` if the project already has code. `/aep:status` always says what to do next.
