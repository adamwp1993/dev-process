# {{APP_NAME}}: Developer Guide

The single source for commands. QA runs every command here exactly as written, so keep them working in {{OWNER}}'s shell ({{SHELL_NOTE, e.g. "PowerShell with the AllSigned policy: use npm.cmd, npx.cmd and uv run, never .ps1 scripts or venv activation"}}).

## Prerequisites
- {{runtime and tools, with versions}}

## Commands
| What | Command |
|---|---|
| Set up | TODO(v0.1) |
| Run the app (dev data folder) | TODO(v0.1) |
| Tests | TODO(v0.1) |
| Lint and type checks | TODO(v0.1) |
| End-to-end tests | TODO(v0.1) |
| Docs check | `python scripts/check_docs.py` (`--strict` before a handoff) |
| Secret scan | `pre-commit run --all-files` (once: `pre-commit install`) |

## Where things are
See ARCHITECTURE.md §2.

## Data and configuration
TODO(v0.1)

## Testing
TODO(v0.1)

## Dependencies
Add one only if the version's approved plan lists it. Use the package manager, commit the lockfile, and add an ARCHITECTURE.md §7 entry.

## Releasing a version
Follow ROADMAP.md, "How every version is built and tested", steps 6 and 9.
