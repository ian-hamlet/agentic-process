# Architecture lens

## Triggers
New projects, modules, folders or namespaces; new package dependencies; changes to project files; a change that touches more than one layer.

## Checklist
- [ ] Dependencies point the way overview.md allows (domain depends on nothing)
- [ ] Domain logic has no I/O: no network, file, console, clock or environment access
- [ ] I/O sits behind an interface (port) so it can be faked in tests
- [ ] No logic duplicated from elsewhere, especially for operations invariants.md assigns to one module
- [ ] New dependency or structural choice has an ADR, or is too small to need one
- [ ] Public types and methods are the minimum needed; internals stay internal
- [ ] Configuration is read in one place and passed in, not read deep inside logic
- [ ] Names match the language of the spec (the same nouns and verbs)
