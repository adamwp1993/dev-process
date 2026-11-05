# Architecture: {{APP_NAME}}

<!-- A builder reads this before every version. Keep §1–§3 stable; §7 grows with every version. -->

## 1. Layers and the dependency rule
<!-- Draw the layers and say who may import whom. WeakSquare's version, adapt it:
  core/      pure logic: no I/O, no wall-clock time, no global randomness (Clock and rng are injected)
  services/  use cases; depend on core and on Protocols, not concrete adapters
  adapters/  db, http, filesystem, secret store, external processes
  bridge/    the UI API: thin, every public method wrapped, DTOs only
  app.py     the only place concrete adapters are wired
  web/       UI, talks only to an ApiClient interface (real client + mock client for tests)
-->

## 2. Repository layout
```
{{tree with one-line comments}}
```

## 3. Decisions locked in at v0.1 (expensive to change later)
<!-- Numbered. Each one is a rule a builder can check, e.g. threading/DB connections, how UI talks to backend,
     no browser storage, injected time and randomness, test data never touches the real data folder. -->
1. {{decision}}

## 4. Key interfaces (in the version that first needs them)
| Interface | Version | Purpose |
|---|---|---|

## 5. Data flow examples
<!-- Two or three flows end to end: user action → UI → bridge → service → adapter → back. -->

## 6. Testing strategy
<!-- Unit (pure core), integration (real DB in tmp, fakes for engines/LLMs/HTTP), contract (bridge allowlist, generated types),
     e2e (Playwright against the mock client), real-app smoke, opt-in live tests (-m live), large-data tests behind a marker. -->

## 7. Decision log
<!-- Newest first. Add an entry for every new dependency, schema shape, protocol change or workaround, and for each round of QA fixes. -->

### YYYY-MM-DD, v0.x: <decision in one line>
- Context:
- Decision:
- Consequences:
