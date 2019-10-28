from players.player import Player
from ships.ship import Ship


class PlayerComputer(Player):
    """A Computer player in the battleships game
    """

    def __init__(self, name: str):
        Player.__init__(self, name)

    def attack(self):
        """Makes a move for the computerPlayer
        """
        # TODO
        pass

    def get_possible_moves(self, row, col):
        """Checks the coordinates surrounding <row> and <col>, returning a
        list that contains the [row, col] of moves that can be made
        """
        # TODO
        pass

    def is_sunk(self):
        """Returns True if the ship is sunk
        """
        pass

    def has_hit(self):
        """Checks to see if the computer player currently has a hit enemy ship
        """
        pass

    def get_hit(self):
        """Returns the coordinates: [row, col], of a shot that has hit an enemy
        ship
        """
        pass

