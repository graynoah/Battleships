from typing import Tuple, List

import pygame

import managers.event_manager as em
from components.panel import Panel
from components.style import Style
from components.label import Label
from components.component import Component

from scene.game_scene import GameScene
from scene.main_menu_scene import MainMenuScene
from scene.settings_scene import SettingsScene


class SceneManager(object):
    """A Singleton that manages all scenes and tracks the appilcation's
    running state. The static instance variable can be used to access this
    object. This class must be created atleast once. The game loop will run
    until the application closes.

    === Private Attributes ===
        _screen_size:
            The size of the screen in pixels.
        _screen:
            The surface that represents the screen.
        _clock:
            A object that records the time inbettween calls to its tick
            function.
        _fps_counter:
            A label that displays the current framerate.
        _scenes:
            A list of all available scenes.
        _running:
            Whether or not the application is currently running.
    """
    instance = None

    _screen_size: Tuple[int, int]
    _screen: pygame.Surface
    _clock: pygame.time.Clock
    _fps_counter: Component
    _scenes: List
    _running: bool

    def __init__(self) -> None:
        """Create a new SceneManager and setup the static instance variable."""
        if(SceneManager.instance is None):
            SceneManager.instance = self

        pygame.init()
        # Open a new window
        self._screen_size = (960, 540)
        self._screen = pygame.display.set_mode(self._screen_size)
        # , (pygame.FULLSCREEN | pygame.HWSURFACE)
        pygame.display.set_caption("Battleships")
        pygame.key.set_repeat(250, 50)
        pygame.scrap.init()

        # The clock will be used to control how fast the screen updates
        self._clock = pygame.time.Clock()

        self._root = Panel(pygame.Rect(0, 0, 960, 540), style=Style(
            background_color=(255, 0, 0), border_width=0))

        em.EventManager()

        self._fps_counter = Label(text="Calculating", rect=pygame.Rect(
            960-200, 0, 200, 100), parent=self._root)

        self._scenes = [MainMenuScene, SettingsScene]
        self.change_scene(0)
        self._running = True
        self._run_game_loop()

    def get_root(self) -> Component:
        """Get the topmost component."""
        return self._root

    def change_scene(self, scene_index: int) -> None:
        """Switch the current scene to the scene at index <scene_index>."""
        self._root.clear_children()
        self._active_scene = self._scenes[scene_index](self._root)
        self._root.add_child(self._fps_counter)
        em.EventManager.instance.set_invalid()

    def quit_game(self) -> None:
        """Close the application."""
        self._running = False

    def _run_game_loop(self) -> None:
        """Run the game loop until the application closes"""
        while self._running:
            # Handle Events
            em.EventManager.instance.update()

            # Update
            self._root.update(self._clock.tick())  # Framerate Limit
            if(self._clock.get_fps() != float("inf")):
                self._fps_counter.set_text(str(int(self._clock.get_fps())))
            else:
                self._fps_counter.set_text("Infinity")

            # Draw
            changed = []
            self._root.render(self._screen, changed)
            pygame.display.update(changed)

        pygame.quit()
