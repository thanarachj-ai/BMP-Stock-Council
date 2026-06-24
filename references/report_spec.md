# Report Specification

Primary deliverable: an English, explanation-first, self-contained HTML report saved as `report/BMP_TICKER_YYYY-MM-DD_report.html`. PDF export is optional only when the user explicitly asks for it.

Canonical default template: use `references/report_template_canonical.md` plus `references/report_template_canonical.html`. The canonical report template is the default structure for every future output. Keep its layout, section order, table order, CSS/interaction primitives, and reader flow, but replace all prior-company facts, segments, evidence IDs, charts, sources, council comments, valuation inputs, and verdicts with the target company's evidence-backed content.

## Language And Reader Rules

- Use English as the default visible language for titles, section labels, explanations, vote tables, chart notes, references, and final user summaries.
- The report must be understandable to a first-time follower. Do not use a chart, table, or metric without a nearby explanation.
- Write for comprehension first. Use short sections, plain-English summaries, definition callouts, and clear "why this matters" language before technical detail.
- Do not make the report hard to digest. Avoid long uninterrupted paragraphs, unexplained abbreviations, dense tables without summaries, or chart-only sections.
- Every analytical section must include explanatory text with these reader jobs, either as exact labels or equivalent English labels:
  - `What it means`
  - `Evidence`
  - `Why it matters`
- Keep wording professional, skeptical, and capital-protective. Avoid promotional language.
- Do not allow Chinese, Japanese, or Korean script in visible report text except inside URLs or official source titles that truly require it.

## Technical Requirements

- Build one self-contained `.html` file that opens directly in a browser without a local server.
- Keep CSS inline in `<style>` and any optional JavaScript inline in `<script>`. Do not depend on CDN assets, Google Fonts, remote JavaScript, Chart.js, D3, Plotly, Observable, React, or Vue.
- Use local/system fonts and local inline SVG/HTML/CSS chart primitives.
- Use semantic long-form sections such as `<section id="cover">`, `<section id="b1-council-vote">`, `<section id="b3-moat">`, `<section id="p1-bruce">`, `<section id="final-scorecard">`, and `<section id="references">`.
- Include a table of contents or sticky navigation for long reports. Navigation is allowed and encouraged in HTML.
- Include interactive explainer controls that improve understanding, such as checklist tabs, council-member filters, native `<details>` evidence expanders, glossary/tooltips, or jump links.
- Optional collapsible details are allowed, but core verdicts, council votes, Bruce calculations, council reviews of Bruce valuation, key risks, scorecard, and references must be visible without requiring interaction.
- Design must be responsive for desktop and mobile. Tables may horizontally scroll only when needed, but the main narrative, verdicts, and key numbers must not be clipped.
- Include print CSS for clean browser printing. PDF export may reuse the same HTML, but the PDF is not required unless explicitly requested.
- Every material source in the references must include a clickable URL when available.

## Required Report Arc

Use this exact major-section flow by default. It must match the canonical template. Do not add standalone `Financial Quality`, standalone `Sensitivity`, `Latest Results`, or standalone `Bruce EPV` sections. Put those facts inside the relevant Business, Management, or Price checklist sections so a non-technical reader can follow the investment logic in order.

1. Title / cover: company name, ticker, exchange, analysis date, current price, market cap, Enterprise Value, and overall verdict.
2. How To Read / Reader Guide: BMP checklist, council members, vote rule, Bruce's Price role, glossary-style definitions, member filter, and educational disclaimer. Use section id `how-to-read`.
3. Executive Summary: key findings, full vote score out of 7, B+M subtotal out of 6, council P1 vote, Bruce P1 gate, investment verdict, and key monitoring variable.
4. Business Model: a deeper but simple explanation of the businesses the company is in, with a revenue-segment table showing each segment's amount, customers, how the segment gains customers, and why customers pay this company instead of alternatives. Include a visible revenue-segment mix chart and a visible revenue plus operating-margin chart.
5. B1 Large and Growing Market.
6. B2 Low Market Share.
7. B3 Moat.
8. B Bonus Disruption Shield.
9. M1 Owner Mindset.
10. M2 Value Drivers.
11. P1 Earnings Yield.
12. Council Review: an overall summary of each council member's view on the stock, not a duplicate standalone Bruce section.
13. Final Scorecard.
14. Monitoring: all material items council members suggest monitoring, including kill conditions, improvement conditions, and what would change the verdict. Each member's monitoring card must be distinct and playbook-specific, not a repeated generic risk sentence.
15. References and method notes.

