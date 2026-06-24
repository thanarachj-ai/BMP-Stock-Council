#!/usr/bin/env python3
"""Collect council, valuation, and checker evidence requests into the research queue."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any


REQUEST_ID_RE = re.compile(r"^REQ(\d+)$", re.IGNORECASE)


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def normalized_key(requester: str, request: dict[str, Any]) -> tuple[str, str, str]:
    return (
        requester.strip().lower(),
        str(request.get("bmp_question", "")).strip().lower(),
        " ".join(str(request.get("needed_evidence", "")).strip().lower().split()),
    )


def next_request_id(existing: list[dict[str, Any]]) -> str:
    highest = 0
    for request in existing:
        match = REQUEST_ID_RE.match(str(request.get("id", "")).strip())
        if match:
            highest = max(highest, int(match.group(1)))
    return f"REQ{highest + 1:03d}"


def iter_request_sources(run_dir: Path, manifest: dict[str, Any]) -> list[Path]:
    paths: list[Path] = []
    for member in manifest.get("council_members", []):
        if isinstance(member, dict):
            output = member.get("output")
            if output:
                paths.append(run_dir / str(output))
    lead = manifest.get("valuation_lead")
    if isinstance(lead, dict) and lead.get("output"):
        paths.append(run_dir / str(lead["output"]))
    artifacts = manifest.get("artifacts", {})
    if isinstance(artifacts, dict) and artifacts.get("checker_audit_json"):
        paths.append(run_dir / str(artifacts["checker_audit_json"]))
    if not paths:
        paths.extend(sorted((run_dir / "council").glob("*.json")))
        paths.extend(sorted((run_dir / "valuation").glob("*.json")))
        paths.extend(sorted((run_dir / "checker").glob("*.json")))
    elif not any(path.parts[-2:] == ("checker", "checker_audit.json") for path in paths if len(path.parts) >= 2):
        checker_path = run_dir / "checker" / "checker_audit.json"
        if checker_path.exists():
            paths.append(checker_path)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge agent evidence_requests into research/missing_evidence_requests.json.")
    parser.add_argument("run_dir", help="Run directory, for example BMP/AAPL_2026-06-04")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be added without editing the queue")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    manifest = load_json(run_dir / "manifest.json")
    queue_path = run_dir / "research" / "missing_evidence_requests.json"
    queue = load_json(queue_path)
    if not queue:
        queue = {
            "ticker": manifest.get("ticker", ""),
            "company": manifest.get("company", ""),
            "analysis_date": manifest.get("analysis_date", date.today().isoformat()),
            "status": "open",
            "requests": [],
        }
    requests = queue.setdefault("requests", [])
    if not isinstance(requests, list):
        raise SystemExit(f"Invalid queue: {queue_path} requests must be a list")

    existing = {
        normalized_key(str(request.get("requester", "")), request)
        for request in requests
        if isinstance(request, dict)
    }
    additions: list[dict[str, Any]] = []
    for source_path in iter_request_sources(run_dir, manifest):
        payload = load_json(source_path)
        if not payload:
            continue
        requester = str(payload.get("member") or payload.get("valuation_lead") or payload.get("checker") or source_path.stem).strip()
        for raw in payload.get("evidence_requests", []):
            if not isinstance(raw, dict):
                continue
            key = normalized_key(requester, raw)
            if not key[2] or key in existing:
                continue
            request = {
                "id": next_request_id(requests + additions),
                "requester": requester,
                "priority": str(raw.get("priority") or "medium").strip().lower(),
                "bmp_question": str(raw.get("bmp_question", "")).strip(),
                "needed_evidence": str(raw.get("needed_evidence", "")).strip(),
                "why_it_matters": str(raw.get("why_it_matters", "")).strip(),
                "preferred_source_type": str(raw.get("preferred_source_type", "")).strip(),
                "status": "open",
                "researcher_response": "",
                "resolved_evidence_ids": [],
                "created_at": date.today().isoformat(),
                "resolved_at": "",
                "source_file": str(source_path.relative_to(run_dir)),
            }
            additions.append(request)
            existing.add(key)

    if args.dry_run:
        for request in additions:
            print(json.dumps(request, ensure_ascii=False))
    else:
        requests.extend(additions)
        queue["status"] = "open" if any(str(req.get("status", "")).lower() == "open" for req in requests) else "resolved"
        write_json(queue_path, queue)
    print(f"added {len(additions)} evidence request(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
