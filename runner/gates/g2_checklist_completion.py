#!/usr/bin/env python3
"""G2 gate: checklist completion validation

meta:
  artifact_id: RUN-G2-CHK-001
  file: g2_checklist_completion.py
  author: "@juria.koga"
  source_type: human
  source: manual
  timestamp: "2026-03-08T15:23:00+09:00"
  content_hash: "PENDING"

Purpose
  Validate human checklist result JSON and fail on dangerous states.

Policy
  - Done does not require a reason.
  - Abort requires a reason.
  - Evidence links/refs are optional.

Input JSON shape (minimum)
  {
    "items": [
      {"status": "todo|done|abort", "reason": "...", "evidence_refs": [...]},
      ...
    ]
  }
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _as_str(x: Any) -> str:
    return "" if x is None else str(x)


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_items(items: List[dict]) -> Dict[str, Any]:
    total = len(items)
    todo = 0
    done = 0
    abort = 0
    abort_no_reason = 0

    for it in items:
        status = _as_str(it.get("status")).strip().lower()
        if status == "todo":
            todo += 1
        elif status == "done":
            done += 1
        elif status == "abort":
            abort += 1
            reason = _as_str(it.get("reason")).strip()
            if not reason:
                abort_no_reason += 1
        else:
            # Unknown status is treated as todo-like for safety
            todo += 1

    abort_rate = (abort / total) if total else 0.0
    return {
        "total": total,
        "todo": todo,
        "done": done,
        "abort": abort,
        "abort_no_reason": abort_no_reason,
        "abort_rate": abort_rate,
    }


def decide_exit_code(
    summary: Dict[str, Any],
    fail_if_todo: bool,
    fail_if_abort_without_reason: bool,
    warn_if_abort_rate_over: float,
) -> Tuple[int, str]:
    todo = int(summary["todo"])
    abort_no_reason = int(summary["abort_no_reason"])
    abort_rate = float(summary["abort_rate"])

    if fail_if_todo and todo > 0:
        return 2, "FAIL"
    if fail_if_abort_without_reason and abort_no_reason > 0:
        return 2, "FAIL"
    if abort_rate > warn_if_abort_rate_over:
        return 1, "WARN"
    return 0, "PASS"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checklist", required=True, help="path to checklist results json")
    ap.add_argument("--fail-if-todo", action="store_true", default=False)
    ap.add_argument("--fail-if-abort-without-reason", action="store_true", default=False)
    ap.add_argument("--warn-if-abort-rate-over", type=float, default=0.30)
    args = ap.parse_args()

    path = Path(args.checklist)
    if not path.exists():
        print(f"[G2] FAIL checklist not found: {path}")
        raise SystemExit(2)

    data = load_json(path)
    items = data.get("items", [])
    if not isinstance(items, list):
        print("[G2] FAIL checklist.items must be a list")
        raise SystemExit(2)

    summary = summarize_items(items)
    code, label = decide_exit_code(
        summary,
        fail_if_todo=bool(args.fail_if_todo),
        fail_if_abort_without_reason=bool(args.fail_if_abort_without_reason),
        warn_if_abort_rate_over=float(args.warn_if_abort_rate_over),
    )

    print(
        "[G2] "
        + label
        + " "
        + json.dumps(summary, ensure_ascii=False)
    )
    raise SystemExit(code)


if __name__ == "__main__":
    main()
