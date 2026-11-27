# Security lens

## Triggers
Paths: anything under an adapters, http, api, auth, io, config or crypto folder; project or package files.
Topics: command-line or file input, network calls, credentials, API keys, tokens, serialisation, logging, new dependencies.

## Checklist
- [ ] Every entry point validates input type, size, range and format; malformed input fails safely
- [ ] Data from external services is treated as untrusted and validated before use
- [ ] Secrets come from the environment or a secret store; none in code, config files, logs, errors or exception messages
- [ ] Credentials are sent only over TLS to the expected hosts; certificate checks are not disabled
- [ ] Outbound requests cannot be redirected to arbitrary or internal addresses by input
- [ ] Queries, shell commands, paths and templates are parameterised; no string-built commands
- [ ] File paths from input cannot escape the intended directory
- [ ] Error messages shown to users reveal no internals or secrets
- [ ] Retries and polling have limits and back-off; nothing can be made to loop or flood a service
- [ ] Crypto uses a vetted library with safe defaults; no custom crypto
- [ ] New dependencies are maintained, licensed acceptably and free of known vulnerabilities
- [ ] threat-model.md is updated if a trust boundary moved
