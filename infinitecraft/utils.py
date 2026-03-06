import os
import sys
import json
import inspect
import logging
from typing import Optional, Any, Mapping, Callable, Coroutine, TypeVar, cast
from fastapi import FastAPI

from . import errors
from .termcolors import *

__all__ = (
    "reify",
    "check_file",
    "dump_json",
    "maybe_coroutine",
    "mock_server",
    "MISSING",
    "is_docker",
    "stream_supports_colour",
    "ColourFormatter",
    "setup_logging",
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
    dump_kwargs: Mapping[str, Any] = {},
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


async def maybe_coroutine(
    __func: Callable[..., Coroutine[Any, Any, Any]], *args: Any, **kwargs: Any
) -> Any | None:
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
    async def pair(  # pyright: ignore[reportUnusedFunction]
        first: str, second: str
    ) -> dict[str, str | bool]:
        print(f"[MOCK API] PAIR: {first} + {second}")
        print(f"[MOCK API] RESULT: 🌌 ???")

        return {"result": "???", "emoji": "🌌", "isNew": False}

    return app


# the following code is heavily inspired from discord.utils from discord.py


class _MissingSentinel:
    __slots__ = ()

    def __eq__(self, other) -> bool:  # type: ignore
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self):
        return "..."


MISSING: Any = _MissingSentinel()


def is_docker() -> bool:
    path = "/proc/self/cgroup"
    return os.path.exists("/.dockerenv") or (
        os.path.isfile(path) and any("docker" in line for line in open(path))
    )


def stream_supports_colour(stream: Any) -> bool:
    is_a_tty = hasattr(stream, "isatty") and stream.isatty()

    # Pycharm and VSCode support colour in their inbuilt editors
    if "PYCHARM_HOSTED" in os.environ or os.environ.get("TERM_PROGRAM") == "vscode":
        return is_a_tty

    if sys.platform != "win32":
        # Docker does not consistently have a tty attached to it
        return is_a_tty or is_docker()

    # ANSICON checks for things like ConEmu
    # WT_SESSION checks if this is Windows Terminal
    return is_a_tty and ("ANSICON" in os.environ or "WT_SESSION" in os.environ)


class ColourFormatter(logging.Formatter):
    LEVEL_COLORS = [
        (logging.DEBUG, bold + bg_black),
        (logging.INFO, bold + blue),
        (logging.WARNING, bold + yellow),
        (logging.ERROR, bold + red),
        (logging.CRITICAL, bg_rgb(200, 0, 0) + white),
    ]

    def __init__(
        self, *args: Any, name_color: Optional[str] = None, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)

        self.FORMATS = {
            level: logging.Formatter(
                f"{bold + black}%(asctime)s{reset} {color}%(levelname)-8s{reset} {name_color or red}%(name)s{reset} %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )
            for level, color in self.LEVEL_COLORS
        }

    def format(self, record: logging.LogRecord) -> str:
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        # Override the traceback to always print in red
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f"\x1b[31m{text}\x1b[0m"

        output = formatter.format(record)

        # Remove the cache layer
        record.exc_text = None
        return output


def setup_logging(
    *,
    name_color: Optional[str] = None,
    handler: Optional[logging.Handler] = None,
    formatter: Optional[logging.Formatter] = None,
    level: Optional[int] = None,
    root: bool = True,
) -> None:
    if level is None:
        level = logging.INFO

    if handler is None:
        handler = logging.StreamHandler(sys.stderr)

    if formatter is None:
        # Cast to Any to suppress 'Unknown' generic type argument warnings
        stream = cast(Any, getattr(handler, "stream", None))
        if isinstance(handler, logging.StreamHandler) and stream_supports_colour(
            stream
        ):
            formatter = ColourFormatter(name_color=name_color)
        else:
            dt_fmt = "%Y-%m-%d %H:%M:%S"
            formatter = logging.Formatter(
                "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
            )

    if root:
        logger = logging.getLogger()
    else:
        library, _, _ = __name__.partition(".")
        logger = logging.getLogger(library)

    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)

    # Cast back to logging.Handler to strip the partially unknown type for strict mode
    logger.addHandler(cast(logging.Handler, handler))
