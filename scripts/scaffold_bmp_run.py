#!/usr/bin/env python3
"""Create a standard public-source BMP run folder."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ROSTER = SKILL_DIR / "references" / "council_roster.json"
DEFAULT_VALUATION_LEAD = SKILL_DIR / "references" / "valuation_lead.json"


COVERAGE_DOMAINS = [
    {
        "id": "council_profile_evidence_demand_brief",
        "bmp_section": "Research",
        "criticality": "high",
        "question": "Have council member profiles been converted into targeted research demands?",
    },
    {
        "id": "source_library_inventory",
        "bmp_section": "Research",
        "criticality": "high",
        "question": "What durable information already exists in the local ticker source library?",
    },
    {
        "id": "sec_filing_freshness_10k_10q",
        "bmp_section": "Research",
        "criticality": "high",
        "question": "For US-listed companies, are the latest annual and quarterly filings fresh and local?",
    },
    {
        "id": "sec_event_proxy_ownership_exhibit_review",
        "bmp_section": "Research",
        "criticality": "high",
        "question": "Have material event, proxy, insider, ownership, offering, merger, foreign-issuer, and exhibit lanes been checked where relevant?",
    },
    {
        "id": "public_market_data_crosscheck",
        "bmp_section": "Research",
        "criticality": "medium",
        "question": "Have public market-data pages been used to cross-check price, shares, market cap, ratios, ownership snapshots, and valuation context?",
    },
    {
        "id": "bruce_quantitative_input_pack",
        "bmp_section": "Price",
        "criticality": "high",
        "question": "Has the Researcher gathered all quantitative inputs Bruce needs for the BMP P1 EPV test?",
    },
    {
        "id": "company_identity_and_listing",
        "bmp_section": "Research",
        "criticality": "high",
        "question": "What security is being analyzed, in what currency, and as of what date?",
    },
    {
        "id": "business_model_and_segments",
        "bmp_section": "Business",
        "criticality": "high",
        "question": "How does the company make money by segment, geography, and customer type?",
    },
    {
        "id": "B1_market_size_and_growth",
        "bmp_section": "Business",
        "criticality": "high",
        "question": "Is the market large and growing?",
    },
    {
        "id": "B2_market_share_and_runway",
        "bmp_section": "Business",
        "criticality": "high",
        "question": "Does the company have low share in a large market with room to grow?",
    },
    {
        "id": "B3_moat_and_unit_economics",
        "bmp_section": "Business",
        "criticality": "high",
        "question": "Does the company have a moat that shows up in economics?",
    },
    {
        "id": "B_bonus_disruption_risk",
        "bmp_section": "Business",
        "criticality": "medium",
        "question": "Is the business protected from disruption or self-disrupting well?",
    },
    {
        "id": "M1_management_owner_mindset",
        "bmp_section": "Management",
        "criticality": "high",
        "question": "Does management act like owners?",
    },
    {
        "id": "M2_value_drivers_and_capital_allocation",
        "bmp_section": "Management",
        "criticality": "high",
        "question": "Does management understand and act on drivers of value?",
    },
    {
        "id": "P1_earnings_yield_price_gate",
        "bmp_section": "Price",
        "criticality": "high",
        "question": "Does evidence-backed Year-3 earnings power clear the 5 percent earnings-yield gate?",
    },
    {
        "id": "negative_research",
        "bmp_section": "Risk",
        "criticality": "high",
        "question": "Has the Researcher gathered the strongest evidence against the thesis?",
    },
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def slugify_ticker(ticker: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", ticker.strip().upper()).strip("_")
    return slug or "TICKER"


def load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def enabled_members(roster_path: Path) -> list[dict[str, Any]]:
    roster = load_json(roster_path, {"members": []})
    members = roster.get("members", []) if isinstance(roster, dict) else []
    return [m for m in members if isinstance(m, dict) and m.get("enabled", True)]


def scaffold_run(args: argparse.Namespace) -> Path:
    ticker = slugify_ticker(args.ticker)
    analysis_date = args.analysis_date or date.today().isoformat()
    workspace = Path(args.workspace).expanduser().resolve() if args.workspace else Path.cwd().resolve()
    run_dir = Path(args.run_dir).expanduser().resolve() if args.run_dir else workspace / "BMP" / f"{ticker}_{analysis_date}"
    company = args.company or ""
    exchange = args.exchange or ""
    currency = args.currency or ""
    stock_source_dir = Path(args.stock_source_dir).expanduser().resolve() if args.stock_source_dir else workspace / ticker

    dirs = [
        "research/local_source_library",
        "research/sec_edgar/primary_documents",
        "research/sec_edgar/companyfacts",
        "research/public_web",
        "council",
        "valuation",
        "checker",
        "report",
        "library",
    ]
    for rel in dirs:
        (run_dir / rel).mkdir(parents=True, exist_ok=True)
    (stock_source_dir / "source_library" / "sec_edgar" / "primary_documents").mkdir(parents=True, exist_ok=True)
    (stock_source_dir / "source_library" / "company_ir").mkdir(parents=True, exist_ok=True)
    (stock_source_dir / "source_library" / "industry").mkdir(parents=True, exist_ok=True)
    (stock_source_dir / "source_library" / "web").mkdir(parents=True, exist_ok=True)

    roster_path = Path(args.roster).expanduser().resolve() if args.roster else DEFAULT_ROSTER
    valuation_lead_path = Path(args.valuation_lead).expanduser().resolve() if args.valuation_lead else DEFAULT_VALUATION_LEAD
    members = enabled_members(roster_path)
    valuation_lead = load_json(valuation_lead_path, {"lead_id": "bruce"})
    lead_id = valuation_lead.get("lead_id", "bruce") if isinstance(valuation_lead, dict) else "bruce"

    manifest = {
        "ticker": ticker,
        "company": company,
        "exchange": exchange,
        "currency": currency,
        "analysis_date": analysis_date,
        "run_dir": str(run_dir),
        "workspace": str(workspace),
        "stock_source_dir": str(stock_source_dir),
        "source_policy": "public_sources_no_private_api_tokens",
        "skill_name": "bmp",
        "roster_path": str(roster_path),
        "valuation_lead_path": str(valuation_lead_path),
        "enabled_council_members": [m.get("id") for m in members],
        "valuation_lead": lead_id,
        "status": "scaffolded",
        "artifact_paths": {
            "research_packet": "research/research_packet.json",
            "coverage_matrix": "research/research_coverage_matrix.json",
            "missing_evidence_requests": "research/missing_evidence_requests.json",
            "bruce_quant_inputs": "research/bruce_quant_inputs.json",
            "bruce_valuation": "valuation/bruce.json",
            "checker_audit": "checker/checker_audit.json",
            "report_html": f"report/BMP_{ticker}_{analysis_date}_report.html",
        },
    }
    write_json(run_dir / "manifest.json", manifest)

    coverage = {
        "ticker": ticker,
        "company": company,
        "analysis_date": analysis_date,
        "status": "not_started",
        "domains": [
            {**domain, "status": "missing", "evidence_ids": [], "notes": "", "gaps": []}
            for domain in COVERAGE_DOMAINS
        ],
        "stop_rules": {
            "ready_for_council": False,
            "critical_missing_domains": [d["id"] for d in COVERAGE_DOMAINS if d["criticality"] == "high"],
        },
    }
    write_json(run_dir / "research" / "research_coverage_matrix.json", coverage)

    research_packet = {
        "ticker": ticker,
        "company": company,
        "exchange": exchange,
        "currency": currency,
        "analysis_date": analysis_date,
        "status": "not_started",
        "source_policy": "public_sources_no_private_api_tokens",
        "evidence": [],
        "source_library_status": {
            "checked": False,
            "stock_source_dir": str(stock_source_dir),
            "source_library_dir": str(stock_source_dir / "source_library"),
        },
        "sec_edgar_status": {"checked": False, "not_applicable_reason": ""},
        "public_market_data_status": {"checked": False},
        "coverage_summary": {},
    }
    write_json(run_dir / "research" / "research_packet.json", research_packet)
    write_text(
        run_dir / "research" / "research_packet.md",
        f"# Research Packet: {ticker}\n\nStatus: not started\n\nUse public filings, company IR, public market-data pages, reputable news, and web search.\n",
    )

    missing = {
        "ticker": ticker,
        "company": company,
        "analysis_date": analysis_date,
        "requests": [],
    }
    write_json(run_dir / "research" / "missing_evidence_requests.json", missing)

    source_inventory = {
        "ticker": ticker,
        "company": company,
        "analysis_date": analysis_date,
        "source_library_dir": str(stock_source_dir / "source_library"),
        "reused_sources": [],
        "added_sources": [],
        "stale_or_missing": [],
    }
    write_json(run_dir / "research" / "local_source_library" / "local_source_inventory.json", source_inventory)
    write_json(stock_source_dir / "source_library" / "local_source_inventory.json", source_inventory)

    write_text(
        run_dir / "research" / "public_web" / "source_log.md",
        f"# Public Web Source Log: {ticker}\n\n| ID | Claim supported | Source title | Publisher | Date | Retrieved | URL |\n| --- | --- | --- | --- | --- | --- | --- |\n",
    )

    bruce_inputs = {
        "ticker": ticker,
        "company": company,
        "analysis_date": analysis_date,
        "status": "not_built",
        "source_policy": "public_sources_no_private_api_tokens",
        "source_priority": ["primary filings", "company IR", "public market data", "government yield source"],
        "market_data": {},
        "capital_structure": {},
        "financial_history": {"annual": [], "quarterly": [], "segments": [], "kpis": []},
        "three_year_revenue_forecast": {},
        "normalization_inputs": {},
        "earnings_power": {},
        "evidence_gaps": [],
    }
    write_json(run_dir / "research" / "bruce_quant_inputs.json", bruce_inputs)
    write_text(
        run_dir / "research" / "bruce_quant_inputs.md",
        f"# Bruce Quantitative Inputs: {ticker}\n\nStatus: not built\n\nGather public-source market data, financial history, segment forecast inputs, margin evidence, and bond-yield context before Bruce starts.\n",
    )

    write_json(
        run_dir / "research" / "council_research_brief.json",
        {"ticker": ticker, "company": company, "analysis_date": analysis_date, "status": "not_built", "members": []},
    )
    write_text(
        run_dir / "research" / "council_research_brief.md",
        f"# Council Research Brief: {ticker}\n\nRun `scripts/build_council_research_brief.py` after confirming the roster.\n",
    )

    for member in members:
        member_id = str(member.get("id", "")).strip()
        if not member_id:
            continue
        write_json(
            run_dir / "council" / f"{member_id}.json",
            {
                "member_id": member_id,
                "display_name": member.get("display_name", member_id),
                "ticker": ticker,
                "company": company,
                "status": "placeholder",
                "checklist": {},
                "evidence_requests": [],
                "bruce_valuation_review": {},
            },
        )

    write_json(
        run_dir / "valuation" / "bruce.json",
        {
            "lead_id": lead_id,
            "ticker": ticker,
            "company": company,
            "status": "placeholder",
            "p1_verdict": "INSUFFICIENT",
            "earnings_power": {},
            "evidence_requests": [],
        },
    )

    write_json(
        run_dir / "checker" / "checker_audit.json",
        {
            "ticker": ticker,
            "company": company,
            "status": "not_run",
            "final_gate": "BLOCK_REPORT",
            "blocking_issues": ["Checker has not run."],
            "warnings": [],
            "mechanical_validation": {},
        },
    )
    write_text(run_dir / "checker" / "checker_audit.md", f"# Checker Audit: {ticker}\n\nStatus: not run\n")
    write_json(run_dir / "checker" / "revision_requests.json", {"requests": []})

    write_text(run_dir / "report" / "reporter_notes.md", f"# Reporter Notes: {ticker}\n\nStatus: not started\n")
    write_json(
        run_dir / "report" / "report_html_qa.json",
        {"status": "not_run", "checks": [], "notes": "Reporter or Checker must fill this after rendering."},
    )
    write_text(run_dir / "library" / "librarian_review.md", f"# Librarian Review: {ticker}\n\nStatus: not started\n")

    return run_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a standard public-source BMP run folder.")
    parser.add_argument("ticker")
    parser.add_argument("--company", default="")
    parser.add_argument("--exchange", default="")
    parser.add_argument("--currency", default="")
    parser.add_argument("--analysis-date", default=date.today().isoformat())
    parser.add_argument("--workspace", help="Stock workspace; defaults to current directory")
    parser.add_argument("--run-dir", help="Explicit run directory")
    parser.add_argument("--stock-source-dir", help="Ticker folder for durable source_library")
    parser.add_argument("--roster", help="Council roster JSON path")
    parser.add_argument("--valuation-lead", help="Valuation lead JSON path")
    args = parser.parse_args()

    run_dir = scaffold_run(args)
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
