# Production Checklist

## Required Before Public GitHub Release

- Confirm `SUPPORTED_CLAUDE_CODE_VERSION` matches the pinned dependency in `node/package.json`.
- Run `npm audit --prefix node --omit=dev`.
- Run Python unit tests.
- Run Python and shell syntax checks.
- Run a live smoke check against `claude-patched` when Claude auth is available.
- Confirm no `.env`, transcript, database, `results/`, `node_modules/`, or `cli.js.orig` files are committed.
- Confirm README install instructions match the scripts.

## Required Before Serious Production Use

- Re-run live smoke checks after every Claude Code version bump.
- Do not widen the npm version range; patching minified upstream code must stay exact-version controlled.
- Treat inconclusive cache tests as failures until rerun successfully.
- Review GitHub advisories for `@anthropic-ai/claude-code`.
- Verify Windows installer behavior on a Windows machine before advertising Windows support as fully validated.

## Future Hosted Dashboard Checklist

- Add backend only when there is a real hosted data workflow.
- Add Supabase migrations only after the data model is designed.
- Enable RLS before exposing any table to clients.
- Add auth before private session or team telemetry is visible online.
- Keep transcript content opt-in and avoid collecting secrets from local sessions.
