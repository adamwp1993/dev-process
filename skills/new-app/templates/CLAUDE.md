# CLAUDE.md: {{APP_NAME}}

{{ONE_PARAGRAPH: what the app is, who it's for, licence, platform.}} The owner is **{{OWNER}}**. Read these before starting any work:
- **REQUIREMENTS.md**: what to build (the source of truth for behavior)
- **ARCHITECTURE.md**: how the code is organized (layers, layout, locked decisions)
- **ROADMAP.md**: which version you're building now, and its *Done when* checklist
- **docs/DEVELOPER_GUIDE.md**: the commands to set up, run and test the app

## Stack
<!-- One bullet per layer: language/runtime, UI, storage, external services, secrets, test tools. -->
- {{STACK}}

## Build order (ROADMAP.md)
- Build **one version at a time**, in order. Use the `/build-version` skill (dev-process plugin). Ask {{OWNER}} which version is current if it's unclear.
- **Build only what the current version lists.** You may add an *interface* a later version will implement (ARCHITECTURE.md §4), but no placeholder code, no dead UI and no "while I'm here" features.
- Follow the 9-step process in ROADMAP.md: plan → build → self-check → **`qa-tester` subagent** → fix loop → tag `v0.x-rc1` + handoff → **stop** for {{OWNER}}'s manual test → fixes → {{OWNER}} signs off → tag `v0.x`. Don't start the next version until {{OWNER}} signs off.
- Every bug fix (from QA or {{OWNER}}) comes with a regression test.
- Respect the layers (ARCHITECTURE.md §1) and the locked decisions (§3).
  <!-- Repeat the 3–6 locked rules a builder is most likely to break, e.g. "core/ does no I/O", "only app.py wires adapters", "every external call goes through adapters/http.py". -->
- **Saving the plan:** save the approved plan to `plans/v0.x.md` as a checklist and tick items as they land. After a `/clear` or a context reset, re-read it before doing anything else.
- **Dependencies:** add a package only if it's in the approved plan. Check the exact name on its registry first, add it with the package manager so the lockfile stays in sync, and commit the lockfile. Each new dependency gets an ARCHITECTURE.md §7 entry.
- **Branches:** each version lives on branch `v0.x`, merged to `main` at sign-off. {{OWNER}} may check out an rc tag in this folder, which detaches HEAD, so check `git branch --show-current` before committing.
<!-- Shell section: keep it if the owner's shell has constraints. WeakSquare's version: -->
- **Shells:** {{OWNER}}'s PowerShell runs with the **AllSigned** execution policy, which blocks unsigned `.ps1` files (`npm.ps1`, `npx.ps1`, a venv's `Activate.ps1`). You run in Git Bash, so a command that works for you can fail for {{OWNER}}.
  - Commands written for humans use `npm.cmd`, `npx.cmd` and `uv run …`.
  - Never write `.ps1` scripts or tell anyone to activate the venv.
  - Python scripts find npm with `shutil.which("npm")`.
- Schema changes are **new migration files only**. Never edit an applied migration.

## Rules
- **Secrets:**
  - Never read, print, echo or log a credential, including from the shell. A PreToolUse hook blocks attempts. If a step needs a real credential, stop and ask {{OWNER}} to run it.
  - Never write a real-looking token or key into any file. Test placeholders look fake (`sk-ant-FAKE…`).
  - Only `{{SECRET_MODULE}}` may touch the OS keyring.
  - Don't try to edit `.claude/`, `.gitleaks.toml` or `.pre-commit-config.yaml`. They're {{OWNER}}'s guardrails, and edits are denied.
- **Privacy:** {{WHAT_MAY_LEAVE_THE_MACHINE}}. Any feature that sends data off the PC says exactly what it sends (User Guide, "Your data and privacy").
<!-- If the app calls paid APIs or LLMs, keep this and the next rule. -->
- **Paid APIs:** a pre-run estimate, a per-run cap, a monthly budget and a hard `max_tokens` on every call. Prices come from data, never code, and model names live in one defaults module.
- **Untrusted output** (LLM or external API) is validated before use and rendered escaped.
- If a decision changes, update REQUIREMENTS.md in the same change.

## Documentation (update as you go, not at the end)
Docs change **in the same commit** as the code they describe. A version isn't done until its docs are.
- **CHANGELOG.md:** one line under `[Unreleased]` per user-visible change, following the rules at the top of that file.
- **docs/USER_GUIDE.md:** every feature, setting and screen the user can see, written for the person using the app ("you"). Shipped features only; each section is marked *Added in v0.x*. Screenshots come from a scripted spec and are never hand-edited.
- **docs/DEVELOPER_GUIDE.md:** the single source for commands. When you add or change a command, update it there and replace the matching `TODO(v0.x)` marker. QA runs every command in it as written.
- **ARCHITECTURE.md §7 decision log:** an entry for every new dependency, schema shape, protocol change or workaround; update §2 if the layout changes.
- **README.md:** keep the description and status line true.
- Run `python scripts/check_docs.py` during the self-check and `--strict` before the handoff. Both must pass.

## Commands
See the Commands table in docs/DEVELOPER_GUIDE.md. Read it at the start of each session; it replaces this section.
