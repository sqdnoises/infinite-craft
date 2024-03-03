from .element import Element
from typing import TypedDict, MutableMapping

__all__ = (
    "RawDiscovery",
    "Discoveries",
    "RawDiscoveries",
    "Emojis"
)

Discovery = Element
Discoveries = list[Element]

class RawDiscovery(TypedDict):
    name: str | None
    is_first_discovery: bool| None

RawDiscoveries = list[RawDiscovery]

Emoji = MutableMapping[str | None, str | None]
Emojis = Emoji