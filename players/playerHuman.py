from typing import Tuple

from players.player import Player


class PlayerHuman(Player):
    """ A Human player in the battleships game.
    Subclass of Player Class.
    """

    def __init__(self, name: str):
        Player.__init__(self, name)

    def square_clicked(self, coordinate: Tuple[int, int]):
        Player.guess(self, coordinate)
