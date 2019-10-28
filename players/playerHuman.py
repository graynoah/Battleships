from players.player import Player


class PlayerHuman(Player):
    """ A Human player in the battleships game
    """

    def __init__(self, name: str):
        Player.__init__(self, name)

    def attack(self):
        """Allow the player to input a move to be made
        """
        # TODO

        while True:
            print("Enter the row and col you would like to attack:")
            row = input("row:")
            col = input("col:")
            if self.is_valid_coordinate(row, col):
                print("You shot at [" + row + ", " + col + "].")
                break
            else:
                print("That is not a valid coordinate")

