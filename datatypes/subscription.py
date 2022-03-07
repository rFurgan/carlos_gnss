from typing import Protocol


class Subscription(Protocol):
    def __call__(self, json_data: str) -> None:
        ...
