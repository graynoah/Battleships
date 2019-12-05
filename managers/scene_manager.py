from typing import Tuple, List
import os

import pygame

import managers.event_manager as em
from components.panel import Panel
from components.style import Style
from components.label import Label
from components.component import Component
from util.constants import DEFAULT_WINDOWED_MODE_SIZE, MINIMUM_SCREEN_SIZE

from scene.game_scene import GameScene
from scene.main_menu_scene import MainMenuScene
from scene.settings_scene import SettingsScene
from scene.pause_menu_scene import PauseMenuScene


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
        _is_fullscreen:
            Whether or not the application is currently in fullscreen mode.
        _active_scene_index:
            The currently active scene's index.
        _active_scene:
            The currently active scene.
    """
    instance = None

    _screen_size: Tuple[int, int]
    _screen: pygame.Surface
    _clock: pygame.time.Clock
    _fps_counter: Component
    _scenes: List
    _running: bool
    _is_fullscreen: bool
    _active_scene_index: int
    _active_scene: object

    def __init__(self) -> None:
        """Create a new SceneManager and setup the static instance variable."""
        if(SceneManager.instance is None):
            SceneManager.instance = self

        # Tell pygame to center the window
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.font.init()

        self._screen_size = (0, 0)
        self._is_fullscreen = True
        self._clock = pygame.time.Clock()
        self._scenes = [MainMenuScene,
                        SettingsScene, GameScene, PauseMenuScene]
        self._running = True

        self._setup_screen()

        # Always visible components
        self._root = Panel(self._screen.get_rect(), style=Style(
            background_color=(255, 0, 0), border_width=0))

        self._fps_counter = Label(text="Calculating",
                                  rect=pygame.Rect(0, 25, 75, 20),
                                  style=Style(
                                      background_color=(255, 0, 0),
                                      border_width=0,
                                      primary_color=(255, 255, 255)),
                                  parent=self._root)
        self._rest_fps_counter_position()

        # Start the game
        self.change_scene(0)
        self._run_game_loop()

    def set_screen_size(self, size: Tuple[int, int]) -> None:
        """Set the screen size. This method re-creates the active scene."""
        em.EventManager.instance.set_invalid()
        if (self._is_fullscreen):
            self._screen_size = (0, 0)
        else:
            self._screen_size = (max(size[0], MINIMUM_SCREEN_SIZE[0]),
                                 max(size[1], MINIMUM_SCREEN_SIZE[1]))
        self._setup_screen()
        self._root.set_rect(self._screen.get_rect())
        self._rest_fps_counter_position()
        self.change_scene(self._active_scene_index)

    def _setup_screen(self) -> None:
        """Create the screen object."""
        pygame.display.init()
        pygame.display.set_caption("Battleships")
        pygame.key.set_repeat(250, 50)

        flags = pygame.RESIZABLE
        if(self._is_fullscreen):
            flags |= pygame.FULLSCREEN

        self._screen = pygame.display.set_mode(self._screen_size, flags)
        self._screen_size = self._screen.get_rect().size

    def is_fullscreen(self) -> bool:
        """Whether or not the the application is in fullscreen mode."""
        return self._is_fullscreen

    def toggle_fullscreen(self) -> None:
        """Toggles the application mode between fullscreen and windowed."""
        self._is_fullscreen = not self._is_fullscreen
        pygame.display.quit()

        if(self._is_fullscreen):
            self.set_screen_size((0, 0))
        else:
            self.set_screen_size(DEFAULT_WINDOWED_MODE_SIZE)

    def _rest_fps_counter_position(self):
        """Sets the position of the fps counter."""
        fps_rect = self._fps_counter.get_rect()
        fps_rect.right = self._screen_size[0] - 25
        self._fps_counter.set_rect(fps_rect)

    def get_screen_size(self) -> Tuple[int, int]:
        """Get the size of the screen in pixels."""
        return self._screen_size

    def get_root(self) -> Component:
        """Get the topmost component."""
        return self._root

    def change_scene(self, scene_index: int) -> None:
        """Switch the current scene to the scene at index <scene_index>."""
        self._root.clear_children()
        self._active_scene_index = scene_index
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
