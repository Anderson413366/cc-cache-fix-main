# Claude Code Cache Fix

Local patch, test, and audit toolkit for Claude Code prompt-cache issues:

- resume cache regression involving `deferred_tools_delta` and `mcp_instructions_delta`
- sentinel replacement behavior involving `cch=00000`
- cache-control TTL behavior

The toolkit never modifies the stock `claude` command. It installs a separate pinned Claude Code runtime and creates a separate `claude-patched` wrapper.

## Production Status

Current supported Claude Code version: see `SUPPORTED_CLAUDE_CODE_VERSION`.

The pinned npm dependency is exact-version controlled because the patcher works against minified upstream code. Do not widen it to a caret range.

This repository is a local CLI toolkit, not a web app. GitHub is the correct distribution target today. Vercel and Supabase are documented as future paths only if a hosted dashboard or shared telemetry service is added later.

## Quick Start

Linux:

```bash
./install.sh
```

macOS:

```bash
./install-mac.sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-windows.ps1
```

Then open a new terminal if needed and verify:

```bash
claude-patched --version
python3 test_cache.py claude-patched --timeout 240 --debug-transcript
```

## Smoke Check

Run installer plus live cache validation:

```bash
./smoke_check.sh --timeout 240
```

macOS with the macOS installer:

```bash
./smoke_check.sh --installer ./install-mac.sh --timeout 240
```

Smoke reports are written under `results/` and ignored by git.

## Usage Audit

Audit recent local Claude transcript usage:

```bash
python3 usage_audit.py --top 10 --window 8
```

Optional live tracker:

```bash
python3 tracker/collector.py
python3 tracker/dashboard.py
```

The tracker database is local-only and ignored by git.

## What the Patches Do

1. Persist `deferred_tools_delta` and `mcp_instructions_delta` attachments in session JSONL so resume can reconstruct the cache prefix.
2. Skip injected meta user messages when selecting the first user message for cache attribution, when that selector exists in the target version.
3. Force 1-hour cache markers by patching the minified TTL gate.

## Development Checks

```bash
python3 -m unittest discover -s tests
python3 -m py_compile patches/apply-patches.py test_cache.py usage_audit.py tracker/collector.py tracker/dashboard.py tracker/db.py
bash -n install.sh
bash -n install-mac.sh
bash -n smoke_check.sh
npm audit --prefix node --omit=dev
```

## Documentation

- Deployment and GitHub readiness: `docs/deployment.md`
- Environment variables: `docs/environment-variables.md`
- Backend setup: `docs/backend-setup.md`
- Supabase setup: `docs/supabase-setup.md`
- Backend and Supabase posture: `docs/backend-readiness.md`
- Production checklist: `docs/production-checklist.md`
- Security notes: `docs/security.md`

## Notes

- Requires Node.js, npm, and Python 3.
- Live tests require Claude auth through `ANTHROPIC_API_KEY` or local Claude auth.
- `test_cache.py` makes live Claude calls and may incur usage.
- A running old `claude-patched` process will not auto-update; start a new session after reinstalling.
