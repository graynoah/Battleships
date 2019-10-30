from typing import List

from pygame import Rect, Surface

from components.component import Component
from components.style import Style


class Label(Component):
    """A GUI element that displays text.

    === Private Attributes ===
        _text:
            The text to be displayed.
        _text_image:
            The surface of the rendered text.
    """
    _text: str
    _text_image: Surface

    def __init__(self,
                 rect: Rect,
                 text: str = "",
                 style: Style = None,
                 parent: Component = None) -> None:
        """Create a new Label. <rect> is the rectangle representing this
        component's position and size on the screen. <text> is the text to be
        displayed. <style> dictates the appearence of the component. If None,
        the default style will be used. <parent> is the component that is
        immediately above this component in the tree.
        """
        Component.__init__(self, rect, style=style, parent=parent)
        self.set_text(text)

    def get_text(self) -> str:
        """Get the displayed text."""
        return self._text

    def set_text(self, text: str) -> None:
        """Set the displayed text."""
        self._text = text
        self._text_image = self._style.font.render(
            text, True, self._style.primary_color)
        self._redraw()

    def _draw(self, screen: Surface, changes: List[Rect]) -> None:
        """Draw the label's background and text to the <screen>. <change> is a
        list of rectangles that represent the changed areas of the screen.
        """
        Component._draw(self, screen, changes)
        self._draw_text(screen, changes)

    def _draw_text(self, screen: Surface, changes: List[Rect]) -> None:
        """Draw the label's text to the <screen>. <change> is a list of
        rectangles that represent the changed areas of the screen.
        """
        orignal_rect = self._text_image.get_rect()

        centered_rect = orignal_rect.copy()
        centered_rect.center = self._rect.center

        clip_rect = centered_rect.clip(self._rect)
        centered_clip_rect = clip_rect.copy()
        centered_clip_rect.center = orignal_rect.center

        changes.append(screen.blit(self._text_image,
                                   clip_rect, centered_clip_rect))
