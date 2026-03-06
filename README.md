[![](https://github.com/sqdnoises/infinite-craft/raw/main/docs/.gitbook/assets/cover.png)](https://github.com/sqdnoises/infinite-craft)

# infinite-craft
[![](https://img.shields.io/pypi/v/infinite-craft.svg)](https://pypi.org/project/infinite-craft/)
[![](https://img.shields.io/pypi/dm/infinite-craft.svg)](https://pypi.org/project/infinite-craft/)
[![](https://img.shields.io/badge/License-MIT-red?labelColor=black)](LICENSE)
[![](https://img.shields.io/badge/Python_Version-3.10+-blue)](https://python.org)
\
An API Wrapper for Neal's Infinite Craft game in Python.

### `infinite-craft`'s GitHub Actions Status
[![](https://github.com/sqdnoises/infinite-craft/actions/workflows/pytest.yml/badge.svg)](https://github.com/sqdnoises/infinite-craft/actions/workflows/pytest.yml)
[![Publish Package to PyPI](https://github.com/sqdnoises/infinite-craft/actions/workflows/publish-package-to-pypi.yml/badge.svg)](https://github.com/sqdnoises/infinite-craft/actions/workflows/publish-package-to-pypi.yml)
[![Create GitHub Release](https://github.com/sqdnoises/infinite-craft/actions/workflows/create-github-release.yml/badge.svg)](https://github.com/sqdnoises/infinite-craft/actions/workflows/create-github-release.yml)

# Key Features:
- Stores elements in a neatly indented JSON file
- Starts with the four main elements: Water, Fire, Wind, Earth
- Uses [`neal.fun`](https://neal.fun/)'s [Infinite Craft](https://neal.fun/infinite-craft/) API to pair elements together
- Built-in ratelimiting handler
- Custom API support
- Asynchronous library
- Conveniently access discovered elements

# Discord Server
> [!TIP]
> Need help? Join our Discord community!\
» https://discord.gg/FF2fSN2sJd \
[![Discord invite](https://invidget.switchblade.xyz/FF2fSN2sJd)](https://discord.gg/FF2fSN2sJd)

# Table of Contents:
- **[Key Features](#key-features)**
- **[Discord Server](#discord-server)**
- **[Installation](#installation)**
- **[Examples](#examples)**
- **[Documentation](#documentation-)**
- **[How does it work?](#how-does-it-work)**
- **[To-do](#to-do)**
- **[License](#license)**

# Installation
> [!IMPORTANT]
> **Python 3.10** or above is required. Any versions below are not guaranteed to work.

To install or update, run:
```
pip install -U infinite-craft
```

> [!NOTE]
> If `pip` is not on PATH, you can use:
> - `python3 -m pip` (for Linux/MacOS) or
> - `python -m pip` (for Windows) instead.

[**View `infinite-craft` on PyPI.**](https://pypi.org/project/infinite-craft/)

# Examples
### Using `async with`
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

### Manually controlling
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

You can find more examples in the **[documentation](#documentation-)**.

# Documentation 📚
Documentation is still in development.

While the documentation is not ready, everything is documented well in the code with docstrings which you can see in an IDE like Visual Studio Code.

*You can also see the in-development documentation page [here](https://sqdnoises.gitbook.io/infinite-craft).*

# How does it work?
This library contacts the URL:
> https://neal.fun/api/infinite-craft/pair?first=Fire&second=Water

Where `Fire` in `first=` parameter is the first element you want to pair and the `Water` in `second=` parameter is the second element.

Everything is handled in a user-friendly manner and asynchronously, so it should be really easy to use it in your programs.

# To-do
- [x] ~~Release version 1.0.0 on PyPI~~
- [x] ~~Make a discord server for support~~ Join our community! https://discord.gg/FF2fSN2sJd
- [x] ~~Add a runnable and configurable CLI mock API server~~
- [x] ~~Make a documentation page~~
- [x] Fix [403 Forbidden Error](https://github.com/sqdnoises/infinite-craft/issues/2)
- [ ] Finish todos in code
- [ ] Implement better documentation
- [ ] Make a playable & interactive Infinite Craft CLI game

<div align="center">

# License
[![](https://img.shields.io/badge/LICENSE-MIT-red?style=for-the-badge&labelColor=black)](LICENSE)\
Click **[<kbd>MIT License</kbd>](LICENSE)** to view the license that comes with this library.

</div>

---

<div align="center">

### 🌟 Please [star the repo](https://github.com/sqdnoises/infinite-craft/stargazers) and show some love 💖

</div>
