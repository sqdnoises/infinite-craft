import os
import argparse

from . import (
    __license__,
    __copyright__,
    __version__,
    InfiniteCraft,
)

# TODO: implement in future
# if os.name == "nt":
#     try:
#         from pyreadline3 import Readline
#     except ModuleNotFoundError:
#         print("Please install Windows dependencies by running:")
#         print(f"pip install {__title__}[windows]")
#         sys.exit()
#     else:
#         readline = Readline()
# else:
#     import readline

library, _, _ = __name__.partition(".")
version = f"{library} {__version__}"


def main(args: argparse.Namespace) -> None:
    if args.version:
        print(version)
    elif args.information:
        print(
            f"{version}\n"
            f"{__copyright__}\n"
            f"License: {__license__}\n"
            "For more information, see: https://github.com/sqdnoises/infinite-craft#license\n"
            "\n"
            "Need help?\n"
            "Join our coummunity server! https://discord.gg/EPr4T2F8bq\n"
            "\n"
            "Play Infinite Craft by Neal Agarwal on your browser -> https://neal.fun/infinite-craft/"
        )
    else:
        parser.print_usage()


def reset_subcommand(args: argparse.Namespace) -> None:
    discoveries_storage = os.path.expandvars(os.path.expanduser(args.discoveries))
    if not os.path.exists(discoveries_storage):
        parser.error(f"File '{discoveries_storage}' not found")

    InfiniteCraft.reset(discoveries_storage=discoveries_storage)
    print(f'"{discoveries_storage}" file contents reset successfully.')


parser = argparse.ArgumentParser(
    prog=library,
    description=(
        f"{version}\n"
        f"{__copyright__}\n"
        f"License: {__license__}\n"
        "For more information, see: https://github.com/sqdnoises/infinite-craft#license\n"
        "\n"
        "Need help?\n"
        "Join our coummunity server! https://discord.gg/EPr4T2F8bq\n"
        "\n"
        "Play Infinite Craft by Neal Agarwal on your browser -> https://neal.fun/infinite-craft/"
    ),
    allow_abbrev=False,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

parser.add_argument(
    "-V", "--version", action="store_true", help="display the version and exit"
)

parser.add_argument(
    "-I",
    "--information",
    action="store_true",
    help="display program information and exit",
)

parser.set_defaults(func=main)
subparser = parser.add_subparsers(help="subcommands")

reset = subparser.add_parser(
    "reset", prog="reset", description="reset discoveries file", allow_abbrev=False
)

reset.add_argument(
    "-d",
    "--discoveries",
    action="store",
    type=str,
    help="Path to discoveries.json file (default: discoveries.json)",
    default="discoveries.json",
)

reset.set_defaults(func=reset_subcommand)


def parse() -> None:
    args = parser.parse_args()
    args.func(args)
