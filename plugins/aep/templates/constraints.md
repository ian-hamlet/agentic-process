---
status: draft          # draft | approved
client: [client or organisation these constraints come from]
confidential: false    # true if this must not be published; check repository visibility
approved_by:
approved_on:
human_min:
---
# Target constraints

Constraints limit how we may build the solution. They come from the client, regulation or our own organisation; they are requirements, not design preferences. The platform decision (ADR-001) must satisfy every **hard** constraint and should satisfy the **soft** ones. Each constraint says how we will check it is met.

| ID | Category | Constraint | Source | Hard / soft | How verified |
|----|----------|------------|--------|-------------|--------------|
| CON-001 | [category from the list below] | [e.g. runs on the client's Windows 11 x64 laptops without admin rights] | [client IT standard, dated] | hard | [CI build for win-x64; installation test] |

## Categories to cover
Every category is answered, even if the answer is "no constraint". Unknowns go under Open questions with the person who can answer.

1. **Where it runs**: cloud (which), on-premises servers, desktop, mobile, browser, embedded device.
2. **Operating system and CPU**: Windows, macOS, Linux; x64, ARM64; minimum versions.
3. **Client technology standards**: required or banned languages, frameworks and minimum versions (e.g. ".NET 10 or later").
4. **Existing systems**: what it must integrate with (identity, APIs, databases, messaging) and their interfaces.
5. **Data**: residency, retention, backup, privacy regulation (e.g. GDPR).
6. **Security and compliance**: certifications, authentication standards, penetration testing, audit.
7. **Operations**: who runs it, monitoring, support hours, availability commitments, release windows.
8. **Licensing and cost**: open-source licence rules, hosting budget, paid components.
9. **People**: skills of the team that will maintain it.
10. **Delivery**: deadlines, environments available (test, staging), approval processes.

## Open questions
[Unknown hard constraints block approval.]
- [ ] [Question] — ask: [person or role]
