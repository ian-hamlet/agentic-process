#!/usr/bin/env python3
"""AEP PreToolUse guard (process rules C09, C10).

Blocks, in AEP projects only (those with process/config.json):
  - commits, merges, cherry-picks and pushes on or to the protected branches
  - force pushes, `git reset --hard`, `git clean -f`
  - piping a download into a shell, `rm -rf` of /, ~ or ..
  - reading or writing .env files or anything under secrets/

Exit code 2 blocks the tool call and shows the reason to the agent.
"""
import json
import os
import pathlib
import re
import subprocess
import sys

SAFE_ENV = re.compile(r"\.env\.(example|sample|template)\b")
ENV_FILE = re.compile(r"(^|[\s/'\"=<>])\.env(\.[\w-]+)?(?![\w.-])")
SECRETS = re.compile(r"(^|[\s/'\"=<>])secrets/")
SEG = r"[^;&|\n]*"  # stay within one shell command segment


def project_root(start):
    p = pathlib.Path(start).resolve()
    for d in [p] + list(p.parents):
        if (d / "process" / "config.json").is_file():
            return d
    return None


def current_branch(cwd):
    try:
        out = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd,
                             capture_output=True, text=True, timeout=5)
        return out.stdout.strip()
    except Exception:
        return ""


def mentions_secret(text):
    cleaned = SAFE_ENV.sub("", text)
    return bool(ENV_FILE.search(cleaned) or SECRETS.search(cleaned))


def check_bash(cmd, cwd, protected):
    reasons = []
    branch = current_branch(cwd)
    prot = "|".join(re.escape(b) for b in protected)

    for m in re.finditer(r"\bgit\b(%s)" % SEG, cmd):
        seg = m.group(1)
        words = seg.split()
        sub = next((w for w in words if not w.startswith("-")), "")
        if sub == "push":
            if re.search(r"(--force\b|--force-with-lease|\s-f\b|\s\+\S)", seg):
                reasons.append("force push is not allowed")
            if re.search(r"(\s|:)(%s)(\s|$)" % prot, seg + " "):
                reasons.append("agents do not push to %s" % "/".join(protected))
            elif len([w for w in words if not w.startswith("-")]) <= 2 and branch in protected:
                reasons.append("agents do not push %s (you are on it)" % branch)
        elif sub in ("commit", "merge", "cherry-pick", "revert", "am", "rebase") and branch in protected:
            reasons.append("agents do not %s on %s; work on a feat/, fix/ or chore/ branch" % (sub, branch))
        elif sub == "reset" and "--hard" in seg:
            reasons.append("`git reset --hard` discards work; a human should run it")
        elif sub == "clean" and re.search(r"\s-[a-zA-Z]*f", seg):
            reasons.append("`git clean -f` deletes untracked files; a human should run it")

    if re.search(r"\b(curl|wget)\b[^|;&]*\|\s*(sudo\s+)?(ba|z|da)?sh\b", cmd):
        reasons.append("piping a download into a shell is not allowed")
    if re.search(r"\brm\s+(-[a-zA-Z]+\s+)*-[a-zA-Z]*r[a-zA-Z]*\s+(-[a-zA-Z]+\s+)*(/|~|\$HOME|\.\.)(\s|/|$)", cmd):
        reasons.append("recursive delete of /, ~ or .. is not allowed")
    if mentions_secret(cmd):
        reasons.append("commands may not touch .env files or secrets/")
    return reasons


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    cwd = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    root = project_root(cwd)
    if root is None:
        return 0  # not an AEP project
    try:
        cfg = json.loads((root / "process" / "config.json").read_text(encoding="utf-8"))
    except Exception:
        cfg = {}
    branches = cfg.get("branches", {})
    protected = sorted({"main", "master", branches.get("integration", "develop"), branches.get("release", "main")})

    tool = data.get("tool_name", "")
    tin = data.get("tool_input", {}) or {}
    if tool == "Bash":
        reasons = check_bash(tin.get("command", ""), cwd, protected)
    else:
        path = str(tin.get("file_path", ""))
        reasons = ["agents may not read or write .env files or secrets/"] if path and mentions_secret(" " + path) else []

    if reasons:
        sys.stderr.write("AEP guard blocked this: " + "; ".join(dict.fromkeys(reasons)) +
                         ".\nSee process/PROCESS.md section 5. If it is really needed, ask the human to do it.\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
