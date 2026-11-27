---
status: draft          # draft | approved
approved_by:
---
# Invariants

Rules that must never break. Each has an ID, the one module allowed to implement it (if any), and how it is tested. Keep the list to five to ten.

| ID | Invariant | Sole implementation | Tested by |
|----|-----------|---------------------|-----------|
| INV-1 | [e.g. Secrets are never written to logs or files] | [module/class] | [property test name or lint rule] |
| INV-2 | | | |
