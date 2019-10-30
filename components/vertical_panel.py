from pygame import Rect

from components.component import Component
from components.style import Style


class VerticalPanel(Component):
    """A layout element that lays outs its children vertically."""

    def __init__(self,
                 rect: Rect,
                 expand_width: bool = True,
                 expand_height: bool = True,
                 space_around: bool = False,
                 style: Style = None,
                 parent: Component = None) -> None:
        """Create a new VerticalPanel. <rect> is the rectangle representing
        this component's position and size on the screen. <expand_width>
        decides whether or not to change the children's width to fill this
        component's rect. <expand_height> decides whether or not to change
        the children's height to fill this component's rect. <space_around>
        decides whether or not to add spacing on the top and bottom side of
        this component's children. The children of this component will be
        centered. <style> dictates the appearence of the component. If None,
        the default style will be used. <parent> is the component that is
        immediately above this component in the tree.
        """
        self._expand_width = expand_width
        self._expand_height = expand_height
        self._space_around = space_around
        Component.__init__(self, rect, style=style, parent=parent)

    def add_child(self, child: Component):
        """Add a component as a child. Does nothing if <child>
        is already a child component.
        """
        Component.add_child(self, child)
        self._layout_children()

    def set_rect(self, child_rect: Rect):
        """Set the component's rectangle."""
        Component.set_rect(self, child_rect)
        self._layout_children()

    def _layout_children(self):
        """Set the position and size of this component's children."""
        if(len(self._children) == 0):
            return

        child_h = 0
        spacing_h = 0
        h_count = self._rect.y

        # Calulate spacing and child size
        if(self._expand_height):
            child_h = self._rect.h / len(self._children)
        else:
            total_h = 0
            for child in self._children:
                total_h += child.get_rect().h

            if(self._space_around):
                spacing_h = (self._rect.h - total_h) / \
                    (len(self._children) + 1)

            elif(len(self._children) > 1):
                spacing_h = (self._rect.h - total_h) / \
                    (len(self._children) - 1)
                h_count -= spacing_h

        # Apply layout
        for child in self._children:
            h_count += spacing_h

            child_rect = child.get_rect()
            child_rect.y = h_count

            if(self._expand_height):
                child_rect.h = child_h

            if(self._expand_width):
                child_rect.x = self._rect.x
                child_rect.w = self._rect.w
            else:
                child_rect.centerx = self._rect.centerx

            child.set_rect(child_rect)
            h_count += child_rect.h
