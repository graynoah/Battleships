from typing import Callable, List

import pygame

from util.constants import TEXTBOX_CURSOR, VALID_CHARACTERS
from components.component import Component
from components.style import Style
from components.label import Label


class Textbox(Label):
    """A GUI element that allows for editing text.

    === Private Attributes ===
        _on_value_changed:
            The function that is called when the textbox's value is changed.
        _on_edit_finished:
            The function that is called when the textbox's value is finalized.
        _is_selection_finished:
            Whether or not a selection is completed.
        _selection_end_pos:
            The character index into the text where the selection ended.
        _time_since_blink:
            The time in miliseconds since the last time the blinker blinked.
        _character_limit:
            The maximum allowed amount of characters for this textbox.
        _time_for_blink:
            The time in miliseconds inbetween blinker blinks.
        _is_blinker_on:
            Whether or not the blinker is currently visible.
        _cursor_pos:
            The character index into the text where the changes will occur.
    """
    _on_value_changed: Callable[[str], None]
    _on_edit_finished: Callable[[str], None]
    _is_selection_finished: int
    _selection_end_pos: int
    _time_since_blink: int
    _character_limit: int
    _time_for_blink: int
    _is_blinker_on: bool
    _cursor_pos: int

    def __init__(self,
                 rect: pygame.Rect,
                 on_value_changed: Callable[[str], None] = None,
                 on_edit_finished: Callable[[str], None] = None,
                 text: str = "",
                 character_limit: int = 14,
                 style: Style = None,
                 parent: Component = None) -> None:
        """Create a new Textbox. <rect> is the rectangle representing this
        component's position and size on the screen. <on_value_changed> is the
        function called when the textbox's text is changed. <on_edit_finished>
        is the function called when the textbox's text is done being changed.
        <text> is the starting text of the textbox. <character_limit> is the
        maximum number of characters that the textbox can have. <style>
        dictates the appearence of the component. If None, the default style
        will be used. <parent> is the component that is immediately above this
        component in the tree.
        """
        Label.__init__(self, rect, text=text, style=style, parent=parent)

        self._on_value_changed = on_value_changed
        self._on_edit_finished = on_edit_finished
        self._time_since_blink = 0
        self._time_for_blink = 500
        self._is_blinker_on = False
        self._cursor_pos = 0
        self._selection_end_pos = 0
        self._is_selection_finished = True
        self._character_limit = character_limit

    def update(self, dt: float) -> None:
        """Update the blink status. <dt> is the time since last update in
        milliseconds.
        """
        Label.update(self, dt)

        if(not self.is_focused()):
            return

        self._time_since_blink += dt

        if(self._time_since_blink >= self._time_for_blink):
            self._time_since_blink -= self._time_for_blink
            self._is_blinker_on = not self._is_blinker_on
            self._redraw()

    def set_text(self, text: str) -> None:
        """Set the textbox's text."""
        Label.set_text(self, text)

        if(not self.is_focused()):
            self._set_cursor_pos(len(self.get_text()))

    def _set_cursor_pos(self, position: int) -> None:
        """Set the cursor position. This method changes the selection end
        position and forces a blink.
        """
        self._cursor_pos = position
        self._selection_end_pos = position
        self._force_blink()

    def _on_key_press(self, key: int, character: str, modifiers: int) -> None:
        """Handle the even when a key is pressed and the component is
        focused.
        """
        if(key == pygame.K_RETURN):
            self.blur()

        elif(key == pygame.K_BACKSPACE):
            self._on_backspace_pressed()

        elif(key == pygame.K_DELETE):
            self._on_delete_pressed()

        elif(key == pygame.K_LEFT):
            self._on_left_arrow_key_pressed()

        elif(key == pygame.K_RIGHT):
            self._on_right_arrow_key_pressed()

        elif(key == pygame.K_v and modifiers & pygame.KMOD_CTRL):
            self._on_ctrl_v_pressed()

        elif(key == pygame.K_c and modifiers & pygame.KMOD_CTRL):
            self._on_ctrl_c_pressed()

        elif(key == pygame.K_a and modifiers & pygame.KMOD_CTRL):
            self._on_ctrl_a_pressed()

        elif(key == pygame.K_x and modifiers & pygame.KMOD_CTRL):
            self._on_ctrl_x_pressed()

        elif(character and character in VALID_CHARACTERS):
            self._on_character_typed(character)

    def _has_multi_char_selection(self) -> bool:
        """Return whether or not the textbox has a multi-character
        selection.
        """
        return self._selection_end_pos != self._cursor_pos

    def _on_character_typed(self, character: str) -> None:
        """Add <character> to the textbox's text. Does nothing if the
        character limit is reached.
        """
        if(self._has_multi_char_selection()):
            self._delete_characters(
                self._cursor_pos, self._selection_end_pos)

        if(len(self.get_text()) < self._character_limit):
            self.set_text(self.get_text()[:self._cursor_pos] + character +
                          self.get_text()[self._cursor_pos:])

            self._set_cursor_pos(self._cursor_pos + 1)

            if(self._on_value_changed is not None):
                self._on_value_changed(self.get_text())

    def _on_left_arrow_key_pressed(self) -> None:
        """Move the cursor to the left of the slection."""
        if(self._has_multi_char_selection()):
            self._set_cursor_pos(
                min(self._cursor_pos, self._selection_end_pos))

        elif(self._cursor_pos > 0):
            self._set_cursor_pos(self._cursor_pos - 1)

    def _on_right_arrow_key_pressed(self) -> None:
        """Move the cursor to the right of the slection."""
        if(self._has_multi_char_selection()):
            self._set_cursor_pos(
                max(self._cursor_pos, self._selection_end_pos))

        elif(self._cursor_pos < len(self.get_text())):
            self._set_cursor_pos(self._cursor_pos + 1)

    def _on_ctrl_a_pressed(self) -> None:
        """Select all text."""
        self._cursor_pos = 0
        self._selection_end_pos = len(self.get_text())
        self._force_blink()

    def _on_ctrl_v_pressed(self) -> None:
        """Paste text from clipboard."""
        if(self._has_multi_char_selection()):
            self._delete_characters(
                self._cursor_pos, self._selection_end_pos)

        pasted_text = pygame.scrap.get(pygame.SCRAP_TEXT)
        if(pasted_text is not None):
            pasted_text = pasted_text.decode('utf-8').replace('\x00', '')

            can_fit = min(len(pasted_text),
                          self._character_limit - len(self.get_text()))

            if(can_fit > 0):
                self.set_text(self.get_text()[:self._cursor_pos] +
                              pasted_text[:can_fit] +
                              self.get_text()[self._cursor_pos:])

                self._set_cursor_pos(self._cursor_pos + can_fit)

                if(self._on_value_changed is not None):
                    self._on_value_changed(self.get_text())

    def _on_backspace_pressed(self) -> None:
        """Delete the character before a selection. For a multi-character
        selection, the entire selection is deleted.
        """
        if(self._has_multi_char_selection()):
            self._delete_characters(
                self._cursor_pos, self._selection_end_pos)

        elif(self._cursor_pos > 0):
            self._delete_characters(self._cursor_pos - 1, self._cursor_pos)

    def _on_delete_pressed(self) -> None:
        """Delete the character after a selection. For a multi-character
        selection, the entire selection is deleted.
        """
        if(self._has_multi_char_selection()):
            self._delete_characters(
                self._cursor_pos, self._selection_end_pos)

        elif(self._cursor_pos < len(self.get_text())):
            self._delete_characters(self._cursor_pos, self._cursor_pos + 1)

    def _on_ctrl_x_pressed(self) -> None:
        """Cut the text from a seletion."""
        if(self._has_multi_char_selection()):
            pygame.scrap.put(pygame.SCRAP_TEXT,
                             self.get_text().encode('utf-8'))

            self._delete_characters(
                self._cursor_pos, self._selection_end_pos)

    def _on_ctrl_c_pressed(self) -> None:
        """Copy the text from a seletion."""
        if(self._has_multi_char_selection()):
            pygame.scrap.put(pygame.SCRAP_TEXT,
                             self.get_text().encode('utf-8'))

    def _force_blink(self) -> None:
        """Force the blinker to be on."""
        self._time_since_blink = 0
        self._is_blinker_on = True
        self._redraw()

    def _delete_characters(self, start: int, end: int) -> None:
        """Delete the characters inbetween indicies <start> and <end>"""
        if(start == end):
            return

        self.set_text(self.get_text()[:min(start, end)] +
                      self.get_text()[max(start, end):])

        self._set_cursor_pos(min(start, end))

        if(self._on_value_changed is not None):
            self._on_value_changed(self.get_text())

    def _on_blur(self) -> None:
        """Finialize the textbox's text and reset the selection."""
        self._is_blinker_on = False
        self._selection_end_pos = self._cursor_pos
        self._redraw()

        if(self._on_edit_finished is not None):
            self._on_edit_finished(self.get_text())

    def _on_hover_enter(self) -> None:
        """Change the mouse cursor when the mouse moves over the textbox."""
        pygame.mouse.set_cursor(*TEXTBOX_CURSOR)

    def _on_hover_exit(self) -> None:
        """Reset the mouse cursor when the mouse moves off the textbox."""
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

    def _on_drag(self) -> None:
        """Change the selection depending on where the mouse is when the
        mouse is dragged.
        """
        offset = self._mouse_pos_to_char_offset()

        if(self._is_selection_finished):
            self._set_cursor_pos(offset)
            self._is_selection_finished = False

        if(offset != self._selection_end_pos):
            self._selection_end_pos = offset
            self._redraw()

    def _mouse_pos_to_char_offset(self) -> int:
        """Translate the mouse's position into an index into the textbox's
        text.
        """
        text_rect = self._text_image.get_rect()
        text_rect.center = self._rect.center

        x, y = pygame.mouse.get_pos()
        x -= text_rect.x

        for i in range(len(self.get_text())):
            size = self._style.font.size(self.get_text()[:i+1])
            if(x < size[0]):
                return i

        return len(self.get_text())

    def _on_click(self, button: int) -> None:
        """Update the selection when the textbox is clicked."""
        if(self._is_selection_finished):
            self._set_cursor_pos(self._mouse_pos_to_char_offset())
        else:
            self._is_selection_finished = True

    def _on_focus(self) -> None:
        """Set the cursor position depending on where the mouse is when the
        textbox comes into focus."""
        self._set_cursor_pos(self._mouse_pos_to_char_offset())

    def _draw(self,
              screen: pygame.Surface,
              changes: List[pygame.Rect]) -> None:
        """Draw the textbox's visuals to the screen. <change> is a list of
        rectangles that represent the changed areas of the screen.
        """
        Component._draw(self, screen, changes)

        text_rect = self._text_image.get_rect()
        text_rect.center = self._rect.center

        # Draw Selection Background
        if(self._has_multi_char_selection()):
            start = self._style.font.size(self.get_text()[:self._cursor_pos])
            end = self._style.font.size(
                self.get_text()[:self._selection_end_pos])

            start_x = min(start[0], end[0])
            end_x = max(start[0], end[0])

            background_rect = pygame.Rect(text_rect.x + start_x, text_rect.y,
                                          end_x - start_x, text_rect.height)
            changes.append(screen.fill((0, 0, 255), background_rect))
            Label._draw_text(self, screen, changes)
            return

        # Draw text
        Label._draw_text(self, screen, changes)

        # Draw Blinker
        if(self._is_blinker_on):
            size = self._style.font.size(self.get_text()[:self._cursor_pos])
            cursor_rect = pygame.Rect(text_rect.x + size[0],
                                      text_rect.y, 2, text_rect.height)

            if(self._rect.x < cursor_rect.x < self._rect.right):
                changes.append(screen.fill(
                    self._style.primary_color, cursor_rect))
