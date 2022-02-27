from common import MAX_STORE_SIZE
from typing import Union, Dict, Tuple
from datatypes import Coordinate, Vector, Recent
import math_operations as mo


class RecentData:
    """Class to store the most recent data and provide velocity, orientation and angular velocity

    Args:
        expiration_time (float): Time in seconds when the stored current timestamp and position is expired
    """

    def __init__(self, expiration_time: float) -> None:
        self._expiration_time: float = expiration_time
        self._recent_timestamp: Recent = Recent(None, None)
        self._recent_position: Recent = Recent(None, None)
        self._recent_orientation: Recent = Recent(None, None)
        self._orientation: Union[float, None] = None
        self._velocity: float = 0
        self._stored: Dict[float, Coordinate] = {}

    @property
    def stored(self) -> Dict[float, Coordinate]:
        """Returns the dictionary with the positions on the corresponding timestamps

        Returns:
            Dict[float, Coordinate]: Dictionary with the most recent timestamps and the corresponding positions
        """
        return self._stored

    def update(
        self, timestamp: float, position: Coordinate
    ) -> Union[Tuple[float, float, float], Tuple[None, None, None]]:
        """Updates the previous and current timestamp and position returning the calculated data

        Args:
            timestamp (float): Most recent timestamp to save
            position (Coordinate): Most recent position to save

        Returns:
            Tuple[None, None, None]: Insufficient data to calculate velocity, orientation and angular velocity
            Tuple[float, float, float]: Current velocity, orientation and angular velocity
        """
        self._store(timestamp, position)
        if (
            self._recent_timestamp.current != None
            and (timestamp - self._recent_timestamp.current) > self._expiration_time
        ):
            self._recent_timestamp.current = None

        self._recent_timestamp.previous = self._recent_timestamp.current
        self._recent_timestamp.current = timestamp

        if self._recent_timestamp.previous != None:
            self._recent_position.previous = self._recent_position.current
            self._recent_position.current = position

            if self._recent_position.has_none():
                return None, None, None
            vec: Vector = mo.vector(
                self._recent_position.current, self._recent_position.previous
            )
            return (
                self._get_velocity(vec),
                self._get_orientation(vec),
                self._get_angular_velocity(),
            )
        return None, None, None

    def _get_velocity(self, vec: Vector) -> float:
        """Calculates and returns the current velocity

        Args:
            vec (Vector): Vector of most recent covered distance

        Returns:
            float: Current velocity
        """
        self._velocity = mo.velocity(
            vec, self._recent_timestamp.previous, self._recent_timestamp.current
        )
        return self._velocity

    def _get_orientation(self, vec: Vector) -> Union[float, None]:
        """Calculates and returns the current orientation

        Args:
            vec (Vector): Vector of most recent covered distance

        Returns:
            float: Current orientation
            None: Insufficient data
        """
        orientation: Union[float, None] = mo.angle_to_y_axis(vec)
        self._recent_orientation.previous = self._recent_orientation.current
        self._recent_orientation.current = orientation
        if orientation != None and self._velocity > 0:
            self._orientation = orientation
        return (
            orientation
            if orientation != None and self._velocity > 0
            else self._orientation
        )

    def _get_angular_velocity(self) -> float:
        """Calculates and returns the current angular velocity

        Returns:
            float: Current angular velocity
        """
        if self._recent_orientation.has_none() or self._recent_timestamp.has_none():
            return 0
        return mo.angular_speed(
            self._recent_orientation.previous,
            self._recent_orientation.current,
            self._recent_timestamp.previous,
            self._recent_timestamp.current,
        )

    def _store(self, timestamp: float, position: Coordinate) -> None:
        """Stores the most recent position and corresponding timestamp

        Args:
            timestamp (float): Timestamp of most recent detected position
            position (Coordinate): Most recent detected position
        """
        if len(self._stored) >= MAX_STORE_SIZE:
            first = list(self._stored.keys())[0]
            del self._stored[first]
        self._stored[timestamp] = position
