import os
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


def main(args: argparse.Namespace) -> None:
    if args.version:
        print(__display_version__)
    
    elif args.information:
        print(__display_version__)
        print(__copyright__)
        print("License: " + __license__)
        print()
        print("This program comes with ABSOLUTELY NO WARRANTY.")
        print("This is free software, and you are welcome to redistribute it")
        print("under certain conditions.")
        print()
        print(f"For more information, see: {__homepage__}?tab=readme-ov-file#license")
        print("Play Infinite Craft by Neal Agarwal on your browser -> https://neal.fun/infinite-craft/")
    
    else:
        parser.print_usage()


def reset_subcommand(args: argparse.Namespace):
    discoveries_storage = os.path.expandvars(os.path.expanduser(args.discoveries))
    
    if not os.path.exists(discoveries_storage):
        parser.error(f"File '{discoveries_storage}' not found")
        
    InfiniteCraft.reset(discoveries_storage=discoveries_storage)

    print(f'"{discoveries_storage}" file contents reset successfully.')


parser = argparse.ArgumentParser(
    prog = __title__,
    description = f"{__display_version__}\n"
                  f"{__copyright__}\n"
                  f"License: {__license__}"
                   "\n"
                   "This program comes with ABSOLUTELY NO WARRANTY.\n"
                   "This is free software, and you are welcome to redistribute it\n"
                   "under certain conditions.\n"
                   "\n"
                  f"For more information, see: {__homepage__}?tab=readme-ov-file#license",
    allow_abbrev = False,
    formatter_class = argparse.RawDescriptionHelpFormatter
)

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


reset_parser = parser.add_subparsers(
    help = "reset discoveries file",
    metavar = "reset"
)

reset = reset_parser.add_parser(
    "reset",
    prog = "reset",
    description = "reset discoveries file",
    allow_abbrev = False
)

reset.add_argument(
    "-d", "--discoveries",
    action = "store",
    type = str,
    help = "Path to discoveries.json file (default: discoveries.json)",
    default = "discoveries.json"
)

reset.set_defaults(func=reset_subcommand)


def parse():
    args = parser.parse_args()
    args.func(args)