"""
ANSI codes are a bit weird to decipher if you're unfamiliar with them, so here's a refresher:

It starts off with a format like `\\033[XXXm` where `XXX` is a semicolon separated list of commands.

Widely used formatting:
- `0` means reset
- `1` means **bold**
- `2` means 𝕕𝕚𝕞 (or faint)
- `3` means *italic*
- `4` means <u>underline</u>
- `9` means ~~strikethrough~~

Pre-defined colors:
- `30-37` are black, red, green, yellow, blue, magenta, cyan and white in that order
- `40-47` are the same except for the background
- `90-97` are the same but "bright" foreground
- `100-107` are the same as the bright ones but for the background

Another way of writing `\\033` would be `\\x1b`.
"""

__all__ = (
    # Format resetting
    "reset",
    "default",
    "bg_default",
    # Formatting
    "bold",
    "dim",
    "faint",
    "italic",
    "underline",
    "overline",
    "strikethrough",
    "hide",
    "conceal",
    "reverse",
    "invert",
    "inverse",
    "hyperlink",
    # Turn off formatting
    "bold_off",
    "dim_off",
    "faint_off",
    "italic_off",
    "underline_off",
    "overline_off",
    "strikethrough_off",
    "reveal",
    "hide_off",
    "conceal_off",
    "reverse_off",
    "invert_off",
    "inverse_off",
    # Miscellaneous
    "empty",
    # Custom
    "ansi",
    "rgb",
    "hex",
    "bg_rgb",
    "bg_hex",
    # Custom Predefined Colors
    "orange",
    "dark_orange",
    # Custom Background Colors
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


orange = rgb(255, 128, 0)
dark_orange = rgb(128, 64, 0)

bg_orange = bg_rgb(255, 128, 0)
bg_dark_orange = bg_rgb(128, 64, 0)

empty = ""
reset = ansi(0)
default = ansi(39)
bg_default = ansi(49)

bold = ansi(1)
dim = faint = ansi(2)
italic = ansi(3)
underline = ansi(4)
overline = ansi(53)
strikethrough = ansi(9)
hide = conceal = ansi(8)
reverse = invert = inverse = ansi(7)


def hyperlink(text: str, url: str) -> str:
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"


bold_off = ansi(22)
dim_off = faint_off = ansi(22)
italic_off = ansi(23)
underline_off = ansi(24)
overline_off = ansi(55)
strikethrough_off = ansi(29)
reveal = hide_off = conceal_off = ansi(28)
reverse_off = invert_off = inverse_off = ansi(27)

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

if __name__ == "__main__":
    from sys import argv
    from typing import Any

    def block(text: str, bg_color: str | None = None, padding: int | None = 2) -> str:
        if padding is not None:
            text = (pad := padding * " ") + text + pad

        return f"{bg_color or ''}{text}{reset}"

    def bprint(text: Any, padding: int = 2) -> None:
        print((" " * padding) + str(text), end="", flush=True)

    def print_rgb_gradient(cols: int, rows: int) -> None:
        def generate_gradient(
            c1: tuple[int, int, int], c2: tuple[int, int, int], *, steps: int = 50
        ) -> list[tuple[int, int, int]]:
            gradient: list[tuple[int, int, int]] = []
            for i in range(steps):
                ratio = i / (steps - 1)
                r = int(c1[0] + (c2[0] - c1[0]) * ratio)
                g = int(c1[1] + (c2[1] - c1[1]) * ratio)
                b = int(c1[2] + (c2[2] - c1[2]) * ratio)
                gradient.append((r, g, b))
            return gradient

        # Colors: red, yellow, green, aqua, blue, magenta, red.
        colors = [
            (255, 0, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 255, 255),
            (0, 0, 255),
            (255, 0, 255),
            (255, 0, 0),
        ]

        # Create one continuous diagonal gradient
        big_gradient: list[tuple[int, int, int]] = []
        for i in range(len(colors) - 1):
            segment = generate_gradient(colors[i], colors[i + 1])
            if i < len(colors) - 2:
                big_gradient.extend(segment[:-1])
            else:
                big_gradient.extend(segment)

        max_sum = (cols - 1) + (rows - 1)

        for row in range(rows):
            for col in range(cols):
                ratio = (col + row) / max_sum
                index = int(ratio * (len(big_gradient) - 1))
                r, g, b = big_gradient[index]
                bprint(block(" ", bg_rgb(r, g, b), 0), 0)
            print()

    dark = rgb(24, 24, 24)
    bg_dark = bg_rgb(24, 24, 24)

    print(
        f"""ANSI codes are a bit weird to decipher if you're unfamiliar with them, so here's a refresher:

It starts off with a format like {yellow}\\033[{green}XXX{yellow}m{reset} where {green}XXX{reset} is a semicolon separated list of commands.

Widely used formatting:
 {bold}{blue}0{reset}: {magenta}reset{reset}
 {bold}{blue}1{reset}: {magenta}{bold}bold{reset}
 {bold}{blue}2{reset}: {magenta}{dim}dim{reset} (or faint)
 {bold}{blue}3{reset}: {magenta}{italic}italic{reset}
 {bold}{blue}4{reset}: {magenta}{underline}underline{reset}
 {bold}{blue}9{reset}: {magenta}{strikethrough}strikethrough{reset}

Pre-defined colors:
 {bold}{red}30-37{reset}: {black}black{reset}, {red}red{reset}, {green}green{reset}, {yellow}yellow{reset}, {blue}blue{reset}, {magenta}magenta{reset}, {cyan}cyan{reset} and {white}white{reset}
 {bold}{red}40-47{reset}: {bg_black}black{reset}, {bg_red}red{reset}, {bg_green}green{reset}, {bg_yellow}yellow{reset}, {bg_blue}blue{reset}, {bg_magenta}magenta{reset}, {bg_cyan}cyan{reset} and {bg_white}white{reset}
 {bold}{red}90-97{reset}: {bright_black}black{reset}, {bright_red}red{reset}, {bright_green}green{reset}, {bright_yellow}yellow{reset}, {bright_blue}blue{reset}, {bright_magenta}magenta{reset}, {bright_cyan}cyan{reset} and {bright_white}white{reset}
 {bold}{red}100-107{reset}: {bg_bright_black}black{reset}, {bg_bright_red}red{reset}, {bg_bright_green}green{reset}, {bg_bright_yellow}yellow{reset}, {bg_bright_blue}blue{reset}, {bg_bright_magenta}magenta{reset}, {bg_bright_cyan}cyan{reset} and {bg_bright_white}white{reset}

Another way of writing {yellow}\\033{reset} would be {yellow}\\x1b{reset}.

To print those colors using {bold}{blue}echo{reset} in bash, use:
{bold}{blue}echo{reset} {green}-e {magenta}"{yellow}\\033[1m\\033[34m{bright_magenta}bold blue text{magenta}"{reset}
To print RGB colors using {bold}{blue}echo{reset} in bash, use:
{bold}{blue}echo{reset} {green}-e {magenta}"{yellow}\\033[38;2;{red}r{yellow};{green}g{yellow};{blue}b{yellow}m{bright_magenta}some text{magenta}"{reset}"""
    )
    print()

    print(
        f"{bold}Formatters:{reset} {dim}(x name/y) where x is on code and y is off code{reset}"
    )
    print()
    bprint(block("0 reset", bg_dark))
    bprint(block("39 default", bg_dark))
    bprint(block("49 bg_default", bg_dark))
    print()
    print()
    bprint(block("1 bold/22", bold + blue + bg_dark))
    bprint(block("2 dim/22", dim + blue + bg_dark))
    bprint(block("3 italic/23", italic + blue + bg_dark))
    bprint(block("4 underline/24", underline + blue + bg_dark))
    print()
    print()
    bprint(block("7 invert/27", invert + blue + bg_dark))
    bprint(block("9 strikethrough/29", strikethrough + blue + bg_dark))
    bprint(block("53 overline/55", overline + blue + bg_dark))
    print()
    print()

    print(
        f"{bold}Colors:{reset} {dim}(x/y) where x is foreground color code and y is background color code{reset}"
    )
    print()
    bprint(block("normal", underline + bg_dark))
    for i in range(0, 8):
        bprint(block(f" 3{i}/4{i}", underline + ansi(40 + i)))
    print()
    bprint(block("bright", bg_dark))
    for i in range(0, 8):
        bprint(block(f"9{i}/10{i}", ansi(100 + i)))
    print()
    print()

    if len(argv) > 1:
        print(f"{bold}RGB Rainbow gradient test:{reset} {dim}(32x10){reset}")
        print()
        print_rgb_gradient(32, 10)
        print()
        for i in range(40, 48):
            bprint(block("    ", ansi(i), 0), 0)
        print(reset)
        for i in range(100, 108):
            bprint(block("    ", ansi(i), 0), 0)
        print(reset)
        print()
