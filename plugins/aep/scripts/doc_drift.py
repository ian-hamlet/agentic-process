#!/usr/bin/env python3
"""AEP doc-drift check (process rule C05).

Fails if a fact declared in a document's frontmatter disagrees with the code,
so a document can repeat a fact (a version, a limit, a URL) without drifting.

Declare facts in a doc's frontmatter like this:

  ---
  facts:
    poll_interval_min_seconds:
      value: 15
      source: src/Program.cs
      pattern: 'MinInterval\\s*=\\s*(\\d+)'
  ---

`pattern` is a regular expression with one capture group, searched in `source`
(a path relative to the repository root).

Usage: python3 scripts/process/doc_drift.py      (needs PyYAML: pip install pyyaml)
"""
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    print("doc_drift: PyYAML is required (pip install pyyaml)")
    sys.exit(2)


def find_root():
    here = pathlib.Path.cwd().resolve()
    for p in [here] + list(here.parents):
        if (p / "process" / "config.json").is_file():
            return p
    return here


def main():
    root = find_root()
    failures, checked = 0, 0
    for doc in sorted((root / "docs").rglob("*.md")) if (root / "docs").is_dir() else []:
        text = doc.read_text(encoding="utf-8", errors="ignore")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end < 0:
            continue
        try:
            meta = yaml.safe_load(text[3:end]) or {}
        except yaml.YAMLError as exc:
            print("%s: frontmatter is not valid YAML: %s" % (doc.relative_to(root), exc))
            failures += 1
            continue
        facts = meta.get("facts") if isinstance(meta, dict) else None
        for name, fact in (facts or {}).items():
            checked += 1
            source = root / str(fact.get("source", ""))
            if not source.is_file():
                print("%s: fact %s points at missing file %s" % (doc.relative_to(root), name, fact.get("source")))
                failures += 1
                continue
            match = re.search(str(fact.get("pattern", "")), source.read_text(encoding="utf-8", errors="ignore"))
            actual = match.group(1) if match and match.groups() else None
            if str(fact.get("value")) != actual:
                print("%s: %s is %r in the doc, %r in %s" % (doc.relative_to(root), name, fact.get("value"),
                                                             actual, fact.get("source")))
                failures += 1
    print("doc_drift: %d facts checked, %d failures" % (checked, failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
