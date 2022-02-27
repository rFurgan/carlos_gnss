from datatypes import Coordinate
import random
import carla

class GnssReceiver:
    """Class that creates GNSS receivers from the implementation the Python API CARLA provides

    Args:
        actor (carla.Actor): Actor to which the GNSS sensor should be attached to
        world (carla.World): CARLA World, into which the actor is located and the GNSS sensor should be spawned into
        on_data (Callback): Callback function to which the collected GNSS data is forwarded to
        error_range (float): Error range in which the collected GNSS data should be distored
        tick (float): Seconds between each position detection
    """
    def __init__(self, actor, world, on_data, error_range: float, tick: float) -> None:
        self._actor = actor
        self._on_data = on_data
        self._distortion = lambda: round(random.uniform(-error_range, error_range), 3)
        self._tick = tick
        self._sensor = world.spawn_actor(
            world.get_blueprint_library().find("sensor.other.gnss"),
            self._actor.get_transform(),
            self._actor,
        )
        self._sensor.listen(lambda event: self._on_gnss_event(event))

    def destroy(self) -> None:
        """Method to destroy GNSS sensor and remove it from the world it is spawned in"""
        self._sensor.destroy()

    def _on_gnss_event(self, event: carla.GnssMeasurement) -> None:
        """Method to be called when new GNSS data comes in
        
        Args:
            event (carla.GnssMeasurement): Detected position data wrapped in longitude, latitude and altitude
        """
        self._on_data(
            self._actor.id,
            event.timestamp,
            Coordinate(
                x=event.longitude + self._distortion(),
                y=event.latitude + self._distortion(),
                z=event.altitude + self._distortion(),
            ),
        )
