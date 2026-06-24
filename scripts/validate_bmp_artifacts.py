#!/usr/bin/env python3
"""Validate public-source BMP run artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


CHECKLIST_ITEMS = ["B1", "B2", "B3", "B Bonus", "M1", "M2", "P1"]
FINAL_GATES = {"CLEAR_FOR_REPORT", "REPORT_WITH_WARNINGS", "BLOCK_REPORT"}
URL_RE = re.compile(r"https?://", re.IGNORECASE)
FORBIDDEN_RE = re.compile(
    r"(private workspace-service|private data-provider|paid data-provider|api[_ -]?key|bearer\s+[a-z0-9._-]+|/users/[a-z0-9._-]+/\\.codex/secrets)",
    re.IGNORECASE,
)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}") from exc


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def required(path: Path, errors: list[str], label: str | None = None) -> bool:
    if not path.exists():
        errors.append(f"missing {label or path}")
        return False
    return True


def validate_no_forbidden(run_dir: Path, errors: list[str]) -> None:
    checked_exts = {".md", ".json", ".html", ".txt", ".csv"}
    for path in run_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in checked_exts:
            continue
        text = read_text(path)
        match = FORBIDDEN_RE.search(text)
        if match:
            errors.append(f"forbidden private-service/credential/personal marker {match.group(0)!r} found in {path.relative_to(run_dir)}")


def validate_research_packet(run_dir: Path, errors: list[str], warnings: list[str]) -> dict:
    path = run_dir / "research" / "research_packet.json"
    if not required(path, errors):
        return {}
    packet = load_json(path)
    if not isinstance(packet, dict):
        errors.append("research_packet.json must be an object")
        return {}
    evidence = packet.get("evidence", [])
    if not isinstance(evidence, list):
        errors.append("research_packet.evidence must be a list")
        return packet
    for idx, item in enumerate(evidence):
        if not isinstance(item, dict):
            errors.append(f"evidence[{idx}] must be an object")
            continue
        if not item.get("id"):
            errors.append(f"evidence[{idx}] missing id")
        if not item.get("url") or not URL_RE.search(str(item.get("url"))):
            warnings.append(f"evidence[{idx}] missing public URL")
        if not item.get("claim") and not item.get("metric_or_fact"):
            warnings.append(f"evidence[{idx}] missing claim or metric_or_fact")
    if not evidence:
        warnings.append("research_packet has no evidence yet")
    return packet


def validate_coverage(run_dir: Path, errors: list[str], warnings: list[str]) -> None:
    path = run_dir / "research" / "research_coverage_matrix.json"
    if not required(path, errors):
        return
    matrix = load_json(path)
    if not isinstance(matrix, dict):
        errors.append("research_coverage_matrix.json must be an object")
        return
    domains = matrix.get("domains", [])
    if not isinstance(domains, list) or not domains:
        errors.append("coverage matrix must contain domains")
        return
    ids = {str(item.get("id", "")) for item in domains if isinstance(item, dict)}
    for required_id in ["public_market_data_crosscheck", "bruce_quantitative_input_pack", "negative_research"]:
        if required_id not in ids:
            errors.append(f"coverage matrix missing domain {required_id}")
    for item in domains:
        if not isinstance(item, dict):
            continue
        status = item.get("status")
        if status not in {"covered", "stale", "weak", "missing"}:
            warnings.append(f"coverage domain {item.get('id')} has nonstandard status {status!r}")


def validate_council(run_dir: Path, errors: list[str], warnings: list[str], roster_path: Path | None) -> None:
    members: list[str] = []
    if roster_path and roster_path.exists():
        roster = load_json(roster_path)
        if isinstance(roster, dict):
            for member in roster.get("members", []):
                if isinstance(member, dict) and member.get("enabled", True) and member.get("id"):
                    members.append(str(member["id"]))
    council_dir = run_dir / "council"
    if not required(council_dir, errors):
        return
    files = sorted(council_dir.glob("*.json"))
    if not files:
        warnings.append("no council member files found")
    for member_id in members:
        if not (council_dir / f"{member_id}.json").exists():
            warnings.append(f"enabled council member file missing: {member_id}.json")
    for path in files:
        payload = load_json(path)
        if not isinstance(payload, dict):
            errors.append(f"{path.relative_to(run_dir)} must be an object")
            continue
        checklist = payload.get("checklist", {})
        if checklist:
            for item in CHECKLIST_ITEMS:
                if item not in checklist:
                    warnings.append(f"{path.name} checklist missing {item}")
        review = payload.get("bruce_valuation_review")
        if payload.get("status") != "placeholder" and not review:
            warnings.append(f"{path.name} missing bruce_valuation_review")


def validate_bruce(run_dir: Path, errors: list[str], warnings: list[str]) -> None:
    path = run_dir / "valuation" / "bruce.json"
    if not required(path, errors):
        return
    payload = load_json(path)
    if not isinstance(payload, dict):
        errors.append("valuation/bruce.json must be an object")
        return
    verdict = payload.get("p1_verdict")
    if verdict and verdict not in {"PASS", "FAIL", "WATCHLIST", "INSUFFICIENT"}:
        errors.append(f"Bruce p1_verdict has invalid value {verdict!r}")
    if payload.get("status") != "placeholder" and not payload.get("earnings_power"):
        warnings.append("Bruce output missing earnings_power block")


def validate_checker(run_dir: Path, errors: list[str], warnings: list[str]) -> None:
    path = run_dir / "checker" / "checker_audit.json"
    if not required(path, errors):
        return
    payload = load_json(path)
    if not isinstance(payload, dict):
        errors.append("checker_audit.json must be an object")
        return
    gate = payload.get("final_gate")
    if gate and gate not in FINAL_GATES:
        errors.append(f"checker final_gate has invalid value {gate!r}")
    revision_path = run_dir / "checker" / "revision_requests.json"
    if required(revision_path, errors):
        revisions = load_json(revision_path)
        if not isinstance(revisions, dict):
            errors.append("revision_requests.json must be an object")
        elif revisions.get("requests"):
            warnings.append("open revision requests remain")


def validate_report(run_dir: Path, errors: list[str], warnings: list[str], allow_missing_report: bool) -> None:
    report_dir = run_dir / "report"
    if not required(report_dir, errors):
        return
    qa_path = report_dir / "report_html_qa.json"
    if required(qa_path, errors):
        qa = load_json(qa_path)
        if isinstance(qa, dict):
            status = qa.get("status")
            if status in {"not_run", "failed"} and not allow_missing_report:
                errors.append(f"report_html_qa status is {status}")
        else:
            errors.append("report_html_qa.json must be an object")
    html_files = sorted(report_dir.glob("*.html"))
    if not html_files:
        if not allow_missing_report:
            errors.append("final report HTML missing")
        return
    html = read_text(html_files[0])
    required_tokens = [
        "Business Model",
        "B1",
        "B2",
        "B3",
        "B Bonus",
        "M1",
        "M2",
        "P1",
        "Morningstar",
        "7 Powers",
        "Bruce",
        "Council",
        "References",
    ]
    for token in required_tokens:
        if token not in html:
            warnings.append(f"report may be missing visible token: {token}")
    if not URL_RE.search(html):
        warnings.append("report appears to contain no URLs")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate public-source BMP run artifacts.")
    parser.add_argument("run_dir")
    parser.add_argument("--allow-missing-report", action="store_true")
    parser.add_argument("--roster", help="Council roster JSON path")
    parser.add_argument("--valuation-lead", help="Accepted for compatibility; not used")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    roster_path = Path(args.roster).expanduser().resolve() if args.roster else None

    required(run_dir / "manifest.json", errors)
    validate_no_forbidden(run_dir, errors)
    validate_research_packet(run_dir, errors, warnings)
    validate_coverage(run_dir, errors, warnings)
    validate_council(run_dir, errors, warnings, roster_path)
    validate_bruce(run_dir, errors, warnings)
    validate_checker(run_dir, errors, warnings)
    validate_report(run_dir, errors, warnings, args.allow_missing_report)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
