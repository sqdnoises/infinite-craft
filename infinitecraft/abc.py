import json
from typing import (
    Any, Callable,
    Protocol, runtime_checkable
)

from .types          import *
from .utils          import reify
from .errors.clients  import ClientResponseError

__all__ = (
    "ElementProtocol",
    "AsyncAPIClientProtocol",
    "AsyncAPIClientResponseProtocol",
    "LoggerProtocol"
)

@runtime_checkable
class ElementProtocol(Protocol):
    """
    Protocol that defines the interface for an element in the Infinite Craft system.

    Attributes:
        name (str | None): The name of the element.
        emoji (str | None): The emoji representing the element.
        is_first_discovery (bool | None): Indicates if the element was the first discovery.
    """
    
    name: str | None
    emoji: str | None
    is_first_discovery: bool | None
    
    def __init__(
        self,
        name:               str  | None = None,
        emoji:              str  | None = None,
        is_first_discovery: bool | None = None
    ) -> None:
        self.name = name
        self.emoji = emoji
        self.is_first_discovery = is_first_discovery
    
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: Any) -> bool: ...
    def __bool__(self) -> bool: ...

# TODO: Complete sync APIClientProtocol
# @runtime_checkable
# class APIClientProtocol(Protocol):
#     """Protocol for API client classes."""
#     ...

@runtime_checkable
class AsyncAPIClientProtocol(Protocol):
    """
    Protocol for asynchronous API client classes.

    Attributes:
        base_url (str): The base URL for the API client.
        closed (bool): Whether the client session is closed.

    Methods:
        start: Starts the session.
        get: Performs a GET request to a specified URL.
        close: Closes the client session.

    Example:
        >>> client = AsyncAPIClientProtocol(base_url="https://api.example.com")
        >>> await client.start()
        >>> response = await client.get("/data")
        >>> await client.close()
    """
    
    _base_url: str
    
    def __init__(self, base_url: str, *args: Any, **kwargs: Any) -> None: ...
    async def __aenter__(self) -> "AsyncAPIClientProtocol": ...
    async def __aexit__(self, *args: Any) -> None: ...
    
    @property
    def base_url(self) -> str:
        """The base URL for the client."""
        return self._base_url
    
    @property
    def closed(self) -> bool:
        """Check if the session is closed."""
        ...
    
    async def start(self) -> None:
        """Start the session."""
        ...
    
    async def get(self, url: str, *args: Any, **kwargs: Any) -> "AsyncAPIClientResponseProtocol":
        """Perform a GET request to the given URL."""
        ...
    
    async def close(self, *args: Any, **kwargs: Any) -> Any:
        """Close the session."""
        ...

@runtime_checkable
class AsyncAPIClientResponseProtocol(Protocol):
    """
    Protocol for asynchronous API client response classes.

    Attributes:
        request_url (str): The URL used for the request.
        request_method (str): The HTTP method used for the request.
        request_headers (dict[str, str]): The headers used in the request.
        url (str): The URL of the response.
        status (int): The status code of the response.
        content_type (str): The content type of the response.
        headers (dict[str, str]): The headers in the response.
        ok (bool): Returns `True` if the status is less than 400, otherwise `False`.

    Methods:
        text: Returns the response content as a string.
        json: Parses the response content as JSON.
        raise_for_status: Raises an exception if the response status is 400 or higher.

    Example:
        >>> response = await client.get("/data")
        >>> await response.json()
    """
    
    _content: str | None
    
    _request_url: str
    _request_method: str
    _request_headers: dict[str, str]
    
    _url: str
    _status: int
    _content_type: str
    _headers: dict[str, str]
    
    @reify
    def request_url(self) -> str:
        """
        str: The URL used to make the request.

        This property retrieves the request URL from the underlying request data.
        It allows clients to access the exact URL that was called for the response.
        """
        return self._request_url
    
    @reify
    def request_method(self) -> str:
        """
        str: The HTTP method used for the request.

        This property returns the HTTP method (e.g., GET, POST) that was employed
        when making the request. It provides insight into how the request was executed.
        """
        return self._request_method
    
    @reify
    def request_headers(self) -> dict[str, str]:
        """
        dict[str, str]: The headers sent with the request.

        This property returns a dictionary of headers that were included
        in the request. It can be useful for debugging or logging purposes.
        """
        return self._request_headers
    
    @reify
    def url(self) -> str:
        """
        str: The URL of the response.

        This property retrieves the URL of the response, which may be different
        from the request URL if redirects occurred. It provides clients with
        the final URL from which the response was obtained.
        """
        return self._url
    
    @reify
    def status(self) -> int:
        """
        int: The status code of the response.

        This property returns the HTTP status code received in the response.
        Common status codes include 200 for success and 404 for not found.
        """
        return self._status
    
    @reify
    def ok(self) -> bool:
        """
        bool: `True` if the status code is less than 400, otherwise `False`.

        This property checks if the response was successful based on its status code.
        It can be used to quickly determine if the request was processed successfully.
        """
        return self._status < 400
    
    @reify
    def content_type(self) -> str:
        """
        str: The content type of the response.

        This property returns the content type header from the response,
        which indicates the media type of the resource returned (e.g., application/json).
        """
        return self._content_type
    
    @reify
    def headers(self) -> dict[str, str]:
        """
        dict[str, str]: The headers in the response.

        This property returns a dictionary of headers that were included
        in the response. It can be useful for accessing metadata about the response.
        """
        return self._headers
    
    async def text(self) -> str:
        """Returns the response content as a string."""
        ...
    
    async def json(
        self,
        *,
        loads: Callable[[str], Any] = json.loads,
        **kwargs: Any
    ) -> Any:
        """Parses the response content as JSON."""
        ...
    
    def raise_for_status(self) -> None:
        """
        Raises an exception if the response status is 400 or higher.

        Raises:
            ClientResponseError: If the response status is >= 400.
        """
        if not self.ok:
            raise ClientResponseError(f"Request failed with status code {self.status}")
    
    async def __aenter__(self) -> "AsyncAPIClientResponseProtocol": ...
    async def __aexit__(self, *args: Any) -> None: ...

@runtime_checkable
class LoggerProtocol(Protocol):
    """
    Protocol for logger classes.

    Attributes:
        log_level (int): The current logging level.

    Methods:
        debug: Logs a debug message.
        info: Logs an informational message.
        warn: Logs a warning message.
        error: Logs an error message.
        critical: Logs a critical message.

    Example:
        >>> logger = LoggerProtocol(log_level=10)
        >>> logger.debug("This is a debug message.")
    """
    log_level: int
    
    def debug(self, message: str | Any) -> None:
        """Log a debug message."""
        ...
    
    def info(self, message: str | Any) -> None:
        """Log an info message."""
        ...
    
    def warn(self, message: str | Any) -> None:
        """Log a warning message."""
        ...
    
    def error(self, message: str | Any) -> None:
        """Log an error message."""
        ...
    
    def critical(self, message: str | Any) -> None:
        """Log a critical message."""
        ...