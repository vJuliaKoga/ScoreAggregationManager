#!/usr/bin/env python3
"""MD YAML-paste guard

This gate checks that Markdown files do not contain YAML-like lines.
It is designed to prevent copying YAML rows directly into MD.

Hard rules
  - If any line looks like a YAML key-value (e.g., "name: ...") it is a violation.
  - If any line looks like a YAML list item with an inline mapping (e.g., "- name: ...") it is a violation.

Notes
  - This is intentionally strict.
  - It does not try to parse Markdown.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List


YAMLISH_PATTERNS: List[re.Pattern] = [
    # YAML list item with inline mapping
    re.compile(r"^\s*-\s*[A-Za-z_][A-Za-z0-9_\-]*\s*:\s*.+$"),
    # YAML key-value
    re.compile(r"^\s*[A-Za-z_][A-Za-z0-9_\-]*\s*:\s*.+$"),
]


def scan_file(path: Path) -> List[Dict[str, object]]:
    findings: List[Dict[str, object]] = []
    text = path.read_text(encoding="utf-8")
    for i, line in enumerate(text.splitlines(), start=1):
        # allow common markdown constructs
        if line.strip().startswith("```"):
            # even inside code fences, we still consider it a violation
            # because the instruction was absolute.
            pass

        for pat in YAMLISH_PATTERNS:
            if pat.match(line):
                findings.append({
                    "file": str(path),
                    "line": i,
                    "text": line.rstrip()[:200],
                })
                break
    return findings


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", required=True, help="glob pattern for md files")
    ap.add_argument("--out", default="", help="optional json report output path")
    args = ap.parse_args()

    files = sorted(Path(".").glob(args.glob))
    all_findings: List[Dict[str, object]] = []
    for fp in files:
        if fp.is_file():
            all_findings.extend(scan_file(fp))

    report = {
        "checked": [str(f) for f in files if f.is_file()],
        "violations": all_findings,
        "violations_count": len(all_findings),
    }

    if args.out:
        outp = Path(args.out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if all_findings:
        print(f"[MD_GUARD] FAIL yaml_like_lines={len(all_findings)}")
        for v in all_findings[:10]:
            print(f"  {v['file']}:{v['line']} {v['text']}")
        raise SystemExit(2)

    print(f"[MD_GUARD] PASS checked_files={len(report['checked'])}")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
