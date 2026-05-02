from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATCHER_PATH = ROOT / "patches" / "apply-patches.py"


def load_patcher():
    spec = importlib.util.spec_from_file_location("apply_patches", PATCHER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ApplyPatchesTests(unittest.TestCase):
    def test_patches_current_supported_filter_and_ttl_gate(self) -> None:
        patcher = load_patcher()
        source = (
            'function Pj6(A){if(A.type==="attachment"&&_qA()!=="ant"){'
            'if(A.attachment.type==="hook_additional_context"'
            '&&r6(process.env.CLAUDE_CODE_SAVE_HOOK_ADDITIONAL_CONTEXT))return!0;'
            'return!1}if(A.type==="progress"&&_18(A.data?.type))return!1;return!0}'
            'function UF({scope:A,querySource:q}={}){return{type:"ephemeral",'
            '...fZz(q)?{ttl:"1h"}:{},...A==="global"?{scope:A}:{}}}'
            'function fZz(A){if(NA()==="bedrock"'
            '&&r6(process.env.ENABLE_PROMPT_CACHING_1H_BEDROCK))return!0;return!1}'
        )

        with tempfile.TemporaryDirectory() as tmp:
            cli = Path(tmp) / "cli.js"
            cli.write_text(source, encoding="utf-8")
            patcher.apply_patches(cli)
            patched = cli.read_text(encoding="utf-8")

        self.assertIn('A.attachment.type==="deferred_tools_delta"', patched)
        self.assertIn('A.attachment.type==="mcp_instructions_delta"', patched)
        self.assertIn('function fZz(A){return!0;if(NA()==="bedrock"', patched)
        self.assertNotIn("function UF({scope:A,querySource:q}={}){return!0;", patched)

    def test_patches_legacy_filter_shape(self) -> None:
        patcher = load_patcher()
        source = (
            'function db8(A){if(A.type==="attachment"&&ss1()!=="ant"){'
            'if(A.attachment.type==="hook_additional_context"'
            '&&a6(process.env.CLAUDE_CODE_SAVE_HOOK_ADDITIONAL_CONTEXT))return!0;'
            'return!1}if(A.type==="progress"&&Ns6(A.data?.type))return!1;return!0}'
            'function zp({scope:A,querySource:q}={}){return{type:"ephemeral",'
            '...sjY(q)?{ttl:"1h"}:{},...A==="global"?{scope:A}:{}}}'
            'function sjY(A){if(QA()==="bedrock"'
            '&&a6(process.env.ENABLE_PROMPT_CACHING_1H_BEDROCK))return!0;return!1}'
        )

        with tempfile.TemporaryDirectory() as tmp:
            cli = Path(tmp) / "cli.js"
            cli.write_text(source, encoding="utf-8")
            patcher.apply_patches(cli)
            patched = cli.read_text(encoding="utf-8")

        self.assertIn('A.attachment.type==="deferred_tools_delta"', patched)
        self.assertIn('function sjY(A){return!0;if(QA()==="bedrock"', patched)


if __name__ == "__main__":
    unittest.main()
