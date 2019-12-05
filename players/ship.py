from typing import List, Tuple


class Ship(object):
    '''
    Create a ship with specific name, length and location.
    coordinates needs to be formed as [(x1,x2), (y1,y2), ...]
    '''
    _hit_points: List[Tuple[int, int, bool]]

    def __init__(self, coordinates: List[Tuple[int, int]]) -> None:
        self._hit_points = []
        for coordinate in coordinates:
            self._hit_points.append((coordinate[0], coordinate[1], False))

    def hit(self, coordinate: Tuple[int, int]) -> int:
        for i in range(len(self._hit_points)):
            point = self._hit_points[i]

            if(point[0] == coordinate[0] and point[1] == coordinate[1]):
                if(point[2]):
                    return -1

                self._hit_points[i] = (point[0], point[1], True)

                if(self.is_sunk()):
                    return 2

                return 1

        return 0

    def get_hit_points(self) -> List[Tuple]:
        return self._hit_points

    def is_sunk(self) -> bool:
        for i in range(len(self._hit_points)):
            if(not self._hit_points[i][2]):
                return False

        return True
