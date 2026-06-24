# BMP Checklist Reference

Use this reference for full stock analysis. The checklist is based on Adam Seessel's Business, Management, Price framework from "Where the Money Is". Use it as a rigorous filter, not as a promotional template.

## Core Principle

Default to NO. A company must earn every YES with evidence. Borderline cases are NO or INSUFFICIENT. Serious red flags are deal breakers, not footnotes.

Rules:

- Challenge every positive conclusion with the strongest bear argument.
- Quantify claims whenever possible.
- Do not confuse growth with a moat.
- Treat missing evidence as a problem.
- For every YES, state the kill condition.
- For every NO, state what would need to improve.

## B: Business Quality

Business quality is the most important factor.

### B1: Large And Growing Market

Question: Does the company operate in a large and growing market?

Required evidence:

- Total addressable market, serviceable market, and practical market where possible.
- Industry growth rate or CAGR.
- Secular growth drivers and constraints.
- Comparison to GDP growth.
- Digital/software or technology-enabled dynamics, if relevant.
- Multiple TAM sources. Search at least 3 sources when available.

TAM methods:

- Top-down industry reports.
- Bottom-up customer count times average revenue.
- Company-disclosed TAM from filings, investor days, or earnings calls.
- Analyst or financial-institution estimates.
- Adjacent-market expansion analysis.

Output:

| Source | TAM value | Year | CAGR | Method | Notes |
| --- | ---: | --- | ---: | --- | --- |

Verdict guidance:

- YES requires a market large enough for long-term compounding and evidence that growth is durable.
- NO if growth is cyclical, saturated, shrinking, purely inflation-driven, or unsupported by evidence.

### B2: Low Market Share

Question: Does the company have low enough market share to compound for many years?

Required evidence:

- Company revenue by relevant market.
- Market share by segment, geography, or product where possible.
- Competitor share table.
- Share gains or losses over time.
- Room-to-grow calculation: company revenue divided by TAM.

Verdict guidance:

- YES if current share is low, market is large, and there is a plausible path to capture share profitably.
- NO if share is already high, growth requires unrelated markets, or marginal share gains require value-destructive spending.

### B3: Sustainable Competitive Advantage

Question: Does the company have a durable moat?

Analyze with both Morningstar's moat types and Hamilton Helmer's 7 Powers.

Morningstar moat types:

- Switching costs.
- Network effects.
- Intangible assets: brand, patents, licenses, regulatory status.
- Cost advantage.
- Efficient scale.

Morningstar rating:

- Wide moat: multiple strong sources, durable for 20 or more years.
- Narrow moat: at least one credible source, durable for 10 or more years.
- No moat: no evidence of excess returns protected from competition.

Helmer 7 Powers:

- Scale economies.
- Network economies.
- Counter-positioning.
- Switching costs.
- Branding.
- Cornered resource.
- Process power.

Rate each power Strong, Moderate, Weak, or Absent with evidence.

Moat summary must include:

- A mapping between Morningstar moat types and 7 Powers.
- Separate Morningstar and 7 Powers scores that can be rendered as two distinct radar/spider visuals in the final HTML report.
- Moat durability estimate: 5 years, 10 years, or 20 or more years.
- Moat erosion risks.
- Evidence from ROIC, retention, pricing power, share stability, or gross margin durability.
- A final B3 verdict that is binary in the report display. Borderline moat evidence is a fail, not a conditional pass.

Verdict guidance:

- YES requires durable excess returns or a clear path to them.
- NO if growth is based mainly on market growth, marketing spend, regulatory subsidy, financial engineering, or a trend without barriers.

### B-Bonus: Disruption Shield

Question: Can the company survive technological, business-model, and regulatory disruption?

Required evidence:

- Whether the business is digital-native, digitally adapting, or analog/legacy.
- Technology threats, platform shifts, regulatory threats, and new entrants.
- Evidence of successful adaptation.
- Value-trap risk: low P/E caused by declining earnings, moat erosion, or stranded assets.

Verdict guidance:

- YES if the company improves with disruption or has credible adaptation evidence.
- NO if the moat was built for an old environment and is deteriorating.

## M: Management Quality

### M1: Owner Mindset

Question: Do managers think and act like owners?

Required evidence:

- Insider ownership and whether it is meaningful relative to personal wealth.
- Compensation alignment and dilution.
- Capital allocation history: reinvestment, M&A, buybacks, dividends, debt use.
- Culture: frugality, long-term orientation, decentralization, customer obsession, or other relevant traits.
- Track record through stress periods.

Verdict guidance:

- YES requires alignment plus good capital allocation behavior.
- NO if management is promotional, overpaid, dilutive, acquisition-addicted, short-term oriented, or misaligned.

### M2: Understanding Value Drivers

Question: Do managers understand what drives business value?

Required evidence:

- ROIC trend and drivers.
- ROIC vs WACC for the latest year and each of the previous 10 years when public data exists.
- Evidence that management discusses the right unit economics and competitive drivers.
- Shareholder letters, earnings calls, investor days, and strategic choices.
- Mistake handling and capital allocation correction.

ROIC:

- ROIC = NOPAT / invested capital.
- Good: above 15 percent.
- Average: around 10 percent.
- Poor: below 8 percent.

WACC must be calculated from inputs:

- Risk-free rate from the company's primary market 10-year government bond.
- Equity risk premium from Damodaran or a credible country-specific source.
- Beta from regression or an industry beta that is re-levered.
- Cost of equity = risk-free rate + beta times ERP.
- Cost of debt from interest expense divided by debt, or actual debt yield when available.
- Effective tax rate.
- Market value equity and interest-bearing debt weights.

