import logging
import sys
import csv
import carla
import pathlib
import math_operations as mo
from hero import Hero
from actor import Actor
from typing import Dict, List, Callable, Union
from common import EActorType, VehicleTypes, ROAD_USER_CODE
from gnss_receiver import GnssReceiver


class Api:
    """Class that provides the access to the program as a whole

    Note:
        Only use this class to work with, the other classes are not to be accessed from the outside
        Refer to the example.py file for an example of the usage

    Args:
        host (string): Address of the host where the Carla world is running
        port (int): Port to the host where the Carla world is running
        relevance_radius (int): Radius of distance that filters out actors that are out of range from the hero
        max_entry_count (int): Amount of entries to be stored for CSV file to be created
        hero_id (int, optional): Id of the actor to be assigned as hero
    """

    def __init__(
        self,
        host: str,
        port: int,
        relevance_radius: float,
        max_entry_count: int,
        hero_id: int = -1,
    ) -> None:
        self._actors: Dict[int, Actor] = {}
        self._road_users: List[carla.Actor] = []
        self._subscribers: List[Callable] = []
        self._stop: bool = False
        self._gnss_receivers: List[GnssReceiver] = []
        self._hero: Union[Hero, None] = None
        self._hero_id: int = hero_id
        self._relevance_radius: float = relevance_radius
        self._max_entry_count: int = max_entry_count
        self._header_written: bool = False
        try:
            client: carla.Client = carla.Client(host, port)
            client.set_timeout(2.0)
            self._world: carla.World = client.get_world()
        except RuntimeError as err:
            logging.error(f"Something went wrong connecting: {err}")
            sys.exit(1)
        for actor in self._world.get_actors():
            if (
                EActorType.VEHICLE.value in actor.type_id
                or EActorType.PEDESTRIAN.value in actor.type_id
            ):
                if self._hero_id != -1 and actor.id == self._hero_id:
                    self._hero = Hero(
                        actor.id,
                        self._actors,
                        self._subscribers,
                        self._relevance_radius,
                    )
                elif (
                    self._hero_id == -1
                    and self._hero == None
                    and mo.vector_length(actor.get_velocity()) > 0
                ):
                    self._hero = Hero(
                        actor.id,
                        self._actors,
                        self._subscribers,
                        self._relevance_radius,
                    )
                self._road_users.append(actor)
                self._actors[actor.id] = Actor(
                    actor.id, self._classify_type(actor.type_id), self._max_entry_count
                )

    def start(self, tick: float, error_range: float = 0) -> None:
        """Method to start a thread to poll and calulate the data of all present actors in the connected Carla world

        Args:
            tick (float): Time in seconds how often the position of the actors is to be polled
            error_range (float, optional): Range from which a random error is generated that falsifies the positions
        """
        if self._hero == None:
            logging.error("No Hero initialized or found")
            sys.exit(1)
        for road_user in self._road_users:
            self._gnss_receivers.append(GnssReceiver(road_user, self._world, self._hero.on_position_data, error_range))

    def stop(self) -> None:
        """Method to stop the polling of positions and calculation of data by killing the thread and main loop"""
        self._stop = True
        for gnss_receiver in self._gnss_receivers:
            gnss_receiver.destroy()

    def save_csv(self, path: str, filename: str) -> None:
        """Method to save collected data into a .csv file on the given path with the given filename

        Args:
            path (string): Path where the file should be saved to
            filename (string): Name of the file the data should be saved to
        """
        with open(pathlib.Path(path, filename), "a", encoding="UTF-8") as f:
            writer = csv.writer(f)
            if not self._header_written:
                writer.writerow(self._header())
                self._header_written = True
            for actor_id in self._actors:
                writer.writerow(self._actors[actor_id].get_data())

    def subscribe(self, callback: Callable) -> None:
        """Method to add callback function to which the calculated data will be forwarded to in runtime

        Args:
            callback (function): Callback function with one argument holding the data in JSON format
        """
        self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable) -> None:
        """Method to remove callback function to which the calculated data is forwarded to in runtime

        Args:
            callback (function): Callback function that should be removed
        """
        for index in range(len(self._subscribers)):
            if self._subscribers[index] == callback:
                self._subscribers.pop(index)
                break

    def _header(self) -> List[str]:
        """Creates a header line for the created CSV file

        Returns:
            List[str]: An array holding all headers for the created CSV file
        """
        header: List[str] = ["ID", "type"]
        header += self._data_header("velocity")
        header += self._data_header("orientation")
        header += self._data_header("angular_speed")
        header += self._data_header("distance_to_hero")
        header += self._data_header("angle_to_hero")
        return header

    def _data_header(self, data_type: str) -> List[str]:
        """Creates multiple headers for each column

        Args:
            data_type (str): Name of the column

        Returns:
            List[str]: Array with index appended to the name
        """
        header: List[str] = []
        for count in range(self._max_entry_count):
            header.append(f"{data_type}_{count}")
        return header

    def _classify_type(self, actor_type: str) -> int:
        """Method to classify the type of an actor encoded as an integer

        Args:
            actor_type (str): Actor type provided by the Carla world

        Returns:
            int: Encoded traffic user type
        """
        for category in VehicleTypes.categories:
            for type in VehicleTypes.types[category]:
                if type in actor_type:
                    return ROAD_USER_CODE[category]
        return ROAD_USER_CODE[EActorType.PEDESTRIAN]
