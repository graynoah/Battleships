import pygame


class HUDManager(object):
    """ A Heads Up Display indicating the player's statistics.
    Player stats include: how many opponent ships have they sunk and
    how many of their own ships remain on the grid.
    """

    def __init__(self):
        """Initialize a Heads Up Display for a human player. 
        """
        self._num_ships_hit = 0
        self._num_ships_left = 0
        self._hit_percentage = 0


    def get_enemy_ships_hit(self)->int:
        """ Return number of enemy ships this player has successfully hit. 
        """
        return self._num_ships_hit = 0
    
    def get_num_remaining_ships(self)->int:
        """ Return number of ships that have not been sunk by enemy.
        """
        return self._num_ships_left
    
    def get_hit_percentage(self)->int:
        """ Return the percentage of accuracy the player has
        when it comes to hitting enemy ships. A high hit percentage
        corresponds to a high number of enemy ships hit. 
        """
        return self._hit_percentage
    
    
