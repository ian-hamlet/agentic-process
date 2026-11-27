# Stack profiles

A stack profile turns a platform decision (ADR-001) into tooling: build and test commands, strict compiler or linter settings, the full CI gate, a pre-commit hook, and rules for the constraints the platform must meet. `/aep:platform` reads this catalogue when comparing candidates, and `/aep:platform apply` installs the chosen profile.

| Profile | Languages and runtime | Runs on | Suits | Constraint-driven settings |
|---------|----------------------|---------|-------|----------------------------|
| [dotnet](dotnet/profile.md) | C# on .NET 10 or later | Windows, macOS, Linux; x64 and ARM64; containers; Azure, AWS | Console tools, services, web APIs, desktop (Windows), libraries | Minimum .NET version (D01), pinned SDK (D03) |

## Adding a profile

When ADR-001 chooses a platform with no profile, writing the profile is the next piece of work, done in this repository. Use `dotnet/` as the model. A profile needs:

1. `profile.md` with the same sections: Suits, Baseline rules (with what enforces each), Tools table, Layout, Test conventions (AC IDs in test names, integration-test marker), Red phase notes, Files table.
2. `config.example.json` with `stack`, `commands` (build, test_fast, test_all, format_check, format_fix, run) and paths.
3. A CI workflow whose job is named `gate`, including the core steps from `templates/ci-core.yml` plus format, build or lint with warnings as errors, a placeholder check, tests with coverage threshold and a dependency audit.
4. A pre-commit hook including the core steps from `templates/pre-commit-core`.
5. Strictness settings for the build or linter, and editor settings.
6. A row in the table above.
