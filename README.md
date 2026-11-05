# dev-process

A Claude Code plugin that packages the way the WeakSquare Chess Trainer was built: you bring an app idea, and Claude turns it into a requirements document, an architecture, and a roadmap of small versions. It then builds them one at a time, with independent QA and a stop for your manual test before each version is signed off.

## What's in it

| Piece | What it does |
|---|---|
| `/new-app` (skill) | Interviews you about the idea, then writes the project charter (CLAUDE.md, REQUIREMENTS.md with IDs, ARCHITECTURE.md, ROADMAP.md, CHANGELOG, User and Developer guides) and the guardrails (secret-guard hook, gitleaks, pre-commit, docs check, CI). It writes no product code. |
| `/build-version` (skill) | The 9-step loop for the next version: plan (you approve it) → build → self-check → independent QA → fix loop with regression tests → `v0.x-rc1` handoff → **stops** for your manual test → fixes → your sign-off → `v0.x` tag. It also resumes a version after `/clear`. |
| `qa-tester` (agent) | Independent QA with a fresh context. It verifies every *Done when* item with evidence, writes missing tests, checks scope, security and docs, and never fixes product code. |
| `skills/new-app/templates/` | The document skeletons, `check_docs.py`, and the guardrail configs that `/new-app` copies into a new repo. |

## Install

From this folder, while you're trying it out locally. Edits here are picked up by `/reload-plugins`:

```
claude plugin marketplace add C:\lab\code\dev-process
claude plugin install dev-process@dev-process
```

Once it's on GitHub:

```
/plugin install dev-process --marketplace adamwp1993/dev-process
```

Choose the **user** scope so it's available in every project.

## Use

1. Make an empty folder, start Claude Code in it, and run `/new-app` with your idea or requirements.
2. Answer the interview, then review REQUIREMENTS.md and ROADMAP.md. Scope is cheapest to change now.
3. Run `pre-commit install` once in the new repo.
4. In a fresh session, run `/build-version`. Repeat for each version after you sign off the previous one.

## Changing the process

Edit the skills and templates here, bump `version` in `.claude-plugin/plugin.json`, and commit. When something in a project shows the process should change (as the memory notes in WeakSquare did), change it here so the next app gets it too.

## Licence

MIT. See [LICENSE](LICENSE). Projects you start from these templates are yours to license however you like.
