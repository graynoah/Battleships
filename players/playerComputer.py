from players.player import Player
from players.ship import Ship
from random import randint


class PlayerComputer(Player):
    """A Computer player in the battleships game.
    """

    def on_turn_started(self):
        """On computer players turn, makes a random shot at enemy's grid
        """
        # if(len(self._guesses) > 0):
        randomX = randint(0, 9)
        randomY = randint(0, 9)
        while self.guess((randomX, randomY)) == -1:
            randomX = randint(0, 9)
            randomY = randint(0, 9)

    def get_possible_moves(self, row, col):
        """Checks the coordinates surrounding <row> and <col>, returning a
        list that contains the [row, col] of moves that can be made
        """
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
