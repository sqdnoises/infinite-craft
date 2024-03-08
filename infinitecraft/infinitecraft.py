"""
MIT License

Copyright (c) 2024-present SqdNoises, Neal Agarwal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import json
import time
import aiohttp
import asyncio
from typing import (
    Callable,
    MutableMapping,
    Any
)

from .          import utils
from .dummies   import DummyClientSession
from .element   import Element
from .logger    import Logger
from .constants import *
from .types     import *


__all__ = (
    "InfiniteCraft",
)


class InfiniteCraft:
    """
    Initialize an Infinite Craft session

    ## Attributes:
        `discoveries` (`list[Element]`): List of `Element` objects that have been discovered.
        `closed` (`bool | None`): Whether the Infinite Craft session is closed or not. `None` if session has not been started.

    ## Arguments:
        `api_url` (`str`, optional): The API URL to contact. Defaults to `"https://neal.fun/api/infinite-craft"`.
        `api_rate_limit` (`int`, optional): The requests per minute the API can handle before ratelimiting. `0` if you want no ratelimit. Defaults to `400` requests per minute. Must be greater than or equal to `0`.
        `manual_control` (`bool`, optional): Manually control `InfiniteCraft.start()` and `InfiniteCraft.stop()`. Useful when using `async with` multiple times. Defaults to `False`.
        `discoveries_storage` (`str`, optional): Path to discoveries storage JSON. Defaults to `"discoveries.json"`.
        `encoding` (`str`, optional): Encoding to use while reading or saving json files. Defaults to `"utf-8"`.
        `do_reset` (`bool`, optional): Whether to reset the discoveries storage JSON and emoji cache JSON. Defaults to `False`.
        `headers` (`dict`, optional): Headers to send to the API. Defaults to `{}`.
        `element_cls` (`Element`, optional): Class to be used for creating elements (MUST BE A SUBCLASS OF `Element`). Defaults to `Element`.
        `logger` (`class`, optional): An initialized logger class or module with methods `info`, `warn`, `error`, `fatal`, and `debug` to use for logging. Defaults to a custom logger `Logger`.
    """
    
    def __init__(
        self, *,
        api_url: str                      = "https://neal.fun", # API to contact
        api_rate_limit: int               = 400,                # 400 requests per minute
        manual_control: bool              = False,
        discoveries_storage: str          = "discoveries.json", # where to store the game data
        encoding: str                     = "utf-8",
        do_reset: bool                    = False,
        make_file: bool                   = True,
        headers: MutableMapping[str, str] = {},
        element_cls: type[Element]        = Element,
        logger: Any                       = Logger()
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
        
        if not issubclass(element_cls, Element): # type: ignore
            raise TypeError("element_cls must be a subclass of 'Element'")
        
        self._api_url = api_url
        self._api_rate_limit = api_rate_limit
        self._manual_control = manual_control
        self._discoveries_location = discoveries_storage
        self._encoding = encoding
        self._element_cls = element_cls
        self._logger = logger

        self._requests: list[float] = []

        if do_reset and not dsreset:
            self._logger.warn(f"Resetting discoveries JSON file ({discoveries_storage})")
            self.reset(
                discoveries_storage=discoveries_storage,
                encoding=encoding
            )

        self._discoveries: Discoveries = []
        self.discoveries: Discoveries = self._discoveries.copy()
        self.get_discoveries(set_value=True)

        self._session: aiohttp.ClientSession = DummyClientSession() # Dummy session # type: ignore
        self._headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
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
            "User-Agent": "Mozilla/5.0 (Windows 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        }
        self._headers.update(headers)

        self._closed: bool | None = None
        self.closed: bool | None = None

    def __str__(self) -> str:
        try:
            discoveries = len(self._discoveries)
        except:
            discoveries = None
        
        return f"<InfiniteCraft discoveries={discoveries} closed={self._closed}>"

    def __repr__(self) -> str:
        return (
            "InfiniteCraft("
                f"api_url={repr(self._api_url)}, "
                f"manual_control={repr(self._manual_control)}, "
                f"discoveries_storage={repr(self._discoveries_location)}, "
                f"encoding={repr(self._encoding)}, "
                f"headers={repr(self._headers)}, "
                f"element_cls={repr(self._element_cls)}, "
                f"logger={repr(self._logger)}"
            ")"
        )

    async def __aenter__(self) -> "InfiniteCraft":
        if not self._manual_control:
            self._logger.debug("ENTER: Manual control is OFF; Starting session")
            await self.start()
        else:
            self._logger.debug("ENTER: Manual control is ON;")
        
        return self

    async def __aexit__(self, *args: Unused) -> None:
        if not self._manual_control:
            self._logger.debug("EXIT: Manual control is OFF; Stopping session")
            await self.close()
        else:
            self._logger.debug("EXIT: Manual control is ON;")

    async def ping(self) -> float:
        """Ping the API and return the latency

        Only works when the session has been started.

        ## Returns:
            `float`: The latency in seconds.
        """
        
        self._logger.debug(f"Pinging API route: {self._api_url}/api/infinite-craft/pair with Fire + Water")
        
        params = {
            "first":  "Fire",
            "second": "Water"
        }
        
        start = time.monotonic()
        async with self._session.get(f"/api/infinite-craft/pair", params=params):
            end = time.monotonic() - start

        self._logger.debug(f"API response time: {end}s")

        return end

    async def start(self) -> None:
        """Start the Infinite Craft session
        
        ## Raises:
            `RuntimeError`: Raises when session is closed or is already.
        """
        if self._closed:
            raise RuntimeError("Cannot start session; Session has been closed")
        
        elif self._closed is None:
            await self._build_session(
                self._api_url,
                headers = self._headers,
                skip_auto_headers = ["User-Agent", "Content-Type"],
                raise_for_status = True
            )
            
            self._closed = False
            self.closed = False
        
        else:
            raise RuntimeError("Session is already running")

    async def close(self) -> None:
        """Close the Infinite Craft session
        
        ## Raises:
            `RuntimeError`: Raises when session has not been started or is already closed.
        """
        if self._closed is None:
            raise RuntimeError("Cannot close session; Session has not been started yet")

        elif not self._closed:
            await self._session.close()
            self._closed = True
            self.closed = True
            self._logger.warn("Closed InfiniteCraft session")
        
        else:
            raise RuntimeError("This InfiniteCraft session is already closed")

    async def stop(self) -> None:
        """Close the Infinite Craft session.

        Alias for `InfiniteCraft.close()`
        
        ## Raises:
            `RuntimeError`: Raises when session has not been started or is already closed.
        """
        await self.close()

    async def pair(self, first: Element, second: Element, *, store: bool = True) -> Element:
        """Pair two elements and return the resulting element

        Returns an `Element` with all attributes as `None` if they could not be paired.
        
        ## Arguments:
            `first` (`Element`): The first element.
            `second` (`Element`): The second element.
            `store` (`bool`): Whether to store the result `Element` to `InfiniteCraft.discoveries`. Defaults to `True`.

        ## Raises:
            `TypeError`: If `first` or `second` is not an instance of `Element`.

        ## Returns:
            `Element`: The resulting element as an `Element` object or an `Element` with all attributes as `None` if they could not be paired.
        """

        if not isinstance(first, Element): # type: ignore
            raise TypeError("first must be an instance of 'Element'")
        
        if not isinstance(second, Element): # type: ignore
            raise TypeError("second must be an instance of 'Element'")
        
        self._logger.debug(f"Pairing {first} and {second}...")
        
        params = {
            "first":  first.name,
            "second": second.name
        }
        
        await self._wait_for_request() # wait for ratelimit requests to finish
        
        async with self._session.get(f"/api/infinite-craft/pair", params=params) as response:
            result = await response.json(encoding=self._encoding)
        
        if result == {
            "result": "Nothing",
            "emoji": "",
            "isNew": False
        }:
            self._logger.debug(f"Unable to mix {first} + {second}")
            return Element(name=None, emoji=None, is_first_discovery=None)
        
        result = self._element_cls(
            name               = result.get("result"),
            emoji              = result.get("emoji"),
            is_first_discovery = result.get("isNew")
        )

        if not result.is_first_discovery:
            self._logger.debug(f"Result: {result} (first: {first} + second: {second})")
        else:
            self._logger.debug(f"Result: {result} (First Discovery) (first: {first} + second: {second})")

        if store:
            discoveries = self._update_discoveries(
                name = result.name,
                emoji = result.emoji,
                is_first_discovery = result.is_first_discovery
            )
            
            if discoveries is None:
                discoveries = self._get_raw_discoveries()

            discoveries = [
                self._element_cls(
                    name = discovery.get("name"),
                    emoji = discovery.get("emoji"),
                    is_first_discovery = discovery.get("is_first_discovery")
                ) for discovery in discoveries
            ]
            
            self._discoveries = discoveries
            self.discoveries = self._discoveries.copy()

        return result

    async def merge(self, first: Element, second: Element, *, store: bool = True) -> Element | None:
        """Pair two elements and return the resulting element

        Returns an `Element` with all attributes as `None` if they could not be paired.
        
        Alias for `InfiniteCraft.pair()`.
        
        ## Arguments:
            `first` (`Element`): The first element.
            `second` (`Element`): The second element.
            `store` (`bool`): Whether to store the result `Element` to `InfiniteCraft.discoveries`. Defaults to `True`.

        ## Raises:
            `TypeError`: If `first` or `second` is not an instance of `Element`.

        ## Returns:
            `Element`: The resulting element as an `Element` object or an `Element` with all attributes as `None` if they could not be paired.
        """
        return await self.pair(first=first, second=second, store=store)
    
    async def combine(self, first: Element, second: Element, *, store: bool = True) -> Element | None:
        """Pair two elements and return the resulting element

        Returns an `Element` with all attributes as `None` if they could not be paired.
        
        Alias for `InfiniteCraft.pair()`.
        
        ## Arguments:
            `first` (`Element`): The first element.
            `second` (`Element`): The second element.
            `store` (`bool`): Whether to store the result `Element` to `InfiniteCraft.discoveries`. Defaults to `True`.

        ## Raises:
            `TypeError`: If `first` or `second` is not an instance of `Element`.

        ## Returns:
            `Element`: The resulting element as an `Element` object or an `Element` with all attributes as `None` if they could not be paired.
        """
        return await self.pair(first=first, second=second, store=store)

    def get_discoveries(self, *, set_value: bool = False, check: Callable[[Element], bool] | None = None) -> Discoveries:
        """Get a `list` containing all discovered elements

        ## Arguments:
            `set_value` (`bool`, optional): Whether to set the value for the `InfiniteCraft.discoveries` attribute after getting it. Defaults to `None`.
            `check` (`Callable[[Element], bool]`, optional): A callable functions that accepts an argument for `element` and returns a bool to whether add the element or not. Defaults to `None`.

        ## Returns:
            `list[Element]`: The `list` containing every `Element` discovered.
        """
        
        raw_discoveries = self._get_raw_discoveries()
        
        discoveries: Discoveries = []
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
    
    def get_discovery(self, name: str, *, from_file: bool = False) -> Element | None:
        """Get a discovered `Element`

        ## Arguments:
            `name` (`str`): Name of element to get.
            `from_file` (`bool`, optional): Whether to check the discoveries JSON file for the element. Defaults to `False`.

        ## Returns:
            `Element | None`: The discovered `Element` or `None` if it wasn't discovered.
        """

        dummy = Element(name=name, emoji=None, is_first_discovery=None)

        if from_file:
            discovery = self.get_discoveries(check=lambda e: e.name == dummy)
            return discovery[0] if discovery else None

        return self._discoveries[self._discoveries.index(dummy)] if dummy in self._discoveries else None

    async def _build_session(self, *args: Unused, **kwargs: Unused) -> None:
        """Build `aiohttp.ClientSession(*args, **kwargs)`
        
        Do not use this method as it is meant for `internal use only` and should not be used by the user.
        """
        self._session = aiohttp.ClientSession(*args, **kwargs)
    
    async def _wait_for_request(self) -> None:
        """Manage requests to abide by the rate limit
        
        Takes the ratelimit requests per minute value from `self._api_rate_limit` and manages them in `self._requests`.

        Please do not use this function as it is meant for `internal use only` and should not be used by the user.
        Only use this if you know what you are doing.
        """
        
        await asyncio.sleep(0)
        current = time.monotonic()
        self._requests.append(current)
        
        while len(self._requests) > self._api_rate_limit and self._requests[0] + 60 > time.monotonic():
            self._logger.warn(f"We are getting ratelimited! Retrying in {(self._requests[0] + 60) - time.monotonic()}s...")
            await asyncio.sleep((self._requests[0] + 60) - time.monotonic())
        
        self._requests.remove(current)

    def _update_discoveries(self, *, name: str | None, emoji: str | None, is_first_discovery: bool | None) -> RawDiscoveries | None:
        """Update the discoveries JSON file with a new element

        Please do not use this function as it is meant for `internal use only` and should not be used by the user.
        Only use this if you know what you are doing.

        ## Arguments:
            `name` (`str | None`): Name of the new element.
            `is_first_discovery` (`bool | None`): Whether the new element was first discovered.

        ## Returns:
            `None | RawDiscoveries`: Returns `None` if element already exists and returns a `list` of all discovered elements with this new element if the discoveries JSON file was updated successfully.
        """
        
        element: RawDiscovery = {
            "name": name,
            "emoji": emoji,
            "is_first_discovery": is_first_discovery
        }

        discoveries = self._get_raw_discoveries()
        if element["name"] in [e["name"] for e in discoveries]:
            return None
        
        discoveries.append(element)

        with open(self._discoveries_location, "w", encoding=self._encoding) as f:
            json.dump(discoveries, f, indent=2)
        
        return discoveries

    def _get_raw_discoveries(self) -> RawDiscoveries:
        """Get a `list` containing all discovered elements where each element is a `dict` without the emoji property

        Please do not use this function as it is meant for `internal use only` and should not be used by the user.
        Only use this if you know what you are doing.

        ## Returns:
            `RawDiscoveries`: The `list` containing every element as a `dict` discovered.
        """

        with open(self._discoveries_location, encoding=self._encoding) as f:
            return json.load(f)
    
    @staticmethod
    def reset(
        *,
        discoveries_storage: str = "discoveries.json",
        encoding: str = "utf-8",
        indent: int = 2,
        make_file: bool = False
    ) -> None:
        
        """Reset the discoveries storage JSON and emoji cache JSON
        
        This is a `@staticmethod`, hence it can be used using `InfiniteCraft.reset()` without initialising the class.

        ## Arguments:
            `discoveries_storage` (`str | None`, optional): Path to discoveries storage JSON. Defaults to `"discoveries.json"`.
            `encoding` (`str`, optional): Encoding to use while reading or saving json files. Defaults to `"utf-8"`.
            `indent` (`int`, optional): Number of spaces to use as indents. Defaults to `2`.
            `make_file` (`bool`, optional): Make the files if they don't exist. Defaults to `False`.
        
        ## Returns:
            `bool`: Whether the file was reset or not.
        """
        
        if not os.path.exists(discoveries_storage):
            if make_file:
                utils.check_file(discoveries_storage)
            else:
                raise FileNotFoundError(f"File '{discoveries_storage}' not found")
        
        utils.dump_json(discoveries_storage, starting_discoveries, encoding=encoding, indent=indent)