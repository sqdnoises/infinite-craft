---
description: Here's a few examples to get started with infinite-craft.
---

# 🍀 Code Examples

The infinite-craft library's module is named `infinitecraft`.

You can import the `InfiniteCraft` class to deal with the game.

```python
from infinitecraft import InfiniteCraft
```

***

## Using InfiniteCraft

There's multiple ways to use the `InfiniteCraft` class.

The main way would be using the `async with` keyword but for larger applications we recommend to use the `InfiniteCraft.start()` and `InfiniteCraft.close()` functions to control your session instead.

Intialising the `InfiniteCraft` class will make a [`discoveries.json`](#user-content-fn-1)[^1] file.

### Using `async with`

We can use `async with` to automatically start and close our sessions. This is useful for small one file projects.

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

Manually controlling basically means using the `start()` and `stop()` functions from `InfiniteCraft` to manually control the session. This is useful when using bigger multiple file projects.

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

#### Using `async with` while manually controlling

Using `async with` while manually controlling is possible, but you have to pass in an extra argument `manual_control=True` so the session does not try to start and close automatically when using `async with`. This is just personal preference for some people who'd like to use infinite-craft library this way.

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

## Pinging the API

You can use the `ping()` function from `InfiniteCraft` to ping the API during a session.

```py
import asyncio
from infinitecraft import InfiniteCraft

async def main():
    async with InfiniteCraft() as game:
        ping = await game.ping() # return type: `float` in seconds
        print(f"Ping: {round(ping * 1000)} ms") # turn into milliseconds and round

asyncio.run(main())
```

## List discovered elements

You can use `game.discoveries` to list currently discovered elements.

```python
import random
import asyncio
from infinitecraft import InfiniteCraft, Element

async def main():
    async with InfiniteCraft() as game:
        for element in game.discoveries:
            print(element)

asyncio.run(main())
```

### Get a discovery

You can get a discovery using the `get_discovery()` function.

```python
import random
import asyncio
from infinitecraft import InfiniteCraft, Element

async def main():
    async with InfiniteCraft() as game:
        element = game.get_discovery("Fire")
        print(element) # 🔥 Fire

asyncio.run(main())
```

{% hint style="info" %}
Please note that the element name is [**case-sensitive**](#user-content-fn-2)[^2].
{% endhint %}

### Fetch all discoveries

You can fetch all discoveries straight from the `discoveries.json` file using `get_discoveries()`.

```python
import random
import asyncio
from infinitecraft import InfiniteCraft, Element

async def main():
    async with InfiniteCraft() as game:
        elements = game.get_discoveries() # returns a 'list'
        print(elements)

asyncio.run(main())
```

### Fetch and save

While fetching the discoveries, you can choose to update the `game.discoveries` attribute as well. Useful for when you make your own changes to the `discoveries.json` file and want to sync it with the current session.

You can pass `set_value=True` to achieve this behaviour.

```python
import random
import asyncio
from infinitecraft import InfiniteCraft, Element

async def main():
    async with InfiniteCraft() as game:
        elements = game.get_discoveries(set_value=True) # returns a 'list'
        print(elements == game.discoveries) # True

asyncio.run(main())
```

### Fetch with a check

While fetching discoveries, you can also choose to use a check to fetch them aswell. Specify the check by using the [`check=callable` argument](#user-content-fn-3)[^3].

```python
import random
import asyncio
from infinitecraft import InfiniteCraft, Element

async def main():
    async with InfiniteCraft() as game:
        elements = game.get_discoveries(set_value=True,
                                        check=lambda e: e.name.startswith("F")) # returns a 'list'
        print(elements) # [Element(name='Fire', emoji='🔥', is_first_discovery=False)]

asyncio.run(main())
```

{% hint style="info" %}
You can also use `set_value=True` with this. This can make it so only items your check approves would be set in `game.discoveries`.
{% endhint %}

## Pairing two elements

You can use the `ping()` function from `InfiniteCraft` to pair two elements together.

Pairing automatically saves the newly paired element in `game.discoveries`.

```py
import random
import asyncio
from infinitecraft import InfiniteCraft, Element

async def main():
    async with InfiniteCraft() as game:
        first = random.choice(game.discoveries)
        second = random.choice(game.discoveries)
        
        print(f"Pairing elements: {first} and {second}")
        result = await game.pair(first, second) # pair the two elements
        print(f"Result: {result}")

asyncio.run(main())z
```

### Pair without saving

You can also pair elements without saving them in `game.discoveries` by specifying `store=False`.

```py
import asyncio
from infinitecraft import InfiniteCraft, Element

async def main():
    async with InfiniteCraft() as game:
        first = Element("Shawarma") # Emoji is not fetched, you must specify it with emoji=""
        second = Element("Chicken")
        
        print(f"Pairing elements: {first} and {second}")
        result = await game.pair(first, second, store=False) # Pair Shawarma and Chicken
        print(f"Result: {result}")

asyncio.run(main())
```

### Pair undiscovered elements

You can create your own elements by making an `Element` object and passing it in `pair()`.

```py
import asyncio
from infinitecraft import InfiniteCraft, Element

async def main():
    async with InfiniteCraft() as game:
        first = Element("Shawarma") # Emoji is not fetched, you must specify it with emoji=""
        second = Element("Chicken")
        
        print(f"Pairing elements: {first} and {second}")
        result = await game.pair(first, second, store=False) # Pair Shawarma and Chicken
        print(f"Result: {result}")

asyncio.run(main())
```

[^1]: This file contains all discovered elements in a neatly-indented JSON file.

[^2]: Which means if you had used `"fire"` instead of `"Fire"` the function would return `None` because it could not find an element named `"fire"`.

[^3]: Where `callable` is a callable function.
