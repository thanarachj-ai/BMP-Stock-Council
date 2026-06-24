# Bruce Quantitative Research Pack

Use this reference when the Researcher gathers quantitative evidence for Bruce's BMP P1 work.

## Purpose

The Researcher owns the evidence. Bruce owns the P1 judgment.

Before Bruce starts, the Researcher must create:

- `research/bruce_quant_inputs.json`
- `research/bruce_quant_inputs.md`

The pack should let Bruce calculate a three-year sustainable revenue forecast, sustainable operating margin, Year-3 earnings power, current-EV earnings yield, the 5 percent test, and margin of safety without searching for basic inputs.

## Public Evidence Standards

Use public sources only:

- Primary filings and annual reports
- Company investor relations materials
- Public regulator and exchange pages
- Public XBRL/companyfacts data where available
- Public market-data pages
- Central-bank, treasury, or bond-market pages
- Reputable public news and transcript sources

Every material number must include:

- Metric name
- Value
- Period or as-of date
- Currency and unit
- Evidence ID from `research/research_packet.json`
- Source type
- Source URL
- Derivation note for calculated, normalized, estimated, rounded, or selected values
- Freshness status: `current`, `stale`, `not_applicable`, or `missing`
- Researcher note for restatements, conflicts, non-comparability, or estimates

If a number cannot be sourced publicly, leave it blank or null, add it to `evidence_gaps`, and explain how the gap affects P1.

## Minimum Sections

### Market Data

Collect:

- Share price, quote date/time, exchange, currency, and source.
- Market cap.
- Enterprise Value.
- Basic shares, diluted shares, weighted average diluted shares, and ADS/ADR ratio when relevant.
- Debt, leases, preferred stock, minority interest, cash, and excess cash.
- Current 10-year government bond yield for the listing country or valuation currency, with source URL and retrieval date.

### Capital Structure

Collect:

- Cash and equivalents, short-term investments, and restricted cash when material.
- Short-term debt, long-term debt, lease liabilities, preferred stock, minority interest, pensions, and other debt-like claims.
- Interest expense, maturities, covenants, credit rating, buybacks, dividends, option dilution, SBC, warrants, and convertibles when relevant.

### Financial History

Use ten years when available. If fewer years are comparable, state the exact years and reason.

Collect:

- Revenue, gross profit, operating income, EBIT, depreciation and amortization, pretax income, tax expense, net income, EPS.
- Operating cash flow, capex, free cash flow, acquisitions, divestitures, working capital, dividends, and buybacks.
- Segment revenue, segment profit, geography, product mix, and key operating KPIs.
- Quarterly history for recent trend breaks.
- Organic growth, acquisition growth, FX, pricing, volume, same-store sales, same-customer growth, seat/user growth, churn, ARPU, or other footprint-adjusted growth drivers when relevant.

### Three-Year Revenue Forecast Inputs

Collect evidence Bruce needs to forecast Year-1, Year-2, and Year-3 sustainable revenue:

- TTM or latest fiscal-year revenue baseline.
- Five- to ten-year revenue CAGR and trailing three-year growth.
- Organic growth rate and non-organic growth bridge.
- Segment revenue history, segment growth, and segment-level drivers.
- Segment-by-segment Year-1, Year-2, and Year-3 growth-rate evidence.
- Segment maturity: mature harvest-mode segments versus high-growth platforms.
- TAM, serviceable market, penetration, current market share, and evidence for the share estimate.
- Evidence that technology and customer behavior are stable enough to forecast three years.
- Secular tailwind evidence.
- Platform leverage and ancillary revenue per user/customer when relevant.
- Conservative deceleration logic.
- Explicit cap check for segment growth rates above 15 percent.

### Normalization Inputs

Identify:

- Sustainable revenue base and why it is sustainable.
- Year-3 sustainable revenue and why the three-year forecast is sustainable.
- Sustainable operating margin and why it is sustainable.
- Five- to ten-year company margin history.
- Reported-to-sustainable operating-margin bridge.
- Accounting distortions that may depress or inflate reported operating income.
- Maintenance-versus-growth spending split for R&D, SG&A, and marketing, with public evidence used to estimate each side.
- Harvest-economics decision evidence, even when no add-back is appropriate.
- Pure-play peer margin table and comparability notes from public sources.
- Management margin guidance, if credible and publicly sourced.
- Segment-level margin evidence.
- Money-losing experimental or auxiliary segments that may hide core franchise profitability.
- Cyclical peak/trough and recession evidence.
- Sustainable tax rate.
- Maintenance capex method and evidence.
- Working-capital normalization.
- One-time items, impairments, restructuring, litigation, acquisition accounting, disposal gains/losses, FX, and accounting changes.
- SBC and dilution treatment.

### Earnings Power Inputs

Provide a clear bridge:

```text
Year-3 Sustainable Revenue
x Sustainable Operating Margin
= Sustainable Operating Profit
x (1 - Sustainable Tax Rate)
= Normalized After-Tax Operating Earnings
+/- Accounting Adjustment Bridge
+/- Maintenance Reinvestment Adjustment
= Earnings Power
```

Each line needs evidence IDs or a derivation note.

### Optional Cross-Checks

Only collect these when relevant and sourced:

- Market-cap earnings yield as an optional equity cross-check.
- Asset reproduction value, liquidation value, or NAV clues.
- ROIC, WACC, and value-driver ratios for M2 context.
- Bull/base/bear sensitivity ranges for revenue, margin, tax, maintenance capex, and share count.

These cross-checks must not replace the core P1 test.

## JSON Shape

```json
{
  "ticker": "",
  "company": "",
  "analysis_date": "",
  "status": "not_built",
  "status_values": ["not_built", "partial", "ready", "blocked"],
  "source_priority": ["primary filings", "company IR", "public market data", "government yield source"],
  "market_data": {},
  "capital_structure": {},
  "financial_history": {
    "annual": [],
    "ten_year_summary": [],
    "quarterly": [],
    "segments": [],
    "kpis": []
  },
  "three_year_revenue_forecast": {
    "baseline_revenue": "",
    "baseline_period": "",
    "segment_forecasts": [],
    "year_1_revenue": "",
    "year_2_revenue": "",
    "year_3_revenue": "",
    "why_sustainable": "",
    "evidence_ids": []
  },
  "normalization_inputs": {
    "normalized_revenue_base": "",
    "reported_operating_margin": "",
    "normalized_operating_margin": "",
    "why_margin_is_sustainable": "",
    "accounting_adjustment_bridge": [],
    "maintenance_vs_growth_spending": [],
    "harvest_mode_decision": {},
    "pure_play_margin_decision": {},
    "segment_margin_bridge": [],
    "sustainable_tax_rate": "",
    "maintenance_reinvestment": "",
    "evidence_ids": []
  },
  "earnings_power": {
    "year_3_revenue": "",
    "sustainable_operating_margin": "",
    "sustainable_operating_profit": "",
    "tax_rate": "",
    "earnings_power": "",
    "enterprise_value": "",
    "earnings_yield": "",
    "five_percent_test": "",
    "margin_of_safety": ""
  },
  "evidence_gaps": []
}
```
