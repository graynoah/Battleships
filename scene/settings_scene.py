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
from components.horizontal_panel import HorizontalPanel
from components.vertical_panel import VerticalPanel
import managers.audio_manager as am


class SettingsScene(object):
    """ The settings menu in Battleships. This menu allows user to
    adjust the sound fx, music volume, switch to full screen,
    and they can return to main menu.
    """

    def __init__(self, root: Component):
        self.create_panels(root)
        self.create_labels(root)
        self.create_buttons(root)
        self.create_sliders(root)

    def create_buttons(self, root: Component) -> None:
        """Create all buttons in the settings menu"""

        button_style = Style(background_color=(0, 255, 255),
                             primary_color=(0, 0, 0),
                             border_color=(0, 0, 0),
                             border_width=1)

        size = sm.SceneManager.instance.get_screen_size()
        self.back_button = Button(on_click=self._open_main_menu,
                                  rect=Rect(20, 20, 100, 100),
                                  style=Style(
                                      background_color=(255, 0, 0),
                                      background_image=pygame.image.load(
                                          "images/left-arrow-icon.png")),
                                  parent=root)

        self.fullscreen_button = Button(on_click=self._toggle_fullscreen,
                                        text=self._get_window_mode_text(),
                                        rect=Rect(450, 320, 150, 50),
                                        style=button_style,
                                        parent=self.window_mode_panel)

    def create_panels(self, root: Component):
        size = sm.SceneManager.instance.get_screen_size()
        self.options_panel = VerticalPanel(rect=Rect(size[0]/4, size[1]/4,
                                                     size[0] / 2, size[1] / 2),
                                           expand_height=False,
                                           parent=root)

        self.soundFx_panel = HorizontalPanel(rect=Rect(150, 120, 500, 50),
                                             parent=self.options_panel)

        self.music_panel = HorizontalPanel(rect=Rect(150, 120, 500, 50),
                                           parent=self.options_panel)

        self.window_mode_panel = HorizontalPanel(rect=Rect(150, 120, 500, 50),
                                                 parent=self.options_panel)

    def create_labels(self, root: Component) -> None:
        """ Create all labels in the settings menu. """
        label_style = Style(background_color=(0, 128, 255),
                            primary_color=(255, 255, 255))

        self.soundFX = Label(text="Adjust Sound FX",
                             rect=Rect(150, 120, 250, 50),
                             style=label_style,
                             parent=self.soundFx_panel)

        self.music = Label(text="Music volume", rect=Rect(200, 200, 200, 50),
                           style=label_style, parent=self.music_panel)

        self.window_mode = Label(text="Window Mode",
                                 rect=Rect(200, 300, 200, 100),
                                 style=label_style,
                                 parent=self.window_mode_panel)

        size = sm.SceneManager.instance.get_screen_size()
        title_rect = Rect(400, 45, 250, 50)
        title_rect.centerx = size[0]/2

        self.menu = Label(text="CHANGE SETTINGS", rect=title_rect,
                          style=label_style,
                          parent=root)

    def create_sliders(self, root: Component) -> None:
        """ Create all sliders in the settings menu. """
        slider_style = Style(background_color=(255, 0, 0),
                             primary_color=(255, 255, 204),
                             secondary_color=(102, 0, 102),
                             tertiary_color=(255, 0, 128))

        self.soundFX_slider = Slider(
            on_value_changed=am.AudioManager.instance.set_fx_volume,
            value=am.AudioManager.instance.get_fx_volume(),
            rect=Rect(450, 140, 150, 20),
            style=slider_style,
            parent=self.soundFx_panel)

        self.music_slider = Slider(
            on_value_changed=am.AudioManager.instance.set_music_volume,
            value=am.AudioManager.instance.get_music_volume(),
            rect=Rect(450, 210, 150, 20),
            style=slider_style,
            parent=self.music_panel)

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
