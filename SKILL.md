---
name: bmp
description: Multi-agent public stock deep-dive workflow using Adam Seessel's BMP checklist, a Researcher, investor council, Bruce-led Earnings Power Value valuation, Checker, Reporter, and Librarian. Use when Codex needs to analyze a listed stock, ticker, public company, long-term compounder, value-investing thesis, BMP checklist, council report, Bruce EPV valuation, local ticker source library, or an explanation-first BMP HTML report using public web sources without private API tokens.
---

# BMP

Run a rigorous public-stock analysis system based on Adam Seessel's Business, Management, Price checklist. This public GitHub version is evidence-first, local-source-first, and token-free: it uses company filings, investor relations pages, public regulator/exchange pages, public market-data pages, reputable news, and web search. It does not use private research workspaces, paid data-provider APIs, or token-gated research tools.

Default final output is an English, explanation-first, self-contained HTML report saved under the current workspace. PDF export is optional only when the user explicitly asks for it. Research, council, valuation, checker, report, and library artifacts remain structured and reusable.

## Public Source Rules

- Do not ask the user for API tokens or private data-provider credentials.
- Do not use private research workspaces or token-gated financial-data APIs.
- Prefer primary filings and company sources over secondary sources.
- Use public web search for current prices, filings, management changes, rates, news, estimates, and market data.
- Use public EDGAR endpoints and downloadable filing pages for US-listed companies. These require no secret key; set `SEC_USER_AGENT` only as a courtesy contact string when running SEC downloads.
- For every material claim, store source title, publisher, URL, date published, date accessed, and the exact metric or claim supported.
- If a source or metric cannot be verified publicly, mark the gap and let it affect the verdict.

## Workflow

1. Resolve ticker, exchange, currency, company name, report language, and output folder. If the listing is ambiguous, ask one concise question before researching.
2. Run `scripts/scaffold_bmp_run.py` to create the run folder unless continuing an existing run.
3. Read the core references before full analysis:
   - `references/agent_contracts.md`
   - `references/bmp_checklist.md`
   - `references/council_profiles.md`
   - `references/council_roster.json`
   - `references/valuation_lead.json`
   - `references/report_spec.md`
4. For each enabled council member in `references/council_roster.json`, read that member's profile under `references/council_members/`. For valuation, read the configured valuation lead under `references/valuation_leads/`.
5. Have the Researcher run `scripts/build_council_research_brief.py` to create `research/council_research_brief.json` and `research/council_research_brief.md`. Use the combined BMP playbook as the evidence demand map before source gathering.
6. Use the local ticker source library first. For workspace `/path/to/Stocks` and ticker `TICKER`, create or reuse `/path/to/Stocks/TICKER/source_library/`. Check it for existing filings, company IR sources, industry sources, web evidence, and previous durable artifacts.
7. For US-listed stocks, read `references/sec_edgar_research.md`, then run `scripts/sec_edgar_filings.py` to fetch EDGAR metadata and download primary filing HTML documents. Store outputs under both `research/sec_edgar/` and `TICKER/source_library/sec_edgar/`.
8. Review relevant filing lanes beyond 10-K/10-Q when they affect Business, Management, Price, dilution, ownership, incentives, or recent material events: 8-K, DEF 14A, Forms 3/4/5, SC 13D/G, 13F context, S-1/S-3/424B, merger/tender-offer filings, 20-F/6-K for foreign private issuers, and exhibit indexes.
9. Have the Researcher read `references/bruce_quant_research.md` and build `research/bruce_quant_inputs.json` plus `research/bruce_quant_inputs.md` for Bruce's P1 EPV test.
10. Create or update `research/research_coverage_matrix.json` before council analysis. The matrix must show which BMP domains are covered, stale, weak, or missing, including council-profile-driven evidence needs, Bruce quantitative-input coverage, local source-library coverage, SEC filing freshness, broader filing review, public-market-data coverage, and negative research.
11. Fill gaps with current primary and high-quality secondary sources. Store unresolved needs in `research/missing_evidence_requests.json`.
12. Have each enabled council member analyze the same research packet independently. Use one subagent per enabled member when subagent tools are available; otherwise run the contracts sequentially and keep each member's output isolated in `council/<member_id>.json`.
13. Consolidate evidence requests from council members, Bruce, and Checker with `scripts/collect_evidence_requests.py`. Resolve high-priority requests or explicitly mark them as unresolved gaps that affect verdicts.
14. Have Bruce read the research packet, quantitative input pack, and council outputs, then produce `valuation/bruce.json`. Bruce owns P1: sustainable revenue, sustainable operating margin, Year-3 earnings power, enterprise-value earnings yield, 5 percent test, margin of safety, and PASS/FAIL-style verdict.
15. Have every enabled council member review Bruce's valuation and add `bruce_valuation_review` to their own council file.
16. Have Checker audit council files, Bruce valuation, source evidence, financial statement numbers, public-market-data cross-checks, formulas, and arithmetic. Checker runs `scripts/checker_validate_bmp_artifacts.py` and writes `checker/checker_audit.json`, `checker/checker_audit.md`, and `checker/revision_requests.json`.
17. If Checker blocks the report, route targeted revisions back to the responsible Researcher, council member, Bruce, or Reporter. Rerun Checker until the final gate is `CLEAR_FOR_REPORT` or `REPORT_WITH_WARNINGS`.
18. Have Reporter synthesize council work, Bruce valuation, and Checker audit into the final HTML report using `references/report_template_canonical.md` and `references/report_template_canonical.html` as the structure guide.
19. Have Librarian recommend which sources should remain in the local ticker source library because they are likely to stay relevant for at least two years.
20. Before final delivery, rerun `scripts/checker_validate_bmp_artifacts.py` and fix missing artifacts, broken references, unresolved blocking evidence requests, missing report QA, missing council comments on Bruce valuation, or inconsistent price assumptions.

