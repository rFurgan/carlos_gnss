import carla
import logging
from api import Api

LOCAL_HOST: str = "127.0.0.1"
LOCAL_PORT: int = 2000
RELEVANCE_RADIUS: int = 50000
MAX_ENTRY_COUNT: int = 10


def change_world(map: str, host: str, port: int) -> None:
    """Method to change Carla world to the provided map

    Args:
        map (str): Map to change to
        host (str): Host adress of the Carla world
        port (int): Port adress of the Carla world
    """
    try:
        client: carla.Client = carla.Client(host, port)
        client.set_timeout(2.0)
        client.load_world(map)
    except RuntimeError as err:
        logging.error(
            f"Failed to connect to CARLA world {host}:{port} due to error: {err}"
        )


if __name__ == "__main__":
    if input("Change map?") == "y":
        change_world("Town02", LOCAL_HOST, LOCAL_PORT)
        input(
            "Wait until map changed and spawn the actors. Now press any key to continue"
        )
    a: Api = Api(LOCAL_HOST, LOCAL_PORT, RELEVANCE_RADIUS, MAX_ENTRY_COUNT)
    a.start(0.5)
    input("Press ENTER to end")
    a.save_csv(r"C:\Users\Pepe\Desktop", "data.csv")
    a.stop()
