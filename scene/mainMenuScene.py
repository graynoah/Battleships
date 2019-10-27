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
        def test(buttn: int):
            print("Nimra")
            if(self.test_but.is_enabled()):
                self.test_but.disable()
            else:
                self.test_but.enable()

        def open_settings(buttn: int):
            sm.SceneManager.instance.change_scene(1)

        def test2(value: float):
            print("value changed", value)
            self.test_but.enable()

        def test3(value: str):
            print("value changed", value)
            self.test_but.enable()

        self.test_but = Button(on_click=test, text="lol",
                               rect=Rect(200, 200, 200, 100),
                               style=Style(background_color=(
                                   0, 255, 0), primary_color=(0, 0, 255)),
                               parent=root)

        self.test_but = Button(on_click=open_settings, text="Settings",
                               rect=Rect(300, 300, 200, 100),
                               style=Style(background_color=(
                                   0, 255, 255), primary_color=(0, 0, 255)),
                               parent=root)

        # test_slider = Slider(on_value_changed=test2,
        #                         rect=Rect(400, 200, 200, 20),
        #                         style=Style(background_color=(
        #                             0, 0, 255), primary_color=(0, 255, 0)),
        #                         parent=root)

        # test_textbox = Textbox(on_edit_finished=test3,
        #                         text="Calculating",
        #                         rect=Rect(500, 0, 200, 100), parent=root)
