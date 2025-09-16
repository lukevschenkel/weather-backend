import logging
import requests
from requests.adapters import HTTPAdapter, Retry

logger = logging.getLogger(__name__)


class HttpClient:
    def __init__(
        self,
        timeout: int = 10,
        retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> None:
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MyAppHttpClient/1.0",
        })

        # Configure retry strategy
        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
            raise_on_status=False  # let us log before raising
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(self, url: str, **kwargs) -> requests.Response:
        try:
            logger.debug(f"HTTP GET {url} | params={kwargs.get('params')}")
            resp = self.session.get(url, timeout=self.timeout, **kwargs)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            logger.error(
                "HTTP GET failed: %s | Error: %s | Status: %s",
                url,
                e,
                getattr(e.response, "status_code", None)
            )
            raise

    def post(self, url: str, **kwargs) -> requests.Response:
        try:
            logger.debug(f"HTTP POST {url} | params={kwargs.get('params')} | \
                        data={kwargs.get('data')}")
            resp = self.session.post(url, timeout=self.timeout, **kwargs)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            logger.error(
                "HTTP POST failed: %s | Error: %s | Status: %s",
                url,
                e,
                getattr(e.response, "status_code", None)
            )
            raise

    def __enter__(self) -> None:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.session.close()
