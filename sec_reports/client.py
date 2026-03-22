import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .settings import USER_AGENT, HTTP_RETRY_TOTAL, HTTP_RETRY_BACKOFF

_RETRY_STRATEGY = Retry(
    total=HTTP_RETRY_TOTAL,
    backoff_factor=HTTP_RETRY_BACKOFF,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
    )
    adapter = HTTPAdapter(max_retries=_RETRY_STRATEGY)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session
