#!/usr/bin/env python3
"""AEP traceability check (process rules C01-C04).

For every spec in the specs directory (default docs/specs/SPEC-nnn-slug/):
  C01  every AC in an approved spec appears in its test plan
  C02  every AC in an approved test plan has a test named after it
  C03  no test names an AC that is not defined in any spec
  C04  no AC is defined in more than one place

A spec's ACs are list items that start with the ID, e.g. "- **AC-001**: Given ...".
They belong to the nearest REQ heading above them, e.g. "### REQ-001: The system shall ...".
Tests reference an AC as AC-001 or AC_001 anywhere in a test file.

Usage:
  python3 scripts/process/traceability.py             # check, exit 1 on failure
  python3 scripts/process/traceability.py --matrix    # also print the traceability matrix
  python3 scripts/process/traceability.py --spec SPEC-001
"""
import argparse
import json
import pathlib
import re
import sys
from collections import OrderedDict

AC_DEF = re.compile(r"^\s*[-*]\s+\**(AC-\d{3})\b")
REQ_DEF = re.compile(r"^#{2,6}\s+\**(REQ-\d{3})\b")
AC_ANY = re.compile(r"\bAC[-_](\d{3})(?!\d)")
SPEC_ID = re.compile(r"SPEC-\d{3}")
ACTIVE = {"approved", "done"}
SKIP_DIRS = {".git", "bin", "obj", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", "TestResults"}
TEXT_SUFFIXES = {".cs", ".fs", ".vb", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".py", ".go", ".java", ".kt",
                 ".rb", ".rs", ".swift", ".feature", ".md", ".txt", ".json", ".yaml", ".yml"}


def find_root():
    here = pathlib.Path.cwd().resolve()
    for p in [here] + list(here.parents):
        if (p / "process" / "config.json").is_file():
            return p
    return here


def load_config(root):
    f = root / "process" / "config.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.is_file() else {}


def frontmatter(text):
    """Minimal flat 'key: value' frontmatter reader (no PyYAML needed)."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    meta = {}
    for line in text[3:end].splitlines():
        if not line or line[0] in " \t#" or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.split(" #", 1)[0].strip().strip("'\"")
        meta[key.strip()] = value
    return meta


class Spec(object):
    def __init__(self, folder):
        self.folder = folder
        text = (folder / "spec.md").read_text(encoding="utf-8", errors="ignore")
        meta = frontmatter(text)
        m = SPEC_ID.search(meta.get("id", "")) or SPEC_ID.search(folder.name)
        self.id = m.group(0) if m else folder.name
        self.status = meta.get("status", "draft").lower()
        self.acs = OrderedDict()  # AC -> REQ (or None)
        self.duplicates = []
        req = None
        for line in text.splitlines():
            m = REQ_DEF.match(line)
            if m:
                req = m.group(1)
                continue
            m = AC_DEF.match(line)
            if m:
                if m.group(1) in self.acs:
                    self.duplicates.append(m.group(1))
                else:
                    self.acs[m.group(1)] = req
        plan = folder / "test-plan.md"
        self.has_plan = plan.is_file()
        self.plan_status = "missing"
        self.plan_acs = set()
        if self.has_plan:
            ptext = plan.read_text(encoding="utf-8", errors="ignore")
            self.plan_status = frontmatter(ptext).get("status", "draft").lower()
            self.plan_acs = {"AC-" + n for n in AC_ANY.findall(ptext)}


def walk(paths):
    for base in paths:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES and not (set(p.parts) & SKIP_DIRS):
                yield p


def test_references(root, test_dirs):
    refs = {}
    for path in walk([root / d for d in test_dirs]):
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for n in AC_ANY.findall(line):
                refs.setdefault("AC-" + n, []).append("%s:%d" % (path.relative_to(root), lineno))
    return refs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--matrix", action="store_true", help="print the traceability matrix as Markdown")
    ap.add_argument("--spec", help="only report on this spec (checks still cover the whole repo)")
    args = ap.parse_args()

    root = find_root()
    cfg = load_config(root)
    paths = cfg.get("paths", {})
    specs_dir = root / paths.get("specs", "docs/specs")
    test_dirs = paths.get("tests", ["tests"])

    specs = [Spec(d) for d in sorted(specs_dir.glob("*")) if (d / "spec.md").is_file()] if specs_dir.is_dir() else []
    refs = test_references(root, test_dirs)
    errors, warnings = [], []

    defined = {}
    for s in specs:
        for ac in s.duplicates:
            errors.append("C04 %s defines %s more than once" % (s.id, ac))
        for ac in s.acs:
            if ac in defined:
                errors.append("C04 %s is defined in both %s and %s" % (ac, defined[ac], s.id))
            defined.setdefault(ac, s.id)

    for s in specs:
        if not s.acs:
            (errors if s.status in ACTIVE else warnings).append("%s (%s) has no acceptance criteria" % (s.id, s.status))
        if s.status in ACTIVE:
            if not s.has_plan:
                (errors if s.status == "done" else warnings).append("C01 %s is %s but has no test-plan.md" % (s.id, s.status))
            else:
                for ac in s.acs:
                    if ac not in s.plan_acs:
                        errors.append("C01 %s: %s is not in the test plan" % (s.id, ac))
        for ac in sorted(s.plan_acs - set(s.acs)):
            errors.append("C03 %s test plan names %s, which the spec does not define" % (s.id, ac))
        if s.plan_status in ACTIVE:
            for ac in s.acs:
                if ac not in refs:
                    errors.append("C02 %s: no test names %s" % (s.id, ac))

    for ac in sorted(set(refs) - set(defined)):
        errors.append("C03 tests name %s, which no spec defines (%s)" % (ac, ", ".join(refs[ac][:3])))

    if args.matrix:
        print("| Spec | Spec status | Plan status | REQ | AC | In plan | Tests |")
        print("|------|-------------|-------------|-----|----|---------|-------|")
        for s in specs:
            if args.spec and s.id != args.spec:
                continue
            if not s.acs:
                print("| %s | %s | %s | | | | |" % (s.id, s.status, s.plan_status))
            for ac, req in s.acs.items():
                tests = refs.get(ac, [])
                print("| %s | %s | %s | %s | %s | %s | %s |" % (
                    s.id, s.status, s.plan_status, req or "", ac,
                    "yes" if ac in s.plan_acs else "no",
                    "%d (%s)" % (len(tests), tests[0]) if tests else "none"))
        print()

    for w in warnings:
        print("WARN " + w)
    for e in errors:
        print("FAIL " + e)
    total_acs = sum(len(s.acs) for s in specs)
    print("traceability: %d specs, %d ACs, %d errors, %d warnings" % (len(specs), total_acs, len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