Checklist sections B1, B2, B Bonus, M1, and M2 must follow this internal order, matching the canonical template:

1. A simple plain-English explanation of the checklist item.
2. The evidence Researcher collected for that item, laid out clearly before the vote table. Use short evidence cards, bullets, or a simple table with source IDs and why each item matters.
3. A `vote-summary` stating `Vote Result`, pass count, and the majority rule.
4. The council vote table. For each member, include the member's PASS/FAIL vote, confidence, evidence IDs, a short reminder of that member's investment playbook, and how that playbook links to the member's checklist comment.
5. The vote result and what would change the vote.

B3 must include the evidence-first section plus visible `Morningstar` moat analysis and visible `7 Powers` analysis before the vote summary and council table.

M2 must include a quantitative `ROIC vs WACC` value-creation panel, ROIC/WACC data table, and latest WACC input table before the vote summary and council table. Use Damodaran-style WACC:

- ROIC should be sourced from standardized financial data or calculated as NOPAT divided by average invested capital, with the method stated plainly.
- WACC should show risk-free rate, equity risk premium, beta, cost of equity, pre-tax cost of debt, tax rate, equity weight, debt weight, and final WACC.
- The report must show the latest WACC input table and a ten-year history comparing ROIC, WACC, and ROIC minus WACC when public data exists.
- Explain in plain English whether the company created value each year, whether the spread is widening or narrowing, and what operational or capital-allocation driver matters most.
- Label the calculation `Damodaran-style WACC` unless it is a direct company-specific WACC from Damodaran. If using Damodaran industry beta, ERP, cost-of-debt, or industry WACC tables, cite the exact Damodaran source in References.

P1 Earnings Yield must start with Bruce's valuation first and follow the canonical order: Bruce setup, metric dashboard, Revenue Growth Forecast bar chart, Segment Revenue Growth Forecast table, revenue reconciliation, Sustainable Operating Margin setup, Segment Operating Margin Bridge table, margin reconciliation, Accounting Distortion, Accounting Adjustment Bridge, Maintenance vs Growth, Harvest Mode decision, Pure-play margin decision, historical margin table, Earnings Power and Enterprise Value math table, Margin of Safety callout, Input Logic And Sources table, and only then the P1 Council Review Of Bruce Valuation table. Show Bruce's base-case numbers only in the main report: sustainable revenue, segment revenue growth forecast, segment operating margin bridge, accounting adjustments, earnings power, Enterprise Value, Earnings Yield, 5 percent hurdle, and margin of safety. Explain the logic behind each input in plain English. Then show the P1 council table, where each member links their investment playbook to their comments on Bruce's valuation. Do not show a separate sensitivity/scenario section unless the user explicitly asks; if fragility matters, explain it briefly in the P1 text or Monitoring section.

Do not create generic standalone update sections such as `Latest results` unless they directly support a BMP checklist section. Put financial-quality evidence inside Business Model, B/M checklist sections, or P1.

## Council Vote Rules

- The report must show each enabled council member for each of the seven BMP checklist items: B1, B2, B3, B Bonus, M1, M2, and P1.
- Each BMP checklist item should have its own readable council panel or table. Do not hide member votes in a single compressed table only.
- Each member must have:
  - Member name.
  - PASS/FAIL vote.
  - A visible theory anchor naming the member's playbook concept used for that item.
  - One lens-specific comment in a single cell or paragraph.
  - A short playbook connection explaining how that member's investing lens leads to the comment.
  - Confidence.
  - Evidence IDs.
