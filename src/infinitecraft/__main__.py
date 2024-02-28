import os
import sys
import argparse
from . import (
    __title__,
    __license__,
    __copyright__,
    __cli_description__,
    __display_version__,
    __homepage__,
    InfiniteCraft
)

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


parser = argparse.ArgumentParser(
    prog = __title__,
    description = __cli_description__,
    epilog = f"""subcommands:
  reset  reset discovered and emoji cache json files
""",
    allow_abbrev = False,
    formatter_class = argparse.RawDescriptionHelpFormatter
)
subparser = parser.add_subparsers(help="subcommands")


def main(args: argparse.Namespace) -> None:
    if args.version:
        print(__display_version__)
    
    elif args.information:
        print(__copyright__)
        print(__display_version__)
        print("Play Infinite Craft by Neal Agarwal on your browser -> https://neal.fun/infinite-craft/")
        print("License: " + __license__)
        print()
        print("This program comes with ABSOLUTELY NO WARRANTY.")
        print("This is free software, and you are welcome to redistribute it")
        print("under certain conditions.")
        print()
        print(f"For more information, see: {__homepage__}?tab=readme-ov-file#license""")
    
    else:
        parser.print_usage()


parser.add_argument(
    "-V", "--version",
    action = "store_true",
    help = "display the version and exit"
)
parser.add_argument(
    "-I", "--information",
    action = "store_true",
    help = "display program information and exit"
)
parser.set_defaults(func=main)

def reset_subcommand(args: argparse.Namespace):
    discoveries_storage = os.path.expandvars(os.path.expanduser(args.disocveries))
    emoji_cache = os.path.expandvars(os.path.expanduser(args.emoji_cache))
    
    if not os.path.exists(discoveries_storage):
        parser.error(f"File '{discoveries_storage}' not found")
    
    if not os.path.exists(emoji_cache):
        parser.error(f"File '{emoji_cache}' not found")
    
    InfiniteCraft.reset(
        discoveries_storage=discoveries_storage,
        emoji_cache=emoji_cache
    )

    print(f'"{discoveries_storage}" file contents reset successfully.')
    print(f'"{emoji_cache}" file contents reset successfully.')

reset = subparser.add_parser(
    "reset",
    prog = "reset",
    description = "reset discovered and emoji cache json files",
    allow_abbrev = False
)
reset.add_argument(
    "-d", "--discoveries",
    action = "store",
    type = str,
    help = "Path to discoveries.json file (default: discoveries.json)",
    default = "discoveries.json"
)
reset.add_argument(
    "-e", "--emoji-cache", 
    action = "store",
    type = str,
    help = "Path to emoji_cache.json file (default: emoji_cache.json)",
    default = "emoji_cache.json"
)
reset.set_defaults(func=reset_subcommand)


def parse():
    args = parser.parse_args()
    args.func(args)