Resolve every bundled script and reference relative to this skill folder. If the current working directory is the stock workspace, call scripts with absolute paths or change directory to the skill folder first.

## Run Folder

Use this structure by default. Every run lives under `BMP/`, while durable source material lives under the ticker folder:

```text
TICKER/
  source_library/
    local_source_inventory.json
    sec_edgar/
      sec_filing_manifest.json
      primary_documents/
      companyfacts/
    company_ir/
    industry/
    web/
  reports/
  runs/
BMP/
  TICKER_YYYY-MM-DD/
    manifest.json
    research/
      research_packet.json
      research_packet.md
      research_coverage_matrix.json
      missing_evidence_requests.json
      council_research_brief.json
      council_research_brief.md
      bruce_quant_inputs.json
      bruce_quant_inputs.md
      local_source_library/
        local_source_inventory.json
      sec_edgar/
        sec_filing_manifest.json
        sec_companyfacts_summary.json
        primary_documents/
      public_web/
        source_log.md
    council/
      <member_id>.json
    valuation/
      bruce.json
    checker/
      checker_audit.json
      checker_audit.md
      revision_requests.json
    report/
      BMP_TICKER_YYYY-MM-DD_report.html
      BMP_TICKER_YYYY-MM-DD_report.pdf  # optional export only when requested
      reporter_notes.md
      report_html_qa.json
    library/
      librarian_review.md
```

The scaffold script creates placeholders. Replace placeholders with real analysis before validation.

## Research Rules

Default to "NO" until evidence proves otherwise. If a point is borderline, mark it "NO" or "INSUFFICIENT", not a soft yes. Lack of evidence is not bullish.

Research must include negative evidence: strongest bear case, deterioration in unit economics, customer or supplier pressure, capital allocation mistakes, regulatory pressure, disruption risk, accounting concerns, dilution, leverage, cyclicality, and management credibility issues.

Local ticker folders are the default source library. Reuse an existing `TICKER/source_library/` folder when found; create it only when absent. Search it before new research and update `research/local_source_library/local_source_inventory.json` with reused or added sources.

For financial history and ratios, use public filings, company filings, XBRL/companyfacts where available, company IR materials, exchange pages, reputable public market-data pages, and calculation tables. Do not use private API-token workflows.

## Subagent Pattern

