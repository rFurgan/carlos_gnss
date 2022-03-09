from datatypes import GnssCallback
import math_operations as mo
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

    def __init__(
        self,
        actor: carla.Actor,
        world: carla.World,
        on_data: GnssCallback,
        error_range: float,
        tick: float,
    ) -> None:
        self._actor: carla.Actor = actor
        self._on_data: GnssCallback = on_data
        self._error_range: float = error_range
        bp = world.get_blueprint_library().find("sensor.other.gnss")
        bp.set_attribute("sensor_tick", str(tick))
        self._sensor: carla.GnssSensor = world.spawn_actor(
            bp,
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
            mo.distorted_coordinate(
                event.longitude, event.latitude, event.altitude, self._error_range
            ),
        )
