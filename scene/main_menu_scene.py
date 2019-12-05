import pygame
from pygame import Rect, Surface

from components.panel import Panel
from components.button import Button
from components.label import Label
from components.style import Style
from components.slider import Slider
from components.textbox import Textbox
from components.vertical_panel import VerticalPanel
import managers.scene_manager as sm
from managers.game_manager import GameManager
from players.playerHuman import PlayerHuman


class MainMenuScene(object):
    """A menu menu for the game."""

    def __init__(self, root: Panel):
        """Create a new MainMenuScene, creating the gui components to
        display.
        """
        size = root.get_rect().size
        title_rect = Rect(0, 0, 500, 70)
        title_rect.center = (size[0] / 2, size[1] / 2 - 200)

        # A panel for all the options
        options_panel = VerticalPanel(rect=Rect(size[0] / 4, size[1] / 2,
                                                size[0] / 2, size[1] / 4),
                                      expand_height=False,
                                      parent=root)

        # Title label
        Label(text="BATTLE SHIP!",
              rect=title_rect,
              style=Style(background_color=None,
                          border_width=0,
                          font=pygame.font.Font(
                              'freesansbold.ttf', 64),
                          primary_color=(255, 255, 255)),
              parent=root)

        # A style for all of the menu options
        button_style = Style(primary_color=(255, 255, 255),
                             background_color=(128, 0, 0),
                             border_width=1,
                             border_color=(0, 0, 0),
                             font=pygame.font.Font('freesansbold.ttf', 32))

        # Player vs Computer button
        Button(rect=Rect(0, 0, 400, 40),
               on_click=self._pvc_clicked,
               text="Player vs Computer",
               style=button_style,
               parent=options_panel)

        # Player vs Player button
        Button(rect=Rect(0, 0, 400, 40),
               on_click=self._pvp_clicked,
               text="Player vs Player",
               style=button_style,
               parent=options_panel)

        # Settings button
        Button(rect=Rect(0, 0, 400, 40),
               on_click=self._settings_clicked,
               text="Settings",
               style=button_style,
               parent=options_panel)

        # Quit button
        Button(rect=Rect(0, 0, 400, 40),
               on_click=self._quit_clicked,
               text="Quit",
               style=button_style,
               parent=options_panel)

    def _pvc_clicked(self, button: int):
        """Start a new game of player vs computer."""
        GameManager.instance.setup_game(
            PlayerHuman("Player"), PlayerHuman("Computer"))
        sm.SceneManager.instance.change_scene(2)

    def _pvp_clicked(self, button: int):
        """Start a new game of player vs player."""
        GameManager.instance.setup_game(
            PlayerHuman("Player1"), PlayerHuman("Player2"))
        sm.SceneManager.instance.change_scene(2)

    def _settings_clicked(self, button: int):
        """Open the settings menu."""
        sm.SceneManager.instance.change_scene(1)

    def _quit_clicked(self, button: int):
        """Close the game."""
        sm.SceneManager.instance.quit_game()
