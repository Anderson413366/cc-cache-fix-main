# Backend and Supabase Readiness

Backend Status: Prepared for Future Use

Supabase Status: Prepared for Future Use

App schema namespace reserved for future use: `app_cc_cache_fix_main`

Authentication Status: no existing login or authentication system was found. No temporary auth bypass is needed for the current deployment.

## Current Need

The current product is a local Python, Bash, PowerShell, and Node toolkit. It installs a pinned local copy of `@anthropic-ai/claude-code`, patches `cli.js`, creates a `claude-patched` wrapper, and provides local smoke/audit tools.

It does not need a hosted backend, database, authentication, file storage, or Vercel deployment today.

## Future Readiness

Supabase is not active in this version. No fake clients, tables, migrations, or database calls were added.

Supabase becomes useful if the project grows into:

- a hosted web dashboard for cache-efficiency history,
- team-level telemetry across multiple machines,
- accounts or organization-level access,
- shared run reports,
- private uploaded transcripts or support bundles,
- admin views for supported Claude Code versions and patch status.

## Recommended Future Supabase Shape

If activated later, use Supabase for Postgres, Auth, Row Level Security, and optionally Storage.

Likely future tables:

- `profiles`: authenticated user profile and team membership.
- `machines`: registered local clients.
- `sessions`: per-Claude-session metadata without transcript text by default.
- `turn_usage`: cache read/create/input/output token counters.
- `patch_runs`: installer version, Claude Code version, patch result, and timestamp.

Security rules:

- Enable RLS on every exposed table.
- Keep `SUPABASE_SERVICE_ROLE_KEY` server-only.
- Store transcript text only if users explicitly opt in.
- Do not use user-editable metadata for authorization.
- Use organization/team membership from trusted app metadata or relational tables.

## Recommendation

Keep the active product local-only now. Prepare Supabase only when there is a real hosted dashboard, shared telemetry need, auth requirement, or private team workflow.