- Map internal council verdicts as follows:
  - `YES` -> `PASS`.
  - `NO`, `INSUFFICIENT`, `WATCHLIST`, or any no-buy/unclear outcome -> `FAIL`.
- For each checklist item, the checklist vote result is `PASS` only when more than 3 enabled council members vote `PASS`.
- Show the pass count explicitly, such as `6 of 6 PASS`.
- Do not hide disagreement. If one or more members fail an item that passes by majority, show their concern.
- Do not use conditional labels such as `PARTIAL`, `WATCHLIST`, `SOFT PASS`, or `PASS WITH CONDITIONS` in vote cells. Put nuance in the comment, not the vote.
- Do not reuse the same member comment, playbook connection, monitoring item, risk, kill condition, or "what would change my view" language across council members. Shared evidence IDs are fine; shared prose is not. If two members watch the same fact, state why each member watches it differently through that member's playbook.
- Do not flatten council voices into generic analyst prose. Warren must sound like an owner judging moats and managers; Charlie must invert; Mohnish must test Dhandho asymmetry; Lu must focus on long-duration evidence and permanent capital loss; Guy must emphasize process and behavior; Peter must use simple story, category, and scuttlebutt framing.
- Do not expose a separate style-signature label, column, paragraph, or JSON-derived field in the report. Use one `Comment` column, and write the member lens naturally inside the comment rather than as repetitive boilerplate.
- Do not build visible comments from a repeated sentence frame such as "`Member Lens uses [angle] on [checklist item]`", "`Evidence point:`", "`Risk point:`", or "`reads the forecast through [angle]`". Those phrases create mechanically distinct but reader-repetitive comments and should be treated as a blocking Reporter/Checker failure.
- Each visible `Comment` cell should be an answer-first judgment specific to that member and that checklist item. The member's lens can appear naturally inside the sentence, but the comment must not start from the same scaffold across rows.

## Price And Bruce Rules

Bruce leads Price math. The report must show both:

- The P1 council vote matrix, using the same majority rule as other checklist items.
- Bruce's EPV gate, which controls the Price math and investment-level price veto.
- The Bruce Method Review Vote, which is each member's `bruce_valuation_review.vote_on_bruce_valuation` and reviews Bruce's valuation discipline only.

If the council P1 vote and Bruce's EPV gate disagree, show both. Explain that Bruce owns the earnings-power math and that BMP Price discipline can veto an otherwise high-quality business.

Do not label the Bruce Method Review Vote as the P1 council vote, P1 checklist vote, investment vote, or price vote. If all members pass Bruce's method review while the P1 investment checklist vote or Bruce P1 Gate is FAIL, the report must explicitly say that the method review passed but the investment price test failed.

P1 must be a Bruce-first section. Start with Bruce's base-case valuation calculation and input logic, then show the P1 council vote/review table. Do not put Bruce's valuation in a later standalone `Bruce EPV` section, and do not show bear/base/bull scenario tables unless the user explicitly requests a sensitivity section.

Bruce sections must visibly include:

