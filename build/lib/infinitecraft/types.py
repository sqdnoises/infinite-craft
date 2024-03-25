from .element import Element
from typing import TypedDict, Any

__all__ = (
    "Unused",
    "RawDiscovery",
    "Discoveries",
    "RawDiscoveries"
)

Unused = Any

Discovery = Element
Discoveries = list[Element]

class RawDiscovery(TypedDict):
    name: str | None
    emoji: str | None
    is_first_discovery: bool| None

RawDiscoveries = list[RawDiscovery]