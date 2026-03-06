import json
import curl_cffi
from typing import Any, Callable
from ..abc import AsyncAPIClientProtocol, AsyncAPIClientResponseProtocol


# TODO: Add docstrings
class CurlCffiClient(AsyncAPIClientProtocol):
    _base_url: str
    _headers: dict[str, str]
    _session: curl_cffi.AsyncSession[curl_cffi.Response] | None
    _session_kwargs: dict[str, Any]

    # I have to use this because curl_cffi doesn't track for me.
    _is_closed: bool

    def __init__(
        self, base_url: str, *, headers: dict[str, str], **kwargs: Any
    ) -> None:
        self._base_url = base_url
        self._headers = headers
        self._session: curl_cffi.AsyncSession[curl_cffi.Response] | None = None
        self._session_kwargs = kwargs
        self._is_closed = True

    @property
    def headers(self) -> dict[str, str]:
        """Get the headers."""
        return self._headers

    @property
    def closed(self) -> bool:
        """Check if the session is closed."""
        return self._is_closed

    @property
    def session(self) -> curl_cffi.AsyncSession[curl_cffi.Response] | None:
        """Get the session."""
        return self._session

    async def __aenter__(self) -> "CurlCffiClient":
        await self.start()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def start(self) -> None:
        """Start the session."""
        self._is_closed = False
        if self._session is None:
            self._session = curl_cffi.AsyncSession(
                base_url=self._base_url, headers=self._headers, **self._session_kwargs
            )
        # Visit the website for cookies
        await self._session.get(
            url=self._base_url,
            allow_redirects=True,
            verify=True,
            impersonate="chrome120",
        )

    async def get(
        self, url: str, *, allow_redirects: bool = True, **kwargs: Any
    ) -> "CurlCffiClientResponse":
        """Perform a GET request."""
        if self._session is None:
            raise RuntimeError("Session has not been started yet")

        self._headers["Referer"] = self.base_url

        response = await self._session.get(
            url=url,
            allow_redirects=allow_redirects,
            verify=True,
            **kwargs,
            impersonate="chrome120",
        )
        return CurlCffiClientResponse(response)

    async def close(self) -> None:
        """Close the session."""
        self._is_closed = True
        if self._session is None:
            raise RuntimeError("Session has not been started yet")
        await self._session.close()


class CurlCffiClientResponse(AsyncAPIClientResponseProtocol):
    _content: str | None

    _request_url: str
    _request_method: str
    _request_headers: dict[str, str | None]

    _url: str
    _status: int
    _content_type: str
    _headers: dict[str, str | None]

    def __init__(self, response: curl_cffi.Response):
        self._response = response
        self._content = None

        if response.request != None:
            self._request_url = str(response.request.url)
            self._request_method = str(response.request.method)
            self._request_headers = dict(response.request.headers)

        self._url = str(response.url)
        self._status = response.status_code
        self._content_type = response.headers.get("Content-Type", "")
        self._headers = dict(response.headers)

    async def text(self) -> str:
        if self._content is None:
            self._content = self._response.text
        return self._content

    async def json(
        self, *, loads: Callable[[str], Any] = json.loads, **kwargs: Any
    ) -> Any:
        content = await self.text()
        return loads(content, **kwargs)

    def raise_for_status(self) -> None:
        if not self.ok:
            self._response.close()
            super().raise_for_status()

    async def __aenter__(self) -> "CurlCffiClientResponse":
        return self

    async def __aexit__(self, *args: Any) -> None:
        self._response.close()