- Sustainable Revenue selected as Year-3 sustainable revenue.
- `Revenue Growth Forecast` showing baseline revenue, Year-1 revenue, Year-2 revenue, Year-3 revenue, and three-year CAGR.
- `Segment Revenue Growth Forecast` showing each segment's baseline revenue, Year-1/Year-2/Year-3 growth rates, Year-1/Year-2/Year-3 revenue, evidence IDs, and plain-English reason for the exact selected rates.
- Consolidated revenue reconciliation showing that Year-1, Year-2, and Year-3 revenue equal the sum of the segment forecast rows.
- Organic growth versus non-organic growth evidence.
- Segment-level revenue forecast when segments have different maturity or economics.
- TAM, market share, penetration, and low-share runway evidence when growth is above GDP.
- Conservative deceleration, GDP anchor, and 15 percent growth cap check.
- Sustainable Operating Margin selected.
- `Reported Operating Margin` and the reported-to-sustainable margin bridge.
- `Segment Operating Margin Bridge` showing each segment's Year-3 revenue, reported or historical margin, selected sustainable margin, Year-3 sustainable operating profit, evidence IDs, and plain-English reason for the selected margin.
- Consolidated sustainable margin reconciliation showing total segment operating profit divided by total segment revenue.
- `Accounting Distortion` review for intangible-heavy spending.
- `Accounting Adjustment Bridge` table whenever accounting noise is named. It must show each item, reported amount, pre-tax adjustment, tax effect, after-tax adjustment, treatment, rationale, and evidence IDs. Zero add-backs are acceptable only when the rationale explains why the distortion does not affect earnings power. If Bruce names an add-back candidate but rejects it, the table must show the zero treatment explicitly rather than leaving an unbooked adjustment implied.
- `Maintenance vs Growth` expense split for R&D, SG&A, or marketing when material.
- `Harvest Mode Decision` table or note showing evidence checked, adjustment used, mature Year-3 margin reason, and confidence impact. This is required even when the company is not in harvest mode. A no-adjustment decision is acceptable only when Bruce explains why harvesting growth spend would be inconsistent with sustainable going-concern earnings power or unsupported by evidence.
- `Pure-play Margin Decision` table or note showing evidence checked, adjustment used, mature segment-margin reason, and confidence impact. This is required even when consolidated margins are healthy. Missing pure-play evidence must not become an upward margin adjustment; it should keep the margin conservative, lower confidence, or create an evidence request.
- Albatross or experimental-unit treatment when relevant.
- Sustainable Operating Profit.
- Tax rate.
- Maintenance reinvestment adjustment.
- Earnings Power.
- Current price, market cap, and Enterprise Value.
- Earnings Yield.
- Current 10-year government bond yield.
- 5 percent hurdle.
- Pass/fail.
- EPV per share or implied fair price at a 5 percent yield when available.
- Margin-of-safety conclusion.
- Source-and-derivation table with input, value, period/as-of date, unit/currency, evidence IDs, source priority, derivation, and why used.
- P1 council review table below Bruce's work, with every enabled council member represented.
- Each council member's `Bruce Method Review Vote`, shown as only `PASS` or `FAIL` and labeled as not the P1 investment checklist vote.
- Each council member's lens-specific comment on Bruce's revenue forecast, margin bridge, earnings power, earnings yield, margin of safety, or P1 verdict.
- Each council member's theory anchor and playbook connection for Bruce's valuation review.

Do not rescue a low earnings yield with long DCF assumptions, terminal value, or a vague growth story. Bruce must forecast exactly three years of sustainable revenue, show why the growth is organic and conservatively decelerated, and use Year-3 earnings power divided by current Enterprise Value for the P1 5 percent test.

## Interaction And Explanation Rules

The HTML report must help the reader learn the analysis rather than merely store it.

- Start with a compact executive dashboard: final verdict, checklist score, Bruce P1 gate, three most important reasons, and one key monitoring variable.
- Keep the Business Model section reader-friendly but richer than a company description: show what the company sells, who pays, how money is earned, why customers choose it, what has to remain true for the business model to keep working, each revenue segment's size, and operating margin next to revenue.
- Use plain-English explainer callouts before technical tables: "What this means in simple terms", "Why this can break", or equivalent labels.
- Include interactive navigation for the major report arc.
- Include at least one interaction pattern for council analysis, such as member filters, checklist tabs, expandable member cards, or compare-all table toggles.
- Include expandable evidence details for dense source tables or long derivations.
- Use glossary/tooltips or short inline definitions for terms such as EPV, earnings yield, Enterprise Value, moat, maintenance capex, and margin of safety.
- Keep interaction accessible: controls should be keyboard-focusable, labeled, and not required to see core conclusions.

## B3 Moat Rules

