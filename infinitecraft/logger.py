from datetime import datetime
from typing import Callable, Any, Literal


__all__ = (
    "Logger",
)


color_log_types = {
    "info":  "\033[38;2;208;209;192m",
    "warn":  "\033[38;2;217;135;22m",
    "error": "\033[38;2;224;60;27m",
    "fatal": "\033[38;2;255;0;0m",
    "debug": "\033[38;2;21;122;230m"
}


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

    def __init__(self, prefix: Callable[[str], str] | None = None, log_level: int = 4, color_log_types: dict[str, str] = color_log_types) -> None:
        self._prefix = prefix
        self.log_level = log_level
        self._log_colors = color_log_types

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
            prefix = str(self._prefix(log_type)) # type: ignore
            print(prefix + message, end="\033[0m\n")
    
    def info(self, message: str | Any) -> None:
        self.log("info", message)
    
    def warn(self, message: str | Any) -> None:
        self.log("warn", message)
    
    def error(self, message: str | Any) -> None:
        self.log("error", message)
    
    def fatal(self, message: str | Any) -> None:
        self.log("fatal", message)
    
    def debug(self, message: str | Any) -> None:
        self.log("debug", message)
    
    def _prefix_handler(self, log_type: str) -> str:
        return f"\033[38;2;88;92;89m{datetime.now()}\033[0m \033[38;2;222;235;47m[INFINITE CRAFT]\033[0m " + self._log_colors.get(log_type, "\033[0m") + "{:<5}".format(log_type.upper()) + "\033[0m "
        #       "0000-00-00 00:00:00.000000                 [INFINITE CRAFT]                                 INFO/WARN/ERROR/FATAL/DEBUG                                                    Message"