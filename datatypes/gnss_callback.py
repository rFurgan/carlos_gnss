from typing import Protocol
from datatypes import Coordinate


class GnssCallback(Protocol):
    """Class to represent a callback function that receives GNSS data from a GNSS sensor

    Args:
        id (int): Id of the actor within the Carla world
        timestamp (float): Timestamp on when the position was retrieved
        position (Coordinate): Position at the given timestamp
    """

    def __call__(self, id: int, timestamp: float, position: Coordinate) -> None:
        ...
