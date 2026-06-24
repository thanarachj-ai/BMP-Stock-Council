#!/usr/bin/env python3
"""Run Checker-owned mechanical validation and record the result."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
VALIDATOR = SCRIPT_DIR / "validate_bmp_artifacts.py"


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def tail_lines(text: str, limit: int = 30) -> list[str]:
    lines = text.splitlines()
    return lines[-limit:]


def summarize(stdout: str, returncode: int) -> str:
    for line in reversed(stdout.splitlines()):
        if line.startswith(("OK:", "FAILED:")):
            return line
    return "validation passed" if returncode == 0 else "validation failed"


def main() -> int:
    parser = argparse.ArgumentParser(description="Checker-owned validation runner for BMP Stock Council artifacts.")
    parser.add_argument("run_dir", help="Run directory, for example BMP/AAPL_2026-06-04")
    parser.add_argument("--allow-missing-report", action="store_true", help="Do not fail if the final report HTML is absent")
    parser.add_argument("--roster", help="Council roster JSON path")
    parser.add_argument("--valuation-lead", help="Valuation lead JSON path")
    parser.add_argument("--no-write", action="store_true", help="Run validation without updating checker_audit.json")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    cmd = [sys.executable, str(VALIDATOR), str(run_dir)]
    if args.allow_missing_report:
        cmd.append("--allow-missing-report")
    if args.roster:
        cmd.extend(["--roster", args.roster])
    if args.valuation_lead:
        cmd.extend(["--valuation-lead", args.valuation_lead])

    proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    result = {
        "status": "passed" if proc.returncode == 0 else "failed",
        "command": cmd,
        "returncode": proc.returncode,
        "last_run_at": datetime.now(timezone.utc).isoformat(),
        "summary": summarize(proc.stdout, proc.returncode),
        "stdout_tail": tail_lines(proc.stdout),
        "stderr_tail": tail_lines(proc.stderr),
    }

    if not args.no_write:
        audit_path = run_dir / "checker" / "checker_audit.json"
        audit = load_json(audit_path)
        if audit:
            audit["mechanical_validation"] = result
            if proc.returncode != 0:
                blockers = audit.setdefault("blocking_issues", [])
                if isinstance(blockers, list) and "Checker mechanical validation failed" not in blockers:
                    blockers.append("Checker mechanical validation failed")
                audit["final_gate"] = "BLOCK_REPORT"
            write_json(audit_path, audit)

    print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
