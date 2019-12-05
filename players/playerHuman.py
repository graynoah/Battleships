from typing import Tuple

from players.player import Player


class PlayerHuman(Player):
    """ A Human player in the battleships game.
    Subclass of Player Class.
    """

    def square_clicked(self, coordinate: Tuple[int, int]):
        self.guess(coordinate)
