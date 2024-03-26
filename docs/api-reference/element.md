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

# 🧪 Element

## _class_ <mark style="color:yellow;">`Element`</mark>

An element object that represents an element of Infinite Craft.

```python
Element(
    name:               str  | None = None,
    emoji:              str  | None = None,
    is_first_discovery: bool | None = None
)
```

### Arguments & Attributes

<mark style="color:red;">**`name`**</mark> (<mark style="color:yellow;">**`str`**</mark> **|** <mark style="color:orange;">**`None`**</mark>, optional): Name of the element

<mark style="color:red;">**`emoji`**</mark> (<mark style="color:yellow;">**`str`**</mark> **|** <mark style="color:orange;">**`None`**</mark>, optional): Emoji of the element.

<mark style="color:red;">**`is_first_discovery`**</mark> (<mark style="color:yellow;">**`bool`**</mark> **|** <mark style="color:orange;">**`None`**</mark>, optional): Whether the current element was a first discovery or not.

<details>

<summary>Special Functions</summary>

<mark style="color:blue;">**`__str__`**</mark>**`()`**: Returns the Emoji (if it exists) and Name of the element combined.

For example:

```py
>>> str(Element(name="Fire", emoji="🔥", is_first_discovery=False))
'🔥 Fire'
>>> str(Element(name="Water", emoji=None, is_first_discovery=True))
'Water'
```

<mark style="color:blue;">**`__repr__`**</mark>**`()`**: Returns a string representing how the class was made.

For example:

```py
>>> repr(Element(name="Fire", emoji="🔥", is_first_discovery=False))
"Element(name='Fire', emoji='🔥', is_first_discovery=False)"
>>> repr(Element(name="Water", emoji=None, is_first_discovery=True))
"Element(name='Water', emoji=None, is_first_discovery=True)"
```

<mark style="color:blue;">**`__eq__`**</mark>**`()`**: Checks if the element name is equal to another element's name.

For example:

```py
>>> fire1 = Element(name="Fire", emoji="🔥", is_first_discovery=False)
>>> fire2 = Element(name="Fire", emoji="❤️‍🔥", is_first_discovery=False)
>>> water = Element(name="Water", emoji="💧", is_first_discovery=True)
>>> fire1 == fire2
True
>>> fire1 == water 
False
```

<mark style="color:blue;">**`__bool__`**</mark>**`()`**: If all attributes are <mark style="color:orange;">**`None`**</mark>, <mark style="color:blue;">`False`</mark> gets returned otherwise <mark style="color:blue;">`True`</mark> gets returned.

For example:

```py
>>> bool(Element(name="Fire", emoji="🔥", is_first_discovery=False))
True
>>> bool(Element(name="Water", emoji=None, is_first_discovery=True))
True
>>> bool(Element(name=None, emoji=None, is_first_discovery=None))
False
```

</details>

You can make your own <mark style="color:yellow;">**`Element`**</mark> class by subclassing this one.

**NOTE:** The emoji is NOT fetched upon the creation of this class. You can fetch it by using [<mark style="color:red;">**`game`**</mark>](#user-content-fn-1)[^1]**`.`**<mark style="color:blue;">**`get_discovery`**</mark>**`()`**.



[^1]: Where <mark style="color:red;">**`game`**</mark> is an initialised <mark style="color:yellow;">**`InfiniteCraft`**</mark> class.
