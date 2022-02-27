from enum import Enum


class EActorType(Enum):
    """
    Enum that holds the two different main types of traffic users
    """

    VEHICLE = "vehicle"
    PEDESTRIAN = "pedestrian"
