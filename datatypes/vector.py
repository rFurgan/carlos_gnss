class Vector:
    """Class to represent a 3D vector

    Args:
        x (float): x component of vector
        y (float): y component of vector
        z (float): z component of vector
    """

    def __init__(self, x: float, y: float, z: float) -> None:
        self._x: float = x
        self._y: float = y
        self._z: float = z

    @property
    def x(self) -> float:
        """
        Returns:
            float: x component of vector"""
        return self._x

    @property
    def y(self) -> float:
        """
        Returns:
            float: y component of vector"""
        return self._y

    @property
    def z(self) -> float:
        """
        Returns:
            float: z component of vector"""
        return self._z
