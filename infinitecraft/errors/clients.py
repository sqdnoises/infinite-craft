__all__ = (
    "BaseException",
    "ClientResponseError"
)

class BaseException(Exception):
    """All errors raised by the clients module are subclassed from this class."""
    ...

class ClientResponseError(BaseException): ...