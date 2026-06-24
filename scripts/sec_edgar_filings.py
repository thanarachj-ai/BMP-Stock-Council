#!/usr/bin/env python3
"""Fetch public SEC EDGAR metadata and primary filing documents."""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SEC_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
SEC_COMPANYFACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
DEFAULT_USER_AGENT = os.environ.get("SEC_USER_AGENT", "BMP-public-research/1.0 (set SEC_USER_AGENT)")
REQUEST_DELAY_SECONDS = 0.15
FORM_BASES = {"10-K": "annual", "10-Q": "quarterly"}


ADDITIONAL_FORM_GROUPS = {
    "current_reports_8k": {
        "label": "Current reports and material events",
        "forms": {"8-K", "8-K/A"},
        "max_count": 8,
        "research_use": "Review for material events before the next 10-Q or 10-K.",
    },
    "proxy_governance_compensation": {
        "label": "Proxy, governance, ownership, and executive compensation",
        "forms": {"DEF 14A", "DEFA14A", "PRE 14A", "PRE14A", "DEF14A"},
        "max_count": 4,
        "research_use": "Review board quality, compensation, shareholder votes, and ownership alignment.",
    },
    "insider_transactions": {
        "label": "Insider holdings and transactions",
        "forms": {"3", "3/A", "4", "4/A", "5", "5/A"},
        "max_count": 20,
        "research_use": "Review insider buying, selling, option exercises, and ownership alignment.",
    },
    "beneficial_ownership": {
        "label": "Beneficial ownership reports",
        "forms": {"SC 13D", "SC 13D/A", "SC 13G", "SC 13G/A"},
        "max_count": 10,
        "research_use": "Review holders above five percent and activist/passive status.",
    },
    "business_combinations": {
        "label": "Business combinations, mergers, and tender offers",
        "forms": {"PREM14A", "DEFM14A", "S-4", "S-4/A", "425", "SC TO-T", "SC TO-I", "SC TO-T/A", "SC TO-I/A", "SC 14D9", "SC 14D9/A"},
        "max_count": 8,
        "research_use": "Review M&A, tender offers, or securities issued as acquisition consideration.",
    },
    "public_offerings": {
        "label": "Public offerings and securities registration",
        "forms": {"S-1", "S-1/A", "S-3", "S-3/A"},
        "prefixes": {"424B"},
        "max_count": 8,
        "research_use": "Review dilution, capital needs, IPO history, secondary offerings, and use of proceeds.",
    },
    "foreign_private_issuer_reports": {
        "label": "Foreign private issuer reports",
        "forms": {"20-F", "20-F/A", "6-K", "6-K/A", "F-1", "F-1/A"},
        "max_count": 8,
        "research_use": "Review annual and interim/current disclosures for foreign private issuers.",
    },
}


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fetch_json(url: str, user_agent: str, timeout: int = 30) -> object:
    req = Request(url, headers={"User-Agent": user_agent, "Accept-Encoding": "identity"})
    with urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_text(url: str, user_agent: str, timeout: int = 30) -> str:
    req = Request(url, headers={"User-Agent": user_agent, "Accept-Encoding": "identity"})
    with urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def normalize_cik(cik: str) -> str:
    digits = re.sub(r"\D+", "", cik)
    if not digits:
        raise ValueError(f"Invalid CIK: {cik!r}")
    return digits.zfill(10)


def lookup_cik(ticker_or_cik: str, user_agent: str) -> tuple[str, str]:
    if ticker_or_cik.isdigit():
        return normalize_cik(ticker_or_cik), ""
    data = fetch_json(SEC_TICKERS_URL, user_agent)
    if not isinstance(data, dict):
        raise RuntimeError("Unexpected SEC ticker map shape")
    needle = ticker_or_cik.upper()
    for item in data.values():
        if not isinstance(item, dict):
            continue
        if str(item.get("ticker", "")).upper() == needle:
            return normalize_cik(str(item.get("cik_str", ""))), str(item.get("title", ""))
    raise RuntimeError(f"Ticker not found in SEC company_tickers.json: {ticker_or_cik}")


def accession_no_dashes(accession: str) -> str:
    return accession.replace("-", "")


def filing_url(cik: str, accession: str, primary_doc: str) -> str:
    cik_int = str(int(cik))
    return f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession_no_dashes(accession)}/{primary_doc}"


def filing_index_url(cik: str, accession: str) -> str:
    cik_int = str(int(cik))
    return f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession_no_dashes(accession)}/"


def recent_filings(submissions: dict) -> list[dict]:
    recent = submissions.get("filings", {}).get("recent", {})
    if not isinstance(recent, dict):
        return []
    keys = list(recent.keys())
    count = max((len(v) for v in recent.values() if isinstance(v, list)), default=0)
    filings: list[dict] = []
    for i in range(count):
        row = {}
        for key in keys:
            values = recent.get(key, [])
            row[key] = values[i] if isinstance(values, list) and i < len(values) else ""
        row["filing_url"] = filing_url(str(submissions.get("cik", "")), row.get("accessionNumber", ""), row.get("primaryDocument", ""))
        row["index_url"] = filing_index_url(str(submissions.get("cik", "")), row.get("accessionNumber", ""))
        filings.append(row)
    return filings


