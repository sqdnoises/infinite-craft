"""
This module provides a customizable logger class for handling various log levels 
with optional color formatting and file saving support.

Usage:
    Pre-initialized example:
    ```py
    from logger import logging

    logging.name = "My Program"
    logging.log_level = 5
    logging.info("Hello World")
    ```

    Manual initialization example:
    ```py
    from logger import Logger

    logging = Logger("My Program", log_level=5)
    logging.info("Hello World")
    ```

    Log Levels:
    - 0: No logs
    - 1: Info
    - 2: Warning
    - 3: Error
    - 4: Critical
    - 5: Debug

Copyright (c) 2023-present SqdNoises
"""

import os
import traceback
from datetime import datetime
from typing import (
    Any, Literal,
    Callable
)

from .termcolors import *
from .termcolors import bg_rgb

__all__ = (
    "Logger",
)

LOGGER_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE_NAME_TIME_FORMAT = "%Y-%m-%d %H-%M-%S"
LOG_TYPES_TEXT = {
    "text": {
        "info": "INFO    ",
        "warning": "WARNING ",
        "error": "ERROR   ",
        "critical": "CRITICAL",
        "debug": "DEBUG   "
    },
    "color": {
        "info": bold + blue + "INFO    ",
        "warning": bold + yellow + "WARNING ",
        "error": bold + red + "ERROR   ",
        "critical": bg_rgb(200, 0, 0) + white + "CRITICAL",
        "debug": bold + bg_black + "DEBUG   "
    }
}


