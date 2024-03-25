"""
MIT License

Copyright (c) 2024-present SqdNoises, Neal Agarwal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import argparse

from .      import (
    __title__,
    __license__,
    __copyright__,
    __cli_description__,
    __display_version__,
    __homepage__,
    __discord__,
    InfiniteCraft
)
from .utils import mock_server

# implement in future
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
        print(f"For more information, see: {__homepage__}#license")
        print()
        print("Need help?")
        print(f"Join our coummunity server! {__discord__}")
        print()
        print("Play Infinite Craft by Neal Agarwal on your browser -> https://neal.fun/infinite-craft/")
    
    else:
        parser.print_usage()


def reset_subcommand(args: argparse.Namespace):
    discoveries_storage = os.path.expandvars(os.path.expanduser(args.discoveries))
    
    if not os.path.exists(discoveries_storage):
        parser.error(f"File '{discoveries_storage}' not found")
        
    InfiniteCraft.reset(discoveries_storage=discoveries_storage)

    print(f'"{discoveries_storage}" file contents reset successfully.')


def mock_subcommand(args: argparse.Namespace):
    mock_server(args.host, args.port)


parser = argparse.ArgumentParser(
    prog = __title__,
    description = f"{__display_version__}\n"
                  f"{__copyright__}\n"
                  f"License: {__license__}\n"
                  f"For more information, see: {__homepage__}#license\n"
                   "\n"
                  f"Need help?\n"
                  f"Join our coummunity server! {__discord__}",
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


subparser = parser.add_subparsers(help="subcommands")

reset = subparser.add_parser(
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

mock = subparser.add_parser(
    "mock",
    prog = "mock",
    description = "mock server for testing purposes",
    allow_abbrev = False
)

mock.add_argument(
    "-H", "--host",
    action = "store",
    type = str,
    help = "Hostname to host at",
    default = "127.0.0.1"
)

mock.add_argument(
    "-p", "-P", "--port",
    action = "store",
    type = int,
    help = "Port to host at",
    default = 8080
)

mock.set_defaults(func=mock_subcommand)


def parse():
    args = parser.parse_args()
    args.func(args)