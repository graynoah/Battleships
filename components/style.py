from typing import Tuple

import pygame


class Style(object):
    """A GUI element that displays text.

    === Public Attributes ===
        background_color:
            The background color for components. None indicates no background
            color.
        background_image:
            The surface of a background image for components. None indicates
            no background image.
        hover_color:
            The multiplicative tint color for when components are hovered over.
        primary_color:
            The primary color for component foregrounds.
        secondary_color:
            The secondary color for component foregrounds.
        force_parent_redraw:
            Whether or not a component will force a parent component to be
            redrawn along with itself.
        font:
            The font to be used for and text.
        border_width:
            The size of a solid component border in pixels. 0 indicates no
            border.
        border_color:
            The color for component borders. None indicates no border color.
    """
    background_color: Tuple[int, int, int]
    background_image: pygame.Surface
    hover_color: Tuple[int, int, int]
    primary_color: Tuple[int, int, int]
    secondary_color: Tuple[int, int, int]
    force_parent_redraw: bool
    font: pygame.font
    border_width: int
    border_color: Tuple[int, int, int]

    def __init__(self,
                 background_image: pygame.Surface = None,
                 background_color: Tuple[int, int, int] = (255, 255, 255),
                 hover_color: Tuple[int, int, int] = (190, 190, 190, 0),
                 primary_color: Tuple[int, int, int] = (0, 0, 0),
                 secondary_color: Tuple[int, int, int] = (0, 0, 0),
                 force_parent_redraw: bool = False,
                 font: pygame.font = None,
                 border_color: Tuple[int, int, int] = (0, 0, 0),
                 border_width: int = 1) -> None:
        """<background_color> is the color to be drawn behind components. A
        value of None indicates no background color. <background_image> is the
        surface of a image to be drawn behind components. A vlue of None
        indicates no background image. <hover_color> is the color that will be
        multiplied to the component's background when it is hovered over.
        <primary_color> is the main general purpose color for component
        foregrounds. <secondary_color> is the alretnate general purpose color
        for component foregrounds. <force_parent_redraw> is whether or not to
        force the parent component to redraw when the component is redrawn.
        <font> is the text style to be used for any displayed text.
        <border_width> is the size of a solid border in pixels around a
        component. A value of 0 indicates no border. <border_color> is the
        color for component borders. A value of None indicates no border color.
        """
        self.background_image = background_image
        self.background_color = background_color
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.force_parent_redraw = force_parent_redraw
        self.hover_color = hover_color
        self.border_width = border_width
        self.border_color = border_color

        if(font is None):
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = font
