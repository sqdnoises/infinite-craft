from .element import Element
from typing import Any, TypedDict

__all__ = (
    "Unused",
    "ResultDict",
    "RawDiscovery",
    "Discoveries",
    "RawDiscoveries"
)

Unused = Any

class ResultDict(TypedDict):
    result: str
    emoji: str
    isNew: bool

Discovery = Element
Discoveries = list[Element]

class RawDiscovery(TypedDict):
    name: str | None
    emoji: str | None
    is_first_discovery: bool| None

RawDiscoveries = list[RawDiscovery]