---
layout:
  title:
    visible: false
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: false
---

# 🛠️ InfiniteCraft

## _class_ <mark style="color:yellow;">`InfiniteCraft`</mark>

Initialize an Infinite Craft session.

```python
InfiniteCraft(
    api_url: str                      = "https://neal.fun",
    api_rate_limit: int               = 400,
    manual_control: bool              = False,
    discoveries_storage: str          = "discoveries.json",
    encoding: str                     = "utf-8",
    do_reset: bool                    = False,
    make_file: bool                   = True,
    headers: MutableMapping[str, str] = {},
    element_cls: type[Element]        = Element,
    logger: Any                       = Logger(),
    debug: bool                       = False
)
```

### Attributes

<mark style="color:red;">**`discoveries`**</mark> (<mark style="color:yellow;">**`list`**</mark>**`[`**<mark style="color:yellow;">**`Element`**</mark>**`]`**): List of <mark style="color:yellow;">**`Element`**</mark> objects that have been discovered.

<mark style="color:red;">**`closed`**</mark> (<mark style="color:yellow;">**`bool`**</mark> **`|`** <mark style="color:orange;">**`None`**</mark>): Whether the Infinite Craft session is closed or not.\
<mark style="color:orange;">**`None`**</mark> if session has not been started.

### Arguments

<mark style="color:red;">**`api_url`**</mark> (<mark style="color:yellow;">**`str`**</mark>, optional): The API URL to contact.

> Defaults to <mark style="color:green;">**`"https://neal.fun/api/infinite-craft"`**</mark>

<mark style="color:red;">**`api_rate_limit`**</mark> (<mark style="color:yellow;">**`int`**</mark>, optional): The requests per minute the API can handle before ratelimiting. <mark style="color:orange;">`0`</mark> if you want no ratelimit.\
Must be greater than or equal to <mark style="color:orange;">`0`</mark>.

> Defaults to <mark style="color:orange;">`400`</mark> requests per minute

<mark style="color:red;">**`manual_control`**</mark> (<mark style="color:yellow;">**`bool`**</mark>, optional): Manually control <mark style="color:yellow;">**`InfiniteCraft`**</mark>**`.`**<mark style="color:blue;">**`start`**</mark>**`()`** and <mark style="color:yellow;">**`InfiniteCraft`**</mark>**`.`**<mark style="color:blue;">**`stop`**</mark>**`()`**.\
Useful when using <mark style="color:purple;">**`async with`**</mark> multiple times.

> Defaults to <mark style="color:blue;">`False`</mark>

<mark style="color:red;">**`discoveries_storage`**</mark> (<mark style="color:yellow;">**`str`**</mark>, optional): Path to discoveries storage JSON.

> Defaults to <mark style="color:green;">**`"discoveries.json"`**</mark>

<mark style="color:red;">**`encoding`**</mark> (<mark style="color:yellow;">**`str`**</mark>, optional): Encoding to use while reading or saving json files.

> Defaults to <mark style="color:green;">**`"utf-8"`**</mark>

<mark style="color:red;">**`do_reset`**</mark> (<mark style="color:yellow;">**`bool`**</mark>, optional): Whether to reset the discoveries storage JSON and emoji cache JSON.

> Defaults to <mark style="color:blue;">`False`</mark>

<mark style="color:red;">**`headers`**</mark> (<mark style="color:yellow;">**`dict`**</mark>, optional): Headers to send to the API.

> Defaults to `{}`

<mark style="color:red;">**`element_cls`**</mark> (<mark style="color:yellow;">**`Element`**</mark>, optional): Class to be used for creating elements.\
**NOTE:** Must be a subclass of <mark style="color:yellow;">**`Element`**</mark>.

> Defaults to <mark style="color:yellow;">**`Element`**</mark>

<mark style="color:red;">**`logger`**</mark> (<mark style="color:purple;">**`class`**</mark>, optional): An initialized logger class or module with methods <mark style="color:blue;">**`info`**</mark>, <mark style="color:blue;">**`warn`**</mark>, <mark style="color:blue;">**`error`**</mark>, <mark style="color:blue;">**`fatal`**</mark>, and <mark style="color:blue;">**`debug`**</mark> to use for logging.

> Defaults to a custom logger <mark style="color:yellow;">**`Logger`**</mark>

<mark style="color:red;">**`debug`**</mark> (<mark style="color:yellow;">**`bool`**</mark>, optional): Whether to send debug logs.\
This sets the current <mark style="color:red;">`logger`</mark> to <mark style="color:yellow;">**`Logger`**</mark>**`(`**<mark style="color:red;">`log_level`</mark>**`=`**<mark style="color:orange;">`5`</mark>**`)`**.\
Only works when <mark style="color:yellow;">**`bool`**</mark>**`(`**<mark style="color:red;">`logger`</mark>**`)`** is <mark style="color:blue;">`False`</mark> or when the custom logger is used.

