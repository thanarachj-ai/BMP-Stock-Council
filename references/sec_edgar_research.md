# SEC EDGAR Research

Use public SEC EDGAR endpoints and filing pages as the primary filing source for US-listed companies.

Official documentation:

- https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- https://www.investor.gov/introduction-investing/getting-started/researching-investments/using-edgar-research-investments
- https://www.sec.gov/about/webmaster-frequently-asked-questions

Key public EDGAR endpoint facts:

- `data.sec.gov` provides public JSON endpoints for company submissions and XBRL facts without secret keys.
- Submissions endpoint: `https://data.sec.gov/submissions/CIK##########.json`
- Company facts endpoint: `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`
- SEC filing data updates throughout the day.
- Use a declared `User-Agent`; set `SEC_USER_AGENT` to a real contact string when possible.
- Stay below SEC's 10 requests per second limit.

## Researcher Flow

1. Create or reuse the local ticker source library at `WORKSPACE/TICKER/source_library/`.
2. Search `WORKSPACE/TICKER/source_library/sec_edgar/` and existing `WORKSPACE/BMP/TICKER_*/research/sec_edgar/` folders before fresh downloads.
3. Fetch SEC filing metadata and primary filing documents:

```bash
python3 scripts/sec_edgar_filings.py TICKER --run-dir RUN_DIR --company "Company Name"
```

The helper downloads selected primary filing HTML documents by default. Use `--skip-primary-doc-download` only for troubleshooting metadata-only runs.

4. Review:

- `research/sec_edgar/sec_filing_manifest.json`
- `research/sec_edgar/sec_filing_upload_queue.md`
- `research/sec_edgar/sec_companyfacts_summary.json`
- `research/sec_edgar/primary_documents_index.md`
- `research/sec_edgar/primary_documents/`
- `WORKSPACE/TICKER/source_library/sec_edgar/sec_filing_manifest.json`
- `WORKSPACE/TICKER/source_library/sec_edgar/primary_documents_index.md`
- `WORKSPACE/TICKER/source_library/sec_edgar/primary_documents/`

5. If the latest annual filing or latest periodic filing is missing from the local ticker source library, rerun the helper without `--skip-primary-doc-download`. The expected files are visible under `primary_documents/` and indexed in `primary_documents_index.md`.

6. Update `research/research_packet.json`:

- `sec_edgar_status.checked = true`
- `sec_edgar_status.cik`
- `sec_edgar_status.latest_10k`
- `sec_edgar_status.latest_10q`
- `sec_edgar_status.latest_periodic_filing`
- `sec_edgar_status.annual_filing_in_source_library`
- `sec_edgar_status.latest_periodic_filing_in_source_library`
- `sec_edgar_status.primary_documents_downloaded`
- `sec_edgar_status.primary_documents_dir`
- `sec_edgar_status.local_source_dir`

7. Add evidence rows for material facts from the filings. Use SEC primary document URLs, filing dates, reporting periods, and accession numbers.

## Investor.gov Form-Type Research Map

Investor.gov's EDGAR guide is useful because it links common research questions to the filing types that answer them. Apply this map after the 10-K/10-Q freshness check:

| Research need | EDGAR forms | What Researcher should extract |
| --- | --- | --- |
| Financial statements, risk factors, MD&A, segments, liquidity, accounting | 10-K, 10-Q | Audited/unaudited statements, MD&A, risk updates, segments, debt/liquidity, accounting changes, period comparability |
| Material events before the next periodic report | 8-K | Item numbers, event date, management changes, compensation changes, material agreements, acquisitions, impairments, auditor changes, debt obligations, delisting, non-reliance on financials |
| Governance, executive compensation, shareholder votes, officer/director ownership | DEF 14A, PRE 14A, DEFA14A; 10-K fallback | Compensation structure, incentives, board independence, ownership alignment, shareholder proposals, vote results when available |
| Insider ownership and transactions | Forms 3, 4, 5 and amendments | Insider purchases/sales, option exercises, grants, planned sales, tax-withholding sales, ownership alignment |
| Large beneficial owners and activists | SC 13D, SC 13G, DEF 14A ownership tables | Active/passive holder status, ownership changes, control intent, concentration, activist signals |
| Institutional holder context | 13F-HR filed by managers | Supporting context only; do not overstate because 13F is manager-filed, delayed, and not a complete issuer ownership register |
| M&A, mergers, tender offers, securities as consideration | PREM14A, DEFM14A, S-4, 425, SC TO-T, SC TO-I, SC 14D9, related 8-Ks | Deal terms, strategic rationale, shareholder vote, fairness/risks, dilution, consideration, recommendation |
| Public offerings and dilution | S-1, S-3, 424B filings, UPLOAD, CORRESP | IPO/secondary/shelf terms, dilution risk, use of proceeds, risk disclosures, SEC review issues when public |
| Foreign private issuer reporting | 20-F, 6-K, F-1 | Annual audited financials, interim/current disclosures, home-country filings and communications |
| Material contracts and legal documents | Exhibit indexes in 10-K, 10-Q, 8-K, proxy, registration, and merger filings | Bylaws, charters, debt agreements, customer/supplier contracts, merger agreements, compensation plans, risk-changing covenants |

The helper script writes this map into `sec_filing_manifest.json.edgar_research_map`. The map identifies candidate filings; the Researcher still has to read material filings and convert facts into evidence IDs.

## Freshness Rules

- Latest annual filing: stale if older than about 455 days unless there is a clear fiscal-calendar reason.
- Latest periodic filing: stale if no 10-K or 10-Q has been filed in about 135 days, unless the company has a known reporting delay or fiscal-calendar exception.
- If a newer 10-K has been filed after the latest 10-Q, the 10-K can be the latest periodic filing for current financial statements.
- For foreign private issuers or non-US listings, mark this flow not applicable and use 20-F, 6-K, annual reports, or local exchange filings instead.

## Local Source Library Storage Criteria

Store in `WORKSPACE/TICKER/source_library/sec_edgar/` when:

- It is a latest 10-K or 10-Q used for Business, Management, Price, or Checker validation.
- It is a latest proxy, major 8-K, 20-F/6-K, registration/prospectus, merger/tender-offer filing, or material exhibit that is central to the thesis and likely to remain relevant for at least two years.
- It resolves a missing or stale source-library gap.
- It is likely to remain relevant for at least two years.

Keep only in the run folder when:

- The source is a daily market-data snapshot, temporary news item, or short-lived commentary.
- The filing is a routine insider sale or routine 8-K with no durable thesis relevance.

## Checker Use

Checker should prefer SEC filings and XBRL companyfacts for US financial statement numbers. When council members or Bruce cite financial statement values, Checker should trace the number to one of:

- SEC filing primary document URL.
- SEC companyfacts concept, period, unit, form, and filed date.
- Company investor relations filing that matches SEC.

If a third-party data source conflicts with SEC filings, Checker should flag the mismatch unless the Researcher documents a restatement, different period definition, non-GAAP adjustment, or currency/unit difference.
