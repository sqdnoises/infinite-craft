from .element import Element
from typing import TypedDict, MutableMapping, Any

__all__ = (
    "Unused",
    "RawDiscovery",
    "Discoveries",
    "RawDiscoveries",
    "Emojis"
)

Unused = Any

Discovery = Element
Discoveries = list[Element]

class RawDiscovery(TypedDict):
    name: str | None
    is_first_discovery: bool| None

RawDiscoveries = list[RawDiscovery]

Emoji = MutableMapping[str | None, str | None]
Emojis = Emoji