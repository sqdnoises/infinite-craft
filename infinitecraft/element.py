from typing import Any

__all__ = (
    "Element",
)

class Element:
    """
    An element object that represents an element of Infinite Craft.

    ## Attributes:
        `name` (`str`): Name of the element.
        `emoji` (`str`): Emoji of the element.
        `first_discovery` (`bool`): Whether the current element was a first discovery or not.
    
    ## Special Functions:
        - `__str__`: Returns the Emoji (if it exists) and Name of the element combined.
        
            - For example:
            
        ```py
        >>> str(Element(name="Fire", emoji="🔥", is_first_discovery=False))
        '🔥 Fire'
        >>> str(Element(name="Water", emoji=None, is_first_discovery=True))
        'Water'
        ```
        
        - `__repr__`: Returns a string representing how the class was made.
        
            - For example:
            
        ```py
        >>> repr(Element(name="Fire", emoji="🔥", is_first_discovery=False))
        "Element(name='Fire', emoji='🔥', is_first_discovery=False)"
        >>> repr(Element(name="Water", emoji=None, is_first_discovery=True))
        "Element(name='Water', emoji=None, is_first_discovery=True)"
        ```
        
        - `__eq__`: Checks if the element name is equal to another element's name.
        
            - For example:
        
        ```py
        >>> fire1 = Element(name="Fire", emoji="🔥", is_first_discovery=False)
        >>> fire2 = Element(name="Fire", emoji="❤️‍🔥", is_first_discovery=False)
        >>> water = Element(name="Water", emoji="💧", is_first_discovery=True)
        >>> fire1 == fire2
        True
        >>> fire1 == water
        False
        ```
        
        - `__bool__`: If all attributes are `None` (not defined) `False` gets returned otherwise `True` gets returned.
        
            - For example:
        
        ```py
        >>> bool(Element(name="Fire", emoji="🔥", is_first_discovery=False))
        True
        >>> bool(Element(name="Water", emoji=None, is_first_discovery=True))
        True
        >>> bool(Element(name=None, emoji=None, is_first_discovery=None))
        False
        ```
    
    You can make your own `Element` class by subclassing this one.
    
    NOTE: The emoji is NOT fetched upon creation of this class. You can fetch it by reading the discoveries JSON file if you need it.
    """

    def __init__(self, name: str | None = None, emoji: str | None = None, is_first_discovery: bool | None = None) -> None:
        self.name = name
        self.emoji = emoji
        self.is_first_discovery = is_first_discovery
    
    def __str__(self) -> str:
        if self.emoji:
            return str(self.emoji) + " " + str(self.name)
        else:
            return str(self.name)
    
    def __repr__(self) -> str:
        return f"Element(name={repr(self.name)}, emoji={repr(self.emoji)}, is_first_discovery={repr(self.is_first_discovery)})"
    
    def __eq__(self, __value: Any) -> bool:
        if bool(self) == False and __value is None:
            return True
        elif isinstance(__value, Element) and __value.name == self.name:
            return True
        else:
            return False
    
    def __bool__(self) -> bool:
        return self.name               is not None and \
               self.emoji              is not None and \
               self.is_first_discovery is not None