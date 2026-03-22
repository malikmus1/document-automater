import json
from pathlib import Path
import time
import click
import jsonschema
from playwright.sync_api import sync_playwright
import yaml
from sec_reports.client import build_session
from sec_reports.converter import render_to_pdf
from sec_reports.filings import get_latest_10k
from sec_reports.resolver import resolve_ticker
from .models import Company
from .settings import CONFIG_PATH, REQUEST_DELAY, COMPANIES_SCHEMA


def _load_companies(config_path: Path = CONFIG_PATH) -> list[Company]:
    try:
        data = yaml.safe_load(config_path.read_text())
    except FileNotFoundError:
        raise SystemExit(f"Config file not found: {config_path}")
    except yaml.YAMLError as exc:
        raise SystemExit(f"Failed to parse config YAML: {exc}")

    try:
        jsonschema.validate(data, COMPANIES_SCHEMA)
    except jsonschema.ValidationError as exc:
        raise SystemExit(f"Invalid config: {exc.message}")

    return [Company(**entry) for entry in data["companies"]]

def _process_company(company: Company, output_dir: Path, session, browser) -> bool:
    print(f"\n-- {company.name} ({company.ticker}) --")

    try:
        cik, official_name = resolve_ticker(company.ticker, session)
        print(f"CIK: {cik}  ({official_name})")
        time.sleep(REQUEST_DELAY)
    except Exception as exc:
        print(f"ERROR resolving ticker: {exc}")
        return False
    
    try:
        filing = get_latest_10k(cik, company, session)
        print(f"Filing: {filing.form}  {filing.filing_date}  ({filing.accession_number})")
        print(f"URL: {filing.document_url}")
        time.sleep(REQUEST_DELAY)
    except Exception as exc:
        print(f"ERROR fetching 10-K: {exc}")
        return False
    
    company_dir = output_dir / company.name.lower().replace(" ", "_")
    company_dir.mkdir(parents=True, exist_ok=True)

    html_path = company_dir / "filing.html"
    try:
        resp = session.get(filing.document_url, timeout=60)
        resp.raise_for_status()
        html_path.write_bytes(resp.content)
        print(f"HTML: {html_path}")
        time.sleep(REQUEST_DELAY)
    except Exception as exc:
        print(f"ERROR downloading HTML: {exc}")
        return False

    pdf_path = company_dir / "filing.pdf"
    try:
        render_to_pdf(html_path, pdf_path, browser)
        print(f"PDF: {pdf_path}")
    except Exception as exc:
        print(f"ERROR rendering PDF: {exc}")
        return False

    metadata = {
        "company": company.name,
        "ticker": company.ticker,
        "cik": cik,
        "form": filing.form,
        "filing_date": filing.filing_date,
        "accession_number": filing.accession_number,
        "sec_filing_url": filing.document_url,
        "local_html": str(html_path),
        "local_pdf": str(pdf_path),
    }
    metadata_path = company_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2))
    print(f"Metadata : {metadata_path}")
    return True
    
    



@click.command()
@click.option("--output", default="output", help="Output directory (default ./output)")
@click.option("--config", default=None, type=click.Path(exists=True, path_type=Path), help="path to companies Yaml config (default: companies.yaml)")
def run(output:str, config: Path | None) -> None:
    output_dir = Path(output)
    session = build_session()
    successes, failures = 0,0

    print("SEC 10-K Report Fetcher")
    print("=" *40)

    with sync_playwright() as playwright:
        browser=playwright.chromium.launch()
        for company in _load_companies(config or CONFIG_PATH):
            ok = _process_company(company, output_dir, session, browser)
            if ok:
                successes += 1
            else:
                failures += 1
        browser.close()

    print(f"\n{'=' * 40}")
    print(f"Done - {successes} succeeeded, {failures} failed.")
    print(f"Reports saved to: {output_dir.resolve()}")
