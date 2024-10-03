import os
import json
import inspect
from typing import (
    Any, Mapping,
    Callable, Coroutine,
    TypeVar
)
from fastapi import FastAPI
from . import errors

__all__ = (
    "reify",
    "check_file",
    "dump_json",
    "maybe_coroutine",
    "mock_server"
)

_T = TypeVar("_T")

class reify:
    """
    A decorator that acts like a cached property. The first time the
    decorated method is called, its result is stored on the instance, and
    subsequent accesses return the cached value.
    """

    def __init__(self, func: Callable[[Any], _T]) -> None:
        self.func = func
        self.__doc__ = func.__doc__
        self.name = func.__name__

    def __get__(self, instance: Any, owner: type[Any] | None = None) -> Any:
        if instance is None:
            return self
        # Check if the cached value already exists
        if self.name in instance.__dict__:
            return instance.__dict__[self.name]
        # Compute the value and cache it
        value = self.func(instance)
        instance.__dict__[self.name] = value
        return value

def check_file(path: str) -> bool:
    """
    Check if a file exists and is writable, or if it can be created.

    Args:
        path (str): The path to the file to check.

    Returns:
        bool: True if the file exists and is writable, False if it doesn't exist but can be created.

    Raises:
        NotWritableError: If the file exists but is not writable.
        NotFileError: If the path exists but is not a file.
        NotDirectoryError: If the parent directory is not a directory.
    """
    path = os.path.abspath(path)
    
    if os.path.exists(path):
        if os.path.isfile(path):
            if not os.access(path, os.W_OK):
                raise errors.NotWritableError(f"path '{path}' is not writable")
            return True
        else:
            raise errors.NotFileError(f"path '{path}' is not a file")
    
    dir = os.path.dirname(path)
    if not os.access(dir, os.R_OK):
        return False
    
    if os.path.isdir(dir):
        os.makedirs(dir, exist_ok=True)
    else:
        raise errors.NotDirectoryError(f"path '{dir}' is not a directory")
    
    return False
    
def dump_json(
    file: str,
    data: Any,
    encoding: str = "utf-8",
    indent: int = 2,
    open_kwargs: Mapping[str, Any] = {},
    dump_kwargs: Mapping[str, Any] = {}
) -> None:
    """
    Dump JSON data into a file.

    Args:
        file (str): Path to the file where JSON data will be written.
        data (Any): JSON-serializable data to be dumped.
        encoding (str, optional): Encoding of the file. Defaults to "utf-8".
        indent (int, optional): Number of spaces to use as indentation. Defaults to 2.
        open_kwargs (Mapping[str, Any], optional): Additional keyword arguments for open(). Defaults to {}.
        dump_kwargs (Mapping[str, Any], optional): Additional keyword arguments for json.dump(). Defaults to {}.
    """
    with open(file, "w", encoding=encoding, **open_kwargs) as f:
        json.dump(data, f, indent=indent, **dump_kwargs)

async def maybe_coroutine(__func: Callable[..., Coroutine[Any, Any, Any]], *args: Any, **kwargs: Any) -> Any | None:
    """
    Execute a callable or coroutine with given arguments.

    This function can handle both regular functions and coroutines. It will await
    coroutines and directly call regular functions.

    Args:
        __func (Callable[..., Coroutine[Any, Any, Any]]): The callable or coroutine to execute.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        Any | None: The return value of the executed function or coroutine.
    """
    if inspect.iscoroutine(__func):
        return await __func
    elif inspect.iscoroutinefunction(__func):
        return await __func(*args, **kwargs)
    else:
        return __func(*args, **kwargs)

def mock_server() -> FastAPI:
    """
    Create and configure a mock FastAPI server for testing purposes.

    This function sets up a FastAPI application with a single endpoint that simulates
    the behavior of an infinite craft pairing API.

    Returns:
        FastAPI: A configured FastAPI application instance with the following endpoint:
            - GET /api/infinite-craft/pair: Simulates pairing two items.

    Endpoint details:
        GET /api/infinite-craft/pair:
            - Parameters:
                - first (str): The name of the first item to pair.
                - second (str): The name of the second item to pair.
            - Returns:
                A dictionary with the following keys:
                - result (str): Always returns "???" to simulate an unknown result.
                - emoji (str): Always returns "🌌" as the result emoji.
                - isNew (bool): Always returns False, indicating the result is not new.

    Note:
        This mock server prints debugging information to the console for each request,
        including the paired items and the mock result.
    """
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

    @app.get("/api/infinite-craft/pair")
    async def pair(first: str, second: str) -> dict[str, str | bool]: # pyright: ignore[reportUnusedFunction]
        print(f"[MOCK API] PAIR: {first} + {second}")
        print(f"[MOCK API] RESULT: 🌌 ???")
        
        return {
            "result": "???",
            "emoji": "🌌",
            "isNew": False
        }
    
    return app