# PROJECT_SCOPE

## Scope 1: Public Patch Toolkit Hardening

### 1.1 Documentation Baseline
- Status: Complete
- Goal: Add root `README.md` with Linux/macOS install + verify commands.
- Outcome: Completed.

### 1.2 Durable Task Tracking
- Status: Complete
- Goal: Add project scope tracking file for future incremental work.
- Outcome: Completed with this file.

### 1.3 One-Command Smoke Validation
- Status: Complete
- Goal: Add a script that runs installer + `test_cache.py` and prints a shareable pass/fail summary.
- Outcome: Completed via `smoke_check.sh`.

## Next Candidate Work

### 2.1 CI Smoke Job (Optional)
- Status: Complete
- Goal: Add a manual GitHub Action that runs lint/syntax checks only (no live API calls).
- Outcome: Completed via `.github/workflows/ci.yml` with Python syntax, unit tests, shell syntax, npm install, and audit checks.

### 2.2 Version Drift Guard (Optional)
- Status: Partially Complete
- Goal: Add a quick check that warns when upstream Claude Code version changes and patch patterns may need updates.
- Outcome: The supported version is centralized in `SUPPORTED_CLAUDE_CODE_VERSION`; future work can add a dedicated drift-check command if needed.

### 2.3 Production Readiness Cleanup
- Status: Complete
- Goal: Remove generated artifacts, duplicate patching code, and version-sensitive dependency risk.
- Outcome: Removed stale local results and duplicate patcher, updated the pinned runtime to `2.1.84`, added tests/docs/CI, and documented future backend posture.

### 2.4 Documentation Consolidation and Post-Deploy Sync
- Status: Complete
- Goal: Update all documentation artifacts with identity alignment, installer hardening, and verification outcomes.
- Outcome: Updated README and all docs (`docs/*`) for `cc-cache-fix-main` identity consistency, mac installer fix, local-only deployment posture, and latest validation commands/results.
