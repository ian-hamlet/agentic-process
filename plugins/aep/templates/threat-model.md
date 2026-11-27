---
status: draft          # draft | approved
approved_by:
updated: [YYYY-MM-DD]
---
# Threat model

Keep this to a page or two. Update it whenever a spec says a trust boundary moved.

## Assets
| Asset | Why it matters |
|-------|----------------|
| [e.g. API key] | [what an attacker could do with it] |

## Actors
- [Legitimate user, operator, attacker on the network, malicious input file ...]

## Trust boundaries
| ID | Boundary | Data crossing it |
|----|----------|------------------|
| TB-1 | [e.g. app ↔ external API over HTTPS] | [credentials, responses] |

## Threats (STRIDE per boundary)
| Boundary | Threat | S/T/R/I/D/E | Mitigation | Status |
|----------|--------|-------------|------------|--------|
| TB-1 | [e.g. response spoofed or malformed] | T | [validate and bound all fields] | [planned / in place / RISK-nnn] |
