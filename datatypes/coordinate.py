class Coordinate:
    """Class to represent a 3D coordinate

    Args:
        x (float): x component of coordinate
        y (float): y component of coordinate
        z (float): z component of coordinate
    """

    def __init__(self, x: float, y: float, z: float):
        self._x: float = x
        self._y: float = y
        self._z: float = z

    @property
    def x(self) -> float:
        """
        Returns:
            float: x component of coordinate"""
        return self._x

    @property
    def y(self) -> float:
        """
        Returns:
            float: y component of coordinate"""
        return self._y

    @property
    def z(self) -> float:
        """
        Returns:
            float: z component of coordinate"""
        return self._z
