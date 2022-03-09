from typing import Protocol


class Subscription(Protocol):
    """Class that represents a callback function as a subscription to forward json data

    Args:
        json_data (str): String containing JSON data with all the calculated data from the received GNSS data"""

    def __call__(self, json_data: str) -> None:
        ...
