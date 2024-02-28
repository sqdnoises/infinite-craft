import os
import json
import aiohttp
from typing import Callable

from .element   import Element
from .logger    import Logger
from .constants import *


__all__ = (
    "InfiniteCraft",
)


class InfiniteCraft:
    """
    Initialize an Infinite Craft session

    ## Attributes:
        `discoveries` (`list`): List of `Element` objects that have been discovered
        `closed` (`bool`): Whether the Infinite Craft session is closed or not

    ## Arguments:
        `api_url` (str): The API URL to contact. Defaults to `"https://neal.fun/api/infinite-craft"`
        `discoveries_storage` (`str`): Path to discoveries storage JSON. Defaults to `"discoveries.json"`
        `emoji_cache` (`str`): Path to emoji cache JSON. Defaults to `"emoji_cache.json"`
        `encoding` (`str`): Encoding to use while reading or saving json files. Defaults to `"utf-8"`
        `do_reset` (`bool`): Whether to reset the discoveries storage JSON and emoji cache JSON
        `headers` (`dict`): Headers to send to the API. Defaults to `{}`
        `element_cls` (`Element`): Class to be used for creating elements (MUST BE A SUBCLASS OF `Element`)
        `logger` (`class`): An initialized logger class or module with methods `info`, `warn`, `error`, `fatal`, and `debug` to use for logging. Defaults to a custom logger `Logger`
    """
    
    def __init__(
        self, *,
        api_url: str             = "https://neal.fun",
        discoveries_storage: str = "discoveries.json",
        emoji_cache: str         = "emoji_cache.json",
        encoding: str            = "utf-8",
        do_reset: bool           = False,
        headers: dict            = {},
        element_cls: Element     = Element,
        logger                   = Logger()
    ) -> None:
        
        if not os.path.exists(discoveries_storage):
            raise FileNotFoundError(f"File '{discoveries_storage}' not found")
        
        if not os.path.exists(emoji_cache):
            raise FileNotFoundError(f"File '{emoji_cache}' not found")
        
        if not issubclass(element_cls, Element):
            raise TypeError("element_cls must be a subclass of 'Element'")
        
        self._api_url = api_url
        self._discoveries_location = discoveries_storage
        self._emoji_cache = emoji_cache
        self._encoding = encoding
        self._element_cls = element_cls
        self._logger = logger

        if do_reset:
            self._logger.warn("Resetting discoveries and emoji cache JSON files")
            self.reset(
                discoveries_storage=discoveries_storage,
                emoji_cache=emoji_cache,
                encoding=encoding
            )

        self._discoveries: list[Element] = []
        self.discoveries: list[Element] = self._discoveries.copy()
        self.get_discoveries(set_value=True)

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
            "User-Agent": "Mozilla/5.0 (Linux) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        }
        self._headers.update(headers)

        self._session = aiohttp.ClientSession(
            api_url,
            headers = self._headers,
            skip_auto_headers = ["User-Agent", "Content-Type"],
            raise_for_status = True,
            timeout = aiohttp.ClientTimeout(60)
        )
        
        self._closed = False
        self.closed = self._closed

    def __str__(self) -> str:
        try:
            discoveries = len(self.discoveries)
        except:
            discoveries = None
        
        return f"<InfiniteCraft discoveries={discoveries} closed={self._closed}>"

    def __repr__(self) -> str:
        return "InfiniteCraft()"

    async def __aenter__(self) -> None:
        self._logger.debug("Entering InfiniteCraft")

    async def __aexit__(self, *args) -> None:
        self._logger.debug("Exiting InfiniteCraft")
        await self.close()
    
    async def close(self) -> None:
        """Close the Infinite Craft session."""
        if not self._closed:
            await self._session.close()
            self._closed = True
            self.closed = True
            self._logger.warn("Closed InfiniteCraft session")
        
        else:
            raise RuntimeError("This InfiniteCraft session is already closed")

    async def stop(self) -> None:
        """Close the Infinite Craft session.

        Alias for `InfiniteCraft.close()`"""
        await self.close()

    async def pair(self, first: Element, second: Element) -> Element | None:
        """Pair two elements and return the resulting element

        Returns `None` if the elements could not be paired.

        ## Arguments:
            `first` (`Element`): The first element
            `second` (`Element`): The second element

        ## Raises:
            `TypeError`: if `first` or `second` is not an instance of `Element`

        ## Returns:
            `Element | None`: The resulting element as an `Element` object or `None`
        """

        if not isinstance(first, Element):
            raise TypeError("first must be an instance of 'Element'")
        
        if not isinstance(second, Element):
            raise TypeError("second must be an instance of 'Element'")
        
        self._logger.debug(f"Pairing {first} and {second}...")
        
        params = {
            "first":  first.name,
            "second": second.name
        }
        async with self._session.get(f"/api/infinite-craft/pair", params=params) as response:
            result = await response.json(encoding=self._encoding)
        
        if result == {
            "result": "Nothing",
            "emoji": "",
            "isNew": False
        }:
            self._logger.debug(f"Unable to mix {first} + {second}")
            return None
        
        result: Element = self._element_cls(
            name               = result.get("result"),
            emoji              = result.get("emoji"),
            is_first_discovery = result.get("isNew")
        )

        if not result.is_first_discovery:
            self._logger.debug(f"Result: {result} (first: {first} + second: {second})")
        else:
            self._logger.debug(f"NEW DISCOVERY: {result} (first: {first} + second: {second})")
        
        emojis = self._update_emojis(
            name = result.name,
            emoji = result.emoji
        )
        
        if emojis is None:
            emojis = self._get_emojis()

        discoveries = self._update_discoveries(
            name = result.name,
            is_first_discovery = result.is_first_discovery
        )
        
        if discoveries is None:
            discoveries = self._get_raw_discoveries()

        discoveries: list[Element] = [
            self._element_cls(
                name = discovery.get("name"),
                emoji = emojis.get(discovery.get("name")),
                is_first_discovery = discovery.get("is_first_discovery")
            ) for discovery in discoveries
        ]
        
        self._discoveries = discoveries
        self.discoveries = self._discoveries.copy()

        return result

    async def merge(self, first: Element, second: Element) -> Element | None:
        """Pair two elements and return the resulting element

        Returns `None` if the elements could not be paired.

        Alias for `InfiniteCraft.pair()`.

        ## Arguments:
            `first` (`Element`): The first element
            `second` (`Element`): The second element

        ## Raises:
            `TypeError`: if `first` or `second` is not of type `Element`

        ## Returns:
            `Element | None`: The resulting element as an `Element` object or `None`
        """
        return await self.pair(first=first, second=second)
    
    async def combine(self, first: Element, second: Element) -> Element | None:
        """Pair two elements and return the resulting element

        Returns `None` if the elements could not be paired.

        Alias for `InfiniteCraft.pair()`.

        ## Arguments:
            `first` (`Element`): The first element
            `second` (`Element`): The second element

        ## Raises:
            `TypeError`: if `first` or `second` is not of type `Element`

        ## Returns:
            `Element | None`: The resulting element as an `Element` object or `None`
        """
        return await self.pair(first=first, second=second)

    def get_discoveries(self, *, set_value: bool = False, check: Callable = None) -> list[Element]:
        """Get a `list` containing all discovered elements

        ## Arguments:
            `set_value` (`bool`): Whether to set the value for the `InfiniteCraft.discoveries` attribute after getting it
            `check` (`Callable[..., Coroutine[Any, Any, Any]]`): A callable or a coroutine that accepts an argument `element` and returns a bool to whether add the element or not

        ## Returns:
            `list[Element]`: The `list` containing every `Element` discovered   
        """
        
        raw_discoveries = self._get_raw_discoveries()
        emojis = self._get_emojis()
        
        discoveries = []
        for discovery in raw_discoveries:
            element: Element = self._element_cls(
                name = discovery.get("name"),
                emoji = emojis.get(discovery.get("name")),
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
    
    def get_discovery(self, *, set_value: bool = False) -> list[Element]:
        """Get a `list` containing all discovered elements

        ## Arguments:
            `set_value` (`bool`): Whether to set the value for the `InfiniteCraft.discoveries` attribute after getting it

        ## Returns:
            `list[Element]`: The `list` containing every `Element` discovered   
        """
        raw_discoveries = self._get_raw_discoveries()
        emojis = self._get_emojis()
        discoveries: list[Element] = [
            self._element_cls(
                name = discovery.get("name"),
                emoji = emojis.get(discovery.get("name")),
                is_first_discovery = discovery.get("is_first_discovery")
            ) for discovery in raw_discoveries
        ]
        
        if set_value:
            self._discoveries = discoveries
            self.discoveries = self._discoveries.copy()
        
        return discoveries

    def _update_discoveries(self, *, name: str, is_first_discovery: bool) -> None | list:
        """Update the discoveries JSON file with a new element

        Please do not use this method as it is meant for `internal use` and should not be used directly.
        Use this if you know what you are doing.

        ## Arguments:
            `name` (`str`): Name of the new element
            `is_first_discovery` (`bool`): Whether the new element was first discovered

        ## Returns:
            `None | list`: Returns `None` if element already exists and returns list of all discovered elements with this new element if the discoveries JSON file was updated successfully
        """
        
        element = {
            "name": name,
            "is_first_discovery": is_first_discovery
        }

        discoveries = self._get_raw_discoveries()
        if element in discoveries:
            return None
        
        discoveries.append(element)

        with open(self._discoveries_location, mode="w", encoding=self._encoding) as f:
            json.dump(discoveries, f, indent=2)
        
        return discoveries

    def _get_raw_discoveries(self) -> list:
        """Get a `list` containing all discovered elements where each element is a `dict` without the emoji property

        Please do not use this method as it is meant for `internal use` and should not be used directly.
        Use this if you know what you are doing.

        ## Returns:
            `list`: The `list` containing every element as a `dict` discovered
        """

        with open(self._discoveries_location, encoding=self._encoding) as f:
            return json.load(f)
    
    def _update_emojis(self, *, name: str, emoji: str) -> None | dict:
        """Update the emoji cache JSON file with a new element's emoji

        Please do not use this method as it is meant for `internal use` and should not be used directly.
        Use this if you know what you are doing.

        ## Arguments:
            `name` (`str`): Name of the element
            `emoji` (`str`): The emoji to save

        ## Returns:
            `None | list`: Returns `None` if element already exists and returns list of all elements' emojis with the added element if the emoji cache JSON file was updated successfully
        """

        emojis = self._get_emojis()
        if name in emojis:
            return None
        
        emojis.update({name: emoji})

        with open(self._emoji_cache, mode="w", encoding=self._encoding) as f:
            json.dump(emojis, f, indent=2)
        
        return emojis

    def _get_emojis(self) -> dict:
        """Get a `dict` containing every element discovered's emoji

        Please do not use this method as it is meant for `internal use` and should not be used directly.
        Use this if you know what you are doing.

        Returns:
            list: The `list` containing every element's emoji
        """

        with open(self._emoji_cache, encoding=self._encoding) as f:
            return json.load(f)
    
    @staticmethod
    def reset(*, discoveries_storage: str = "discoveries.json", emoji_cache: str = "emoji_cache.json", encoding: str = "utf-8") -> None:
        """Reset the discoveries storage JSON and emoji cache JSON

        ## Arguments:
            `discoveries_storage` (`str`): Path to discoveries storage JSON. Defaults to `"discoveries.json"`
            `emoji_cache` (`str`): Path to emoji cache JSON. Defaults to `"emoji_cache.json"`
            `encoding` (`str`): Encoding to use while reading or saving json files. Defaults to `"utf-8"`
        """

        if not os.path.exists(discoveries_storage):
            raise FileNotFoundError(f"File '{discoveries_storage}' not found")

        if not os.path.exists(emoji_cache):
            raise FileNotFoundError(f"File '{emoji_cache}' not found")
        
        with open(discoveries_storage, mode="w", encoding=encoding) as f:
            json.dump(starting_discoveries, f, indent=2)

        with open(emoji_cache, mode="w", encoding=encoding) as f:
            json.dump(starting_emoji_cache, f, indent=2)