def select_periodic_filings(filings: list[dict], annual_count: int, quarterly_count: int, include_amendments: bool) -> list[dict]:
    selected: list[dict] = []
    counts = {"10-K": 0, "10-Q": 0}
    for filing in filings:
        form = str(filing.get("form", ""))
        base = form.replace("/A", "")
        if base not in FORM_BASES:
            continue
        if form.endswith("/A") and not include_amendments:
            continue
        limit = annual_count if base == "10-K" else quarterly_count
        if counts[base] >= limit:
            continue
        counts[base] += 1
        selected.append(filing)
    return selected


def select_additional_forms(filings: list[dict]) -> dict[str, list[dict]]:
    result: dict[str, list[dict]] = {}
    for group_id, spec in ADDITIONAL_FORM_GROUPS.items():
        forms = set(spec.get("forms", set()))
        prefixes = set(spec.get("prefixes", set()))
        limit = int(spec.get("max_count", 5))
        matches: list[dict] = []
        for filing in filings:
            form = str(filing.get("form", ""))
            if form in forms or any(form.startswith(prefix) for prefix in prefixes):
                matches.append(filing)
            if len(matches) >= limit:
                break
        result[group_id] = matches
    return result


def download_primary_documents(filings: list[dict], docs_dir: Path, user_agent: str) -> list[dict]:
    docs_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    for filing in filings:
        accession = str(filing.get("accessionNumber", ""))
        primary_doc = str(filing.get("primaryDocument", ""))
        url = str(filing.get("filing_url", ""))
        if not accession or not primary_doc or not url:
            continue
        safe_name = f"{accession}_{primary_doc}".replace("/", "_")
        path = docs_dir / safe_name
        try:
            text = fetch_text(url, user_agent)
            path.write_text(text, encoding="utf-8")
            status = "downloaded"
            error = ""
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            status = "error"
            error = str(exc)
        results.append(
            {
                "form": filing.get("form", ""),
                "filing_date": filing.get("filingDate", ""),
                "report_date": filing.get("reportDate", ""),
                "accession_number": accession,
                "primary_document": primary_doc,
                "url": url,
                "local_path": str(path) if status == "downloaded" else "",
                "status": status,
                "error": error,
            }
        )
        time.sleep(REQUEST_DELAY_SECONDS)
    return results


def summarize_companyfacts(companyfacts: object) -> dict:
    if not isinstance(companyfacts, dict):
        return {"status": "unexpected_shape"}
    facts = companyfacts.get("facts", {})
    us_gaap = facts.get("us-gaap", {}) if isinstance(facts, dict) else {}
    wanted = [
        "Revenues",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "OperatingIncomeLoss",
        "NetIncomeLoss",
        "Assets",
        "Liabilities",
        "StockholdersEquity",
        "NetCashProvidedByUsedInOperatingActivities",
        "PaymentsToAcquirePropertyPlantAndEquipment",
    ]
    concepts = {}
    for name in wanted:
        payload = us_gaap.get(name, {}) if isinstance(us_gaap, dict) else {}
        units = payload.get("units", {}) if isinstance(payload, dict) else {}
        unit_summary = {}
        for unit, rows in units.items():
            if isinstance(rows, list):
                unit_summary[unit] = rows[-5:]
        if unit_summary:
            concepts[name] = unit_summary
    return {"status": "ready", "concepts": concepts}


