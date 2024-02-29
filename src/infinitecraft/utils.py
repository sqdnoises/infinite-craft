import inspect
from typing import Callable, Coroutine, Any, NoReturn


def session_not_started(*args, **kwargs) -> NoReturn:
    raise RuntimeError("Session has not been started")


async def maybe_coroutine(__func: Callable[..., Coroutine[Any, Any, Any]], *args, **kwargs) -> Any | None:
    """An asynchronous function that runs a callable or a coroutine with the given arguments

    ## Arguments:
        `__func` (`Callable[..., Coroutine[Any, Any, Any]]`): The callable or coroutine
        `*args`: Arguments to be passed to the callable or coroutine
        `*kwargs`: Keyword arguments to be passed to the callable or coroutine

    ## Returns:
        `Any | None`: Returns the returned value of the callable or coroutine
    """
    
    if inspect.iscoroutine(__func):
        return await __func
    elif inspect.iscoroutinefunction(__func):
        return await __func(*args, **kwargs)
    else:
        return __func(*args, **kwargs)