from typing import List, Callable

from pygame import Rect, Surface, mouse, BLEND_RGB_MULT, cursors

from util.constants import BUTTON_CURSOR
from components.label import Label
from components.style import Style
from components.component import Component


class Button(Label):
    """A GUI element that displays clickable text."""

    def __init__(self,
                 rect: Rect,
                 on_click: Callable[[int], None] = None,
                 text: str = "",
                 style: Style = None,
                 parent: Component = None) -> None:
        """Create a new Button. <rect> is the rectangle representing this
        component's position and size on the screen. <on_click> is the
        function called when the button is clicked. <text> is the text to be
        displayed. <style> dictates the appearence of the component. If None,
        the default style will be used. <parent> is the component that is
        immediately above this component in the tree.
        """
        Label.__init__(self, rect, text=text, style=style, parent=parent)

        if(on_click is not None):
            self._on_click = on_click

    def _draw(self, screen: Surface, changes: List[Rect]) -> None:
        """Draw the button's visuals to the screen. <change> is a list of
        rectangles that represent the changed areas of the screen.
        """
        Component._draw(self, screen, changes)

        # Draw hover color
        if(self.is_hovered()):
            changes.append(screen.fill(self._style.hover_color,
                                       self.get_rect(), BLEND_RGB_MULT))

        self._draw_text(screen, changes)

    def _on_hover_enter(self) -> None:
        """Change the mouse cursor when the mouse moves over the button."""
        mouse.set_cursor(*BUTTON_CURSOR)
        self._redraw()

    def _on_hover_exit(self) -> None:
        """Reset the mouse cursor when the mouse moves off the button."""
        mouse.set_cursor(*cursors.arrow)
        self._redraw()
