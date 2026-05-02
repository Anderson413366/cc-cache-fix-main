#!/usr/bin/env python3
"""
Patch Claude Code cli.js to fix known prompt-cache regressions.

This script intentionally patches only a locally installed Claude Code copy.
It does not modify the stock `claude` command unless the caller explicitly
passes that binary's cli.js path.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


CACHE_ATTACHMENT_TYPES = ("deferred_tools_delta", "mcp_instructions_delta")
HOOK_CONTEXT_ENV = "CLAUDE_CODE_SAVE_HOOK_ADDITIONAL_CONTEXT"


@dataclass(frozen=True)
class PatchResult:
    name: str
    status: str
    detail: str


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: Path, source: str) -> None:
    path.write_text(source, encoding="utf-8")


def _find_attachment_filter(source: str) -> tuple[int, int, str, str] | None:
    """Locate the minified transcript attachment filter around the hook env."""
    for env_match in re.finditer(re.escape(HOOK_CONTEXT_ENV), source):
        window_start = max(0, env_match.start() - 500)
        window_end = min(len(source), env_match.end() + 800)
        window = source[window_start:window_end]
        env_offset = env_match.start() - window_start
        function_matches = list(
            re.finditer(
                r"function\s+([A-Za-z_$][\w$]*)\(([A-Za-z_$][\w$]*)\)\{",
                window[:env_offset],
            )
        )
        if not function_matches:
            continue

        function_match = function_matches[-1]
        function_name, arg_name = function_match.groups()
        function_start = window_start + function_match.start()
        body = window[function_match.start():]
        required = (
            f'{arg_name}.type==="attachment"',
            f'{arg_name}.attachment.type==="hook_additional_context"',
            f"process.env.{HOOK_CONTEXT_ENV}",
        )
        if not all(piece in body for piece in required):
            continue

        return_match = re.search(r"return!1\}", body)
        if not return_match:
            continue

        function_end = window_start + function_match.start() + return_match.end()
        return function_start, function_end, function_name, arg_name

    return None


def _attachment_filter_is_patched(source: str) -> bool:
    found = _find_attachment_filter(source)
    if not found:
        return False
    function_start, function_end, _, _ = found
    function_source = source[function_start:function_end]
    return all(f'attachment.type==="{item}"' in function_source for item in CACHE_ATTACHMENT_TYPES)


def patch_attachment_filter(source: str) -> tuple[str, PatchResult]:
    """Persist cache-relevant attachment messages in the session JSONL."""
    if _attachment_filter_is_patched(source):
        return source, PatchResult(
            "attachment filter",
            "already-applied",
            "cache attachment allowlist present",
        )

    found = _find_attachment_filter(source)
    if not found:
        return source, PatchResult(
            "attachment filter",
            "failed",
            "could not locate hook attachment filter",
        )

    function_start, _, function_name, arg_name = found
    body = source[function_start:]
    return_match = re.search(r"return!1\}", body)
    if not return_match:
        return source, PatchResult(
            "attachment filter",
            "failed",
            f"{function_name} has no target return",
        )

    insert_at = function_start + return_match.start()
    insert = "".join(
        f'if({arg_name}.attachment.type==="{item}")return!0;'
        for item in CACHE_ATTACHMENT_TYPES
    )
    source = source[:insert_at] + insert + source[insert_at:]
    return source, PatchResult("attachment filter", "applied", f"patched {function_name}")


def patch_fingerprint_meta(source: str) -> tuple[str, PatchResult]:
    """Skip injected meta user messages when selecting the first user message."""
    if '"isMeta"in' in source and 'type==="user"&&!(' in source:
        return source, PatchResult(
            "fingerprint meta skip",
            "already-applied",
            "meta-user guard present",
        )

    exact = 'function FA9(A){let q=A.find((_)=>_.type==="user");'
    if exact in source:
        patched = 'function FA9(A){let q=A.find((_)=>_.type==="user"&&!("isMeta"in _&&_.isMeta));'
        return (
            source.replace(exact, patched, 1),
            PatchResult("fingerprint meta skip", "applied", "patched known FA9 selector"),
        )

    pattern = re.compile(
        r"function ([A-Za-z_$][\w$]*)\(([A-Za-z_$][\w$]*)\)\{"
        r"let ([A-Za-z_$][\w$]*)=([A-Za-z_$][\w$]*)\.find"
        r'\(\(([A-Za-z_$][\w$]*)\)=>\5\.type==="user"\);'
    )
    match = pattern.search(source)
    if not match:
        return source, PatchResult("fingerprint meta skip", "skipped", "selector not found")

    var_name = match.group(5)
    old = match.group(0)
    new = old.replace(
        f'{var_name}.type==="user"',
        f'{var_name}.type==="user"&&!("isMeta"in {var_name}&&{var_name}.isMeta)',
        1,
    )
    source = source[:match.start()] + new + source[match.end():]
    return source, PatchResult("fingerprint meta skip", "applied", f"patched {match.group(1)}")


def _ttl_gate_name(source: str) -> str | None:
    match = re.search(r"\.\.\.([A-Za-z_$][\w$]*)\([^)]*\)\?\{ttl:\"1h\"\}:\{\}", source)
    if match:
        return match.group(1)

    match = re.search(r"([A-Za-z_$][\w$]*)\([^)]*\)\?\{ttl:\"1h\"\}:\{\}", source)
    if match:
        return match.group(1)
    return None


def patch_ttl_gate(source: str) -> tuple[str, PatchResult]:
    """Force the cache-control TTL gate to allow 1-hour cache markers."""
    gate = _ttl_gate_name(source)
    if not gate:
        return source, PatchResult("1h cache ttl", "skipped", "ttl gate call not found")

    pattern = re.compile(rf"(function\s+{re.escape(gate)}\([A-Za-z_$][\w$]*\)\{{)")
    match = pattern.search(source)
    if not match:
        return source, PatchResult("1h cache ttl", "skipped", f"{gate} definition not found")

    after_open = match.end()
    if source[after_open : after_open + len("return!0;")] == "return!0;":
        return source, PatchResult("1h cache ttl", "already-applied", f"{gate} already returns true")

    source = source[:after_open] + "return!0;" + source[after_open:]
    return source, PatchResult("1h cache ttl", "applied", f"patched {gate}")


def apply_patches(path: str | Path) -> list[PatchResult]:
    cli_path = Path(path)
    print(f"[*] Reading {cli_path}...")
    source = _read(cli_path)
    print(f"    {len(source):,} bytes")

    results: list[PatchResult] = []
    for patcher in (patch_attachment_filter, patch_fingerprint_meta, patch_ttl_gate):
        source, result = patcher(source)
        results.append(result)
        prefix = "[*]" if result.status in {"applied", "already-applied"} else "[!]"
        print(f"{prefix} Patch {result.name}: {result.status} ({result.detail})")

    critical = next(result for result in results if result.name == "attachment filter")
    if critical.status == "failed":
        print("[!] Critical patch failed. cli.js was not modified.")
        raise SystemExit(1)

    _write(cli_path, source)
    print(f"[*] Wrote patched file ({len(source):,} bytes)")

    verify = _read(cli_path)
    if not _attachment_filter_is_patched(verify):
        print("[!] Verification failed: attachment filter patch is missing")
        raise SystemExit(1)

    print("[*] Verification: attachment filter confirmed")
    return results


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Patch Claude Code cli.js for cache stability.")
    parser.add_argument("cli_js", help="Path to @anthropic-ai/claude-code/cli.js")
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = _parse_args(sys.argv[1:])
    apply_patches(args.cli_js)
