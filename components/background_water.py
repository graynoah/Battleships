from pygame import Rect, Surface, transform, BLEND_RGB_MULT, BLEND_RGB_ADD

from components.style import Style
from components.component import Component
from components.animated_image import AnimatedImage


class BackgroundWater(AnimatedImage):
    """A GUI element that displays an animated background water."""

    def __init__(self,
                 rect: Rect,
                 style: Style = None,
                 parent: Component = None) -> None:
        """Create a new BackgroundWater. <rect> is the rectangle representing
        this component's position and size on the screen. <style> dictates the
        appearence of the component. If None, the default style will be used.
        <parent> is the component that is immediately above this component in
        the tree.
        """
        self._horizontal_tile_count = 10
        self._vertical_tile_count = 10

        AnimatedImage.__init__(self, rect,
                               folder_path="images/water4",
                               animation_duration=1000,
                               style=style,
                               parent=parent)

    def _generate_animation_frames(self) -> None:
        """Create the water's tiles animation frames."""
        square_w = self._rect.w // self._horizontal_tile_count
        square_h = self._rect.h // self._vertical_tile_count

        self._animation_frames = []
        for i in range(len(self._raw_frames)):

            animation_frame = Surface(self._rect.size).convert()
            frame = transform.smoothscale(
                self._raw_frames[i], (square_w, square_h))
            frame.set_colorkey(None)

            for y in range(self._vertical_tile_count):
                for x in range(self._horizontal_tile_count):
                    animation_frame.blit(frame, (square_w * x, square_h * y))

            self._animation_frames.append(animation_frame)
