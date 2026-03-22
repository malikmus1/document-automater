from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "companies.yaml"

TICKER_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"

USER_AGENT = "Malik malik.interista@hotmail.com"
HTTP_RETRY_TOTAL = 3
HTTP_RETRY_BACKOFF = 1.5
REQUEST_DELAY = 0.1 # 10 request per sec according to doc

COMPANIES_SCHEMA = {
    "type": "object",
    "required": ["companies"],
    "additionalProperties": False,
    "properties": {
        "companies": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {
                "type": "object",
                "required": ["name", "ticker"],
                "additionalProperties": False,
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "ticker": {"type": "string", "minLength": 1},
                },
            },
        }
    },
}
