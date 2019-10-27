from __future__ import annotations

from typing import List

from pygame import Rect, Surface, transform

from components.style import Style
import managers.event_manager as em


class Component(object):
    """A base class for all GUI elements.

    === Private Attributes ===
        _rect:
            The rectangle representing this component's position and size on
            the screen.
        _needs_redraw:
            Whether or not this component should be redrawn next render cycle.
        _is_enabled:
            Whether or not this component is active.
        _children:
            A list of all child components
        _style:
            A Style object that dictates the appearance of the component
        _parent:
            The component immediately above this component in the tree
    """
    _rect: Rect
    _needs_redraw: bool
    _is_enabled: bool
    _children: List[Component]
    _style: Style
    _parent: Component

    def __init__(self,
                 rect: Rect,
                 style: Style = None,
                 parent: Component = None) -> None:
        """Create a new Component. <rect> is the rectangle representing this
        component's position and size on the screen. <style> dictates the
        appearence of the component. If None, the default style will be used.
        <parent> is the component that is immediately above this component in
        the tree.
        """
        self._needs_redraw = False
        self._is_enabled = True
        self._children = []
        self.set_style(style)
        self._parent = None
        self.set_parent(parent)
        self.set_rect(rect)

    def set_rect(self, rect: Rect) -> None:
        """Set the component's rectangle."""
        self._rect = rect

    def set_style(self, style: Optional[Style]) -> None:
        """Set the component's style. The default style is used if <style> is
        None.
        """
        self._style = style

        if(style is None):
            self._style = Style()

        self._redraw()

    def set_parent(self, parent: Optional[Component]) -> None:
        """Set the component's parent. The default style is used if <parent>
        is None.
        """
        if(parent is None):
            if(self._parent is not None):
                self._parent.remove_child(self)
        else:
            parent.add_child(self)

    def add_child(self, child: Component) -> None:
        """Add a component as a child. Does nothing if <child>
        is already a child component.
        """
        if(child not in self._children):
            if(child._parent is not None):
                child._parent.remove_child(child)

            child._parent = self
            self._children.append(child)
            self._redraw()
            em.EventManager.instance.set_invalid()

    def remove_child(self, child: Component) -> None:
        """Remove a child component. Does nothing if <child>
        is not a child component.
        """
        for i in range(len(self._children)-1, -1, -1):
            if(self._children[i] == child):
                self._children.pop(i)._parent = None
                self._redraw()
                em.EventManager.instance.set_invalid()
                return

    def clear_children(self) -> None:
        """Remove all child components."""
        for i in range(len(self._children)-1, -1, -1):
            self._children.pop(i)._parent = None
        self._redraw()
        em.EventManager.instance.set_invalid()

    def get_children(self) -> List[Component]:
        """Get a list of all child components."""
        return self._children

    def enable(self) -> None:
        """Turn on the component. Does nothing if the component is already
        enabled.
        """
        if(not self._is_enabled):
            self._is_enabled = True
            self._redraw()
            em.EventManager.instance.set_invalid()

    def disable(self) -> None:
        """Turn off the component. Does nothing if the component is already
        disabled.
        """
        if(self._is_enabled):
            self._is_enabled = False
            em.EventManager.instance.set_invalid()
            self._blur_children()

            if(self._parent is not None):
                self._parent._redraw()

    def blur(self) -> None:
        """Blur the component. Does nothing if the component is not focused."""
        if(self.is_focused()):
            em.EventManager.instance.blur_focused_component()

    def is_hovered(self) -> bool:
        """Return whether or not the mouse is over the component."""
        return em.EventManager.instance.get_hovered_component() is self

    def is_focused(self) -> bool:
        """Return whether or not the component is focused."""
        return em.EventManager.instance.get_focused_component() is self

    def is_enabled(self) -> bool:
        """Return whether or not the component is enabled."""
        return self._is_enabled

    def get_rect(self) -> Rect:
        """Get the component's rectangle."""
        return self._rect

    def update(self, dt: float) -> None:
        """Update the component. <dt> is the time since last update in
        milliseconds.
        """
        for child in self._children:
            child.update(dt)

    def render(self, screen: Surface, changes: List[Rect]) -> None:
        """Render the component to the <screen>. <change> is a list of
        rectangles that represent the changed areas of the screen.
        """
        if(not self._is_enabled):
            return

        if(self._needs_redraw):
            self._needs_redraw = False
            self._draw(screen, changes)

        for child in self._children:
            child.render(screen, changes)

    def _redraw(self) -> None:
        """Mark the component to be redrawn next render cycle. Does nothing
        if the component is already marked for being redrawn.
        """
        if(not self._needs_redraw):
            if(self._style.force_parent_redraw and self._parent is not None):
                self._parent._redraw()
            else:
                self._redraw_children()

    def _draw(self, screen: Surface, changes: List[Rect]) -> None:
        """Draw the component's visuals to the <screen>. <change> is a list of
        rectangles that represent the changed areas of the screen.
        """

        # Draw background_color
        if(self._style.background_color is not None):
            changes.append(screen.fill(
                self._style.background_color, self._rect))

        # Draw Background Image
        if(self._style.background_image is not None):
            changes.append(screen.blit(transform.scale(
                self._style.background_image, (self._rect.w, self._rect.h)),
                self._rect))

        # Draw Border
        if(self._style.border_color is not None and
           self._style.border_width > 0):
            top_rect = Rect(self._rect.x, self._rect.y,
                            self._rect.w, self._style.border_width)

            bottom_rect = Rect(self._rect.x, self._rect.y + self._rect.height -
                               self._style.border_width,
                               self._rect.width, self._style.border_width)

            left_rect = Rect(self._rect.x, self._rect.y,
                             self._style.border_width, self._rect.height)

            right_rect = Rect(self._rect.x + self._rect.width -
                              self._style.border_width, self._rect.y,
                              self._style.border_width, self._rect.height)

            changes.append(screen.fill(self._style.border_color, top_rect))
            changes.append(screen.fill(self._style.border_color, bottom_rect))
            changes.append(screen.fill(self._style.border_color, left_rect))
            changes.append(screen.fill(self._style.border_color, right_rect))

    def _redraw_children(self) -> None:
        """Mark the component and all child components to be redrawn next
        render cycle.
        """
        self._needs_redraw = True

        for child in self._children:
            child._redraw_children()

    def _blur_children(self) -> None:
        """Blur the component and all child components."""
        self.blur()
        for child in self._children:
            child._blur_children()

    # Event Callbacks
    def _on_click(self, button: int) -> None:
        """Called when the component is clicked."""
        pass

    def _on_hover_enter(self) -> None:
        """Called when the mouse moves over the component."""
        pass

    def _on_hover_exit(self) -> None:
        """Called when the mouse moves off the component."""
        pass

    def _on_drag(self) -> None:
        """Called when the mouse is pressed and the component is focused."""
        pass

    def _on_focus(self) -> None:
        """Called when the component comes into focus."""
        pass

    def _on_blur(self) -> None:
        """Called when the component goes out of focus."""
        pass

    def _on_key_press(self, key: int, character: str, modifiers: int) -> None:
        """Called when a key is pressed and the component is focused."""
        pass