1. Researcher first pass: owns `research/`, creates the research packet, Bruce quantitative input pack, coverage matrix, and missing-evidence queue.
2. Council: one agent per enabled council member, each owning one `council/<member_id>.json`.
3. Researcher second pass: resolves high-priority evidence requests or marks gaps with verdict impact.
4. Valuation lead: Bruce owns `valuation/bruce.json`.
5. Checker first pass: owns `checker/`, audits outputs against evidence and runs mechanical validation.
6. Targeted redo pass: only the named owner revises the named file.
7. Checker rerun: verifies revisions.
8. Reporter: owns `report/`.
9. Librarian: owns `library/`.

Tell every subagent that other agents may be editing separate files and that they must not overwrite unrelated work.

## Council Output Contract

Each council member must answer every BMP checklist question with:

- Bull case
- Bear case
- Verdict: `YES`, `NO`, or `INSUFFICIENT`
- Confidence: High, Medium, or Low
- Kill condition
- Improvement condition
- Key evidence IDs
- Evidence requests for missing facts that could change the verdict

Council answers must be written in that member's distinct analytical lens. Do not reuse generic wording across members.

After Bruce writes `valuation/bruce.json`, each council member must add `bruce_valuation_review` to their own file. Reporter maps council votes to final report votes: `YES` maps to `PASS`; `NO` and `INSUFFICIENT` map to `FAIL`.

For each BMP checklist item, the final checklist vote result is `PASS` only when more than 3 enabled council members vote `PASS`; otherwise it is `FAIL`. Price must additionally display Bruce's EPV gate. If the council vote result and Bruce's P1 gate disagree, Reporter must show both and explain that Bruce controls the Price math and investment-level price veto.

## Reporter Requirements

The final report must include:

- Executive summary, BMP score, overall verdict, and key variable to monitor
- Business Model, B1, B2, B3, B Bonus, M1, M2, P1 Earnings Yield, Council Review, Final Scorecard, Monitoring, and References
- Researcher evidence before each council vote table
- Council matrix with every enabled member's PASS/FAIL vote and lens-specific comment
- B3 Morningstar moat analysis and 7 Powers analysis
- M2 ten-year ROIC versus Damodaran-style WACC value-spread analysis where public data exists
- Bruce's visible P1 calculation, current government bond yield context, 5 percent hurdle, and margin of safety
- Checker audit summary
- Clickable source URLs for every material source
- Educational disclaimer, not investment advice

Reporter or Checker must record HTML QA in `report/report_html_qa.json`; final delivery is incomplete while that artifact is missing, `not_run`, or `failed`.

## Bundled Resources

- `references/bmp_checklist.md`: Detailed BMP checklist and scoring rules.
- `references/agent_contracts.md`: Role prompts, handoff schemas, and subagent instructions.
- `references/council_profiles.md`: Council roster maintenance instructions and profile template.
- `references/council_roster.json`: Source of truth for enabled council members.
- `references/council_members/`: One profile file per council subagent.
- `references/valuation_lead.json`: Source of truth for the valuation lead.
- `references/valuation_leads/bruce.md`: Bruce valuation lead profile and EPV rules.
- `references/sec_edgar_research.md`: Public EDGAR research instructions for US filing freshness and local filing downloads.
- `references/bruce_quant_research.md`: Researcher-owned quantitative input standard for Bruce's P1 EPV work.
- `references/report_spec.md`: HTML report structure, chart expectations, council vote matrix, Bruce P1 display rules, and validation checklist.
- `references/report_template_canonical.md`: Canonical report layout, section order, table order, and adaptation rules.
- `references/report_template_canonical.html`: Neutral exemplar used as the default visual/structural template.
- `scripts/scaffold_bmp_run.py`: Create a standard run folder and placeholder artifacts.
- `scripts/build_council_research_brief.py`: Generate Researcher's per-run evidence-demand brief.
- `scripts/manage_council_roster.py`: Add, list, enable, disable, or remove council members.
- `scripts/sec_edgar_filings.py`: Fetch public SEC EDGAR filing metadata, XBRL companyfacts summaries, and local primary-document downloads.
- `scripts/collect_evidence_requests.py`: Merge council, Bruce, and Checker evidence requests.
- `scripts/checker_validate_bmp_artifacts.py`: Checker-owned validation runner.
- `scripts/validate_bmp_artifacts.py`: Mechanical validation checks for core artifacts, council files, source URLs, revision gates, and checklist coverage.
