"""
ANSI codes are a bit weird to decipher if you're unfamiliar with them, so here's a refresher

It starts off with a format like `\\033[XXXm` where `XXX` is a semicolon separated list of commands

The important ones here relate to colour.

`30-37` are black, red, green, yellow, blue, magenta, cyan and white in that order

`40-47` are the same except for the background

`90-97` are the same but "bright" foreground

`100-107` are the same as the bright ones but for the background.

`0` means reset, `1` means bold, `2` means dim, `3` means italic, `4` means underline and `9` means strikethrough.

Another way of writing `\\033` would be `\\x1b`.
"""

# ANSI codes are a bit weird to decipher if you're unfamiliar with them, so here's a refresher
# It starts off with a format like \033[XXXm where XXX is a semicolon separated list of commands
# The important ones here relate to colour.
# 30-37 are black, red, green, yellow, blue, magenta, cyan and white in that order
# 40-47 are the same except for the background
# 90-97 are the same but "bright" foreground
# 100-107 are the same as the bright ones but for the background.
# 0 means reset, 1 means bold, 2 means dim, 3 means italic, 4 means underline and 9 means strikethrough.
# Another way of writing \033 would be \x1b.

__all__ = (
    # Formatting
    "reset",
    "bold",
    "dim",
    "italic",
    "underline",
    "strikethrough",
    
    # Miscellaneous
    "empty",
    
    # Custom Colors
    "lime",
    "orange",
    "dark_orange",
    
    # Custom Background Colors
    "bg_lime",
    "bg_orange",
    "bg_dark_orange",
    
    # Colors
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    
    # Bright Colors
    "bright_black",
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "bright_white",
    
    # Background Colors
    "bg_black",
    "bg_red",
    "bg_green",
    "bg_yellow",
    "bg_blue",
    "bg_magenta",
    "bg_cyan",
    "bg_white",
    
    # Bright Background Colors
    "bg_bright_black",
    "bg_bright_red",
    "bg_bright_green",
    "bg_bright_yellow",
    "bg_bright_blue",
    "bg_bright_magenta",
    "bg_bright_cyan",
    "bg_bright_white",
)

def ansi(code: int) -> str:
    return f"\033[{code}m"

def rgb(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"

def hex(hex: int) -> str:
    r = hex >> 16
    g = hex >> 8 & 0xFF
    b = hex & 0xFF
    return rgb(r, g, b)

def bg_rgb(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"

def bg_hex(hex: int) -> str:
    r = hex >> 16
    g = hex >> 8 & 0xFF
    b = hex & 0xFF
    return bg_rgb(r, g, b)

lime = rgb(0, 255, 128)
orange = rgb(255, 128, 0)
dark_orange = rgb(128, 64, 0)

bg_lime = bg_rgb(0, 255, 128)
bg_orange = bg_rgb(255, 128, 0)
bg_dark_orange = bg_rgb(128, 64, 0)

empty = ""
reset = ansi(0)
bold = ansi(1)
dim = ansi(2)
italic = ansi(3)
underline = ansi(4)
strikethrough = ansi(9)

black = ansi(30)
red = ansi(31)
green = ansi(32)
yellow = ansi(33)
blue = ansi(34)
magenta = ansi(35)
cyan = ansi(36)
white = ansi(37)

bright_black = ansi(90)
bright_red = ansi(91)
bright_green = ansi(92)
bright_yellow = ansi(93)
bright_blue = ansi(94)
bright_magenta = ansi(95)
bright_cyan = ansi(96)
bright_white = ansi(97)

bg_black = ansi(40)
bg_red = ansi(41)
bg_green = ansi(42)
bg_yellow = ansi(43)
bg_blue = ansi(44)
bg_magenta = ansi(45)
bg_cyan = ansi(46)
bg_white = ansi(47)

bg_bright_black = ansi(100)
bg_bright_red = ansi(101)
bg_bright_green = ansi(102)
bg_bright_yellow = ansi(103)
bg_bright_blue = ansi(104)
bg_bright_magenta = ansi(105)
bg_bright_cyan = ansi(106)
bg_bright_white = ansi(107)