The B3 section must visibly include the words `Morningstar` and `7 Powers`.

Show both frameworks:

- Morningstar's five moat types: switching costs, network effects, intangible assets, cost advantage, and efficient scale.
- Hamilton Helmer's 7 Powers: scale economies, network economies, counter-positioning, switching costs, branding, cornered resource, and process power.

Render two separate visible radar/spider visuals:

- One radar for Morningstar's five moat types.
- One radar for 7 Powers.

Also include an explanation of which dimensions are strong, weak, or absent, why that matters, moat durability, and moat erosion risks. If a radar cannot render, replace it with a table and a visible limitation note; do not leave a blank chart.

## Chart Rules

Use self-contained chart rendering:

- Bar charts: inline SVG `<rect>` or HTML/CSS bars with numeric labels.
- Line charts: inline SVG `<polyline>` or `<path>`.
- Donut/pie charts: inline SVG circles or a labeled stacked bar if slice labels would be fragile.
- Radar charts: inline SVG polygons for Morningstar and 7 Powers.
- ROIC vs WACC charts: inline SVG/CSS, preferably a line or bar-plus-line chart showing ROIC, WACC, and the value spread across 10 years.
- Scenario charts: use only when the user explicitly requests sensitivity/scenario analysis. The default report should keep P1 to Bruce's base case and move fragility notes into P1 or Monitoring.

Analytical charts must be interactive HTML/SVG/CSS, not static picture exports. Do not render the revenue and margin picture, Morningstar radar, 7 Powers radar, ROIC/WACC chart, or other analytical visuals as PNG/JPEG/WebP screenshots or `<img>` tags. Each chart must include at least one reader-useful interaction such as focusable data points with titles/tooltips, legend toggles, show/hide data buttons, expandable source/data tables, or accessible native `<details>` data views.

Every chart must include:

- Clear title.
- Visible data labels.
- Units.
- Source note or evidence IDs.
- A short explanation of how to read the chart and why it matters.

Avoid overlapping labels. Move labels outside narrow bars or use a table/legend. Do not use `white-space: nowrap` inside narrow chart segments.

## Checker And Reporter QA

Before final delivery:

