import json
import aiohttp
from typing import (
    Any,
    Callable
)

from ..abc   import (
    AsyncAPIClientProtocol,
    AsyncAPIClientResponseProtocol
)

__all__ = (
    "AiohttpClient",
    "AiohttpClientResponse"
)

# TODO: Add docstrings
class AiohttpClient(AsyncAPIClientProtocol):
    _base_url: str
    _headers: dict[str, str]
    _session: aiohttp.ClientSession | None
    _session_kwargs: dict[str, Any]
    
    def __init__(
        self,
        base_url: str,
        *,
        headers: dict[str, str],
        **kwargs: Any
    ) -> None:
        self._base_url = base_url
        self._headers = headers
        self._session: aiohttp.ClientSession | None = None
        self._session_kwargs = kwargs
    
    @property
    def headers(self) -> dict[str, str]:
        """Get the headers."""
        return self._headers
    
    @property
    def closed(self) -> bool:
        """Check if the session is closed."""
        return self._session.closed if self._session is not None else False
    
    @property
    def session(self) -> aiohttp.ClientSession | None:
        """Get the session."""
        return self._session
    
    async def __aenter__(self) -> "AiohttpClient":
        await self.start()
        return self
    
    async def __aexit__(self, *args: Any) -> None:
        await self.close()
    
    async def start(self) -> None:
        """Start the session."""
        if self._session is None:
            self._session = aiohttp.ClientSession(
                self._base_url,
                headers = self._headers,
                **self._session_kwargs
            )
    
    async def get(
        self,
        url: str,
        *,
        allow_redirects: bool = True,
        **kwargs: Any
    ) -> "AiohttpClientResponse":
        """Perform a GET request."""
        if self._session is None:
            raise RuntimeError("Session has not been started yet")
        
        response = await self._session.get(
            url,
            allow_redirects=allow_redirects,
            **kwargs
        )
        return AiohttpClientResponse(response)

    async def close(self) -> None:
        """Close the session."""
        if self._session is None:
            raise RuntimeError("Session has not been started yet")
        await self._session.close()

class AiohttpClientResponse(AsyncAPIClientResponseProtocol):
    _content: str | None
    
    _request_url: str
    _request_method: str
    _request_headers: dict[str, str]
    
    _url: str
    _status: int
    _content_type: str
    _headers: dict[str, str]
    
    def __init__(self, response: aiohttp.ClientResponse):
        self._response = response
        self._content = None
        
        self._request_url = str(response.request_info.url)
        self._request_method = response.request_info.method
        self._request_headers = dict(response.request_info.headers)
        
        self._url = str(response.url)
        self._status = response.status
        self._content_type = response.content_type
        self._headers = dict(response.headers)

    async def text(self) -> str:
        if self._content is None:
            self._content = await self._response.text()
        return self._content

    async def json(
        self,
        *,
        loads: Callable[[str], Any] = json.loads,
        **kwargs: Any
    ) -> Any:
        content = await self.text()
        return loads(content, **kwargs)
    
    def raise_for_status(self) -> None:
        if not self.ok:
            self._response.release()
            super().raise_for_status()
    
    async def __aenter__(self) -> "AiohttpClientResponse":
        return self
    
    async def __aexit__(self, *args: Any) -> None:
        self._response.release()
        await self._response.wait_for_close()
