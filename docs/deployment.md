# Deployment Guide

This is not a web app. The correct production target is a clean GitHub repository plus local installers, not Vercel hosting.

## Local Setup

Prerequisites:

- Python 3.10 or newer
- Node.js 18 or newer
- npm
- Claude local auth or `ANTHROPIC_API_KEY` for live validation

Install:

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

Verify:

```bash
claude-patched --version
python3 test_cache.py claude-patched --timeout 240 --debug-transcript
```

## GitHub Setup

Recommended repository name: `claude-code-cache-fix`.

Commit:

- source scripts,
- `node/package.json`,
- `node/package-lock.json`,
- docs,
- tests,
- `.github/workflows/ci.yml`,
- `.env.example`.

Never commit:

- `.env` files,
- `node/node_modules/`,
- `results/`,
- `tracker/*.db`,
- `*.orig` patched backups,
- local Claude transcripts,
- API keys.

## Hosting Recommendation

Vercel is not recommended for the current product because there is no frontend route, API route, or hosted application.

If a hosted web dashboard is added later, use Vercel for the dashboard and Supabase for auth/database/storage if team telemetry or accounts are required.

## Supabase Playground

Use Supabase Playground only if the app later gains hosted backend functionality.

Reserved future namespace:

- Project: `Playground`
- Project ID: `qbnetjcztbsbnzuwrigk`
- Schema: `app_cc_cache_fix_main`
- Bucket, if needed later: `cc-cache-fix-main-files`

No Supabase objects are required for the current local CLI deployment.

## Post-Install Verification

Before publishing a release:

```bash
python3 -m unittest discover -s tests
python3 -m py_compile patches/apply-patches.py test_cache.py usage_audit.py tracker/collector.py tracker/dashboard.py tracker/db.py
bash -n install.sh
bash -n install-mac.sh
bash -n smoke_check.sh
npm audit --prefix node --omit=dev
```

Run the live smoke check only when Claude auth and API cost are acceptable:

```bash
./smoke_check.sh --timeout 240
```
