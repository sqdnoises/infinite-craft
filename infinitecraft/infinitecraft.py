"""
An API Wrapper for Neal's Infinite Craft game in Python.
Copyright (C) 2024-present SqdNoises, Neal Agarwal
License: MIT License
To view the full license, visit https://github.com/sqdnoises/infinite-craft#license

Need help with something?
Join our Discord server -> https://discord.gg/EPr4T2F8bq

Play Infinite Craft by Neal Agarwal on your browser -> https://neal.fun/infinite-craft/
"""

import os
import copy
import json
import time
import asyncio
from typing import (
    Any, Callable,
    MutableMapping
)

from .          import utils
from .logger    import Logger
from .element   import Element
from .clients   import AiohttpClient
from .abc       import (
    LoggerProtocol,
    ElementProtocol,
    AsyncAPIClientProtocol
)
from .constants import starting_discoveries
from .types     import (
    ResultDict,
    Discovery
)

__all__ = (
    "InfiniteCraft",
)

class InfiniteCraft:
    """
    An API Wrapper for Neal's Infinite Craft game in Python.

    This class provides an interface to interact with the Infinite Craft game,
    allowing users to discover new elements, manage game sessions, and handle
    API interactions.

    Attributes:
        discoveries (list[Element]): List of Element objects that have been discovered.
        closed (bool | None): Whether the Infinite Craft session is closed or not.
                              None if the session has not been started.
        api_url (str): The API URL being used for requests.
        api_rate_limit (int): The current rate limit for API requests.
        manual_control (bool): Whether manual session control is enabled.
        discoveries_location (str): Path to the discoveries storage JSON file.
        encoding (str): The encoding used for file operations.
        headers (dict[str, str]): Headers used for API requests.
        element_cls (type[ElementProtocol]): The class used for creating elements.
        session_cls (type[AsyncAPIClientProtocol]): The class used for API client sessions.
        session (AsyncAPIClientProtocol | None): The current API client session, if active.

    Args:
        api_url (str, optional): The API URL to contact. 
            Default: "https://neal.fun/api/infinite-craft"
        api_rate_limit (int, optional): Requests per minute before rate limiting. 
            Set to 0 for no limit. Default: 400. Must be >= 0.
        manual_control (bool, optional): Manually control session start/stop. 
            Useful for multiple `async with` usage. Default: False
        discoveries_storage (str, optional): Path to discoveries storage JSON. 
            Default: "discoveries.json"
        encoding (str, optional): Encoding for reading/saving JSON files. 
            Default: "utf-8"
        do_reset (bool, optional): Reset discoveries storage and emoji cache. 
            Default: False
        make_file (bool, optional): Create storage file if it doesn't exist. 
            Default: True
        headers (MutableMapping[str, str], optional): Custom headers for API requests. 
            Default: {}
        logger (LoggerProtocol, optional): Custom logger for the class. 
            Default: Logger()
        element_cls (type[ElementProtocol], optional): Class for creating elements. 
            Must subclass Element. Default: Element
        session_cls (type[AsyncAPIClientProtocol], optional): Class for API client session. 
            Default: AiohttpClient
        debug (bool, optional): Enable debug logging. 
            Sets logger to Logger(log_level=5). Default: False

    Raises:
        ValueError: If api_rate_limit is negative.
        FileNotFoundError: If discoveries_storage file doesn't exist and make_file is False.
        TypeError: If element_cls is not a subclass of ElementProtocol.

    Example:
        >>> import asyncio
        >>> import infinitecraft
        >>> 
        >>> async def main():
        ...     game = InfiniteCraft()
        ...     await game.start()
        ...     result = await game.pair(Element("Water"), Element("Fire"))
        ...     print(result)
        ...     await game.close()
        >>> 
        >>> asyncio.run(main())

    Note:
        For assistance, join our Discord server: https://discord.gg/EPr4T2F8bq
    """
    
    _api_url: str
    _api_rate_limit : int
    _manual_control: bool
    _discoveries_location: str
    _encoding: str
    _logger: LoggerProtocol
    _element_cls: type[ElementProtocol]
    _requests: list[float]
    _session_cls: type[AsyncAPIClientProtocol]
    _requests: list[float]
    _discoveries: list[ElementProtocol]
    discoveries: list[ElementProtocol]
    _session: AsyncAPIClientProtocol | None
    _headers: MutableMapping[str, str]
    
    def __init__(
        self, *,
        api_url: str                              = "https://neal.fun", # API to contact
        api_rate_limit: int                       = 400,                # 400 requests per minute
        manual_control: bool                      = False,
        discoveries_storage: str                  = "discoveries.json", # where to store the game data
        encoding: str                             = "utf-8",
        do_reset: bool                            = False,
        make_file: bool                           = True,
        headers: MutableMapping[str, str]         = {},
        logger: LoggerProtocol                    = Logger(),
        element_cls: type[ElementProtocol]        = Element,
        session_cls: type[AsyncAPIClientProtocol] = AiohttpClient,
        debug: bool                               = False
    ) -> None:
        if not api_rate_limit >= 0:
            raise ValueError("api_rate_limit must be greater than or equal to 0")
        
        dsreset = False
                
        if not utils.check_file(discoveries_storage):
            if not make_file:
                raise FileNotFoundError(f"File '{discoveries_storage}' not found")
            
            logger.warn(f"Resetting discoveries storage JSON file ({discoveries_storage})")
            self.reset(
                discoveries_storage=discoveries_storage,
                encoding=encoding,
                make_file=make_file
            )
            dsreset = True
        
        self._api_url = api_url
        self._api_rate_limit = api_rate_limit
        self._manual_control = manual_control
        self._discoveries_location = discoveries_storage
        self._encoding = encoding
        
        self._logger = logger
        if debug and isinstance(logger, LoggerProtocol): # pyright: ignore[reportUnnecessaryIsInstance]
            self._logger.log_level = 5
        self._element_cls = element_cls
        self._session_cls = session_cls
        
        self._requests = []
        
        if do_reset and not dsreset:
            self._logger.warn(f"Resetting discoveries JSON file ({discoveries_storage})")
            self.reset(
                discoveries_storage=discoveries_storage,
                encoding=encoding
            )

        self._discoveries = []
        self.discoveries = copy.deepcopy(self._discoveries)
        self.get_discoveries(set_value=True)

        self._session = None
        self._headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "priority": "u=1, i",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "Referer": "https://neal.fun/infinite-craft/",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        }
        self._headers.update(headers)

        self._logger.debug("InfiniteCraft has been initialised.")
        self._logger.debug("Need help? Join the community server -> https://discord.gg/EPr4T2F8bq")

    @property
    def api_url(self) -> str:
        """
        The base URL for the Infinite Craft API.

        Returns:
            str: The API URL being used for requests.
        """
        return self._api_url

    @property
    def api_rate_limit(self) -> int:
        """
        The rate limit for API requests.

        Returns:
            int: The maximum number of requests allowed per minute.
        """
        return self._api_rate_limit
    
    @property
    def manual_control(self) -> bool:
        """
        Whether manual session control is enabled.

        Returns:
            bool: True if manual control is enabled, False otherwise.
        """
        return self._manual_control
    
    @property
    def discoveries_location(self) -> str:
        """
        The file path for storing discoveries.

        Returns:
            str: The path to the discoveries storage JSON file.
        """
        return self._discoveries_location
    
    @property
    def encoding(self) -> str:
        """
        The encoding used for file operations.

        Returns:
            str: The encoding (e.g., 'utf-8') used for reading and writing files.
        """
        return self._encoding

    @property
    def headers(self) -> MutableMapping[str, str]:
        """
        The headers used for API requests.

        Returns:
            dict[str, str]: A dictionary of headers sent with each API request.
        """
        return self._headers
    
    @property
    def element_cls(self) -> type[ElementProtocol]:
        """
        The class used for creating elements.

        Returns:
            type[ElementProtocol]: The class (subclass of ElementProtocol) used to instantiate new elements.
        """
        return self._element_cls
    
    @property
    def session_cls(self) -> type[AsyncAPIClientProtocol]:
        """
        The class used for API client sessions.

        Returns:
            type[AsyncAPIClientProtocol]: The class used to create API client sessions.
        """
        return self._session_cls
    
    @property
    def session(self) -> AsyncAPIClientProtocol | None:
        """
        The current API client session.

        Returns:
            AsyncAPIClientProtocol | None: The active API client session, or None if no session is active.
        """
        return self._session
    
    @property
    def closed(self) -> bool | None:
        """
        The closed status of the current session.

        Returns:
            bool | None: True if the session is closed, False if it's open, or None if no session has been started.
        """
        return self._session.closed if self._session is not None else None
    
    def __str__(self) -> str:
        """
        Returns a string representation of the InfiniteCraft instance.

        Returns:
            str: A string containing the number of discoveries and the closed status of the session.
        """
        discoveries = len(self._discoveries)
        return f"<InfiniteCraft discoveries={discoveries} closed={self.closed}>"

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the InfiniteCraft instance.

        Returns:
            str: A string containing all the initialization parameters of the instance.
        """
        return (
            f"InfiniteCraft("
            f"api_url={repr(self.api_url)}, "
            f"api_rate_limit={repr(self.api_rate_limit)}, "
            f"manual_control={repr(self.manual_control)}, "
            f"discoveries_storage={repr(self.discoveries_location)}, "
            f"encoding={repr(self.encoding)}, "
            f"headers={repr(self._headers)}, "
            f"element_cls={repr(self._element_cls)}, "
            f"session_cls={repr(self._session_cls)}, "
            f"logger={repr(self._logger)}, "
            f"debug={repr(self._logger.log_level == 5)}"
            f")"
        )
    
    async def __aenter__(self) -> "InfiniteCraft":
        if not self.manual_control:
            self._logger.debug("Starting session automatically because manual control is OFF")
            await self.start()
        else:
            self._logger.debug("Not starting session automatically because manual control is ON")
        
        return self

    async def __aexit__(self, *args: Any) -> None:
        if not self.manual_control:
            self._logger.debug("Stopping session automatically because manual control is OFF")
            await self.close()
        else:
            self._logger.debug("Not stopping session automatically because manual control is ON")
    
    async def _build_session(self) -> None:
        """
        Build the API client session.

        This internal method initializes the API client session using the specified
        session class. It sets up the base URL and headers for API requests.

        Note:
            This method is intended for internal use only.
        """
        self._session = self._session_cls(
            base_url = self.api_url,
            headers = self._headers
        )
        await self._session.start()

    async def start(self) -> None:
        """
        Start the InfiniteCraft session.

        This method initializes the session if it hasn't been started yet. It uses the
        session class specified during initialization to create a new session.

        Raises:
            RuntimeError: If the session is already running or has been closed.
        """
        if self._session is None:
            await self._build_session()
            self._logger.debug("Started session")
        elif self._session and self._session.closed:
            raise RuntimeError("Session is closed")
        else:
            raise RuntimeError("Session is already running")

    async def close(self) -> None:
        """
        Close the InfiniteCraft session.

        This method closes the current session if it's active. It ensures that all
        resources associated with the session are properly released.

        Raises:
            RuntimeError: If the session has not been started or is already closed.
        """
        if self._session is None:
            raise RuntimeError("Session has not been started yet")
        elif self._session and self._session.closed:
            raise RuntimeError("Session is already closed")
        else:
            await self._session.close()
            self._logger.debug("Closed session")

    async def stop(self) -> None:
        """
        Close the Infinite Craft session.

        Alias for `InfiniteCraft.close()`.

        This method closes the current session if it's active. It ensures that all
        resources associated with the session are properly released.

        Raises:
            RuntimeError: If the session has not been started or is already closed.
        """
        await self.close()
    
    async def ping(self) -> float:
        """
        Ping the API and return the latency.

        This method sends a request to the API using a predefined pair of elements
        (Fire and Water) to measure the response time. It's useful for checking the
        API's responsiveness and the connection quality.

        Returns:
            float: The latency in seconds.

        Raises:
            RuntimeError: If the session has not been started yet.
        """
        if self._session is None:
            raise RuntimeError("Session has not been started yet")
        
        self._logger.debug(f"Pinging API route: {self.api_url}/api/infinite-craft/pair with Fire + Water")
        
        params = {
            "first":  "Fire",
            "second": "Water"
        }
        
        request = await self._wait_for_request() # wait for ratelimit requests to finish
        
        start = time.monotonic()
        async with await self._session.get(f"/api/infinite-craft/pair", params=params) as response:
            self._done_with_request(request) # mark request as done
            end = time.monotonic() - start
            self._logger.debug(f"API response time: {end}s")
            response.raise_for_status()
        
        return end

    async def pair(self, first: ElementProtocol, second: ElementProtocol, *, store: bool = True) -> ElementProtocol:
        """
        Pair two elements and return the resulting element.

        This method sends a request to the API to combine two elements and returns
        the result. If the combination is not possible, it returns an Element with
        all attributes set to None.

        Args:
            first (ElementProtocol): The first element to pair.
            second (ElementProtocol): The second element to pair.
            store (bool, optional): Whether to store the result in discoveries. Defaults to True.

        Returns:
            ElementProtocol: The resulting element from the pairing, or an ElementProtocol
                              with all attributes as None if they couldn't be paired.

        Raises:
            RuntimeError: If the session has not been started yet.
        """
        if self._session is None:
            raise RuntimeError("Session has not been started yet")
        
        self._logger.debug(f"Pairing {first} and {second}...")
        
        params = {
            "first":  first.name,
            "second": second.name
        }
        
        request = await self._wait_for_request() # wait for ratelimit requests to finish
        
        async with await self._session.get(f"/api/infinite-craft/pair", params=params) as response:
            self._done_with_request(request) # mark request as done
            # Request & Response Info
            self._logger.debug(f"{response.request_method} {response.request_url}\n"
                               f"Request Headers: {json.dumps(dict(response.request_headers), indent=4)}\n"
                               f"Response Status: {response.status}\n"
                               f"Response Content Type: {response.content_type}\n"
                               f"Response Headers: {json.dumps(dict(response.headers), indent=4)}\n"
                               f"Response Body: {await response.text()}")
            
            response.raise_for_status()
            result_data: ResultDict = await response.json()
        
        if result_data == {
            "result": "Nothing",
            "emoji": "",
            "isNew": False
        }:
            self._logger.debug(f"Unable to mix {first} + {second}")
            return self._element_cls(name=None, emoji=None, is_first_discovery=None)
        
        result = self._element_cls(
            name               = result_data.get("result"),
            emoji              = result_data.get("emoji"),
            is_first_discovery = result_data.get("isNew")
        )

        if not result.is_first_discovery:
            self._logger.debug(f"Result: {result} (first: {first} + second: {second})")
        else:
            self._logger.debug(f"Result: {result} (First Discovery) (first: {first} + second: {second})")

        if store:
            self._update_discoveries(
                name = result.name,
                emoji = result.emoji,
                is_first_discovery = result.is_first_discovery
            )
            
            raw_discoveries: list[Discovery] = self._get_raw_discoveries()
            discoveries: list[ElementProtocol] = [
                self._element_cls(
                    name = rd.get("name"),
                    emoji = rd.get("emoji"),
                    is_first_discovery = rd.get("is_first_discovery")
                ) for rd in raw_discoveries
            ]
            
            self._discoveries = discoveries
            self.discoveries = self._discoveries.copy()

        return result

    async def merge(self, first: ElementProtocol, second: ElementProtocol, *, store: bool = True) -> ElementProtocol | None:
        """
        Pair two elements and return the resulting element.

        Alias for `InfiniteCraft.pair()`.

        This method sends a request to the API to combine two elements and returns
        the result. If the combination is not possible, it returns an Element with
        all attributes set to None.

        Args:
            first (ElementProtocol): The first element to pair.
            second (ElementProtocol): The second element to pair.
            store (bool, optional): Whether to store the result in discoveries. Defaults to True.

        Returns:
            ElementProtocol: The resulting element from the pairing, or an ElementProtocol
                              with all attributes as None if they couldn't be paired.

        Raises:
            RuntimeError: If the session has not been started yet.
        """
        return await self.pair(first=first, second=second, store=store)
    
    async def combine(self, first: ElementProtocol, second: ElementProtocol, *, store: bool = True) -> ElementProtocol | None:
        """
        Pair two elements and return the resulting element.

        Alias for `InfiniteCraft.pair()`.

        This method sends a request to the API to combine two elements and returns
        the result. If the combination is not possible, it returns an Element with
        all attributes set to None.

        Args:
            first (ElementProtocol): The first element to pair.
            second (ElementProtocol): The second element to pair.
            store (bool, optional): Whether to store the result in discoveries. Defaults to True.

        Returns:
            ElementProtocol: The resulting element from the pairing, or an ElementProtocol
                              with all attributes as None if they couldn't be paired.

        Raises:
            RuntimeError: If the session has not been started yet.
        """
        return await self.pair(first=first, second=second, store=store)

    def get_discoveries(self, *, set_value: bool = False, check: Callable[[ElementProtocol], bool] | None = None) -> list[ElementProtocol]:
        """
        Get a list containing all discovered elements.

        This method retrieves all discovered elements from the discoveries storage file.
        It can optionally update the instance's discoveries attribute and filter the
        results based on a provided check function.

        Args:
            set_value (bool, optional): Whether to update the instance's discoveries
                                        attribute with the retrieved data. Defaults to False.
            check (Callable[[ElementProtocol], bool] | None, optional): A function to filter
                                                                        the discoveries. Defaults to None.

        Returns:
            list[ElementProtocol]: A list of all discovered elements, potentially filtered.
        """
        raw_discoveries = self._get_raw_discoveries()
        discoveries: list[ElementProtocol] = []
        for discovery in raw_discoveries:
            element = self._element_cls(
                name = discovery.get("name"),
                emoji = discovery.get("emoji"),
                is_first_discovery = discovery.get("is_first_discovery")
            )

            if check is not None:
                if check(element):
                    discoveries.append(element)
            else:
                discoveries.append(element)

        if set_value:
            self._discoveries = discoveries
            self.discoveries = self._discoveries.copy()
        
        return discoveries
    
    def get_discovery(self, name: str, *, from_file: bool = False) -> ElementProtocol | None:
        """
        Get a specific discovered Element by its name.

        This method searches for an element with the given name in the discoveries.
        It can search either in the instance's cached discoveries or directly from the file.

        Args:
            name (str): The name of the element to find.
            from_file (bool, optional): Whether to search in the file instead of
                                        the cached discoveries. Defaults to False.

        Returns:
            ElementProtocol | None: The discovered Element if found, None otherwise.

        """
        dummy = self._element_cls(name=name, emoji=None, is_first_discovery=None)

        if from_file:
            discovery = self.get_discoveries(check=lambda e: e.name == dummy)
            return discovery[0] if discovery else None

        return self._discoveries[self._discoveries.index(dummy)] if dummy in self._discoveries else None
    
    async def _wait_for_request(self) -> float:
        """
        Manage request timing to adhere to the API rate limit.

        This internal method ensures that requests are sent at a rate that doesn't
        exceed the API's rate limit. It tracks the timing of requests and delays
        new requests if necessary to avoid rate limiting.

        Returns:
            float: The timestamp of the current request.

        Note:
            This method is intended for internal use only.
        """
        await asyncio.sleep(0)
        current = time.monotonic()
        self._requests.append(current)
        
        while len(self._requests) > self.api_rate_limit and self._requests[0] + 60 > time.monotonic():
            self._logger.warn(f"We are getting ratelimited! Retrying in {(self._requests[0] + 60) - time.monotonic()}s...")
            await asyncio.sleep((self._requests[0] + 60) - time.monotonic())
        
        return current
    
    def _done_with_request(self, request: float) -> None:
        """
        Mark a request as completed and remove it from the tracking queue.

        This internal method is called after a request is completed to update
        the request tracking system used for rate limiting.

        Args:
            request (float): The timestamp of the completed request.

        Note:
            This method is intended for internal use only.
        """
        self._requests.remove(request)

    def _update_discoveries(self, *, name: str | None, emoji: str | None, is_first_discovery: bool | None) -> list[Discovery] | None:
        """
        Update the discoveries JSON file with a new element.

        This internal method adds a new element to the discoveries file if it doesn't
        already exist. It's typically called after a successful pairing operation.

        Args:
            name (str | None): Name of the new element.
            emoji (str | None): Emoji associated with the new element.
            is_first_discovery (bool | None): Whether this element is a first discovery.

        Returns:
            list[Discovery] | None: Updated list of discoveries if the element was added,
                                    None if the element already existed.

        Note:
            This method is intended for internal use only.
        """
        element: Discovery = {
            "name": name,
            "emoji": emoji,
            "is_first_discovery": is_first_discovery
        }

        discoveries = self._get_raw_discoveries()
        if element["name"] in [e["name"] for e in discoveries]:
            return None
        
        discoveries.append(element)

        with open(self.discoveries_location, "w", encoding=self.encoding) as f:
            json.dump(discoveries, f, indent=2)
        
        return discoveries

    def _get_raw_discoveries(self) -> list[Discovery]:
        """
        Retrieve the raw list of discoveries from the JSON file.

        This internal method reads the discoveries JSON file and returns its contents
        as a list of Discovery dictionaries.

        Returns:
            list[Discovery]: A list of all discovered elements as dictionaries.

        Note:
            This method is intended for internal use only.
        """
        with open(self.discoveries_location, encoding=self.encoding) as f:
            return json.load(f)
    
    @staticmethod
    def reset(
        *,
        discoveries_storage: str = "discoveries.json",
        encoding: str = "utf-8",
        indent: int = 2,
        make_file: bool = False
    ) -> None:
        """
        Reset the discoveries storage file to its initial state.

        This static method resets the discoveries file to its default state, containing
        only the starting discoveries. It can optionally create the file if it doesn't exist.

        Args:
            discoveries_storage (str, optional): Path to the discoveries storage file.
                                                 Defaults to "discoveries.json".
            encoding (str, optional): Encoding to use for the file. Defaults to "utf-8".
            indent (int, optional): Number of spaces for indentation in the JSON file.
                                    Defaults to 2.
            make_file (bool, optional): Whether to create the file if it doesn't exist.
                                        Defaults to False.

        Raises:
            FileNotFoundError: If the file doesn't exist and make_file is False.
        """
        if not os.path.exists(discoveries_storage):
            if make_file:
                utils.check_file(discoveries_storage)
            else:
                raise FileNotFoundError(f"File '{discoveries_storage}' not found")
        
        utils.dump_json(discoveries_storage, starting_discoveries, encoding=encoding, indent=indent)