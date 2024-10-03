from typing import TypedDict

__all__ = (
    "ResultDict",
    "Discovery"
)

class ResultDict(TypedDict):
    result: str
    emoji: str
    isNew: bool

class Discovery(TypedDict):
    name: str | None
    emoji: str | None
    is_first_discovery: bool| None