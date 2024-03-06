"""
An API Wrapper of Neal's Infinite Craft game in Python for people to implement in their programs.
Copyright (C) 2024-present SqdNoises
License: GNU Lesser General Public License v3.0
To view the full license, visit https://github.com/sqdnoises/infinite-craft?tab=readme-ov-file#license

Play Infinite Craft by Neal Agarwal on your browser -> https://neal.fun/infinite-craft/
"""

__title__ = "infinite-craft"
__full_title__ = "Infinite Craft"
__description__ = "An API Wrapper of Neal's Infinite Craft game in Python for people to implement in their programs."
__cli_description__ = "Infinite Craft Utilities"
__author__ = "SqdNoises"
__license__ = "GNU Lesser General Public License v3.0 (GNU LGPL-3.0)"
__copyright__ = "Copyright (C) 2024-present SqdNoises, Neal Agarwal"
__homepage__ = "https://github.com/sqdnoises/infinite-craft"
__version__ = "0.2.4"
__display_version__ = __title__ + " " + __version__

from .element import *
from .infinitecraft import *
from .logger import *
from .errors import *