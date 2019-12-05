from typing import List, Tuple

from players.ship import Ship
import managers.game_manager as gm
from util.observable import Observable


class Player(Observable):
    """ A player in the Battleships game.
    === Private Attributes ===
        _name:
            The name of the player
        _sunken_ships:
            The number of enemy ships that this player has sunk
        _num_of_ships:
            The total num of players ship
        _ships:
            A List of this players ships
        _remaining_ships:
            The number of ships this player has that are not sunk
        _guesses:
            A list that records the locations of any shots made
            (regardless of hit or miss)
    """

    _name: str
    _sunken_ships: int
    _num_of_ships: int
    _ships: List[Ship]
    _remaining_ships: int
    _guesses: List[Tuple[int, int, bool]]

    def __init__(self, name: str):
        Observable.__init__(self)

        self._name = name
        self._ships = [Ship([(0, 0), (1, 1)])]
        self._remaining_ships = len(self._ships)
        self._sunken_ships = 0
        self.num_of_ships = 6
        self._guesses = []

    def square_clicked(self, coordinate: Tuple[int, int]):
        """Called when a square on the grid is clicked. To be implemented in
        sub classes.
        """
        pass

    def guess(self, coordinate: Tuple[int, int]):
        """Called by a player's sqaure_clicked. Takes a shot at the given
        <coordinate>, resulting in either a Hit, Miss, or Sinking an enemy
        ship.
        """
        for guess in self._guesses:
            if(guess[:2] == coordinate):
                return

        result = gm.GameManager.instance.guess(self, coordinate)
        if(result == 0):
            print(self._name, "Miss")
            self._guesses.append((coordinate[0], coordinate[1], False))
        elif(result == 1):
            print(self._name, "Hit")
            self._guesses.append((coordinate[0], coordinate[1], True))
        elif(result == 2):
            print(self._name, "SUNK")
            self._guesses.append((coordinate[0], coordinate[1], True))
            self._sunken_ships += 1
        else:
            return

        self.notify_observers()

    def get_guesses(self) -> List[Tuple[int, int, bool]]:
        """Returns the List of this player's guesses.
        """
        return self._guesses

    def get_ships(self) -> List[Ship]:
        """Returns the List of this player's ships.
        """
        return self._ships

    def on_turn_started(self):
        """Called at the start of a player's turn.
        To be implemented in sub classes.
        """
        pass

    def get_name(self) -> str:
        """Returns the players name.
        """
        return self._name

    def get_sunken_ships(self):
        """Returns the number of enemy ships you have sunken.
        """
        return self._sunken_ships

    def set_num_of_ships(self, num: int):
        """Changes the number of ships to <num>.
        """
        self._num_of_ships = num

    def add_num_of_ships(self):
        """Adds one to the number of ships a player has.
        """
        self._num_of_ships += 1

    def get_num_of_ships(self) -> int:
        """Returns the total number of ships that the player has.
        """
        return self._num_of_ships

    def add_sunken_ship(self):
        """Increments the number of enemy ships you have sunken by one.
        """
        self._sunken_ships += 1

    def get_ships_left(self) -> int:
        """Return the number of ships that have not been sunk by enemy.
        """
        return self._remaining_ships

    def decrement_remaining_ships(self):
        """Decrease how many remaining ships this player has left, by one.
        """
        if self._remaining_ships > 0:
            self._remaining_ships -= 1

    def hit(self, coordinate: Tuple[int, int]) -> int:
        """Returns whether the a players ship is at <coordinate> and if a shot
        at <coordinate> would be a hit, miss, or sink a ship.
        """
        for ship in self._ships:
            result = ship.hit(coordinate)
            if(result != 0):
                return result
        return 0
