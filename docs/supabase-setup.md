# Supabase Setup

Project name: Playground

Project ID: `qbnetjcztbsbnzuwrigk`

Supabase Status: Prepared for Future Use

No Supabase schema, table, bucket, policy, function, or auth setting is active for this app today.

## App Namespace

Use this namespace if Supabase is activated later:

| Item | Value |
| --- | --- |
| App slug | `cc-cache-fix-main` |
| Schema slug | `cc_cache_fix_main` |
| Preferred schema | `app_cc_cache_fix_main` |
| Private schema, if needed later | `app_cc_cache_fix_main_private` |
| Storage bucket, if needed later | `cc-cache-fix-main-files` |

## What Was Inspected

The Playground project is currently reused for multiple apps (per existing project convention).
No active schema, table, bucket, function, or auth changes were made for this app yet.

## Safe Future Migration Pattern

Use idempotent, app-scoped migrations only:

```sql
create schema if not exists app_cc_cache_fix_main;

create table if not exists app_cc_cache_fix_main.patch_runs (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  claude_code_version text not null,
  patcher_version text not null,
  patch_status text not null
);

alter table app_cc_cache_fix_main.patch_runs enable row level security;
```

Do not run destructive SQL against existing schemas in Playground. Do not put this app's tables directly in `public` unless there is a documented technical reason.

## Future Table Candidates

- `profiles`
- `machines`
- `sessions`
- `turn_usage`
- `patch_runs`

These tables are candidates only. They should not be created until the hosted product actually needs them.

## Security Rules

- Enable RLS before browser access.
- Keep `SUPABASE_SERVICE_ROLE_KEY` server-only.
- Do not use user-editable metadata for authorization.
- Do not collect raw transcript text by default.
- Keep every bucket private unless public access is explicitly required.
