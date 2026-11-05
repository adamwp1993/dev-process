---
name: build-version
description: Build the next ROADMAP version of a project set up with /new-app (or any repo with CLAUDE.md, REQUIREMENTS.md, ARCHITECTURE.md and a versioned ROADMAP.md). Runs the 9-step loop - plan (approved in plan mode), build, self-check, independent qa-tester review, fix loop, rc tag and handoff, stop for the owner's manual test, fixes, sign-off and release tag. Also use it to resume a version after /clear, to handle the owner's manual-test feedback, and to sign a version off.
---

# Build one version, the way the owner expects

The project's contract lives in its own files. Read them before anything else, every session:
- **CLAUDE.md**: rules, stack, the owner's name and shell constraints.
- **REQUIREMENTS.md**: what to build. It's the source of truth for behaviour.
- **ARCHITECTURE.md**: the layers, layout and locked decisions (§3), plus the decision log (§7).
- **ROADMAP.md**: the versions in order. Each has a goal, scope bullets, **Done when** items and the **owner's manual test**.
- **docs/DEVELOPER_GUIDE.md**: the commands table. It replaces any command list you remember.
- **plans/v0.x.md**: if it exists, you're resuming. Re-read it and carry on from the first unticked item.

`OWNER` below means the person named in CLAUDE.md.

## Which version, and where you are
- Build **one version at a time, in ROADMAP order**. The current version is the first one with no release tag (`git tag -l "v*"`). If that's unclear, ask the owner.
- Check `git branch --show-current` and `git status` before anything. Each version lives on a branch named after it (`v0.x`), cut from `main`.
  - Not on it yet: create it from an up-to-date `main`.
  - **HEAD detached**: the owner probably checked out an rc tag. Switch back to the branch before committing.
- Work out the step from what exists:

| What exists | Step |
|---|---|
| no plan file | 1 (plan) |
| a plan with unticked build items | 2 (build) |
| everything ticked, no QA report | 3–4 |
| a `qa/QA-v0.x.md` with open bugs | 5 |
| an rc tag | 7–8 (wait for the owner, or fix their findings) |
| the owner signed off | 9 |

## The 9 steps

### 1. Plan (plan mode, the owner approves)
- Explore the code this version touches before proposing anything. Do it inline, or with Explore agents only if the owner allows subagents for exploration.
- Ask the owner every question whose answer changes the build. Use AskUserQuestion with a recommended option first. Don't ask about things that have a conventional default; choose those and list them as your choices.
- The plan contains:
  - the context
  - **Decisions from OWNER**: a table of every question with the answer recorded
  - **My own choices**: defaults the owner didn't name, open to veto at approval
  - out of scope, naming the later version each item belongs to
  - any new dependencies, each with its purpose
  - a numbered **checklist**: files, interfaces, migrations, tests and docs per item
  - **Verification**: every Done when item mapped to the test that proves it
- **Before ExitPlanMode**, recap in chat each question and the answer as the plan records it, and flag which parts were your own choice. The owner rejects plans whose decisions they can't check at a glance.
- Once approved, save the plan as a checklist to `plans/v0.x.md`. Tick items as they land. After a `/clear` or context reset, that file is how you resume.
- If a decision changes a requirement, update REQUIREMENTS.md in the same change.

### 2. Build
- Use small commits on the version branch, running the relevant tests as you go.
- **Build only what this version lists.** You may add an interface that a later version will implement. No placeholder code, no dead UI, no "while I'm here" features.
- **Docs go in the same commit as the code they describe** (the Documentation section of CLAUDE.md):
  - a CHANGELOG `[Unreleased]` line per user-visible change
  - User Guide sections for shipped features only, marked *Added in v0.x*
  - Developer Guide commands
  - an ARCHITECTURE §7 entry for each new dependency, schema shape, protocol change or workaround
