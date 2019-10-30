import pygame
from pygame import Rect, Surface

from components.panel import Panel
from components.button import Button
from components.label import Label
from components.style import Style
from components.slider import Slider
from components.textbox import Textbox
import managers.scene_manager as sm


class MainMenuScene(object):
    def __init__(self, root: Panel):

        WIDTH, HEIGHT = sm.SceneManager.instance.get_screen_size()
        title_rect = Rect(0, 0, 500, 70)
        pvc_rect = Rect(0, 0, 400, 40)
        pvp_rect = Rect(0, 0, 400, 40)
        settings_rect = Rect(0, 0, 400, 40)
        quit_rect = Rect(0, 0, 400, 40)

        title_rect.center = (WIDTH/2, HEIGHT/4)
        pvc_rect.center = (WIDTH/2, (HEIGHT/2) + (HEIGHT/20))
        pvp_rect.center = (WIDTH/2, (HEIGHT/2) + (3*HEIGHT/20))
        settings_rect.center = (WIDTH/2, (HEIGHT/2) + (5*HEIGHT/20))
        quit_rect.center = (WIDTH/2, (HEIGHT/2) + (7*HEIGHT/20))

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

        self.pvc_button = Button(on_click=self._pvc_clicked,
                                 text="Player vs Computer",
                                 rect=pvc_rect,
                                 style=button_style,
                                 parent=root)

        self.pvp_button = Button(on_click=self._pvp_clicked,
                                 text="Player vs Player",
                                 rect=pvp_rect,
                                 style=button_style,
                                 parent=root)

        self.settings_button = Button(on_click=self._settings_clicked,
                                      text="Settings",
                                      rect=settings_rect,
                                      style=button_style,
                                      parent=root)

        self.quit_button = Button(on_click=self._quit_clicked,
                                  text="Quit",
                                  rect=quit_rect,
                                  style=button_style,
                                  parent=root)

    def _pvc_clicked(self, button: int):
        pass

    def _pvp_clicked(self, button: int):
        pass

    def _settings_clicked(self, button: int):
        sm.SceneManager.instance.change_scene(1)

    def _quit_clicked(self, button: int):
        sm.SceneManager.instance.quit_game()
