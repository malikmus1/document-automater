# SEC 10-K Report Fetcher

Fetches the latest 10-K filings from SEC EDGAR for a list of companies and converts them to PDF.

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python package manager

## Setup

Install dependencies and the Playwright browser:

```bash
uv sync
uv run playwright install chromium
```

## Running

```bash
uv run fetch-reports
```

Reports are saved to `./output/<company>/` with `filing.html`, `filing.pdf`, and `metadata.json`.

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--output <dir>` | `output` | Directory to write reports into |
| `--config <path>` | `sec_reports/companies.yaml` | Path to a custom companies YAML file |

```bash
uv run fetch-reports --output reports --config my_companies.yaml
```

## Companies config

Edit `sec_reports/companies.yaml` to change which companies are fetched:

```yaml
companies:
  - name: Apple
    ticker: AAPL
  - name: Meta
    ticker: META
```