- Add a dependency only if the approved plan lists it. Check the exact package name on its registry first, add it with the package manager, and commit the lockfile.
- **Requests the owner makes mid-build:** if one fits this version, add it to the plan (as a lettered item, such as 9b) and to the ROADMAP bullets. If not, record it in REQUIREMENTS and ROADMAP for a later version and don't build it.
- **Secrets:** never read, print, echo or log a credential, even from a shell. If a step needs a real credential, stop and ask the owner to run it. Test placeholders must look fake (`sk-ant-FAKE…`).

### 3. Self-check
Run every check in the Developer Guide's commands table: the full test suite, linters and type checkers, `pre-commit run --all-files`, e2e tests, and regenerating the screenshots. Then run `python scripts/check_docs.py` and `--strict`. Everything must be green before QA. Fix what's red; don't hand red to QA.

### 4. Independent QA
Run the **`qa-tester`** subagent (from this plugin, or a project override in `.claude/agents/`). Give it only the version and, on re-runs, the bug IDs. Don't brief it with your own conclusions. It writes `qa/QA-v0.x.md` and never fixes product code. Its report is not shown to the owner, so pass on what matters.

### 5. Fix loop
- Fix every blocker and major bug, and the minor ones unless the fix is risky.
- **Each fix comes with a regression test.** Check that it fails on the old code (stash the fix, run the test, unstash), then passes.
- QA's xfail tests for a bug become plain tests once it's fixed.
- Run QA again in re-verification mode with the bug IDs. **At most 3 rounds**, then escalate to the owner with what's still open.
- Record the fixes in the plan's QA item and in an ARCHITECTURE §7 "QA fixes" entry.

### 6. Handoff: tag `v0.x-rc1`, then stop
- Make sure the **checkpoint gate** in ROADMAP.md holds.
- Add `Candidates: v0.x-rc1 (date)` under CHANGELOG `[Unreleased]`, commit, then tag. **Run checks, edits and the commit as separate steps.** Never chain a commit or tag after a check with `&&`; a failing check once skipped the edits but not the commit.
- The handoff message, short and in plain words:
  - what's in it, and the QA verdict (rounds, bugs fixed)
  - **how to run it**: `git checkout v0.x` (**the branch, not the tag**, because a tag checkout detaches HEAD and later fixes get lost), then the run command copied from the Developer Guide
  - any migrations, and the backup they take
  - the ROADMAP manual test as numbered steps, plus anything the owner asked for mid-build to try
  - choices you made that they may want to revisit
  - known limits
- Then **stop**. Don't start the next version.

### 7. The owner's manual test
Wait. When feedback arrives, each reported problem is a bug for step 8, even if it predates this version. A request for something new goes into REQUIREMENTS and ROADMAP for the right version, after asking where it belongs if that's unclear.

### 8. Fix and re-test
- **Check the branch first.** The owner may be on a detached rc tag.
- Fix with a regression test that fails on the old code, and run the affected suites.
- Add a CHANGELOG Fixed line only for bugs in a version that was already signed off. Bugs inside the current version live in the QA report or `qa/manual-v0.x.md`.
- Commit, tell the owner what changed and how to pick it up (the rebuild and run commands), and re-tag `-rc2`… when a batch is ready for re-testing.

### 9. Sign-off (only when the owner says so)
- Rename `[Unreleased]` to `[v0.x] - YYYY-MM-DD`, keeping the Candidates line, and open a new empty `[Unreleased]`.
- Update the README status line, then tag `v0.x`.
- Merge to `main` the way the owner prefers (ask the first time, and note it in CLAUDE.md).
- The next version starts in a **fresh session** (`/clear`).

## Always
- When you pick a default that matters, state it.
- Report outcomes faithfully. If something wasn't run, say so.
- Never edit an applied migration (schema changes are new files only), the guardrail files (`.claude/`, the gitleaks and pre-commit configs), or anything CLAUDE.md protects.
- Written for humans (handoffs, guides): plain words, no internal jargon, and commands that work in the owner's shell as CLAUDE.md describes it.
