---
name: new-app
description: Start a new app with the owner's versioned build process. Takes an idea or a requirements text, interviews the owner, then writes the project charter (CLAUDE.md, REQUIREMENTS.md with IDs, ARCHITECTURE.md with locked decisions, ROADMAP.md as small testable versions, CHANGELOG, User and Developer guides) plus the guardrails (secret-guard hook, gitleaks, pre-commit, docs check, CI). Building then goes version by version with /build-version. Use when the owner brings a new app idea or asks to set up a project "the way we built WeakSquare".
---

# Kick off a new app

The output is a repository that `/build-version` can build: the documents that define the app, and the guardrails. **No product code is written here.** v0.1 is built afterwards with `/build-version`, through its own plan approval.

The templates are in this skill's folder under `templates/`; the base directory is given when the skill loads. Each `{{PLACEHOLDER}}` gets filled in, and each `<!-- guidance -->` comment is replaced with real content or deleted.

## 1. Where and who
- Ask for the target folder, or suggest `<parent>/<app-slug>`.
- If the folder exists and isn't empty, stop and ask: it may be an existing project to adopt rather than a new one.
- `git init -b main`.
- The **owner**'s name goes in CLAUDE.md, because the process refers to the owner by name throughout.

## 2. Interview (AskUserQuestion, recommended option first, at most 4 questions a round)
Start from what the owner gave you. Ask only what the idea doesn't already answer, and offer a recommendation for each question. Cover:
1. **Purpose and users:** who it's for, the core loop, and the non-goals.
2. **Platform and shell:** OS, desktop/web/CLI/mobile, and the owner's shell constraints.
3. **Stack:** recommend one that fits the platform. The defaults below worked before.
4. **Data:** local or server, the database, any import of external data, and whether it needs migrations.
5. **External services:** APIs (auth, rate limits, terms that forbid things), anything paid, and LLMs.
6. **Security:** a round of its own, never skipped, even for a small local app. See "The security round" below.
7. **Privacy:** what may leave the machine. Every feature that sends data gets a "what is sent" rule.
8. **Public repo and licence:** if public, fixtures are scrubbed and anonymized. The licence is chosen by the owner.
9. **First usable version:** the smallest thing worth testing by hand (v0.1), and what "v1.0" means.

Then **recap every question and answer in chat**, flag your own defaults, and get a go-ahead before writing.

### The security round
Start with a short threat model in plain words: what's worth protecting (keys, accounts, the user's data, money spent through paid APIs), who could get at it (a leaked repo, a malicious dependency or download, hostile input from an API, a web page or an LLM, another program on the PC), and what the worst realistic outcome is. Then ask, with a recommendation for each:
1. **Credentials:** which keys, tokens or passwords the app holds.
   - Where they live: the OS credential store behind one module. Never a file, env var, log or UI payload.
   - How the user signs in: OAuth with PKCE where the service offers it, with the narrowest scopes.
   - How a user revokes access or signs out.
2. **What Claude may touch while building:**
   - Claude never reads or prints a credential. A step that needs one is run by the owner.
   - Live tests are opt-in and use a separate, scoped test credential on the owner's own account, with limits on what they write (e.g. unrated, at most N actions a run).
   - The guardrail files are owner-only.
3. **Leaks into the repo:**
   - Each service's token format becomes a guard and gitleaks rule.
   - Test placeholders are visibly fake.
   - Recorded HTTP fixtures are scrubbed when recorded, and anonymized (no real usernames, ids or URLs) if the repo is public.
   - A test enforces this.
4. **Untrusted input:** list every source: external APIs, imported files, LLM output, URLs and deep links.
   - Each is validated before use and rendered as escaped text, never raw HTML.
   - LLM output is never trusted to name a URL, command, file path or move without checking.
   - Anything passed to a subprocess or engine is validated first.
5. **Network:**
   - All HTTP goes through one adapter, with timeouts, a descriptive User-Agent, and rate limits that follow each service's terms.
   - Links the app opens are built by the app from an allowlist of hosts.
   - Debug ports and test hooks are enabled only by the test harness.
6. **Supply chain:**
   - A dependency is added only through an approved plan, after checking the exact name on its registry.
   - Lockfiles are committed. Dependency alerts are turned on once the repo is on GitHub.
   - Downloaded binaries come from a pinned manifest with a SHA-256 check before use, and are never committed.
7. **Money and quotas** (paid APIs): an estimate before each run, a per-run cap, a monthly budget, `max_tokens` on every call, and a guard against double submits spending twice.
8. **Local data:** what's stored and where, and whether any of it is sensitive enough to need encryption or a "delete my data" path. Dev runs and tests never use the real data folder. Logs never hold secrets or personal data.

