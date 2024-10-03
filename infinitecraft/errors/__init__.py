__all__ = (
    "BaseException",
    "NotFileError",
    "NotDirectoryError",
    "NotWritableError"
)

class BaseException(Exception):
    """All errors raised by this library are subclassed from this class."""
    ...

class NotFileError(BaseException): ...
class NotDirectoryError(BaseException): ...
class NotWritableError(BaseException): ...