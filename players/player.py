from typing import List
from ships.ship import Ship


class Player(object):
    """ A player in the Battleships game.
    """
    _name: str
    _sunken_ships: int  # Number of enemy ships that this player has sunk
    _num_of_ships: int  # Total num of players ship
    _ships: List[Ship]
    _remaining_ships: int

    def __init__(self, name: str):
        self._name = name
        self._ships = []  # all ships belonging to player
        self._remaining_ships = len(self._ships)
        self._sunken_ships = 0
        self.num_of_ships = 6

    def attack(self):
        """Abstract method: to be implemented in playerComputer and playerHuman
        """
        pass

    def is_valid_coordinate(self, row, col):
        """Returns true if <row> and <col> on the grid.
        """
        # TODO: implement the grid

        board_len = 8  # board_len = grid.get_len, once implemented
        grid = [[None]]
        if (0 <= row <= board_len) and \
           (0 <= col <= board_len) and \
           (grid[row][col] is None):
            return True
        else:
            return False

    def get_name(self) -> str:
        """Returns the players name
        """
        return self._name

    def get_sunken_ships(self):
        """Returns the number of enemy ships you have sunken.
        """
        return self._sunken_ships

    def set_num_of_ships(self, num: int):
        """Changes the number of ships to <num>
        """
        self._num_of_ships = num

    def get_num_of_ships(self) -> int:
        """Returns the total number of ships that the player has
        """
        return self._num_of_ships

    def add_sunken_ship(self):
        """Increments the number of enemy ships you have sunken by one.
        """
        self._sunken_ships += 1

    def get_ships_left(self) -> int:
        """Return the number of ships that have not been sunk by enemy
        """
        return self._remaining_ships

    def decrement_remaining_ships(self):
        """Update how many remaining ships this player has left.
        """
        if self._remaining_ships > 0:
            self._remaining_ships -= 1
