from players.player import Player
from players.ship import Ship
from typing import List, Tuple


class GameManager(object):
    """A Singleton that manages the model of the game. The static instance
    variable can be used to access this object. This class must be created
    atleast once.

    === Private Attributes ===
        _size:
            The size of the playing grid.
        _player1:
            The player object for player 1.
        _player2:
            The player object for player 2.
        _whosTurn:
            The currently active scene.
    """
    instance = None

    _size: int
    _player1: Player
    _player2: Player
    _whosTurn: Player

    def __init__(self):
        """Create a new GameManager and setup the static instance variable."""
        if(GameManager.instance is None):
            GameManager.instance = self

        self._size = 0
        self._player1 = None
        self._player2 = None
        self._whosTurn = None

    def setup_game(self,
                   player1: Player,
                   player2: Player,
                   size: int = 10):
        """Set the starting values for a new game."""

        self._size = size
        self._player1 = player1
        self._player2 = player2
        self._whosTurn = player1

    def guess(self, player: Player, coordinate: Tuple[int, int]) -> int:
        """Make a guess for <player> at coordinate <coordinate>. Returns 1 if
        the guess results in a hit, 2 if it sinks a ship, and -1 if its an
        invalid move."""
        if(not self.is_valid_coordinate(coordinate) or
           player != self._whosTurn):
            return -1

        result = self.other_player(self._whosTurn).hit(coordinate)

        if(result != -1):
            self._whosTurn = self.other_player(self._whosTurn)
            self._whosTurn.on_turn_started()
            return result

        return -1

    def other_player(self, player: Player) -> Player:
        """Get the opponent of <player>."""
        if(player == self._player1):
            return self._player2

        if(player == self._player2):
            return self._player1

        return None

    def get_whos_turn(self) -> Player:
        """Get the player who currently has to make a move."""
        return self._whosTurn

    def is_valid_coordinate(self, coordinate: Tuple[int, int]):
        """Return true if <coordinate> is on the grid."""
        return (0 <= coordinate[0] <= self._size) \
            and (0 <= coordinate[1] <= self._size)

    def square_clicked(self, coordinate: Tuple[int, int]):
        """Relay a square click to the currently playing player."""
        self._whosTurn.square_clicked(coordinate)

    def get_player1(self) -> Player:
        """Get the player object for player 1."""
        return self._player1

    def get_player2(self) -> Player:
        """Get the player object for player 2."""
        return self._player2
