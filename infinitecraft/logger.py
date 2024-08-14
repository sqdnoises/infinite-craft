"""
Use either (pre initialised)
```py
from logger import logging

logging.name = "My Program"
logging.log_level = 5
logging.info("Hello World")
```

or
```py
from logger import Logger

logging = Logger("My Program", log_level=5)
logging.info("Hello World")
```

Copyright (c) 2023-present SqdNoises
"""

import traceback
from datetime import datetime
from typing import Callable, Any, Literal

from .termcolors import *
from .termcolors import rgb

__all__ = (
    "Logger",
)

LOGGER_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
NAME_COLOR = rgb(222, 235, 47)
LOG_TYPES_TEXT = {
    "info"    : bold + rgb(208, 209, 192) + "INFO    " + reset,
    "warning" : bold + rgb(217, 135, 22)  + "WARNING " + reset,
    "error"   : bold + rgb(224, 60, 27)   + "ERROR   " + reset,
    "critical": bold + rgb(255, 0, 0)     + "CRITICAL" + reset,
    "debug"   : bold + rgb(21, 122, 230)  + "DEBUG   " + reset
}

class Logger:
    """
    A simple logger class.
    
    Example:
    ```py
    from logger import Logger

    logging = Logger("My Program", log_level=5)
    logging.info("Hello World")
    ```
    
    #### Log Levels:
    `0` - nothing

    `1` - info
    
    `2` - warning
    
    `3` - error
    
    `4` - critical
    
    `5` - debug
    """

    def __init__(
        self,
        name: str = "[INFINITE CRAFT]",
        *,
        prefix: Callable[[str], str] | None = None,
        log_level: int = 4,
        name_color: str = NAME_COLOR,
        timestamp_color: str = bold + black,
        message_color: str = "",
        time_format: str = LOGGER_TIME_FORMAT,
        log_types_text: dict[str, str] = LOG_TYPES_TEXT
    ) -> None:
        self.name = str(name)
        self.prefix = prefix
        self.log_level = log_level
        self.name_color = name_color
        self.timestamp_color = timestamp_color
        self.message_color = message_color
        self.time_format = time_format
        self.log_types_text = log_types_text

        if self.prefix is None:
            self.prefix = self._prefix_handler

    def log(self, log_type: Literal["info", "warning", "error", "critical", "debug"], message: Any) -> None:
        if log_type == "info":
            log_level = 1
        elif log_type == "warning":
            log_level = 2
        elif log_type == "error":
            log_level = 3
        elif log_type == "critical":
            log_level = 4
        else:
            log_level = 5

        if log_level <= self.log_level:
            prefix = str(self.prefix(log_type)) if self.prefix is not None else ""
            print(prefix + message, end=reset+"\n", flush=True)
    
    def info(self, message: str | Any) -> None:
        self.log("info", message)
    
    def warn(self, message: str | Any) -> None:
        self.warning(message)
    
    def warning(self, message: str | Any) -> None:
        self.log("warning", message)
    
    def err(self, message: str | Any, exc_info: Exception | None = None) -> None:
        self.error(message, exc_info)
    
    def error(self, message: str | Any, exc_info: Exception | None = None) -> None:
        if exc_info:
            message += "\n" + red + "".join(traceback.format_exception(exc_info)).rstrip("\n")
        
        self.log("error", message)
    
    def critical(self, message: str | Any, exc_info: Exception | None = None) -> None:
        if exc_info:
            message += "\n" + red + "".join(traceback.format_exception(exc_info)).rstrip("\n")
        
        self.log("critical", message)
    
    def debug(self, message: str | Any) -> None:
        self.log("debug", message)
    
    def _prefix_handler(self, log_type: str) -> str:
        return f"{reset}{self.timestamp_color}{datetime.now().strftime(self.time_format)}{reset} {self.log_types_text.get(log_type, '')}{reset} {self.name_color}{self.name}{reset} {self.message_color}"