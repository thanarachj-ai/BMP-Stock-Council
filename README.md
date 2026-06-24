# BMP Stock Council

BMP is a Codex skill for public-stock deep dives using Adam Seessel's Business, Management, Price checklist plus a multi-agent investor council, Bruce-led Earnings Power Value work, Checker validation, Reporter synthesis, and Librarian source curation.

This public version is designed for sharing on GitHub. It uses public filings, company investor-relations pages, regulator/exchange pages, public market-data pages, reputable news, and web search. It does not require paid credentials or private research services.

## Install

Clone this repo into your Codex skills folder as `bmp`:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/thanarachj-ai/BMP-Stock-Council.git ~/.codex/skills/bmp
```

Or download the repo as a ZIP and place the unzipped folder here:

```text
~/.codex/skills/bmp
```

Restart Codex after installing.

## Use

```text
Use $bmp to analyze AAPL.
```

For another market:

```text
Use $bmp to analyze CPALL.BK.
```

## Visual Overview

Open [`docs/team.html`](docs/team.html) for a visual team grid and pipeline flow of the BMP Stock Council workflow.

## What The Workflow Produces

- Structured run folder under `BMP/TICKER_YYYY-MM-DD/`
- Research packet and coverage matrix
- Council member analyses
- Bruce EPV valuation
- Checker audit and revision requests
- Explanation-first HTML report
- Librarian review for durable sources

## Public Source Policy

The workflow is intentionally token-free. It does not depend on paid data-provider accounts or private research-workspace services. For US-listed companies, the bundled EDGAR helper uses public SEC endpoints and filing pages. You may set `SEC_USER_AGENT` to a contact string before running SEC downloads, but it is not a secret.

## Generated Outputs

Generated reports, source libraries, caches, and run artifacts should stay outside the skill repo or remain ignored by Git. The `.gitignore` file excludes typical generated stock-analysis outputs.

## Disclaimer

This skill produces educational analysis, not investment advice. Verify important facts and make independent investment decisions.
