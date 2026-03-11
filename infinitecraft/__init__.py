"""
An API Wrapper for Neal's Infinite Craft game in Python.
Copyright 2024-present SqdNoises
License: MIT
To view the full license, visit https://github.com/sqdnoises/infinite-craft#license

Need help with something?
Join our Discord server -> https://discord.gg/EPr4T2F8bq

Play Infinite Craft by Neal Agarwal on your browser -> https://neal.fun/infinite-craft/
"""

__author__ = "SqdNoises"
__license__ = "MIT"
__copyright__ = "Copyright 2024-present SqdNoises"
__version__ = "1.3.0a"

from typing import NamedTuple, Literal

from .element import *
from .errors import *
from .infinitecraft import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info = VersionInfo(major=1, minor=3, micro=0, releaselevel="alpha", serial=0)
