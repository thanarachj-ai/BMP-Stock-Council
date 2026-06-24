# Canonical Report Template

Use `references/report_template_canonical.html` as the default visual and structural template for BMP Stock Council reports.

The template file is an exemplar, not a content source. Future reports must keep the same format, layout, section order, and table order, but must replace every company-specific fact, number, source, segment, verdict, chart data point, council comment, and valuation input with the target company's evidence-backed content.

## Required Section Order

1. `#cover` - company, ticker, date, currency, current price, dashboard, and plain-English answer.
2. `#how-to-read` - reader guide, vote rule, Bruce's role, member filter, and disclaimer.
3. `#executive-summary` - Business, Management, Price cards plus final vote explanation.
4. `#business-model` - revenue-segment table with amount, customer, how the segment gains customers, and why customers pay; visible revenue segment/mix chart; visible revenue plus operating-margin chart.
5. `#b1-council-vote` - B1 evidence cards, vote summary, and council vote table.
6. `#b2-council-vote` - B2 evidence cards, vote summary, and council vote table.
7. `#b3-moat` - B3 evidence cards, Morningstar radar, 7 Powers radar, vote summary, and council vote table.
8. `#bbonus-council-vote` - disruption evidence cards, vote summary, and council vote table.
9. `#m1-council-vote` - management evidence cards, vote summary, and council vote table.
10. `#m2-council-vote` - value-driver evidence cards, ROIC vs WACC panel, WACC input table, vote summary, and council vote table.
11. `#p1-bruce` - Bruce-first P1 valuation, then P1 council review.
12. `#council-overall-review` - distinct overall view cards for every council member.
13. `#final-scorecard` - all seven checklist rows and Bruce gate.
14. `#monitoring` - distinct monitoring cards plus Bruce's price watchlist.
15. `#references` - clickable source list and method notes.

## Checklist Section Table Order

For B1, B2, B Bonus, M1, and M2:

1. Section kicker and heading.
2. `What it means`, `Evidence`, and `Why it matters` text.
3. Three to four `evidence-card` items before the vote table.
4. `vote-summary` with the exact majority rule: more than 3 PASS votes.
5. `table.vote-table` with member rows and these columns: Member, Vote, Theory anchor, Comment, Playbook link, Confidence, Evidence. Do not expose a separate style-signature column or label; the member's lens must be integrated naturally into the comment cell.

B3 uses the same order, but adds two named `radar-card moat-radar` blocks between the evidence cards and vote summary: one `Morningstar Moat Radar` using Morningstar moat types, and one `7 Powers Moat Radar` using Hamilton Helmer's 7 Powers.

M2 uses the same order, but adds the `m2-roic-wacc` panel, the ROIC vs WACC chart, the ROIC/WACC data table, and the latest WACC input table between the evidence cards and vote summary.

## P1 Bruce Section Order

P1 must follow the canonical order:

1. Bruce plain-English setup.
2. Dashboard cards for Sustainable Revenue, Sustainable Operating Margin, Earnings Power, and Earnings Yield.
3. `Revenue Growth Forecast` bar chart.
4. `Segment Revenue Growth Forecast` table.
5. Consolidated revenue reconciliation.
6. `Sustainable Operating Margin` setup.
7. `Segment Operating Margin Bridge` table.
8. Consolidated margin reconciliation.
9. Accounting Distortion note.
10. `Accounting Adjustment Bridge` table with treatment, tax effect, after-tax adjustment, rationale, and evidence.
11. Maintenance vs Growth, Harvest Mode, and Pure-play decision notes, including mature Year-3 logic and no-adjustment rationale when the adjustment is zero.
12. Historical margin table.
13. Earnings Power and Enterprise Value math table.
14. Margin-of-safety callout.
15. `Input Logic And Sources` table.
16. `P1 Council Review Of Bruce Valuation` table with every enabled member's Bruce Method Review Vote.

The P1 section must keep three ideas visibly separate:

- `P1 Investment Checklist Vote`: the actual P1 checklist majority vote from `council/<member>.json.checklist.P1_price.verdict`.
- `Bruce P1 Gate`: Bruce's earnings-power verdict from `valuation/bruce.json.p1_verdict.display_result`.
- `Bruce Method Review Vote`: each member's `bruce_valuation_review.vote_on_bruce_valuation`, which reviews Bruce's valuation discipline only. It is not the P1 investment checklist vote.

If all members pass Bruce's method review but the P1 investment checklist vote or Bruce P1 Gate is FAIL, the report must say so plainly.

Do not move Bruce's calculation into a later standalone section. Do not add standalone `Financial Quality`, `Sensitivity`, `Latest Results`, or `Bruce EPV` sections unless the user explicitly asks for that variant.

## Layout And Interaction Rules

- Preserve the canonical layout primitives: sticky `.nav`, dashboard metric cards, `.grid.two`, `.grid.three`, `.table-wrap`, `.vote-table`, `.vote-summary`, `.evidence-card`, `.review-card`, `.chart-block`, `.chart-data`, member filters, local inline SVG/CSS charts, and print CSS.
- Keep analytics self-contained. Do not use Chart.js, D3, Plotly, CDNs, Google Fonts, remote scripts, or raster chart images.
- Mobile must keep the same reading order. Tables may scroll inside `.table-wrap`, but the cover, dashboard, narrative text, and vote summaries must not clip horizontally.
- When adapting the canonical template, search the finished HTML for the old ticker, company name, prior-company segment names, prior-company evidence IDs, and prior-company sources before delivery.