class Logger:
    """
    A customizable logger class that supports logging messages with different log levels,
    optional color formatting, and saving to a log file.
    
    Parameters:
    - name (str): Name of the logger (default: BOT_NAME).
    - logs_folder (str | None): Directory to save log files (default: "logs").
    - prefix (Callable[[str], str] | None): Custom prefix function for log messages (default: None).
    - log_level (int): Minimum log level for printing to the console (default: 4).
    - log_file_log_level (int): Minimum log level for saving to a log file (default: 5).
    - name_color (str): Color for the logger name in log messages (default: red).
    - timestamp_color (str): Color for the timestamp in log messages (default: bold + black).
    - message_color (str): Color for the message content (default: "").
    - time_format (str): Format for the log timestamps (default: LOGGER_TIME_FORMAT).
    - log_file_name_time_format (str): Format for log file names (default: LOG_FILE_NAME_TIME_FORMAT).
    - log_types_text (dict): Dictionary containing text and color formats for different log types (default: LOG_TYPES_TEXT).
    
    Example:
    ```py
    from logger import Logger
    
    logging = Logger("My Program", log_level=5)
    logging.info("Hello World")
    ```
    """
    
    def __init__(
        self,
        name: str = "INFINITE CRAFT",
        logs_folder: str | None = "logs",
        *,
        prefix: Callable[[str], str] | None = None,
        log_level: int = 4,
        log_file_log_level: int = 5,
        name_color: str = red,
        timestamp_color: str = bold + black,
        message_color: str = "",
        time_format: str = LOGGER_TIME_FORMAT,
        log_file_name_time_format: str = LOG_FILE_NAME_TIME_FORMAT,
        log_types_text: dict[str, dict[str, str]] = LOG_TYPES_TEXT
    ) -> None:
        """
        Initialize the Logger instance with the specified configuration options.
        """
        self.name = str(name)
        self.logs_folder = logs_folder
        self.log_file = self._get_log_file_path(logs_folder, log_file_name_time_format) if logs_folder else None
        self.prefix = prefix or self._prefix_handler
        self.log_level = log_level
        self.log_file_log_level = log_file_log_level
        self.name_color = name_color
        self.timestamp_color = timestamp_color
        self.message_color = message_color
        self.time_format = time_format
        self.log_file_name_time_format = log_file_name_time_format
        self.log_types_text = log_types_text
    
    def _get_log_file_path(self, logs_folder: str, log_file_name_time_format: str) -> str:
        """
        Generates a log file path with an incremented number if the file already exists.
        
        Parameters:
        - logs_folder (str): Directory to save the log file.
        - log_file_name_time_format (str): Format for log file names.
        
        Returns:
        - str: The path to the log file.
        """
        base_name = f"{self.name} {datetime.now().strftime(log_file_name_time_format)}"
        log_file = os.path.join(logs_folder, f"{base_name}.log")
        counter = 1
        
        while os.path.exists(log_file):
            log_file = os.path.join(logs_folder, f"{base_name} {counter}.log")
            counter += 1
        
        return log_file
    
    def log(
        self,
        log_type: Literal["info", "warning", "error", "critical", "debug"] | int,
        message: Any,
        *,
        do_print: bool = True,
        do_save: bool = True
    ) -> None:
        """
        Logs a message with a given log type and message content.
        
        Parameters:
        - log_type (str or int): Log type (e.g., "info", "warning", "error", "critical", "debug" or corresponding integer).
        - message (Any): Message content to log.
        - do_print (bool): Whether to print the log message to the console (default: True).
        - do_save (bool): Whether to save the log message to the log file (default: True).
        """
        log_level = self._get_log_level(log_type)
        
        # Print log message if the level is less than or equal to current log level
        if do_print and log_level <= self.log_level:
            prefix = str(self.prefix(log_type))  # type: ignore
            print(prefix + str(message), end=reset + "\n", flush=True)
        
        # Save log message to file if applicable
        if do_save and self.log_file and log_level <= self.log_file_log_level:
            prefix = str(self.prefix(log_type, color=False))  # type: ignore
            if self.logs_folder: os.makedirs(self.logs_folder, exist_ok=True)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(prefix + str(message) + "\n")
    
    def _get_log_level(self, log_type: Literal["info", "warning", "error", "critical", "debug"] | int) -> int:
        """Helper method to map log types to log levels."""
        log_level_mapping = {
            "info": 1,
            "warning": 2,
            "error": 3,
            "critical": 4,
            "debug": 5
        }
        if isinstance(log_type, int):
            return log_type
        return log_level_mapping.get(log_type, 5)
    
    def info(self, message: str | Any, *, do_print: bool = True, do_save: bool = True) -> None:
        """
        Logs an info-level message.

        Parameters:
        - message (Any): Message content to log.
        - do_print (bool): Whether to print the log message to the console (default: True).
        - do_save (bool): Whether to save the log message to the log file (default: True).
        """
        self.log("info", message, do_print=do_print, do_save=do_save)
    
    def warn(self, message: str | Any, *, do_print: bool = True, do_save: bool = True) -> None:
        """
        Alias for warning(). Logs a warning-level message.

        Parameters:
        - message (Any): Message content to log.
        - do_print (bool): Whether to print the log message to the console (default: True).
        - do_save (bool): Whether to save the log message to the log file (default: True).
        """
        self.warning(message, do_print=do_print, do_save=do_save)
    
    def warning(self, message: str | Any, *, do_print: bool = True, do_save: bool = True) -> None:
        """
        Logs a warning-level message.

        Parameters:
        - message (Any): Message content to log.
        - do_print (bool): Whether to print the log message to the console (default: True).
        - do_save (bool): Whether to save the log message to the log file (default: True).
        """
        self.log("warning", message, do_print=do_print, do_save=do_save)
    
    def err(self, message: str | Any, exc_info: Exception | None = None, *, do_print: bool = True, do_save: bool = True) -> None:
        """
        Alias for error(). Logs an error-level message with optional exception information.

        Parameters:
        - message (Any): Message content to log.
        - exc_info (Exception | None): Exception information to include in the log (default: None).
        - do_print (bool): Whether to print the log message to the console (default: True).
        - do_save (bool): Whether to save the log message to the log file (default: True).
        """
        self.error(message, exc_info, do_print=do_print, do_save=do_save)
    
    def error(self, message: str | Any, exc_info: Exception | None = None, *, do_print: bool = True, do_save: bool = True) -> None:
        """
        Logs an error-level message with optional exception information.
        
        Parameters:
        - message (Any): Message content to log.
        - exc_info (Exception | None): Exception information to include in the log (default: None).
        - do_print (bool): Whether to print the log message to the console (default: True).
        - do_save (bool): Whether to save the log message to the log file (default: True).
        """
        if exc_info:
            message = f"{message}\n{traceback.format_exc()}"
        self.log("error", message, do_print=do_print, do_save=do_save)
    
    def crit(self, message: str | Any, exc_info: Exception | None = None, *, do_print: bool = True, do_save: bool = True) -> None:
        """
        Alias for critical(). Logs a critical-level message.
        
        Parameters:
        - message (Any): Message content to log.
        - exc_info (Exception | None): Exception information to include in the log (default: None).
        - do_print (bool): Whether to print the log message to the console (default: True).
        - do_save (bool): Whether to save the log message to the log file (default: True).
        """
        self.critical(message, exc_info, do_print=do_print, do_save=do_save)
    
    def critical(self, message: str | Any, exc_info: Exception | None = None, *, do_print: bool = True, do_save: bool = True) -> None:
        """
        Logs a critical-level message.
        
        Parameters:
        - message (Any): Message content to log.
        - exc_info (Exception | None): Exception information to include in the log (default: None).
        - do_print (bool): Whether to print the log message to the console (default: True).
        - do_save (bool): Whether to save the log message to the log file (default: True).
        """
        if exc_info:
            message = f"{message}\n{traceback.format_exc()}"
        self.log("critical", message, do_print=do_print, do_save=do_save)
    
    def debug(self, message: str | Any, *, do_print: bool = True, do_save: bool = True) -> None:
        """
        Logs a debug-level message.

        Parameters:
        - message (Any): Message content to log.
        - do_print (bool): Whether to print the log message to the console (default: True).
        - do_save (bool): Whether to save the log message to the log file (default: True).
        """
        self.log("debug", message, do_print=do_print, do_save=do_save)
    
    def _prefix_handler(self, log_type: Literal["info", "warning", "error", "critical", "debug"], color: bool = True) -> str:
        """
        Generates the log message prefix including the timestamp, logger name, and log type.
        
        Parameters:
        - log_type (str): Log type (e.g., "info", "warning", "error", "critical", "debug").
        - color (bool): Whether to include color formatting in the prefix (default: True).

        Returns:
        - str: The formatted log message prefix.
        """
        if color:
            return f"{reset}{self.timestamp_color}{datetime.now().strftime(self.time_format)}{reset} {self.log_types_text['color'].get(log_type, '')}{reset} {self.name_color}{self.name}{reset} {self.message_color}"
        return f"{datetime.now().strftime(self.time_format)} {self.log_types_text['text'].get(log_type, '')} {self.name} > "

logging = Logger()