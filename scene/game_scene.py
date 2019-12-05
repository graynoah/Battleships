from typing import Tuple, List

import pygame
from pygame import Rect, Surface

from components.panel import Panel
from components.button import Button
from components.label import Label
from components.style import Style
from components.slider import Slider
from components.textbox import Textbox
from components.animated_grid import AnimatedGrid
from components.vertical_panel import VerticalPanel
from components.horizontal_panel import HorizontalPanel
from components.background_water import BackgroundWater
import managers.scene_manager as sm
import managers.event_manager as em
from managers.game_manager import GameManager
from util.observer import Observer
from components.pause_menu_panel import PauseMenuPanel


class GameScene(Observer):
    """The in game view.

    === Private Attributes ===
        _background_water:
            A component that displays the background as water.
        _player1_grids:
            A tuple containing the player 1 ship, hit, and miss grids.
        _player2_grids:
            A tuple containing player 2 ship, hit, and miss grids.
    """
    _player1_grids: Tuple[AnimatedGrid, AnimatedGrid, AnimatedGrid]
    _player2_grids: Tuple[AnimatedGrid, AnimatedGrid, AnimatedGrid]
    _background_water: BackgroundWater
    _pause_menu: PauseMenuPanel

    def __init__(self, root: Panel):
        """Create a new GameScene, creating the gui components to
        display and starting the game.
        """
        self._pause_menu = PauseMenuPanel(
            Rect(0, 0, 0, 0),
            style=Style(background_color=None,
                        border_width=0,
                        force_parent_redraw=True))

        # A style for all
        button_style = Style(background_color=(0, 255, 255),
                             primary_color=(0, 0, 0),
                             border_color=(0, 0, 0),
                             border_width=1)

        size = root.get_rect().size

        rect1 = Rect(size[0]/8, size[1]/8, size[0] * 3 / 8, size[1] * 3 / 4)
        rect2 = Rect(size[0]/2, size[1]/8, size[0] * 3 / 8, size[1] * 3 / 4)

        # The background water for the game
        self._background_water = BackgroundWater(
            rect=Rect(0, 0, size[0], size[1]), parent=root)

        # A style for for the pause button
        pause_style = Style(
            background_color=None,
            force_parent_redraw=True,
            border_color=(0, 0, 0),
            border_width=2,
            background_image=pygame.image.load(
                "images/pause.jpg"))

        # Pause Button
        Button(on_click=self._pause_clicked,
               rect=Rect(20, 20, 100, 100),
               style=pause_style,
               parent=self._background_water)

        # A style for player 1 grids
        player1_grid_style = Style(background_color=None,
                                   primary_color=(255, 0, 0, 100),
                                   secondary_color=(0, 0, 0, 200),
                                   border_color=(0, 0, 0),
                                   border_width=1,
                                   force_parent_redraw=True)

        # Create player 1 grids
        self._player1_grids = self._create_player_grids(
            rect1, player1_grid_style)

        # A style for player 2 grids
        player2_grid_style = Style(background_color=None,
                                   primary_color=(0, 255, 0, 50),
                                   secondary_color=(0, 0, 0, 200),
                                   border_color=(0, 0, 0),
                                   border_width=1,
                                   force_parent_redraw=True)

        # Create player 2 grids
        self._player2_grids = self._create_player_grids(
            rect2, player2_grid_style)

        # Setup observers
        player1 = GameManager.instance.get_player1()
        player2 = GameManager.instance.get_player2()
        player1.clear_observers()
        player2.clear_observers()
        player1.add_observer(self)
        player2.add_observer(self)

        # Start the game
        current_player = GameManager.instance.get_whos_turn()
        current_player.on_turn_started()
        current_player.notify_observers()

    def _create_player_grids(self, rect: Rect, style: Style) -> \
            Tuple[AnimatedGrid, AnimatedGrid, AnimatedGrid]:
        """Create a ship grid, hit grid, and miss grid. The function returns
        the grids as a list in the same order."""

        # A style for the hit and miss grids
        overlay_style = Style(background_color=None,
                              primary_color=(0, 0, 0, 0),
                              secondary_color=None,
                              border_color=None,
                              border_width=0,
                              force_parent_redraw=True)

        # A grid of boats
        ships = AnimatedGrid(rect=rect,
                             folder_path="images/boat",
                             style=style,
                             parent=self._background_water)

        # A grid of hits
        hits = AnimatedGrid(rect=rect,
                            folder_path="images/hit",
                            style=overlay_style,
                            parent=ships)

        # A grid of misses
        misses = AnimatedGrid(rect=rect,
                              folder_path="images/miss",
                              style=overlay_style,
                              parent=hits)

        return (ships, hits, misses)

    def _pause_clicked(self, button: int) -> None:
        """Open the pause menu."""
        self._pause_menu.set_parent(self._background_water)

    def on_notify(self) -> None:
        """Update the animated grids when the player makes a move."""
        current_player = GameManager.instance.get_whos_turn()
        player1 = GameManager.instance.get_player1()
        player2 = GameManager.instance.get_player2()

        player1_ships = []
        player2_ships = []

        # Setup the current player
        if(current_player is player1):
            player1_ships = player1.get_ships()
            self._player1_grids[2]._on_click_callback = None

            self._player2_grids[2]._on_click_callback = \
                GameManager.instance.square_clicked
        else:
            player2_ships = player2.get_ships()

            self._player1_grids[2]._on_click_callback = \
                GameManager.instance.square_clicked

            self._player2_grids[2]._on_click_callback = None

        # Ships
        self._player1_grids[0].set_tiles(
            self.ships_to_list(player1_ships))
        self._player2_grids[0].set_tiles(
            self.ships_to_list(player2_ships))

        # Hits
        self._player1_grids[1].set_tiles(
            self.guesses_to_list(player2.get_guesses(), True))
        self._player2_grids[1].set_tiles(
            self.guesses_to_list(player1.get_guesses(), True))

        # Misses
        self._player1_grids[2].set_tiles(
            self.guesses_to_list(player2.get_guesses(), False))
        self._player2_grids[2].set_tiles(
            self.guesses_to_list(player1.get_guesses(), False))

    def ships_to_list(self, ships) -> List[Tuple[int, int]]:
        """Convert a list of ships into a list of coordinates."""
        lst = []
        for ship in ships:
            for point in ship.get_hit_points():
                lst.append(point)

        return lst

    def guesses_to_list(self, guesses: Tuple[int, int, int], hit: bool):
        """Convert a list of guesses into a list of coordinates. <hit>
        speficies whether to include guesses that are hits or misses."""
        return [x[:2] for x in guesses if x[2] is hit]
