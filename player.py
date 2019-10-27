class Player(object):
    """ A player in the Battleships game.
    """

    def __init__(self):
        self._enemy_ships_sunk = 0
        self._ships = []  # all ships belonging to player
        self._remaining_ships = len(self._ships)

    def get_ships_sunk(self) -> int:
        """ Return the number of enemy ships this player has sunk."""
        return self._enemy_ships_sunk

    def get_ships_left(self) -> int:
        """ Return the number of ships that have not been sunk by enemy"""
        return self._remaining_ships

    def decrement_remaining_ships(self):
        """ Update how many remaining ships this player has left."""
        if(self._remaining_ships > 0):
            self._remaining_ships -= 1
