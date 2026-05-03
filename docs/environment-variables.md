# Environment Variables

This project is a local CLI toolkit. It does not need environment variables to install the pinned Claude Code runtime when local Claude auth is already configured.

## Active Variables

| Variable | Required | Scope | Purpose |
| --- | --- | --- | --- |
| `ANTHROPIC_API_KEY` | Optional | Private local/server | Used by `test_cache.py` if Claude local auth is not already configured. Never commit it. |
| `CC_CACHE_FIX_CLAUDE_VERSION` | Optional | Local installer | Overrides `SUPPORTED_CLAUDE_CODE_VERSION` for manual compatibility testing. Use carefully because patch signatures are version-sensitive. |

### Current Deployment Pass Notes

- This release has no active backend env usage beyond optional `ANTHROPIC_API_KEY`/`CC_CACHE_FIX_CLAUDE_VERSION`.
- No Supabase environment variables are required for runtime in this local-only toolkit release.
- Future-ready variables are documented but not wired to active code paths.

## Future-Ready Variables, Not Active

These are documented for a future hosted dashboard or team telemetry service. They are not consumed by current code.

| Variable | Scope | Future purpose |
| --- | --- | --- |
| `SUPABASE_URL` | Server/client safe when intentionally used | Future Supabase project URL. |
| `SUPABASE_ANON_KEY` | Public-safe only after policies are designed | Future browser/client access through RLS-protected APIs. |
| `SUPABASE_SERVICE_ROLE_KEY` | Private server-only | Future trusted server jobs. Never expose to client code. |

Do not add active Supabase variables to a deployment until there is real backend code, RLS design, and a hosted surface that uses them.