> Defaults to <mark style="color:blue;">`False`</mark>



## _async def_ <mark style="color:blue;">`ping`</mark>`()` -> <mark style="color:yellow;">`float`</mark>

Ping the API with a simple pair request and return the latency.

{% hint style="info" %}
This function only works when the session has been started.
{% endhint %}

### Returns

<mark style="color:yellow;">**`float`**</mark>: The latency in seconds.



## _async def_ <mark style="color:blue;">`start`</mark>`()`

Start the <mark style="color:yellow;">**`InfiniteCraft`**</mark> session.

### Raises

<mark style="color:yellow;">**`RuntimeError`**</mark>: Raises when session is closed or has already started.



## _async def_ <mark style="color:blue;">`close`</mark>`()`

Start the <mark style="color:yellow;">**`InfiniteCraft`**</mark> session.

### Raises

<mark style="color:yellow;">**`RuntimeError`**</mark>: Raises when session has not been started or is already closed.



## _async def_ <mark style="color:blue;">`stop`</mark>`()`

Alias for [<mark style="color:yellow;">**`InfiniteCraft`**</mark>**`.`**<mark style="color:blue;">**`close`**</mark>**`()`**](infinitecraft.md#def-close)



## _async def_ <mark style="color:blue;">`pair`</mark>`()` -> <mark style="color:yellow;">`Element`</mark>

Pair two elements and return the resulting element.

```python
async def pair(
    first: Element,
    second: Element,
    *,
    store: bool = True
) -> Element
```

{% hint style="info" %}
If the elements could not be paired, it would result in an <mark style="color:yellow;">**`Element`**</mark> with all attributes set to <mark style="color:orange;">**`None`**</mark>.\
We can check if all attributes are <mark style="color:orange;">**`None`**</mark> by doing <mark style="color:yellow;">**`bool`**</mark>**`(`**[<mark style="color:red;">**`element`**</mark>](#user-content-fn-1)[^1]**`)`**.\
If it returns <mark style="color:blue;">`False`</mark>, then all attributes are <mark style="color:orange;">**`None`**</mark>.\
Useful in <mark style="color:purple;">**`if`**</mark> statements.
{% endhint %}

### Arguments

<mark style="color:red;">**`first`**</mark> (<mark style="color:yellow;">**`Element`**</mark>): The first element.

<mark style="color:red;">**`second`**</mark> (<mark style="color:yellow;">**`Element`**</mark>): The second element.

> Required.

<mark style="color:red;">**`store`**</mark> (<mark style="color:yellow;">**`bool`**</mark>, optional): Whether to store the result <mark style="color:yellow;">**`Element`**</mark> to <mark style="color:yellow;">**`InfiniteCraft`**</mark>**`.`**<mark style="color:red;">**`discoveries`**</mark>.

> Defaults to <mark style="color:blue;">`True`</mark>.

### Raises

<mark style="color:yellow;">**`TypeError`**</mark>: If <mark style="color:red;">**`first`**</mark> or <mark style="color:red;">**`second`**</mark> is not an instance of <mark style="color:yellow;">**`Element`**</mark>.

### Returns

<mark style="color:yellow;">**`Element`**</mark>: The resulting element as an <mark style="color:yellow;">**`Element`**</mark> object or an <mark style="color:yellow;">**`Element`**</mark> with all attributes as <mark style="color:orange;">**`None`**</mark> if they could not be paired.



## _async def_ <mark style="color:blue;">`merge`</mark>`()`

Alias for [<mark style="color:yellow;">**`InfiniteCraft`**</mark>**`.`**<mark style="color:blue;">**`pair`**</mark>**`()`**](infinitecraft.md#async-def-pair-greater-than-element)



## _async def_ <mark style="color:blue;">`combine`</mark>`()`

Alias for [<mark style="color:yellow;">**`InfiniteCraft`**</mark>**`.`**<mark style="color:blue;">**`pair`**</mark>**`()`**](infinitecraft.md#async-def-pair-greater-than-element)



## def <mark style="color:blue;">**`get_discoveries`**</mark>**`()` -> **<mark style="color:yellow;">**`Element`**</mark>**, **<mark style="color:orange;">**`None`**</mark>







{% content-ref url="../this-is-it.md" %}
[this-is-it.md](../this-is-it.md)
{% endcontent-ref %}

[^1]: Where <mark style="color:red;">**`element`**</mark> is the result of the <mark style="color:blue;">**`pair`**</mark>**`()`** function.
