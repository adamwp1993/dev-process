# Roadmap: versions and test checkpoints

Each version is a **checkpoint**. Claude Code builds that version, an independent QA agent verifies it, then Claude Code **stops** and hands it to {{OWNER}} for manual testing. The next version starts only after {{OWNER}} signs off. Requirement IDs refer to REQUIREMENTS.md.

## How every version is built and tested

Each version lives on a branch (`v0.x`), merged to `main` only after {{OWNER}} signs off. The `/build-version` skill runs these steps.

| Step | Who | What |
|---|---|---|
| 1. Plan | Builder (plan mode) | Reads CLAUDE.md, ARCHITECTURE.md, this version's section and its requirement IDs, asks the questions that change the build, then proposes a plan: files, interfaces, tests, any new dependency with its purpose, and anything out of scope. Before approval it recaps every decision and flags its own choices. **{{OWNER}} approves** before any code is written. The plan is saved to `plans/v0.x.md` as a checklist and ticked off as work lands. |
| 2. Build | Builder | Small commits, running tests as it goes. Each commit that changes behavior also updates CHANGELOG `[Unreleased]` and the affected docs. |
| 3. Self-check | Builder | Every check in the Developer Guide (tests, linters, type checks, `pre-commit run --all-files`, e2e, screenshots) and `python scripts/check_docs.py --strict`. Everything green before QA. |
| 4. Independent QA | `qa-tester` subagent | Fresh context. Verifies every *Done when* item and requirement ID with evidence, writes missing tests under `tests/`, runs the real app, explores edge cases, checks scope, security and docs (runs every Developer Guide command, follows the new User Guide steps). Writes `qa/QA-v0.x.md`. Never fixes product code. |
| 5. Fix loop | Builder, then QA | Fix every blocker and major bug, with a regression test each (shown to fail on the old code). QA re-verifies and re-runs the suite. At most 3 rounds, then escalate to {{OWNER}}. |
| 6. Handoff | Builder | Add the rc to the CHANGELOG `Candidates:` line, commit, tag **`v0.x-rc1`**, and post: what's in, how to run it (`git checkout v0.x`, the branch, not the tag), known limits, the QA verdict and the manual checklist. Then **stop**. |
| 7. Manual test | **{{OWNER}}** | Run the checklist, plus free exploration. Read this version's User Guide sections and CHANGELOG entry against what you see; wrong or confusing docs are bugs too. |
| 8. Fix and re-test | Builder, QA, {{OWNER}} | Fix with regression tests → QA re-verifies if the fixes are large → {{OWNER}} re-checks. Re-tag `-rc2`, `-rc3`… as needed. |
| 9. Sign-off | {{OWNER}}, then builder | Rename CHANGELOG `[Unreleased]` to `[v0.x] - <date>` and open a new one, update the README status line, tag **`v0.x`**, merge to `main`. The next version starts in a **fresh session** (`/clear`). |

### Checkpoint gate (all must be true at step 6)
- [ ] All tests pass; the QA verdict is PASS or PASS WITH ISSUES (minor issues only).
- [ ] Static checks and `pre-commit run --all-files` (gitleaks included) are clean, and CI is green once the repo is on GitHub.
- [ ] No dependency was added that wasn't in the approved plan, and the lockfiles are committed.
- [ ] Nothing from a **later** version was built (interfaces only).
- [ ] `python scripts/check_docs.py --strict` passes.
- [ ] CHANGELOG `[Unreleased]` covers every user-visible *Done when* item.
- [ ] User Guide screenshots are regenerated, and QA ran every Developer Guide command as written.
- [ ] ARCHITECTURE.md §2 and §7 are updated if the structure changed or a decision was made.

---

<!-- One section per version, v0.1 first. Keep each small enough for a manual test under an hour; put the riskiest integration early. -->
## v0.1: {{FIRST_VERSION_NAME}} (MVP)
**Goal:** {{the smallest thing worth testing by hand}}
- {{scope bullet}} (FR-x.y)
- **Docs:** {{User Guide chapters this version adds}}

**Done when:**
- {{an automatable check}} (test)

**{{OWNER}}'s manual test:** {{5–8 steps a person does in the running app}}

---

## v1.0: {{RELEASE_NAME}}
- {{scope}}

**Done when:** {{…}}
**{{OWNER}}'s manual test:** {{…}}

---

## After v1.0 (parked ideas, not committed)
- {{idea}}
