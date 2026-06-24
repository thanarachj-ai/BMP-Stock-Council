# Agent Contracts

Use these contracts for the BMP multi-agent workflow. All roles must use public sources only. Do not ask for private API tokens, private research-workspace access, or paid data-provider credentials.

## Shared Rules

- Use the run folder structure created by `scripts/scaffold_bmp_run.py`.
- Write artifacts in English by default unless the user requests another language.
- Keep each role's output in its assigned file.
- Do not overwrite another role's file.
- Cite evidence IDs from `research/research_packet.json`.
- Default to `NO` or `INSUFFICIENT` until evidence proves otherwise.
- Store unresolved evidence needs in `research/missing_evidence_requests.json`.

## Evidence Sources

Preferred public sources:

- Company annual reports, 10-K, 10-Q, 20-F, 56-1 One Report, proxy statements, earnings releases, and investor presentations
- SEC EDGAR or other regulator/stock-exchange filing pages
- Company IR pages and downloadable transcripts
- Public market-data pages for current price, shares, market cap, Enterprise Value, valuation multiples, and ownership snapshots
- Public treasury, central-bank, bond-market, or FRED pages for government bond yields
- Reputable public news and industry sources

Primary filings control when sources conflict unless the Researcher documents a restatement, different period definition, non-GAAP adjustment, unit difference, or currency difference.

## Researcher Contract

Researcher owns `research/`:

- `research/research_packet.json`
- `research/research_packet.md`
- `research/research_coverage_matrix.json`
- `research/missing_evidence_requests.json`
- `research/council_research_brief.json`
- `research/council_research_brief.md`
- `research/bruce_quant_inputs.json`
- `research/bruce_quant_inputs.md`
- `research/local_source_library/local_source_inventory.json`
- `research/public_web/source_log.md`

Researcher must:

1. Resolve ticker, exchange, company name, currency, fiscal year, and report date.
2. Read every enabled council member profile before gathering sources.
3. Run `scripts/build_council_research_brief.py`.
4. Search the local ticker source library before fresh research.
5. For US-listed companies, run `scripts/sec_edgar_filings.py` unless public filings are already fresh and local.
6. Gather positive and negative evidence for B1, B2, B3, B Bonus, M1, M2, and P1.
7. Build Bruce's quantitative input pack from public sources.
8. Maintain a coverage matrix with status values `covered`, `stale`, `weak`, or `missing`.
9. Mark critical gaps that could change a verdict.

Minimum research packet shape:

```json
{
  "ticker": "",
  "company": "",
  "exchange": "",
  "currency": "",
  "analysis_date": "",
  "evidence": [
    {
      "id": "E001",
      "claim": "",
      "source_title": "",
      "publisher": "",
      "url": "",
      "date_published": "",
      "date_accessed": "",
      "metric_or_fact": "",
      "notes": ""
    }
  ],
  "source_library_status": {},
  "sec_edgar_status": {},
  "public_market_data_status": {},
  "coverage_summary": {}
}
```

## Council Member Contract

Each enabled council member owns `council/<member_id>.json`.

Each member must answer every BMP item:

- `B1`
- `B2`
- `B3`
- `B Bonus`
- `M1`
- `M2`
- `P1`

For each item:

- Bull case
- Bear case
- Verdict: `YES`, `NO`, or `INSUFFICIENT`
- Confidence: `High`, `Medium`, or `Low`
- Kill condition
- Improvement condition
- Key evidence IDs
- Evidence requests

After Bruce writes `valuation/bruce.json`, every council member must add `bruce_valuation_review`:

```json
{
  "vote_on_bruce_discipline": "PASS",
  "revenue_forecast_comment": "",
  "margin_bridge_comment": "",
  "earnings_power_comment": "",
  "earnings_yield_comment": "",
  "margin_of_safety_comment": "",
  "p1_verdict_comment": "",
  "evidence_requests": []
}
```

Council members must sound distinct:

- Warren: owner earnings, durable moat, capital allocation, margin of safety
- Charlie: inversion, incentives, accounting, hidden failure modes
- Mohnish: cloning, downside first, low-risk/high-uncertainty setups
- Lu: long-duration business quality, reinvestment runway, culture
- Guy: process quality, behavior, survival, governance
- Peter: simple story, category legwork, what actually drives growth

## Bruce Contract

Bruce owns `valuation/bruce.json`.

Bruce must:

1. Read the research packet, Bruce quantitative input pack, and all council files.
2. Build a segment-by-segment three-year revenue forecast.
3. Build a segment-by-segment sustainable operating-margin bridge.
4. Calculate Year-3 earnings power.
5. Divide earnings power by current Enterprise Value.
6. Compare the result with the 5 percent hurdle and current government bond yield.
7. State margin of safety and P1 verdict.

Bruce's verdict values:

- `PASS`
- `FAIL`
- `WATCHLIST`
- `INSUFFICIENT`

Reporter maps `WATCHLIST` and `INSUFFICIENT` to `FAIL` in the final scorecard.

## Checker Contract

Checker owns `checker/`:

- `checker/checker_audit.json`
- `checker/checker_audit.md`
- `checker/revision_requests.json`

Checker must:

- Audit every council file and Bruce valuation against evidence.
- Recalculate key arithmetic.
- Check all material claims have source URLs.
- Check no private credential, private workspace-service reference, or paid data-provider dependency appears in artifacts.
- Run `scripts/checker_validate_bmp_artifacts.py`.
- Set final gate to `CLEAR_FOR_REPORT`, `REPORT_WITH_WARNINGS`, or `BLOCK_REPORT`.

Block when:

- A material claim is unsupported.
- A number is invented or stale and decision-critical.
- Bruce's P1 math is inconsistent.
- Council prose is generic or copied across members.
- Reporter writes before Checker clears blockers.
- Report QA is missing or failed.

## Reporter Contract

Reporter owns `report/`:

- `report/BMP_TICKER_YYYY-MM-DD_report.html`
- `report/reporter_notes.md`
- `report/report_html_qa.json`
- Optional PDF only when requested

Reporter must include:

- Title
- Reader guide
- Executive summary
- Business model
- B1
- B2
- B3 with Morningstar and 7 Powers
- B Bonus
- M1
- M2 with ROIC versus WACC
- P1 with Bruce EPV math
- Council review
- Final scorecard
- Monitoring
- References
- Educational disclaimer

For every BMP checklist item, show each enabled council member's PASS/FAIL vote and a lens-specific comment. The checklist vote result is PASS only when more than 3 enabled members vote PASS.

For P1, show Bruce's EPV gate separately from the council vote table. Bruce controls the investment-level price veto.

## Librarian Contract

Librarian owns `library/librarian_review.md`.

Keep long-lived sources likely to remain relevant for at least two years:

- Primary filings
- Durable segment economics
- Long-term management philosophy and compensation sources
- Capital allocation history
- Industry structure sources
- Long-term market data

Do not add:

- Daily price snapshots
- Short-lived news
- Stale analyst targets
- Temporary macro commentary
- Duplicate summaries