- Confirm the primary file is `report/BMP_TICKER_YYYY-MM-DD_report.html`.
- Confirm the report uses the canonical template structure: section ids appear in this order: `cover`, `how-to-read`, `executive-summary`, `business-model`, `b1-council-vote`, `b2-council-vote`, `b3-moat`, `bbonus-council-vote`, `m1-council-vote`, `m2-council-vote`, `p1-bruce`, `council-overall-review`, `final-scorecard`, `monitoring`, `references`.
- Confirm the canonical layout primitives are present: sticky `.nav`, dashboard metric cards, `.grid.two`, `.grid.three`, `.table-wrap`, `.vote-table`, `.vote-summary`, `.evidence-card`, `.review-card`, `.chart-block`, `.chart-data`, member filters, local inline SVG/CSS charts, and print CSS.
- Confirm no prior-company company name, ticker, segment names, evidence IDs, or source claims remain in a non-TICKER report.
- Confirm the HTML exists, is non-empty, opens locally, and is self-contained.
- Confirm the HTML has meaningful `<section>` elements and usable anchors for cover, council votes, B3, P1, scorecard, and references.
- Confirm chart primitives exist: `<svg>`, `<rect>`, `<polyline>`, `<path>`, `<circle>`, `<polygon>`, `.bar-fill`, `.chart-row`, or equivalent local vector/CSS primitives.
- Confirm analytical charts are interactive local HTML/SVG/CSS, not raster image exports or static screenshots.
- Confirm every analytical chart has a nearby `chart-data` details block, visible backing data rows or point titles, and evidence IDs/source links for the charted values. SVG analytical charts must have a backing data table.
- Confirm there are no required CDN chart, JavaScript, or font dependencies.
- Confirm Business Model includes each material revenue segment, segment amount, customer type, how the segment gains customers, why customers pay, a segment revenue/mix chart, and an operating-margin chart. Missing segment economics or hidden-only margin data is a blocking issue.
- Confirm B3 contains `Morningstar`, `7 Powers`, and two separate radar/spider visuals.
- Confirm M2 contains `ROIC vs WACC`, `Damodaran-style WACC`, latest WACC inputs, and a ten-year value-spread chart/table when public data exists.
- Confirm the report contains a council vote matrix for all seven checklist items and every enabled council member.
- Confirm each B/M checklist section presents Researcher's evidence before the council vote table.
- Confirm each council vote table includes every enabled member's playbook connection, lens-specific comment, PASS/FAIL vote, confidence, and evidence IDs.
- Confirm each council vote table visibly includes every enabled member's theory anchor and a `Comment` cell. If a reader could remove the member names and the comments would still sound interchangeable, block the report.
- Confirm the report contains a Council Review section summarizing every enabled member's overall view on the stock.
- Confirm every council member's visible comments, Council Review card, P1 review, and Monitoring card are distinct. If the same prose appears for multiple members, or if comments use repetitive template phrasing, block the report and send the duplicated owner work back for revision.
- Confirm visible `Comment` cells are not assembled from repeated scaffolding such as "`uses ... on ...`", "`Evidence point:`", "`Risk point:`", or "`reads the forecast through ...`". If the table uses those markers repeatedly, block the report even when exact duplicate text is absent.
- Confirm visible paragraphs, table cells, Council Review cards, Monitoring cards, and P1 review comments are not near-copies of earlier prose. If two blocks would read as the same paragraph with only nouns swapped, block the report and send it back for revision.
- Confirm the visible report contains member-specific language for Warren's moat/owner lens, Charlie's inversion, Mohnish's Dhandho asymmetry, Lu's permanent-capital-loss discipline, Guy's process lens, and Peter's scuttlebutt/category lens.
- Confirm P1 begins with Bruce's base-case valuation and then separately shows `P1 Investment Checklist Vote`, `Bruce P1 Gate`, and every enabled member's `Bruce Method Review Vote` with playbook-linked comments on Bruce's valuation.
- Confirm any P1 accounting-distortion language has a visible Accounting Adjustment Bridge before the Earnings Power table. If Bruce says amortization, tax, minority/NCI, SBC, restructuring, impairment, FX, or one-time items make earnings noisy, block the report unless the bridge quantifies the treatment.
- Confirm the P1 section includes Harvest Mode Decision and Pure-play Margin Decision, including any no-adjustment rationale and confidence impact.
- Confirm the default report does not include standalone `Financial Quality`, standalone `Sensitivity`, or standalone `Bruce EPV` sections.
- Confirm the report contains interactive explainer controls such as tabs, filters, buttons, `<details>`, glossary/tooltips, or equivalent local HTML/CSS/JS controls.
- Confirm the report uses plain-English explanation scaffolding and does not rely on dense tables or chart-only sections.
- Confirm the scorecard includes all seven rows and uses only `PASS` or `FAIL` as vote/result states.
- Confirm the scorecard visibly states the majority rule: more than 3 council member PASS votes means checklist PASS.
- Confirm the visible scorecard and every checklist vote count match the underlying council JSON files, including P1 council vote count and Bruce's P1 gate from `valuation/bruce.json`.
- Confirm current market data, government bond yield, share count, capital structure, and Bruce valuation-critical inputs are fresh for the report date. If any valuation-critical domain is stale, weak, or missing, block the report instead of burying the problem in a footnote.
- Confirm `research/missing_evidence_requests.json` and all owner evidence requests have no high-priority open or unresolved gaps. A final report may discuss lower-priority limitations, but it must not present itself as complete while a high-priority gap is still unresolved.
- Confirm Bruce's EPV calculation is visible: Sustainable Revenue, Revenue Growth Forecast, Segment Revenue Growth Forecast, Year-3 Revenue, Sustainable Operating Margin, Segment Operating Margin Bridge, reported-to-sustainable margin bridge, Earnings Power, Enterprise Value, Earnings Yield, 5 percent hurdle, and pass/fail.
- Confirm every analytical chart/table section has explanatory text.
- Run a visible-text contamination check for CJK ranges such as `[\u4E00-\u9FFF\u3040-\u30FF\uAC00-\uD7AF]`.
- Inspect the HTML at desktop and mobile widths. Confirm text, charts, tables, vote cards, and source notes do not overlap or clip.
- Record the result in `report/report_html_qa.json`. Set `status` to `passed` only after the HTML exists, representative sections were inspected, desktop and mobile views were checked, no clipping/overlap is visible, B3 has two radar visuals, M2 has ROIC/WACC value-spread analysis, council votes are visible, Bruce EPV math is visible, Bruce's three-year revenue forecast and margin bridge are visible, the scorecard uses binary PASS/FAIL verdicts, the CJK check passed, and local interactive chart primitives were verified.
- Set `status` to `passed` only when the interactive controls, plain-English explanations, P1 council valuation review, and overall Council Review are also visible and working.
- Set `status` to `passed` only when council voice and theory differentiation is visible in checklist sections, P1 Bruce valuation reviews, Council Review, and Monitoring.

