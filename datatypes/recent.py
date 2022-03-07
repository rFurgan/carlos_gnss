from datatypes import Coordinate
from typing import TypeVar, Generic

T = TypeVar("T")


class Recent(Generic[T]):
    """Class to represent previous and current data

    Args:
        previous (T): Previous data
        current (T): Most recent data
    """

    def __init__(
        self,
        previous: T,
        current: T,
    ) -> None:
        self._previous: T = previous
        self._current: T = current

    @property
    def previous(self) -> T:
        """
        Returns:
            T: Value that is stored as previous data
        """
        return self._previous

    @property
    def current(self) -> T:
        """
        Returns:
            T: Value that is stored as current data
        """
        return self._current

    @previous.setter
    def previous(self, previous: T) -> None:
        """
        Args:
            previous (T): Value to set as previous data
        """
        self._previous = previous

    @current.setter
    def current(self, current: T) -> None:
        """
        Args:
            current (T): Value to set as current data
        """
        self._current = current

    def has_none(self) -> bool:
        """Check if either previous or current is set to None

        Returns:
            bool: True if one of the attributes set to None, False otherwise
        """
        return self._current == None or self._previous == None
