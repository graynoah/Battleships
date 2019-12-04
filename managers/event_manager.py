from typing import Tuple

import pygame

from components.component import Component
import managers.scene_manager as sm


class EventManager(object):
    """A Singleton that manages all pygame events. The static instance
    variable can be used to access this object. This class must be created
    atleast once.

    === Private Attributes ===
        _is_invalid:
            Whether or not the EventManger needs to reset the hovered
            component.
        _pressed_button:
            The mouse button that is currently pressed.
        _focused_component:
            The component that is currently recieves all events.
        _hovered_component:
            The component that the mouse is currently over.
    """
    instance = None

    _is_invalid: bool
    _pressed_button: int
    _focused_component: Component
    _hovered_component: Component

    def __init__(self) -> None:
        """Create a new EventManager and setup the static instance variable."""
        if(EventManager.instance is None):
            EventManager.instance = self

        self._is_invalid = True
        self._pressed_button = -1
        self._focused_component = None
        self._hovered_component = None

    def get_focused_component(self) -> Component:
        """Get the currently focused component."""
        return self._focused_component

    def get_hovered_component(self) -> Component:
        """Get the currently hovered component."""
        return self._hovered_component

    def blur_focused_component(self) -> None:
        """Blur the curretly focused component."""
        self._set_focused_component(None)

    def set_invalid(self) -> None:
        """Mark the EventManager to reset the hovered component next update
        cycle.
        """
        self._is_invalid = True

    def update(self) -> None:
        if(self._is_invalid):
            self._is_invalid = False
            self._invalidate()

        # Poll Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sm.SceneManager.instance.quit_game()

            elif(event.type == pygame.VIDEORESIZE):
                sm.SceneManager.instance.set_screen_size((event.w, event.h))

            elif(not sm.SceneManager.instance.get_root().is_enabled()):
                return

            elif(event.type == pygame.MOUSEMOTION):
                self._invalidate()

                if(self._pressed_button != -1):
                    if(self._focused_component is not None):
                        self._focused_component._on_drag()

            elif(event.type == pygame.MOUSEBUTTONUP):
                if((event.button == 1 or event.button == 3) and
                        self._pressed_button == event.button):

                    hit = self._hit_test(
                        event.pos, sm.SceneManager.instance.get_root())
                    if(hit is self._focused_component):
                        self._focused_component._on_click(self._pressed_button)
                    else:
                        self._set_hovered_component(hit)

                    self._pressed_button = -1

            elif(event.type == pygame.MOUSEBUTTONDOWN):
                if(event.button == 1 or event.button == 3):
                    self._pressed_button = event.button
                    self._set_focused_component(self._hovered_component)

            elif(event.type == pygame.KEYDOWN):
                if(self._focused_component is not None):
                    self._focused_component._on_key_press(
                        event.key, event.unicode, event.mod)

    def _invalidate(self) -> None:
        """Reset the hovered component. Does nothing if the mouse is currently
        pressed.
        """
        if(self._pressed_button == -1):
            self._set_hovered_component(
                self._hit_test(pygame.mouse.get_pos(),
                               sm.SceneManager.instance.get_root()))

    def _hit_test(self,
                  pos: Tuple[int, int],
                  component: Component) -> Component:
        """Get which component is at postion <pos> starting from <component>"""

        children = component.get_children()
        for i in range(len(children) - 1, -1, -1):

            hit = self._hit_test(pos, children[i])
            if(hit is not None):
                return hit

        if(component.get_rect().collidepoint(pos) and component.is_enabled()):
            return component

        return None

    def _set_hovered_component(self, hovered_component: Component) -> None:
        """Set the hovered component. Does nothing if <hovered_component> is
        already the hovered component
        """
        if(self._hovered_component is not hovered_component):
            if(self._hovered_component is not None):
                self._hovered_component._on_hover_exit()

            self._hovered_component = hovered_component
            self._hovered_component._on_hover_enter()

    def _set_focused_component(self, focused_component: Component) -> None:
        """Set the focused component. Does nothing if <focused_component> is
        already the focused component
        """
        if(self._focused_component is not focused_component):
            if(self._focused_component is not None):
                self._focused_component._on_blur()

            self._focused_component = focused_component

            if(self._focused_component is not None):
                self._focused_component._on_focus()
