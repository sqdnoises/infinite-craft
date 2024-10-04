from dataclasses import dataclass
from .abc import ElementProtocol

__all__ = (
    "Element",
)

@dataclass(frozen=True)
class Element(ElementProtocol):
    """
    Represents an element in the Infinite Craft system.

    This class provides attributes for an element's name, emoji, and whether 
    it was a first discovery. It also implements several special methods 
    (`__str__`, `__repr__`, `__eq__`, `__bool__`) for more user-friendly 
    object representations and comparisons.

    Attributes:
        name (str | None): The name of the element.
        emoji (str | None): The emoji representing the element.
        is_first_discovery (bool | None): Whether the element was the first discovery.

    Methods:
        __str__: Returns a string combining the emoji and name of the element.
        __repr__: Returns a string representation of how the object was created.
        __eq__: Compares the element name with another element's name.
        __bool__: Returns False if all attributes are None, otherwise True.

    Example:
        >>> fire = Element(name="Fire", emoji="🔥", is_first_discovery=False)
        >>> print(str(fire))
        '🔥 Fire'
        >>> water = Element(name="Water", emoji=None, is_first_discovery=True)
        >>> print(str(water))
        'Water'

        >>> repr(fire)
        "Element(name='Fire', emoji='🔥', is_first_discovery=False)"
        >>> fire == water
        False
    
    Note:
        The `emoji` attribute is not fetched upon creation of the class. 
        If the emoji is not provided, it must be fetched manually, such as by reading 
        a discoveries JSON file or other data source.
    """
    
    name: str | None = None
    emoji: str | None = None
    is_first_discovery: bool | None = None
    
    def __str__(self) -> str:
        """
        Returns a string representation of the element, combining the emoji (if it exists) 
        and the name.

        Returns:
            str: The emoji and name combined or just the name if no emoji is present.
        
        Example:
            >>> str(Element(name="Fire", emoji="🔥"))
            '🔥 Fire'
            >>> str(Element(name="Water", emoji=None))
            'Water'
        """
        if self.emoji:
            return str(self.emoji) + " " + str(self.name)
        else:
            return str(self.name)
    
    def __repr__(self) -> str:
        """
        Returns a string that shows how the Element object was constructed.

        Returns:
            str: A string representation of the object’s creation.
        
        Example:
            >>> repr(Element(name="Fire", emoji="🔥"))
            "Element(name='Fire', emoji='🔥', is_first_discovery=None)"
        """
        return (
            f"Element("
            f"name={repr(self.name)}, "
            f"emoji={repr(self.emoji)}, "
            f"is_first_discovery={repr(self.is_first_discovery)}"
            f")"
        )
    
    def __eq__(self, other: ElementProtocol | None) -> bool:
        """
        Compares this element with another element based on the name.

        Args:
            other (ElementProtocol | None): Another element to compare to.

        Returns:
            bool: True if the names of the two elements are the same, or if both elements are None. 
            False otherwise.
        
        Example:
            >>> fire1 = Element(name="Fire", emoji="🔥")
            >>> fire2 = Element(name="Fire", emoji="❤️‍🔥")
            >>> fire1 == fire2
            True
            >>> fire1 == Element(name="Water")
            False
        """
        if not self and other is None:
            return True
        elif isinstance(other, ElementProtocol) and other.name == self.name:
            return True
        else:
            return False
    
    def __bool__(self) -> bool:
        """
        Returns whether the element is considered "truthy" or not.

        The element is considered True if all attributes (name, emoji, and is_first_discovery) are 
        defined (not None). If any of these are None, it returns False.

        Returns:
            bool: True if all attributes are not None, False otherwise.
        
        Example:
            >>> bool(Element(name="Fire", emoji="🔥"))
            True
            >>> bool(Element(name=None, emoji=None))
            False
        """
        return self.name               is not None \
           and self.emoji              is not None \
           and self.is_first_discovery is not None
