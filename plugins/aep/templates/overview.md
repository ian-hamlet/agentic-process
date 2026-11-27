---
status: draft          # draft | approved
approved_by:
---
# Architecture overview

## Layers and allowed dependencies
| Layer | Contains | May depend on |
|-------|----------|---------------|
| Domain | Pure rules and calculations, no I/O | nothing |
| Application | Use cases that orchestrate the domain | Domain, ports (interfaces) |
| Adapters | HTTP, files, clock, console, external APIs | Application, Domain |
| Host | Entry point, configuration, wiring | everything |

## Components
[One line per project/module: name, layer, responsibility.]

## External dependencies
[Services, packages that matter, and the ADR that chose them.]
