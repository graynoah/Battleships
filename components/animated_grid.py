from typing import List, Callable, Tuple
import math
import os

from pygame import Rect, Surface, transform, mouse, BLEND_RGB_MULT, cursors

from util.constants import BUTTON_CURSOR
from components.label import Label
from components.style import Style
from components.component import Component
from components.animated_image import AnimatedImage
from players.ship import Ship


class AnimatedGrid(AnimatedImage):
    """A GUI element that displays an grid of animated images.

    === Private Attributes ===
        _hover_pos:
            The position of the tile that is currently being hovered over.
        _tiles:
            The list of grid tile positions that indicate an image should be
            drawn at those positions.
        _on_click_callback:
            The function that is called when a tile is clicked.
        _scaled_frames:
            The list of raw frames scaled to the correct resolution.
        _vertical_tile_count:
            The amount of tiles to be put vertically.
        _horizontal_tile_count:
            The amount of tiles to be put horizontally.
    """
    _hover_pos: Tuple[int, int]
    _tiles: List[Tuple[int, int]]
    _on_click_callback: Callable[[Tuple[int, int]], None]
    _horizontal_tile_count: int
    _vertical_tile_count: int
    _scaled_frames: List[Surface]

    def __init__(self,
                 rect: Rect,
                 folder_path: str = "images/boat2",
                 animation_duration: float = 1000,
                 horizontal_tile_count: int = 10,
                 vertical_tile_count: int = 10,
                 on_click: Callable[[Tuple[int, int]], None] = None,
                 style: Style = None,
                 parent: Component = None) -> None:
        """Create a new AnimatedGrid. <rect> is the rectangle representing this
        component's position and size on the screen.<folder_path> is the path
        to the folder containing the frames of the animation to be displayed.
        <animation_duration> is the length of the animation in miliseconds.
        <vertical_tile_count> is the number of tiles to be put vertically.
        <horizontal_tile_count> is the number of tiles to be put horizontally.
        <on_click> is the function called when a tile is clicked. <style>
        dictates the appearence of the component. If None, the default style
        will be used. <parent> is the component that is immediately above this
        component in the tree.
        """
        self._hover_pos = (0, 0)
        self._tiles = []
        self._on_click_callback = on_click
        self._horizontal_tile_count = horizontal_tile_count
        self._vertical_tile_count = vertical_tile_count
        self._scaled_frames = []

        AnimatedImage.__init__(self, rect,
                               folder_path=folder_path,
                               animation_duration=animation_duration,
                               style=style,
                               parent=parent)

    def set_tiles(self, tiles: List[Tuple[int, int]]) -> None:
        """Set the animated grid's tiles to <tiles>. This function will
        update the animation frames.
        """
        added = [tile for tile in tiles if tile not in self._tiles]
        removed = [tile for tile in self._tiles if tile not in tiles]

        self._tiles = tiles
        self._draw_tiles(added)
        self._remove_tiles(removed)
        self._redraw()

    def _remove_tiles(self, tiles):
        """Remove every tile in <tiles> from the animation frames."""
        for i in range(len(self._animation_frames)):
            for tile in tiles:
                rect = Rect(self._square_w * tile[0], self._square_h *
                            tile[1], self._square_w, self._square_h)

                # Draw background color
                self._animation_frames[i].fill(self._style.primary_color, rect)

                # Draw outlines
                if(self._style.border_width > 0 and
                   self._style.secondary_color is not None):
                    self._draw_outline(self._animation_frames[i], rect,
                                       self._style.secondary_color,
                                       self._style.border_width)

    def _draw_tiles(self, tiles):
        """Dray every tile in <tiles> to the animation frames."""
        for i in range(len(self._scaled_frames)):

            # Draw tile images
            for tile in tiles:
                rect = Rect(self._square_w * tile[0], self._square_h *
                            tile[1], self._square_w, self._square_h)
                self._animation_frames[i].blit(self._scaled_frames[i], rect)

    def update(self, dt: float) -> None:
        """Update the hovered tile position. <dt> is the time since last
        update in milliseconds.
        """
        AnimatedImage.update(self, dt)

        pos = self._mouse_pos_to_square_offset()
        if(pos != self._hover_pos):
            self._hover_pos = pos
            self._redraw()

    def _generate_animation_frames(self) -> None:
        """Create the animated grid's animation frames."""
        self._animation_frames = []
        self._square_w = self._rect.w // self._horizontal_tile_count
        self._square_h = self._rect.h // self._vertical_tile_count

        tint_surface = Surface(self._rect.size).convert_alpha()
        tint_surface.set_colorkey(None)

        if(self._style.primary_color is not None):
            tint_surface.fill(self._style.primary_color)

        if(self._style.primary_color is None and
            len(self._tiles) == 0 and
            (self._style.border_width == 0 or
             self._style.secondary_color is None)):
            return

        self._scaled_frames = []
        for i in range(len(self._raw_frames)):
            animation_frame = tint_surface.copy()
            self._scaled_frames.append(transform.smoothscale(
                self._raw_frames[i], (self._square_w, self._square_h)))

            # Draw outlines
            if(self._style.border_width > 0 and
               self._style.secondary_color is not None):

                for y in range(self._vertical_tile_count):
                    for x in range(self._horizontal_tile_count):
                        rect = Rect(self._square_w * x, self._square_h *
                                    y, self._square_w, self._square_h)
                        self._draw_outline(animation_frame, rect,
                                           self._style.secondary_color,
                                           self._style.border_width)

            self._animation_frames.append(animation_frame)

    def _draw(self, screen: Surface, changes: List[Rect]) -> None:
        """Draw the animated grid's visuals to the screen. <change> is a list
        of rectangles that represent the changed areas of the screen.
        """
        AnimatedImage._draw(self, screen, changes)

        if(self.is_hovered()):
            rect = Rect(self._square_w * self._hover_pos[0] + self._rect.x,
                        self._square_h *
                        self._hover_pos[1] + self._rect.y,
                        self._square_w, self._square_h)

            changes.append(screen.fill(self._style.hover_color,
                                       rect,
                                       BLEND_RGB_MULT))

    def _draw_outline(self,
                      surface: Surface,
                      rect: Rect,
                      border_color: Tuple[int, int, int],
                      border_width: int) -> None:
        """Draw an outline of a rectangle onto <surface> with color
        <border_color> and line width <border_width>. The line's width grows
        towards the center of the rectangle.
        """

        if(border_color is not None and border_width > 0):
            top_rect = Rect(rect.x, rect.y,
                            rect.w, border_width)

            bottom_rect = Rect(rect.x, rect.bottom - border_width,
                               rect.width, border_width)

            left_rect = Rect(rect.x, rect.y, border_width, rect.height)

            right_rect = Rect(rect.right - border_width, rect.y,
                              border_width, rect.height)

            surface.fill(border_color, top_rect)
            surface.fill(border_color, bottom_rect)
            surface.fill(border_color, left_rect)
            surface.fill(border_color, right_rect)

    def _mouse_pos_to_square_offset(self) -> int:
        """Translate the mouse's position into an index into the animated
        grids's tiles.
        """
        x, y = mouse.get_pos()
        x -= self._rect.x
        y -= self._rect.y

        return (x // (self._rect.w / self._horizontal_tile_count),
                y // (self._rect.h / self._vertical_tile_count))

    def _on_hover_enter(self) -> None:
        """Change the mouse cursor when the mouse moves over the animated grid.
        """
        mouse.set_cursor(*BUTTON_CURSOR)
        self._redraw()

    def _on_hover_exit(self) -> None:
        """Reset the mouse cursor when the mouse moves off the animated grid.
        """
        mouse.set_cursor(*cursors.arrow)
        self._redraw()

    def _on_click(self, button) -> None:
        """Call the on click callback with the position of the clicked tile
        when the animated grid is clicked.
        """
        pos = self._mouse_pos_to_square_offset()
        if(self._on_click_callback is not None):
            self._on_click_callback(pos)
