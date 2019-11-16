from ship import Ship

class Player(object):
    '''
    Create ...
    '''

    _ships: list
    _id: list
    
    def __init__(self,
                 ID: str = "default",
                 ships: list = None) -> None:
        
        self._ships = ships
        self._id = ID

    def all_sunk(self) -> bool:
        return self._ships == []

    def remove_ship(self, ship:
                    Ship = None) -> None:
        self._ships = [element for element in self._ships if element != ship]

    def ships_get_hit(self,
                      coordinate: list = None) -> bool:
        for s in self._ships:
            if s.is_hit(coordinate):
                s._coordinates.remove(coordinate)
                s.is_gone() and self._ships.remove(s)
                return True
        return False
        
    def __repr__(self) -> str:
        return (
            "ID: %s | Ships: %s\n" %(self._id, self._ships)
            )
