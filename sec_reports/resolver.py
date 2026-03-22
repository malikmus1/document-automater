import requests

from .settings import TICKER_URL


def resolve_ticker(ticker:str, session: requests.Session) -> tuple[str,str]:
    """
    Resolve the ticker symboil to (cik_padded_10, official_company_name)
    usinmg SEC:s company_tickers.json mapping.
    """
    resp = session.get(TICKER_URL, timeout=30)
    resp.raise_for_status()

    # Shouldnt be necessary if we add schema validation
    ticker_upper = ticker.upper()
    for entry in resp.json().values():
        if entry["ticker"] == ticker_upper:
            cik = str(entry["cik_str"]).zfill(10)
            return cik, entry["title"]
    
    raise ValueError(f"Ticker {ticker!r} not found in SEC ticker mapping")