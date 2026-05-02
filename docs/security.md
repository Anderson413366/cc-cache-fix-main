# Security Notes

## Current Security Posture

This toolkit patches a local copy of a third-party CLI. That is inherently sensitive, so the repository keeps the patched runtime separate from the stock `claude` command and creates a separate `claude-patched` wrapper.

No real secrets are stored in the repository. `.env` files, local smoke results, SQLite tracker databases, `node_modules`, and original `cli.js` backups are ignored.

## Dependency Advisory Handling

The previous pinned dependency, `@anthropic-ai/claude-code@2.1.81`, was in a high-severity advisory range. The supported target has been bumped to `2.1.84`, the first locally verified `cli.js` package version outside that advisory range.

The current latest npm package line has a different package layout. Do not update blindly; patch compatibility must be verified before changing `SUPPORTED_CLAUDE_CODE_VERSION`.

## Operational Risks

- `test_cache.py` makes live Claude calls and can incur API usage.
- `tracker/collector.py` reads local Claude transcript metadata from `~/.claude/projects`.
- `tracker/cache_tracker.db` can reveal session IDs and usage patterns, so it is ignored.
- The installer writes a wrapper to `~/.local/bin`.

## Future Backend Rules

If a hosted dashboard is added later:

- use RLS on all Supabase tables,
- store transcript text only with explicit opt-in,
- keep service keys server-side,
- do not expose local transcript paths or raw prompts by default,
- add authentication before shared telemetry is viewable.
