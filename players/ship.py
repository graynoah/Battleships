from typing import List, Tuple


class Ship(object):
    """
    A ship object in the Batleships game.

    === Private Attributes ===
        _hit_points:
            A list of the ships hit points
            (The locations on the grid the ship takes up)
        _ship_length:
            The number of spots on the grid, that the ship takes up
    """

    _hit_points: List[Tuple[int, int, bool]]
    _ship_length: int

    def __init__(self, coordinates: List[Tuple[int, int]]) -> None:
        """Create a ship of a certain length given by <coordinates>, covering
        one or more locations.
        coordinates needs to be formed as [(x1,x2), (y1,y2), ...]
        """
        self._hit_points = []
        for coordinate in coordinates:
            self._hit_points.append((coordinate[0], coordinate[1], False))
        self._ship_length = len(coordinates)

    def hit(self, coordinate: Tuple[int, int]) -> int:
        """Checks to see if the given <coordinate> is the location of part of
        this ship.
        Returns whether <coordinate> is a hit, miss, or sink, on ship
        """
        for i in range(len(self._hit_points)):
            point = self._hit_points[i]

            if(point[0] == coordinate[0] and point[1] == coordinate[1]):
                if(point[2]):  # Invalid move
                    return -1

                self._hit_points[i] = (point[0], point[1], True)

                if(self.is_sunk()):  # Ship sunk
                    return 2

                return 1    # Ship hit

        return 0  # Ship miss

    def get_hit_points(self) -> List[Tuple]:
        """Returns a list of this ships hit points
        (coordinates of the ship on the grid)
        """
        return self._hit_points

    def is_sunk(self) -> bool:
        """Returns whether or not every spot on the ship is hit
        """
        for i in range(len(self._hit_points)):
            if(not self._hit_points[i][2]):
                return False

        return True
