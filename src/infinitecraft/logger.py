from datetime import datetime
from typing import Callable, Any, Literal


__all__ = (
    "Logger",
)


class Logger:
    """
    #### Log Levels:
    `0` - nothing

    `1` - info
    
    `2` - warn
    
    `3` - error
    
    `4` - fatal
    
    `5` - debug
    """

    def __init__(self, prefix: Callable = None, log_level: int = 4) -> None:
        self._prefix = prefix
        self.log_level = log_level

        if self._prefix is None:
            self._prefix = self._prefix_handler

    def log(self, log_type: Literal["info", "warn", "error", "fatal", "debug"], message: Any) -> None:
        if log_type == "info":
            log_level = 1
        elif log_type == "warn":
            log_level = 2
        elif log_type == "error":
            log_level = 3
        elif log_type == "fatal":
            log_level = 4
        else:
            log_level = 5

        if log_level <= self.log_level:
            prefix = str(self._prefix(log_type))
            print(prefix + message, end="\033[0m\n")
    
    def info(self, message) -> None:
        self.log("info", message)
    
    def warn(self, message) -> None:
        self.log("warn", message)
    
    def error(self, message) -> None:
        self.log("error", message)
    
    def fatal(self, message) -> None:
        self.log("fatal", message)
    
    def debug(self, message) -> None:
        self.log("debug", message)
    
    @staticmethod
    def _prefix_handler(log_type: str) -> str:
        return f"{datetime.now()} [INFINITE CRAFT] " + "{:<5}".format(log_type.upper()) + " "