The answers become the REQUIREMENTS **Security** section (`SR-` IDs, one testable sentence each), the CLAUDE.md "Secrets" and "Rules" bullets, the guard config's `project_patterns` and the gitleaks rules. `qa-tester`'s security check verifies each `SR-` ID.

### Defaults from the owner's last project (WeakSquare Chess Trainer); confirm, don't assume
- Windows 11, with PowerShell under the **AllSigned** execution policy, so unsigned `.ps1` files are blocked.
  - Human-facing commands use `npm.cmd`, `npx.cmd` and `uv run …`; never venv activation or `.ps1` scripts.
  - Python finds npm with `shutil.which("npm")`.
  - You run in Git Bash, so a command that works for you can still fail for the owner.
- **Python 3.12+** with **uv**, pytest, ruff and mypy. **React + TypeScript + Vite + Mantine** front end; ESLint, `tsc --noEmit` and Playwright e2e against a **mock API client**.
- A desktop shell via **pywebview**, with **SQLite** and numbered migration files (never edit an applied one).
- Secrets go through **keyring** behind one `secret_store` module; only that module imports keyring.
- **Layers:** a pure `core/` (no I/O, no wall-clock time or global randomness, so clock and rng are injected), `services/`, `adapters/` and a thin bridge. Only `app.py` wires the concrete adapters.
- **Paid APIs and LLMs:** a pre-run estimate, a per-run cap, a monthly budget, `max_tokens` on every call, and prices in a table rather than code. Untrusted output is validated before use. Prompts follow an allowlist of what may be sent.
- Docs are written in plain words for the person using the app, task first.

## 3. Write the charter (from `templates/`)

| File | What goes in it |
|---|---|
| `CLAUDE.md` | The rules Claude must follow in this repo: stack, build order, layers, locked decisions, secrets, privacy, the docs rules, the owner's shell. Keep it short: rules, not explanations. |
| `REQUIREMENTS.md` | Numbered sections with **IDs** (`FR-3.2`, `NFR-4`, `SR-7`), each a testable sentence. Note the decisions the owner made, with name and date. Add a "Verified external facts" section for API facts you checked. |
| `ARCHITECTURE.md` | §1 layers and the dependency rule, §2 repository layout, §3 **decisions locked in at v0.1**, §4 interfaces in the version that first needs them, §5 data-flow examples, §6 testing strategy, §7 the decision log. |
| `ROADMAP.md` | "How every version is built and tested" (the 9-step table and the checkpoint gate, copied from the template), then **v0.1 … v1.0**. Each version gets a goal, scope bullets with requirement IDs, **Done when** items (each automatable) and **the owner's manual test** (5–8 steps). Keep versions small enough to test by hand in under an hour, and put the riskiest integration early. |
| `CHANGELOG.md` | Keep a Changelog, with the entry rules at the top. |
| `README.md` | A paragraph saying what the app is, plus a status line ("Planning: v0.1 next"). |
| `docs/USER_GUIDE.md` | The title, an intro, the planned chapters as an HTML comment, and the privacy section. |
| `docs/DEVELOPER_GUIDE.md` | Prerequisites and a **Commands** table. Commands that don't exist yet get `TODO(v0.1)` markers. |
| `plans/`, `qa/` | Each starts with a one-line README. |

## 4. Guardrails (from `templates/guardrails/`)
- `.claude/settings.json`, `.claude/hooks/guard_secrets.py` and `.claude/hooks/guard_config.json`. Adapt only the config: `owner`, `secret_store_suffix` (null if the app stores no secrets) and `project_patterns` for the token formats of the services this app uses. Then run `python .claude/hooks/guard_secrets.py --self-test`. The settings deny Claude edits to `.claude/**`, `.gitleaks.toml` and `.pre-commit-config.yaml`, so from then on only the owner changes them. Tell the owner that.
- `.gitleaks.toml` and `.pre-commit-config.yaml`. Add a pygrep hook for the single-module secret rule if there is one.
- `scripts/check_docs.py`: set the project paths in its settings block.
- `.github/workflows/ci.yml`: static checks, tests and the docs check, on the owner's OS.
- `.gitignore` for the stack, data folders and test artifacts.

## 5. Finish
- Run `python scripts/check_docs.py` (it passes with an empty Unreleased section) and the hook's self-test.
- Commit the charter on `main`: "Project charter: requirements, architecture, roadmap, guardrails". Don't push. Creating the remote and pushing are the owner's call.
- Give the owner the next step: review REQUIREMENTS and ROADMAP (wrong scope is cheapest to fix now), then start a fresh session in the new folder and run `/build-version`.
- Tell them to run `pre-commit install` once, since it changes their git hooks.
