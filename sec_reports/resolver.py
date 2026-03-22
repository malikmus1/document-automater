import requests

from .settings import TICKER_URL


def fetch_ticker_map(session: requests.Session) -> dict:
    """Fetch the full SEC ticker-to-CIK mapping."""
    resp = session.get(TICKER_URL, timeout=30)
    resp.raise_for_status()
    return resp.json()


def resolve_ticker(ticker: str, ticker_map: dict) -> tuple[str, str]:
    """
    Resolve a ticker symbol to (cik_padded_10, official_company_name)
    using a pre-fetched SEC ticker map.
    """
    ticker_upper = ticker.upper()
    for entry in ticker_map.values():
        if entry["ticker"] == ticker_upper:
            cik = str(entry["cik_str"]).zfill(10)
            return cik, entry["title"]

    raise ValueError(f"Ticker {ticker!r} not found in SEC ticker mapping")
