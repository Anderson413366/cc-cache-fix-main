# Backend Setup

Backend Status: Prepared for Future Use

The current `cc-cache-fix-main` app is a local CLI toolkit. It does not require an active hosted backend to install, patch, test, or audit Claude Code cache behavior.

## Current Backend

Active backend: none.

Active local persistence:

- `tracker/cache_tracker.db`, created locally by `tracker/collector.py`
- ignored by git
- not uploaded to Supabase or any hosted service

## Future Backend Triggers

Add a hosted backend only when the project needs one of these:

- hosted cache-efficiency dashboard,
- team or organization accounts,
- shared machine/session telemetry,
- private run reports,
- uploaded transcript bundles,
- admin management for supported Claude Code versions,
- user-specific settings.

## Recommended Future Backend

Use Supabase Playground with the app-specific namespace:

- Supabase schema slug: `cc_cache_fix_main`
- Preferred schema: `app_cc_cache_fix_main`
- Optional private schema later: `app_cc_cache_fix_main_private`
- Optional storage bucket later: `cc-cache-fix-main-files`

Do not store transcript text by default. If transcript upload is added later, make it explicit opt-in and redact secrets before upload.

## Activation Order

1. Create an app-specific schema in Supabase Playground.
2. Add migrations for only this app's schema.
3. Enable RLS before exposing any table to browser clients.
4. Add authentication before shared telemetry is visible online.
5. Add server-only jobs for privileged operations.
6. Add environment variables only to the app-specific deployment target.

## Completed Work Snapshot (2026-05-03)

- Verified deployment scope and kept this release strictly local-only (no hosted API, no RLSed schema, no auth service dependency).
- Preserved a clean future path with explicit namespace plan:
  - `app_cc_cache_fix_main`
  - `app_cc_cache_fix_main_private` (optional later)
  - `cc_cache_fix_main`
- Confirmed local persistence remains `tracker/cache_tracker.db` only (ignored by `.gitignore`) and is not part of Supabase active data yet.
