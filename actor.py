from typing import List, Union, Dict


class Actor:
    """Class to store a certain amount of data (velocity, orientation, angular speed, distance to hero and angle to hero)

    Args:
        id (int): Id that represents the actor in the Carla world
        type (int): Number that represents the type of traffic user in the Carla world
        max_entry_count: (int): Maximum amount of entries to be stored
    """

    def __init__(self, id: int, type: int, max_entry_count: int) -> None:
        self._data: Dict[int, int] = [id, type]
        self._max_entry_count: int = max_entry_count
        self._velocity: List[float] = []
        self._orientation: List[float] = []
        self._angular_speed: List[float] = []
        self._distance_to_hero: List[float] = []
        self._angle_to_hero: List[float] = []

    def add_data(
        self,
        velocity: Union[float, None],
        orientation: Union[float, None],
        angular_speed: Union[float, None],
        distance_to_hero: Union[float, None],
        angle_to_hero: Union[float, None],
    ) -> None:
        """Add new entry to saved data

        Args:
            velocity (float | None): Velocity to be saved
            orientation (float | None): Orientation to be saved
            angular_speed (float | None): Angular speed to be saved
            distance_to_hero (float | None): Distance to hero to be saved
            angle_to_hero (float | None): Angle to hero to be saved
        """
        if len(self._velocity) >= self._max_entry_count:
            self._velocity.pop(0)
        self._velocity.append(velocity if velocity != None else 0)

        if len(self._orientation) >= self._max_entry_count:
            self._orientation.pop(0)
        self._orientation.append(orientation if orientation != None else 0)

        if len(self._angular_speed) >= self._max_entry_count:
            self._angular_speed.pop(0)
        self._angular_speed.append(angular_speed if angular_speed != None else 0)

        if len(self._distance_to_hero) >= self._max_entry_count:
            self._distance_to_hero.pop(0)
        self._distance_to_hero.append(
            distance_to_hero if distance_to_hero != None else 0
        )

        if len(self._angle_to_hero) >= self._max_entry_count:
            self._angle_to_hero.pop(0)
        self._angle_to_hero.append(angle_to_hero if angle_to_hero != None else 0)

    def get_data(self) -> List[Union[int, float]]:
        """Returns all saved data in a single big array with id and type as first entries

        Returns:
            List[int | float]: Array of all stored data with id and type as first entries
        """
        return (
            self._data
            + self._velocity
            + self._orientation
            + self._angular_speed
            + self._distance_to_hero
            + self._angle_to_hero
        )
