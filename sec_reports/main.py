from pathlib import Path
import click
from playwright.sync_api import sync_playwright
import yaml
from sec_reports.client import build_session
from sec_reports.resolver import resolve_ticker
from .models import Company

_CONFIG_PATH = Path(__file__).parent / "companies.yaml"

def _load_companies(config_path: Path = _CONFIG_PATH) -> list[Company]:
    # TODO: Add try + schema validator 
    data = yaml.safe_load(config_path.read_text())
    return [Company(**entry) for entry in data ["companies"]]

def _process_company(company: Company, output_dir: Path, session, browser) -> bool:
    print(f"\n-- {company.name} ({company.ticker}) --")

    try:
        cik, official_name = resolve_ticker(company.ticker, session)
        print(f"CIK: {cik}  ({official_name})")
    except Exception as exc:
        print(f"   ERROR resolving ticker: {exc}")
        return False
    
    



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
        for company in _load_companies(config or _CONFIG_PATH):
            ok = _process_company(company, output_dir, session, browser)
            if ok:
                successes += 1
            else:
                failures += 1
        browser.close()

    print(f"\n{'=' * 40}")
    print(f"Done - {successes} succeeeded, {failures} failed.")
    print(f"Reports saved to: {output_dir.resolve()}")
