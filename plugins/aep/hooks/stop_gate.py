#!/usr/bin/env python3
"""AEP Stop hook (process rule C08): the agent cannot finish a turn that changed
code while the fast tests fail.

Runs `commands.test_fast` from process/config.json when source or test files
differ from the integration branch or are uncommitted, unless:
  - the same code state already passed (remembered in .git/aep-last-green), or
  - the latest commit is a red-phase `test(...)` commit with nothing uncommitted
    (failing tests are expected between /aep:tests and /aep:implement).

On failure it exits 2 so the output goes back to the agent. If the agent has
already been sent back once (stop_hook_active), it lets the turn end but warns
the human.
"""
import hashlib
import json
import os
import pathlib
import subprocess
import sys


def run(args, cwd, timeout=30):
    try:
        r = subprocess.run(args, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout + r.stderr
    except Exception as exc:
        return 1, str(exc)


def project_root(start):
    p = pathlib.Path(start).resolve()
    for d in [p] + list(p.parents):
        if (d / "process" / "config.json").is_file():
            return d
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    root = project_root(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd())
    if root is None:
        return 0
    cfg = json.loads((root / "process" / "config.json").read_text(encoding="utf-8"))
    cmd = cfg.get("commands", {}).get("test_fast")
    if not cmd:
        return 0
    paths = cfg.get("paths", {})
    code_paths = list(paths.get("source", ["src"])) + list(paths.get("tests", ["tests"]))
    integration = cfg.get("branches", {}).get("integration", "develop")

    _, head = run(["git", "rev-parse", "HEAD"], root)
    _, dirty = run(["git", "status", "--porcelain", "--"] + code_paths, root)
    _, uncommitted = run(["git", "diff", "HEAD", "--"] + code_paths, root)
    code, vs_integration = run(["git", "diff", "--name-only", integration + "...HEAD", "--"] + code_paths, root)
    if not dirty.strip() and (code != 0 or not vs_integration.strip()):
        return 0  # no code changes in play

    _, subject = run(["git", "log", "-1", "--format=%s"], root)
    if not dirty.strip() and subject.startswith(("test(", "test:")):
        return 0  # red phase: failing tests are expected

    key = hashlib.sha256((head + dirty + uncommitted).encode()).hexdigest()
    stamp = root / ".git" / "aep-last-green"
    try:
        if stamp.read_text().strip() == key:
            return 0
    except OSError:
        pass

    try:
        r = subprocess.run(cmd, shell=True, cwd=str(root), capture_output=True, text=True, timeout=570)
        rc, out = r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        rc, out = 1, "fast tests timed out"

    if rc == 0:
        try:
            stamp.write_text(key)
        except OSError:
            pass
        return 0

    tail = "\n".join(out.strip().splitlines()[-60:])
    if data.get("stop_hook_active"):
        print(json.dumps({"systemMessage": "AEP: fast tests are still failing (`%s`). Do not treat this work as done." % cmd}))
        return 0
    sys.stderr.write("AEP Stop gate: fast tests fail (`%s`). Fix them before finishing, or explain to the human "
                     "why they fail.\n\n%s\n" % (cmd, tail))
    return 2


if __name__ == "__main__":
    sys.exit(main())
