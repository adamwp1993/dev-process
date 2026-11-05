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
- **SR-1** Secrets are stored only in the OS credential store, through one module.
- **SR-2** No secret appears in logs, files, test fixtures, UI data or the AI transcript.
- **SR-3** Recorded HTTP fixtures are scrubbed when recorded, and anonymized if the repo is public.

## {{N+1}}. Your data and privacy
- {{What leaves the machine, to whom, and when. Each feature that sends data has a line here.}}

## {{N+2}}. Milestones → see ROADMAP.md

## {{N+3}}. Verified external facts (as of {{DATE}})
<!-- API endpoints, rate limits, formats and licences you checked, each with its source. Re-check before relying on one. -->
- {{fact}} (source: {{url}})
