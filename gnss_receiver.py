from datatypes import Coordinate
import random

class GnssReceiver:
    def __init__(self, actor, world, on_data, error_range: float):
        self._actor = actor
        self._on_data = on_data
        self._distortion = lambda: round(random.uniform(-error_range, error_range), 3)
        self._sensor = world.spawn_actor(
            world.get_blueprint_library().find("sensor.other.gnss"),
            self._actor.get_transform(),
            self._actor,
        )
        self._sensor.listen(lambda event: self._on_gnss_event(event))

    def destroy(self):
        self._sensor.destroy()

    def _on_gnss_event(self, event):
        self._on_data(
            self._actor.id,
            event.timestamp,
            Coordinate(
                x=event.longitude + self._distortion(),
                y=event.latitude + self._distortion(),
                z=event.altitude + self._distortion(),
            ),
        )
