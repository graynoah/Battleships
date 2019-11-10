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


class PauseMenuScene(object):
    def __init__(self, root: Panel):

        size = sm.SceneManager.instance.get_screen_size()
        title_rect = Rect(0, 0, 500, 70)
        title_rect.center = (size[0] / 2, size[1] / 2 - 200)

        self.options_panel = VerticalPanel(rect=Rect(size[0] / 4, size[1] / 2,
                                                     size[0] / 2, size[1] / 4),
                                           expand_height=False,
                                           parent=root)

        self.title_label = Label(text="BATTLE SHIP!",
                                 rect=title_rect,
                                 style=Style(background_color=None,
                                             border_width=0,
                                             font=pygame.font.Font(
                                                 'freesansbold.ttf', 64),
                                             primary_color=(255, 255, 255)),
                                 parent=root)

        button_style = Style(primary_color=(255, 255, 255),
                             background_color=(128, 0, 0),
                             border_width=1,
                             border_color=(0, 0, 0),
                             font=pygame.font.Font('freesansbold.ttf', 32))

        self.cont_button = Button(rect=Rect(0, 0, 400, 40),
                                 on_click=self._pvc_clicked,
                                 text="Continue",
                                 style=button_style,
                                 parent=self.options_panel)

        self.settings_button = Button(rect=Rect(0, 0, 400, 40),
                                      on_click=self._settings_clicked,
                                      text="Settings",
                                      style=button_style,
                                      parent=self.options_panel)

        self.quit_button = Button(rect=Rect(0, 0, 400, 40),
                                  on_click=self._quit_clicked,
                                  text="Quit",
                                  style=button_style,
                                  parent=self.options_panel)

    def _cont_clicked(self, button: int):
        pass
    
    def _settings_clicked(self, button: int):
        sm.SceneManager.instance.change_scene(1)

    def _quit_clicked(self, button: int):
        sm.SceneManager.instance.quit_game()
