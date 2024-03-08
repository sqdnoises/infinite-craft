# infinite-craft `0.2.5`
[![](https://img.shields.io/badge/infinite--craft_version-0.2.5-red)](https://github.com/sqdnoises/infinite-craft)
[![](https://img.shields.io/pypi/v/infinite-craft.svg)](#coughs)
[![](https://img.shields.io/badge/License-MIT-red?labelColor=black)](LICENSE)
[![](https://img.shields.io/badge/Python_Version-3.10_|_3.11_|_3.12-blue)](https://python.org)
\
[![](https://github.com/sqdnoises/infinite-craft/actions/workflows/pytest.yml/badge.svg)](https://github.com/sqdnoises/infinite-craft/actions/workflows/pytest.yml)
[![](https://github.com/sqdnoises/infinite-craft/actions/workflows/publish-package-to-pypi.yml/badge.svg)](https://github.com/sqdnoises/infinite-craft/actions/workflows/publish-package-to-pypi.yml)
\
An API Wrapper of Neal's Infinite Craft game in Python for people to implement in their programs.

# Key Features:
- Stores elements in a neatly indented JSON file
- Starts with the four main elements: Water, Fire, Wind, Earth
- Uses [`neal.fun`](https://neal.fun/)'s [Infinite Craft](https://neal.fun/infinite-craft/) API to pair elements together
- Built-in ratelimiting handler
- Custom API support
- Asynchronous library
- Conveniently access discovered elements

# Table of Contents:
- **[Key Features](#key-features)**
- **[Installation](#installation)**
  - **[Dev requirements](#dev-requirements)**
- **[Usage Examples](#usage-examples)**
  - **[CLI](#cli)**
- **[How does it work?](#how-does-it-work)**
- **[To-do](#to-do)**
- **[Documentation](#documentation)**
- **[License](#license)**

# Installation
Requires **Python 3.10** or above.\
To install, run:
```
pip install infinite-craft
```

To update, run:
```
pip install -U infinite-craft
```

**NOTE:** If `pip` is not on PATH, you can use `python3 -m pip` (for Linux/MacOS) or `python -m pip` (for Windows) instead.

### Dev requirements
To install the dev requirements too, either clone this repo and install requirements:
```
git clone https://github.com/sqdnoises/infinite-craft
pip install -r requirements.txt
```
or you can install the extra `dev`:
```
pip install infinite-craft[dev]
```
Recommended to use a virtual environment (`venv`) while using dev requirements.

# Usage Examples
By using `async with`
```py
import asyncio
from infinitecraft import InfiniteCraft

async def main():
    async with InfiniteCraft() as game: # automatically start session and end session on async with end
        print(f"Pairing elements: {game.discoveries[0]} and {game.discoveries[1]}")
        result = await game.pair(game.discoveries[0], game.discoveries[1]) # Pair Water and Fire
        print(f"Result: {result}")

asyncio.run(main())
```

Another `async with` example with manual session control
```py
import asyncio
from infinitecraft import InfiniteCraft

game = InfiniteCraft(manual_control=True) # control start and stop of session automatically

async def main():
    await game.start() # Start InfiniteCraft Session
    
    async with game:
        print(f"Pairing elements: {game.discoveries[0]} and {game.discoveries[1]}")
        result = await game.pair(game.discoveries[0], game.discoveries[1]) # Pair Water and Fire
        print(f"Result: {result}")

    await game.close() # Close InfiniteCraft Session

asyncio.run(main())
```

Example that is basically like manual control except we don't need to use `async with` control
```py
import asyncio
from infinitecraft import InfiniteCraft

game = InfiniteCraft()

async def main():
    await game.start() # Start InfiniteCraft Session
    
    print(f"Pairing elements: {game.discoveries[0]} and {game.discoveries[1]}")
    result = await game.pair(game.discoveries[0], game.discoveries[1]) # Pair Water and Fire
    print(f"Result: {result}")

    await game.close() # Close InfiniteCraft Session

asyncio.run(main())
```

Example that pings the API to check its latency
```py
import asyncio
from infinitecraft import InfiniteCraft

async def main():
    async with InfiniteCraft() as game:
        ping = await game.ping() # return type: `float` in seconds
        print(f"Ping: {round(ping * 1000)} ms") # turn into milliseconds and round

asyncio.run(main())
```

Example that pairs two user-defined elements and doesn't store the result in `game.discoveries`
```py
import asyncio
from infinitecraft import InfiniteCraft, Element

async def main():
    async with InfiniteCraft() as game:
        first = Element("Shawarma") # Emoji is not fetched, you must specify it with emoji=""
        second = Element("Chicken")
        
        print(f"Pairing elements: {first} and {second}")
        result = await game.pair(first, second) # Pair Shawarma and Chicken
        print(f"Result: {result}")

asyncio.run(main())
```

## CLI
By default, two CLI apps are also installed. `infinite-craft` and `infinitecraft`.\
You can use either, both do the exact same thing.

Display help:
```
infinite-craft -h
```

Reset your discoveries JSON file to the initial 4 elements
```
infinite-craft reset -d "/path/to/discoveries.json"
```

**NOTE:** If `infinite-craft` or `infinitecraft` are not on PATH, you can use `python3 -m infinite-craft` or `python3 -m infinitecraft` (Linux/MacOS) or `python3 -m infinite-craft` or `python3 -m infinitecraft` (Windows) instead.

# How does it work?
This library basically contacts the URL: https://neal.fun/api/infinite-craft/pair?first=element+name&second=element+name \
tricks it with some headers, and handles everything accordingly. Everything is handled in a user-friendly manner and asynchronously, so it should be really easy to use it in your programs.

# To-do
- [x] Release version 1.0.0 on PyPI
- [ ] Make a discord server for support
- [ ] Add a runnable and configurable CLI mock API server
- [ ] Make a playable Infinite Craft CLI game (interactive, probably)

# Documentation
Documentation coming soon
However everything is documented well in the code, you can check the below section to see how to install this in-development library.\
**Warning:** Might be unstable especially if the builds (Library Tests) are failing.

## *coughs*
Sorry, the library is still in beta. Once v1.0.0 comes out, the library will be released to [PyPI](https://pypi.org/).

Butttt if you still wanna use the in-dev version of this library, you can install it by doing (must have `git` installed):
```
pip install git+https://github.com/sqdnoises/infinite-craft.git
```
**Warning:** This library might be unstable especially if the builds (Library Tests) are failing.

<div align="center">

# License
[![](https://img.shields.io/badge/LICENSE-MIT-red?style=for-the-badge&labelColor=black)](LICENSE)\
View the **[MIT License](LICENSE)** license that comes with this library.

</div>

---

<div align="center">

### 🌟 Please star the repo and show some love 💖

</div>
