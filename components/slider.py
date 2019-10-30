from typing import Callable, List

from pygame import Rect, Surface, mouse, draw

from components.component import Component
from components.style import Style


class Slider(Component):
    """A GUI element that allows the user to click and drag to input a value.

    === Private Attributes ===
        _on_value_changed:
            The function that is called when the slider's value is changed.
        _min_value:
            The smallest number the slider can have.
        _max_value:
            The largest number the slider can have.
        _value:
            The current value of the slider.
        _handle_radius:
            The size of the handle.
        _fill_rect:
            A rectangle representing the usable dragging area.
    """
    _on_value_changed: Callable[[float], None]
    _min_value: float
    _max_value: float
    _value: float
    _handle_radius: int
    _fill_rect: Rect

    def __init__(self,
                 rect: Rect,
                 on_value_changed: Callable[[float], None] = None,
                 value: float = 0,
                 min_value: float = 0,
                 max_value: float = 1,
                 show_handle: bool = True,
                 style: Style = None,
                 parent: Component = None) -> None:
        """Create a new Button. <rect> is the rectangle representing this
        component's position and size on the screen. <on_value_changed> is the
        function called when the slider's value is changed. <value> is the
        starting value of the slider. <min_value> is the smallest number the
        slider can have. <max_value> is the largest number the slider can have.
        <show_handle> is whether or not the handle should be displayed. <style>
        dictates the appearence of the component. If None, the default style
        will be used. <parent> is the component that is
        immediately above this component in the tree.
        """
        self._show_handle = show_handle
        Component.__init__(self, rect, style=style, parent=parent)

        self._value = value
        self._min_value = min_value
        self._max_value = max_value
        self._on_value_changed = on_value_changed

    def set_rect(self, rect: Rect) -> None:
        """Set the slider's rectangle and update the useful area."""
        Component.set_rect(self, rect)
        self._fill_rect = rect.inflate(
            -2 * self._style.border_width,
            -2 * self._style.border_width)

        if(self._show_handle):
            self._handle_radius = self._fill_rect.height // 2
            self._fill_rect.inflate_ip(-2 * self._handle_radius,
                                       -self._handle_radius)

    def get_value(self) -> float:
        """Get the current value of slider."""
        return self._value

    def _on_focus(self) -> None:
        """Set the slider's value depending on where the mouse is when the
        slider comes into focus.
        """
        self._update_value()

    def _on_click(self, button: int) -> None:
        """Set the slider's value depending on where the mouse is when the
        slider is clicked.
        """
        self._update_value()

    def _on_drag(self) -> None:
        """Set the slider's value depending on where the mouse is when the
        slider is dragged.
        """
        self._update_value()

    def _update_value(self) -> None:
        """Change the slider's value depending on where the mouse is."""
        x, y = mouse.get_pos()
        normalized_value = (x - self._fill_rect.x) / self._fill_rect.width
        normalized_value = max(0, min(1, normalized_value))

        new_value = self._min_value + \
            (self._max_value - self._min_value) * normalized_value

        if(self._value != new_value):
            self._value = new_value
            self._redraw()

            if(self._on_value_changed is not None):
                self._on_value_changed(new_value)

    def _draw(self, screen: Surface, changes: List[Rect]) -> None:
        """Draw the slider's visuals to the screen. <change> is a list of
        rectangles that represent the changed areas of the screen.
        """
        Component._draw(self, screen, changes)

        # Fill Background
        changes.append(screen.fill(self._style.primary_color, self._fill_rect))

        filled_rect = self._fill_rect.copy()
        filled_rect.width = filled_rect.width * \
            (self._value - self._min_value) / \
            (self._max_value - self._min_value)

        # Fill Foreground
        changes.append(screen.fill(self._style.secondary_color, filled_rect))

        if(self._show_handle):
            # Handle Fill
            changes.append(draw.circle(
                screen, self._style.tertiary_color,
                filled_rect.midright, self._handle_radius-1))

            # Handle Outline
            if(self._style.border_width > 0 and
               self._style.border_color is not None):

                changes.append(draw.circle(
                    screen, self._style.border_color, filled_rect.midright,
                    self._handle_radius, self._style.border_width))
