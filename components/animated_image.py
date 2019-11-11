from typing import List

from pygame import Rect, Surface, image

from components.component import Component
from components.style import Style
import os


class AnimatedImage(Component):
    """A GUI element that displays an animated image.

    === Private Attributes ===
        _animation_duration:
            The length of the animation in miliseconds.
        _time_since_last_frame:
            The length of the time passed since the frame index changed in
            miliseconds.
        _animation_frames:
            The list of loaded animation frames.
        _raw_frames:
            The list of loaded images.
        _frame_index:
            The index of the current animation frame in _animation_frames.
    """
    _animation_duration: float
    _time_since_last_frame: float
    _animation_frames: List[Surface]
    _raw_frames: List[Surface]
    _frame_index: int

    def __init__(self,
                 rect: Rect,
                 folder_path: str = "",
                 animation_duration: float = 1000,
                 style: Style = None,
                 parent: Component = None) -> None:
        """Create a new AnimatedImage. <rect> is the rectangle representing
        this component's position and size on the screen. <folder_path> is
        the path to the folder containing the frames of the animation to be
        displayed. <animation_duration> is the length of the animation in
        miliseconds. <style> dictates the appearence of the component. If None,
        the default style will be used. <parent> is the component that is
        immediately above this component in the tree.
        """
        self._animation_frames = []
        self._raw_frames = []

        self._frame_index = 0
        self._time_since_last_frame = 0

        self._animation_duration = animation_duration
        self._load_animation(folder_path)

        Component.__init__(self, rect, style=style, parent=parent)

    def set_rect(self, rect: Rect):
        """Set the animated image's rectangle and generate the animation's
        frames.
        """
        Component.set_rect(self, rect)
        self._generate_animation_frames()

    def update(self, dt: float):
        """Update the frame index. <dt> is the time since last update in
        milliseconds.
        """
        Component.update(self, dt)

        if(len(self._animation_frames) == 0):
            return

        self._time_since_last_frame += dt
        if(self._time_since_last_frame > self._time_per_frame):
            self._time_since_last_frame -= self._time_per_frame
            self._frame_index = (self._frame_index +
                                 1) % len(self._animation_frames)
            self._redraw()

    def _load_animation(self, folder_path: str) -> None:
        """Load the raw frames of the animation from <folder_path>. The images
        are sorted by filename in ascending order.
        """
        self._raw_frames.clear()

        for filepath in sorted(os.listdir(folder_path)):
            self._raw_frames.append(
                image.load(f"{folder_path}/{filepath}").convert())

        self._time_per_frame = self._animation_duration / \
            len(self._raw_frames)

    def _draw(self, screen: Surface, changes: List[Rect]) -> None:
        """Draw the current animation frame to the screen. <changes> is a list
        of rectangles that represent the changed areas of the screen.
        """
        Component._draw(self, screen, changes)

        if(len(self._animation_frames) == 0):
            return

        changes.append(screen.blit(self._animation_frames[self._frame_index],
                                   self._rect))

    def _generate_animation_frames(self) -> None:
        """Create the animation's frames. Modify a copy of the raw frames."""
        self._animation_frames = self._raw_frames