Output:

Show the latest WACC input table and a ten-year value-spread table. Label the result `Damodaran-style WACC` unless the source is Damodaran's own company-specific WACC. Do not call a generic industry WACC a company WACC without showing the company weights and assumptions.

| Input | Value | Source | URL |
| --- | ---: | --- | --- |
| Risk-free rate |  |  |  |
| Equity risk premium |  |  |  |
| Beta |  |  |  |
| Cost of equity |  |  |  |
| Cost of debt |  |  |  |
| Tax rate |  |  |  |
| Equity weight |  |  |  |
| Debt weight |  |  |  |
| WACC |  |  |  |

| Fiscal year | ROIC | WACC | ROIC minus WACC | Value creation verdict | Main driver |
| --- | ---: | ---: | ---: | --- | --- |
| YYYY |  |  |  |  |  |

Verdict guidance:

- YES if management creates value, understands the drivers, and allocates capital rationally.
- NO if ROIC is below WACC without a credible path, management focuses on vanity metrics, or strategy destroys value.

## P: Price

Price is the veto question. A great business at the wrong price is still a bad investment.

### P1: Earnings Yield At Least 5 Percent

Question: Can we buy the company at a reasonable earnings yield, normally at least 5 percent on earnings power?

Step 1: Determine earnings power.

- Start with current revenue.
- Project revenue 3 years forward using a conservative growth rate.
- Apply a justified mature operating margin.
- Calculate earnings power and EPS.
- Use current Enterprise Value as the primary P1 denominator, with market cap as an equity cross-check.

Step 2: Justify mature margin.

Use four evidence layers:

1. Empirical evidence:
   - Company gross, operating, and net margin history for 5 to 10 years.
   - Peak margin and conditions behind the peak.
   - Trailing 3-year average.
   - Mature peer margin comparison using at least 3 to 5 peers where available.
   - Management long-term margin guidance, if any.

2. Structural analysis:
   - Industry margin range.
   - Cost structure: COGS, R&D, SG&A, D&A as percent of revenue.
   - Maintenance vs growth spending.
   - Segment-level target margins for multi-segment companies.

3. Scenario analysis:

| Scenario | Margin | Reason | Earnings power | Earnings yield | Pass 5 percent? |
| --- | ---: | --- | ---: | ---: | --- |
| Bull |  |  |  |  |  |
| Base |  |  |  |  |  |
| Bear |  |  |  |  |  |

4. Final margin reasoning:
   - Explain why the base margin was chosen.
   - State the main risk to that margin.
   - Show how a different margin changes earnings yield.

Step 3: Current bond yield context.

Search for the current 10-year government bond yield for the primary listing country at analysis time. Present:

| Metric | Value | Source | Date retrieved |
| --- | ---: | --- | --- |
| Risk-free rate |  |  |  |
| Required earnings yield | 5.00 percent | BMP framework |  |
| Spread above risk-free rate |  | Calculated |  |
| Company earnings yield |  | Calculated |  |
| Pass or fail |  |  |  |

Step 4: Margin of safety.

- Downside valuation if growth stops.
- Balance sheet protection or risk.
- Bear-case earnings power.
- What market expectations are embedded in current price.

Verdict guidance:

- PASS if evidence-supported earnings yield is at least 5 percent and has adequate margin of safety.
- FAIL if earnings yield is below 5 percent, depends on heroic margin expansion, or the bear case has poor downside protection.

## BMP Score

The full BMP checklist has seven explicit questions:

- B1 large growing market.
- B2 low market share.
- B3 moat.
- B-Bonus disruption shield.
- M1 owner mindset.
- M2 value-driver understanding.
- P1 Earnings Yield at least 5 percent.

Report both scores:

- Full BMP score: count `PASS`/`YES` out of 7, including P1.
- B+M quality subtotal: count `PASS`/`YES` out of 6, excluding P1.

Final report display rules:

- Display checklist verdicts only as `PASS` or `FAIL` in English reports, or `ผ่าน` / `ไม่ผ่าน` in Thai reports.
- Internal council verdicts may be `YES`, `NO`, or `INSUFFICIENT`, but `NO` and `INSUFFICIENT` both display as fail.
- Bruce may use internal Price verdicts such as `WATCHLIST` or `INSUFFICIENT`, but any no-buy or uncertain Price verdict displays as fail.
- The final scorecard must include a separate row labeled `P1 Earnings Yield ได้อย่างน้อย 5% หรือไม่` or the English equivalent if the user explicitly requested an English report.
- Do not replace P1 with a generic `Price` row.
- Do not display conditional states such as partial, watchlist, insufficient, borderline, or conditional pass in the final scorecard.

Interpret the B+M subtotal before applying the Price veto:

Interpretation:

- 5 to 6 YES: strong candidate, proceed to Price with discipline.
- 3 to 4 YES: watchlist or special situation, Price and improvement path matter.
- 0 to 2 YES: reject for long-term compounding unless there is an exceptional special-situation reason.

Price is a veto. If P1 fails, the investment does not pass even if B and M are strong, but P1 still counts as its own row in the full score out of 7.

## Understanding Verification

Before final verdict, answer:

- Two-minute drill: explain the business, moat, and risks simply.
- Short argument: strongest bear case and best counterargument.
- Key variable: the single metric or condition most likely to determine success or failure.
