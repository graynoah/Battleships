from player import Player
from ship import Ship

class Board(object):
    '''
    Create ...
    '''
    _size: int
    _squares: list
    _players: list

    def __init__(self,
                 size: int = 0,
                 players:  list = None) -> None:
        
        self._size = size
        self._players = players
        self._initializers()

    def _initializers(self) -> None:
        self._squares = [[None for i in range(self._size)] \
                         for j in range(self._size)]
        print(self._players)
        for p in self._players:
            for s in p._ships:
                self._fill_holes(s)
                
                
    def _fill_holes(self,
                    ship: Ship = None) -> None:
        
        for coordinate in ship._coordinates:
            self._squares[coordinate[0]][coordinate[1]] = ship

    def guess(self, coordinate: list = None, player_num : int = 1) -> None:
        '''
        Player one = 0
        Player two = 1
        '''
        if player_num == 0:
            self._squares[coordinate[0]][coordinate[1]] = Ship("_hit") \
                                                          if self._players[1].ships_get_hit(coordinate) \
                                                          else Ship("miss")
        else:
            self._squares[coordinate[0]][coordinate[1]] = Ship("_hit") \
                                                          if self._players[0].ships_get_hit(coordinate) \
                                                          else Ship("miss")

    def who_is_winner(self) -> int:
        '''
        0 if player one win
        1 if player two win
        -1 if is not finished
        '''
        for index in range(len(self._players)):
            if self._players[index].all_sunk():
                return index
        return -1
        
    def __repr__(self) -> str:
        return str(self._squares)

    
