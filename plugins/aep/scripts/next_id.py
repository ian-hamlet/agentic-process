#!/usr/bin/env python3
"""Print the next free ID for an AEP prefix.

IDs are global to the repository and never reused. Only the places where IDs
are defined are scanned, so examples in other documents do not count.

Usage:
  python3 scripts/process/next_id.py SPEC
  python3 scripts/process/next_id.py AC --count 5     # five consecutive IDs
Prefixes: CAP QA CON SPEC REQ AC ADR DEF RISK DEC
"""
import argparse
import json
import pathlib
import re
import sys

SKIP_DIRS = {".git", "bin", "obj", "node_modules", ".venv", "venv", "__pycache__", "TestResults"}


def find_root():
    here = pathlib.Path.cwd().resolve()
    for p in [here] + list(here.parents):
        if (p / "process" / "config.json").is_file():
            return p
    return here


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prefix", choices=["CAP", "QA", "CON", "SPEC", "REQ", "AC", "ADR", "DEF", "RISK", "DEC"])
    ap.add_argument("--count", type=int, default=1)
    args = ap.parse_args()

    root = find_root()
    cfg_file = root / "process" / "config.json"
    cfg = json.loads(cfg_file.read_text(encoding="utf-8")) if cfg_file.is_file() else {}
    paths = cfg.get("paths", {})
    specs = paths.get("specs", "docs/specs")
    where = {
        "CAP": ["docs/product"],
        "QA": ["docs/product"],
        "CON": ["docs/product"],
        "SPEC": [specs],
        "REQ": [specs],
        "AC": [specs] + paths.get("tests", ["tests"]),
        "ADR": ["docs/architecture/adr"],
        "DEF": ["docs/records"],
        "RISK": ["docs/records"],
        "DEC": ["docs/records"],
    }[args.prefix]

    pattern = re.compile(r"\b%s[-_](\d{3,})(?!\d)" % args.prefix)
    highest = 0
    for rel in where:
        base = root / rel
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if set(p.parts) & SKIP_DIRS:
                continue
            for n in pattern.findall(p.name):
                highest = max(highest, int(n))
            if p.is_file() and p.stat().st_size < 2000000:
                for n in pattern.findall(p.read_text(encoding="utf-8", errors="ignore")):
                    highest = max(highest, int(n))

    for i in range(1, args.count + 1):
        print("%s-%03d" % (args.prefix, highest + i))
    return 0


if __name__ == "__main__":
    sys.exit(main())
