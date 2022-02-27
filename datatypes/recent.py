from datatypes import Coordinate
from typing import Union


class Recent:
    """Class to represent previous and current data

    Args:
        previous (float | Coordinate | None]): Previous data
        current (float | Coordinate | None]): Most recent data
    """

    def __init__(
        self,
        previous: Union[float, Coordinate, None],
        current: Union[float, Coordinate, None],
    ) -> None:
        self._previous: Union[float, Coordinate, None] = previous
        self._current: Union[float, Coordinate, None] = current

    @property
    def previous(self) -> Union[float, Coordinate, None]:
        """
        Returns:
            float: Previously stored float data
            Coordinate: Previously stored Coordinate
            None: No data stored previously
        """
        return self._previous

    @property
    def current(self) -> Union[float, Coordinate, None]:
        """
        Returns:
            float: Most recently stored float data
            Coordinate: Most recently stored Coordinate
            None: No data stored recently
        """
        return self._current

    @previous.setter
    def previous(self, previous: Union[float, Coordinate, None]) -> None:
        """
        Args:
            previous (float | Coordinate | None]): Value to set previous
        """
        self._previous = previous

    @current.setter
    def current(self, current: Union[float, Coordinate, None]) -> None:
        """
        Args:
            current (float | Coordinate | None]): Value to set current
        """
        self._current = current

    def has_none(self) -> bool:
        """Check if either previous or current is set to None

        Returns:
            bool: True if one of the attributes set to None, False otherwise
        """
        return self._current == None or self._previous == None
