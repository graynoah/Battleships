from typing import Optional

import pygame
from pygame import Rect, Surface

from components.component import Component
from components.panel import Panel
from components.button import Button
from components.label import Label
from components.style import Style
from components.slider import Slider
from components.textbox import Textbox
from components.vertical_panel import VerticalPanel
import managers.scene_manager as sm


class PauseMenuPanel(Panel):

    def set_parent(self, parent: Optional[Component]) -> None:
        """Set the component's parent. The default style is used if <parent>
        is None.
        """
        Panel.set_parent(self, parent)

        if(self._parent is None):
            return

        self.set_rect(self._parent.get_rect())
        size = self.get_rect().size

        title_rect = Rect(0, 0, 500, 70)
        title_rect.center = (size[0] / 2, size[1] / 2 - 200)

        self.clear_children()

        self.options_panel = VerticalPanel(rect=Rect(size[0] / 4, size[1] / 2,
                                                     size[0] / 2, size[1] / 4),
                                           expand_height=False,
                                           parent=self)

        self.title_label = Label(text="BATTLE SHIP!",
                                 rect=title_rect,
                                 style=Style(background_color=None,
                                             border_width=0,
                                             font=pygame.font.Font(
                                                 'freesansbold.ttf', 64),
                                             primary_color=(255, 255, 255)),
                                 parent=self)

        button_style = Style(primary_color=(255, 255, 255),
                             background_color=(128, 0, 0),
                             border_width=1,
                             border_color=(0, 0, 0),
                             font=pygame.font.Font('freesansbold.ttf', 32))

        self.cont_button = Button(rect=Rect(0, 0, 400, 40),
                                  on_click=self._cont_clicked,
                                  text="Continue",
                                  style=button_style,
                                  parent=self.options_panel)

        self.main_menu_button = Button(rect=Rect(0, 0, 400, 40),
                                       on_click=self._main_menu_clicked,
                                       text="Main menu",
                                       style=button_style,
                                       parent=self.options_panel)

        self.quit_button = Button(rect=Rect(0, 0, 400, 40),
                                  on_click=self._quit_clicked,
                                  text="Quit",
                                  style=button_style,
                                  parent=self.options_panel)

    def _cont_clicked(self, button: int):
        self.set_parent(None)

    def _main_menu_clicked(self, button: int):
        sm.SceneManager.instance.change_scene(0)

    def _quit_clicked(self, button: int):
        sm.SceneManager.instance.quit_game()