def update_research_packet(run_dir: Path, manifest: dict) -> None:
    packet_path = run_dir / "research" / "research_packet.json"
    if not packet_path.exists():
        return
    try:
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    if not isinstance(packet, dict):
        return
    packet["sec_edgar_status"] = {
        "checked": True,
        "cik": manifest.get("cik", ""),
        "company_name": manifest.get("company_name", ""),
        "latest_10k": manifest.get("freshness", {}).get("latest_10k_accession", ""),
        "latest_10q": manifest.get("freshness", {}).get("latest_10q_accession", ""),
        "primary_documents_downloaded": manifest.get("primary_documents_downloaded", 0),
        "manifest": "research/sec_edgar/sec_filing_manifest.json",
        "primary_documents_dir": "research/sec_edgar/primary_documents",
    }
    packet_path.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def mirror_to_source_library(output_dir: Path, stock_source_dir: Path | None) -> None:
    if not stock_source_dir:
        return
    target = stock_source_dir / "source_library" / "sec_edgar"
    target.mkdir(parents=True, exist_ok=True)
    for name in ["sec_filing_manifest.json", "sec_companyfacts_summary.json", "primary_documents_index.md"]:
        src = output_dir / name
        if src.exists():
            (target / name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    docs_src = output_dir / "primary_documents"
    docs_target = target / "primary_documents"
    docs_target.mkdir(parents=True, exist_ok=True)
    if docs_src.exists():
        for src in docs_src.iterdir():
            if src.is_file():
                (docs_target / src.name).write_bytes(src.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch public SEC EDGAR filing metadata for BMP runs.")
    parser.add_argument("ticker", help="US ticker or CIK")
    parser.add_argument("--cik", help="CIK if ticker lookup should be skipped")
    parser.add_argument("--company", default="", help="Company name for source titles")
    parser.add_argument("--run-dir", help="BMP run directory; output goes to RUN_DIR/research/sec_edgar")
    parser.add_argument("--output-dir", help="Output directory when not using --run-dir")
    parser.add_argument("--stock-source-dir", help="Ticker folder where durable sources are stored, for example WORKSPACE/AAPL")
    parser.add_argument("--analysis-date", default=date.today().isoformat())
    parser.add_argument("--annual-count", type=int, default=10)
    parser.add_argument("--quarterly-count", type=int, default=4)
    parser.add_argument("--include-amendments", action="store_true")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="SEC User-Agent contact string")
    parser.add_argument(
        "--download-primary-docs",
        dest="download_primary_docs",
        action="store_true",
        default=True,
        help="Download selected primary filing HTML documents (default)",
    )
    parser.add_argument(
        "--skip-primary-doc-download",
        dest="download_primary_docs",
        action="store_false",
        help="Metadata-only run; do not download primary filing HTML documents",
    )
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve() if args.run_dir else None
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else (run_dir / "research" / "sec_edgar" if run_dir else Path.cwd() / "sec_edgar")
    stock_source_dir = Path(args.stock_source_dir).expanduser().resolve() if args.stock_source_dir else None
    output_dir.mkdir(parents=True, exist_ok=True)

    cik, sec_name = (normalize_cik(args.cik), "") if args.cik else lookup_cik(args.ticker, args.user_agent)
    submissions = fetch_json(SEC_SUBMISSIONS_URL.format(cik=cik), args.user_agent)
    if not isinstance(submissions, dict):
        raise RuntimeError("Unexpected SEC submissions response")
    filings = recent_filings(submissions)
    periodic = select_periodic_filings(filings, args.annual_count, args.quarterly_count, args.include_amendments)
    additional = select_additional_forms(filings)

    companyfacts_summary = {}
    try:
        facts = fetch_json(SEC_COMPANYFACTS_URL.format(cik=cik), args.user_agent)
        companyfacts_summary = summarize_companyfacts(facts)
    except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        companyfacts_summary = {"status": "error", "error": str(exc)}

    downloads: list[dict] = []
    if args.download_primary_docs:
        downloads = download_primary_documents(periodic, output_dir / "primary_documents", args.user_agent)

    latest_10k = next((f for f in filings if str(f.get("form", "")).replace("/A", "") == "10-K"), {})
    latest_10q = next((f for f in filings if str(f.get("form", "")).replace("/A", "") == "10-Q"), {})

    manifest = {
        "ticker": args.ticker.upper(),
        "company_name": args.company or sec_name or submissions.get("name", ""),
        "analysis_date": args.analysis_date,
        "source_policy": "public_sec_edgar_no_private_api_token",
        "cik": cik,
        "sic": submissions.get("sic", ""),
        "sic_description": submissions.get("sicDescription", ""),
        "entity_type": submissions.get("entityType", ""),
        "fiscal_year_end": submissions.get("fiscalYearEnd", ""),
        "freshness": {
            "latest_10k_accession": latest_10k.get("accessionNumber", ""),
            "latest_10k_filing_date": latest_10k.get("filingDate", ""),
            "latest_10k_report_date": latest_10k.get("reportDate", ""),
            "latest_10q_accession": latest_10q.get("accessionNumber", ""),
            "latest_10q_filing_date": latest_10q.get("filingDate", ""),
            "latest_10q_report_date": latest_10q.get("reportDate", ""),
        },
        "selected_periodic_filings": periodic,
        "additional_form_review": {
            group_id: {
                "label": ADDITIONAL_FORM_GROUPS[group_id]["label"],
                "research_use": ADDITIONAL_FORM_GROUPS[group_id]["research_use"],
                "filings": rows,
            }
            for group_id, rows in additional.items()
        },
        "primary_document_downloads": downloads,
        "primary_documents_downloaded": sum(1 for item in downloads if item.get("status") == "downloaded"),
        "companyfacts_summary": "research/sec_edgar/sec_companyfacts_summary.json",
        "output_dir": str(output_dir),
    }

    write_json(output_dir / "sec_filing_manifest.json", manifest)
    write_json(output_dir / "sec_companyfacts_summary.json", companyfacts_summary)

    index_lines = [f"# SEC Primary Documents: {args.ticker.upper()}", ""]
    if not downloads:
        index_lines.append("No primary documents downloaded.")
    for item in downloads:
        index_lines.append(f"- {item.get('form')} {item.get('report_date')} {item.get('accession_number')}: {item.get('url')} ({item.get('status')})")
    (output_dir / "primary_documents_index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    if run_dir:
        update_research_packet(run_dir, manifest)
    mirror_to_source_library(output_dir, stock_source_dir)
    print(output_dir / "sec_filing_manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
