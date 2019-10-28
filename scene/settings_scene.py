import pygame
from pygame import event
from pygame import Rect, Surface

from components.component import Component
import managers.scene_manager as sm
from components.style import Style
from components.button import Button
from components.slider import Slider
from components.textbox import Textbox
from components.label import Label
from components.panel import Panel


class SettingsScene(object):
    """ The settings menu in Battleships. This menu allows user to
    adjust the sound fx, music volume, switch to full screen,
    and they can return to main menu.
    """

    def __init__(self, root: Component):
        self.is_fullscreen = False
        self.create_buttons(root)
        self.create_labels(root)
        self.create_sliders(root)

    def create_buttons(self, root: Component) -> None:
        """Create all buttons in the settings menu"""

        button_style = Style(background_color=(0, 255, 255),
                             primary_color=(0, 0, 0))

        self.back_button = Button(on_click=self._open_main_menu,
                                  rect=Rect(100, 450, 100, 100),
                                  style=Style(
                                      background_image=pygame.image.load(
                                          "images/left-arrow-icon.png"),
                                      background_color=(0, 255, 255),
                                      primary_color=(0, 0, 0)),
                                  parent=root)

        self.fullscreen_button = Button(on_click=self._toggle_fullscreen,
                                        text=self._get_window_mode_text(),
                                        rect=Rect(450, 320, 150, 50),
                                        style=button_style,
                                        parent=root)

    def create_labels(self, root: Component) -> None:
        """ Create all labels in the settings menu. """
        label_style = Style(background_color=(0, 128, 255),
                            primary_color=(255, 255, 255))

        self.return_back = Label(text="Return to main menu",
                                 rect=Rect(220, 475, 250, 50),
                                 style=Style(
                                     background_color=(0, 0, 0),
                                     primary_color=(255, 255, 255)),
                                 parent=root)

        self.soundFX = Label(text="Adjust Sound FX",
                             rect=Rect(150, 120, 250, 50),
                             style=label_style,
                             parent=root)

        self.music = Label(text="Music volume", rect=Rect(200, 200, 200, 50),
                           style=label_style, parent=root)

        self.menu = Label(text="CHANGE SETTINGS", rect=Rect(400, 0, 250, 90),
                          style=label_style,
                          parent=root)

        self.window_mode = Label(text="Window Mode",
                                 rect=Rect(200, 300, 200, 100),
                                 style=label_style,
                                 parent=root)

    def create_sliders(self, root: Component) -> None:
        """ Create all sliders in the settings menu. """
        slider_style = Style(background_color=(102, 0, 102),
                             primary_color=(255, 255, 204))

        self.soundFX_slider = Slider(on_value_changed=self._change_volume,
                                     rect=Rect(450, 140, 150, 20),
                                     style=slider_style,
                                     parent=root)

        self.music_slider = Slider(on_value_changed=self._change_volume,
                                   rect=Rect(450, 210, 150, 20),
                                   style=slider_style,
                                   parent=root)

    def _toggle_fullscreen(self, button: int) -> None:
        """Toggle the window mode between fullscreen and windowed."""
        sm.SceneManager.instance.toggle_fullscreen()

    def _get_window_mode_text(self) -> str:
        """Get the text to display on the window mode button."""
        if(sm.SceneManager.instance.is_fullscreen()):
            return "Fullscreen"
        else:
            return "Windowed"

    def _open_main_menu(self, buttn: int) -> None:
        """Switches to the main menu."""
        sm.SceneManager.instance.change_scene(0)

    def _change_volume(self, value: float) -> None:
        """ Change the volume of sound FX or music."""
        print("volume changed to ", value)
