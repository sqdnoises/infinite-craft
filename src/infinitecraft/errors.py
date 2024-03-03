__all__ = (
    "NotFileError",
    "NotDirectoryError",
    "NotWritableError"
)

class NotFileError(Exception):
    pass

class NotDirectoryError(Exception):
    pass

class NotWritableError(Exception):
    pass