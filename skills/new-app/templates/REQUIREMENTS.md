# {{APP_NAME}}: Requirements

<!-- Every requirement has an ID and is one testable sentence. FR = functional, NFR = non-functional, SR = security.
     IDs are never reused. When the owner decides something, note it inline: "(Owner, YYYY-MM-DD)".
     A requirement's version is the ROADMAP version that builds it. CHANGELOG lines cite these IDs, and check_docs.py verifies they exist. -->

## 1. Purpose
{{Who it's for and the problem it solves, in a paragraph.}}

### Non-goals
- {{what it deliberately won't do}}

## 2. Platform and stack
- **NFR-1** {{platform}}
- **NFR-2** Dev runs and tests never use the default data folder.

## 3. {{First feature area}}
- **FR-3.1** {{…}}

## {{N}}. Security
<!-- From the /new-app security round. Keep the threat model short; every SR- line is testable and QA checks each one. -->
### Threat model
- **Worth protecting:** {{keys, accounts, the user's data, money spent through paid APIs}}
- **Threats:** {{leaked repo, malicious dependency or download, hostile API/LLM/file input, other local programs}}
- **Out of scope:** {{e.g. an attacker with full control of the user's PC}}

### Requirements
- **SR-1** Secrets are stored only in the OS credential store, through one module.
- **SR-2** No secret appears in logs, files, test fixtures, UI data or the AI transcript.
- **SR-3** Recorded HTTP fixtures are scrubbed when recorded, and anonymized if the repo is public.
- **SR-4** Claude Code never reads or prints a credential; a PreToolUse hook blocks attempts, and steps that need one are run by the owner.
- **SR-5** Live tests are opt-in, use a separate scoped test credential, and are limited in what they write.
- **SR-6** Every untrusted input (external APIs, imported files, LLM output) is validated before use and rendered as escaped text.
- **SR-7** All network calls go through one HTTP adapter; links the app opens are built by the app from an allowlist of hosts.
- **SR-8** Dependencies are added only through an approved plan and locked; downloaded binaries are pinned and SHA-256 checked before use.
<!-- Add the app-specific ones: sign-in flow and scopes, revocation, spend guardrails, local data protection, debug ports test-only. -->

## {{N+1}}. Your data and privacy
- {{What leaves the machine, to whom, and when. Each feature that sends data has a line here.}}

## {{N+2}}. Milestones → see ROADMAP.md

## {{N+3}}. Verified external facts (as of {{DATE}})
<!-- API endpoints, rate limits, formats and licences you checked, each with its source. Re-check before relying on one. -->
- {{fact}} (source: {{url}})
