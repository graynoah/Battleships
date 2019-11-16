class Ship(object):
    '''
    Create a ship with specific name, length and location.
    coordinates needs to be formed as [(x1,x2), (y1,y2), ...]
    '''
    _ship_type: str
    _coordinates: list 
    
    def __init__(self,
                 ship_type: str = "default",
                 coordinates: list = None) -> None:

        self._ship_type = ship_type
        self._coordinates = coordinates

    def is_hit(self,
               coordinate: list = None) -> bool:
        
        return [element for element in self._coordinates \
                if coordinate == element] != []

    def is_gone(self) -> bool:
        return self._coordinates == []
                          
    def __repr__(self) -> str:
        return self._ship_type

    def __eq__(self, other) -> bool:
        return ( isinstance(other,Ship) and
            [element for element in self._coordinates if \
             other._coordinates[0] == element]
            != []
            )
            
