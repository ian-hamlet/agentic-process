#!/bin/sh
# Run a Python 3.9+ script with whichever interpreter this machine has.
# macOS/Linux usually have python3; Windows (Git Bash) usually has python or py,
# and may have a python3 Store stub that does not work, so each is tested first.
for p in python3 python py; do
  if command -v "$p" >/dev/null 2>&1 && \
     "$p" -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >/dev/null 2>&1; then
    exec "$p" "$@"
  fi
done
echo "AEP: Python 3.9+ not found, so AEP hooks are not running. See SETUP.md." >&2
exit 0
