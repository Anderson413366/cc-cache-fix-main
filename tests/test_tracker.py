from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(module)
    return module


class TrackerTests(unittest.TestCase):
    def test_detect_mode_defaults_to_stock_and_marks_patched(self) -> None:
        collector = load_module("collector", ROOT / "tracker" / "collector.py")

        self.assertEqual(collector._detect_mode('{"type":"assistant"}'), "stock")
        self.assertEqual(
            collector._detect_mode('{"env":"CC_CACHE_FIX_MODE=patched"}'),
            "patched",
        )

    def test_turn_insert_is_idempotent(self) -> None:
        db = load_module("tracker_db", ROOT / "tracker" / "db.py")

        with tempfile.TemporaryDirectory() as tmp:
            conn = db.get_db(Path(tmp) / "cache_tracker.db")
            db.upsert_session(conn, "session-1", mode="stock", start_time="2026-05-01T00:00:00Z")
            db.insert_turn(conn, "session-1", 1, "2026-05-01T00:00:01Z", 10, 20, 30, 40)
            db.insert_turn(conn, "session-1", 1, "2026-05-01T00:00:01Z", 10, 20, 30, 40)
            count = conn.execute("SELECT COUNT(*) FROM turns").fetchone()[0]
            summary = db.get_summary(conn)
            conn.close()

        self.assertEqual(count, 1)
        self.assertIn("stock", summary)
        self.assertEqual(summary["stock"]["total_turns"], 1)


if __name__ == "__main__":
    unittest.main()