`report/report_html_qa.json` must include these fields:

```json
{
  "status": "passed",
  "html_path": "report/BMP_TICKER_YYYY-MM-DD_report.html",
  "optional_pdf_path": "report/BMP_TICKER_YYYY-MM-DD_report.pdf",
  "section_count": 30,
  "html_exists": true,
  "html_non_empty": true,
  "representative_sections_inspected": true,
  "desktop_view_checked": true,
  "mobile_view_checked": true,
  "no_clipping_or_overlap": true,
  "b3_two_radars_visible": true,
  "scorecard_binary_verdicts_visible": true,
  "council_votes_visible": true,
  "bruce_council_reviews_visible": true,
  "interactive_explainer_checked": true,
  "plain_english_explanations_visible": true,
  "bruce_epv_calculation_visible": true,
  "bruce_margin_bridge_visible": true,
  "bruce_revenue_forecast_visible": true,
  "explanatory_text_visible": true,
  "cjk_check_passed": true,
  "local_chart_primitives_checked": true,
  "interactive_analytical_charts_checked": true,
  "m2_roic_wacc_history_visible": true,
  "scorecard_consistency_checked": true,
  "p1_council_vote_result_visible": true,
  "current_market_data_freshness_checked": true,
  "member_distinctiveness_checked": true,
  "council_voice_theory_visible": true,
  "representative_sections": [
    {"label": "cover", "selector": "#cover", "inspected": true, "passed": true},
    {"label": "council_votes", "selector": "#b1-council-vote", "inspected": true, "passed": true},
    {"label": "b3", "selector": "#b3-moat", "inspected": true, "passed": true},
    {"label": "p1", "selector": "#p1-bruce", "inspected": true, "passed": true},
    {"label": "council_review", "selector": "#council-overall-review", "inspected": true, "passed": true},
    {"label": "scorecard", "selector": "#final-scorecard", "inspected": true, "passed": true},
    {"label": "references", "selector": "#references", "inspected": true, "passed": true}
  ]
}
```

## Final User Summary

After creating the report, tell the user:

- Overall checklist vote score out of 7, B+M subtotal out of 6, P1 council vote result, and Bruce P1 gate.
- Key findings for Business, Management, and Price.
- Investment verdict.
- HTML file path.
- HTML verification result, including representative section QA, desktop/mobile checks, council vote matrix check, council voice/theory differentiation check, scorecard consistency check against council JSON, P1 council vote result check, current market-data freshness check, M2 ROIC/WACC display check, Bruce P1 calculation display check, Bruce revenue forecast display check, and confirmation that analytical charts are interactive local inline SVG/HTML/CSS primitives rather than raster pictures or Chart.js/CDN-dependent charts.
