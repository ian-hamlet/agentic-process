# .NET profile

Used by `/aep:frame` when the repository contains `*.sln`, `*.slnx` or `*.csproj` files.

## Tools

| Concern | Tool | Where it runs |
|---------|------|---------------|
| Format | `dotnet format` with `.editorconfig` | pre-commit hook, CI |
| Lint and types | Roslyn analyzers, nullable reference types, warnings as errors (`Directory.Build.props`) | every build, CI |
| Tests | xUnit | Stop hook (fast), CI (all) |
| Coverage | coverlet.msbuild, threshold from `coverage_threshold` | CI |
| Property-based tests | FsCheck.Xunit | in tests |
| Architecture rules | NetArchTest.Rules, as ordinary tests in the test project | CI |
| Vulnerable packages | `dotnet list package --vulnerable --include-transitive` | CI |
| Secret scan | gitleaks | CI (and pre-commit if installed) |
| Placeholders | grep for TODO, FIXME, NotImplementedException in source | CI |

## Layout

```text
<Name>.sln                        # at the repo root; CI and dotnet format use it
src/<Name>/                       # one or more projects; split Domain/Adapters when the code grows
tests/<Name>.Tests/               # xUnit project referencing src projects
Directory.Build.props             # strictness for every project
.editorconfig
```

## Test conventions

- Test method names start with the AC ID: `AC_001_Rejects_interval_below_15_seconds`.
- Integration tests (real network, disk or process) carry `[Trait("Category", "Integration")]` and are excluded from the fast suite.
- Architecture rules are tests named `ARCH_<rule>` and do not need an AC.
- Fakes are hand-written classes implementing the port interface. Avoid mocking libraries for domain code.

## Test project packages

```bash
dotnet new xunit -o tests/<Name>.Tests
dotnet add tests/<Name>.Tests package coverlet.msbuild
dotnet add tests/<Name>.Tests package FsCheck.Xunit
dotnet add tests/<Name>.Tests package NetArchTest.Rules
dotnet add tests/<Name>.Tests reference src/<Name>/<Name>.csproj
dotnet sln add tests/<Name>.Tests
```

To test `internal` types, add `<InternalsVisibleTo Include="<Name>.Tests" />` in an `<ItemGroup>` of the source project.

## Red phase in a compiled language

Tests that reference types or methods that do not exist yet will not compile. In the red phase the implementer adds compile-only stubs that `throw new NotImplementedException()`, so tests fail at run time for the right reason. CI's placeholder check fails while stubs remain, which is intended: the branch cannot merge until `/aep:implement` replaces them.

## Files in this profile

| File | Copied to |
|------|-----------|
| `config.example.json` | `process/config.json` (paths and names filled in) |
| `Directory.Build.props` | `Directory.Build.props` |
| `editorconfig` | `.editorconfig` |
| `github/ci.yml` | `.github/workflows/ci.yml` |
| `githooks/pre-commit` | `.githooks/pre-commit` (executable) |
| `vscode/tasks.json`, `vscode/extensions.json` | `.vscode/` |
