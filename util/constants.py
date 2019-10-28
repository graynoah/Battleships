import pygame

# The size of the screen when changing into windowed mode
DEFAULT_WINDOWED_MODE_SIZE = (800, 600)

# Valid characters for user input
VALID_CHARACTERS = ("abcdefghijklmnopqrstuvwxyz"
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    "1234567890!()[]_ ")

# Cursor to be displayed when over a textbox
TEXTBOX_CURSOR = ((8, 16), (4, 4), *pygame.cursors.compile((
    "XXX XXX ",
    "   X    ",
    "   X    ",
    "   X    ",
    "   X    ",
    "   X    ",
    "   X    ",
    "   X    ",
    "   X    ",
    "   X    ",
    "   X    ",
    "   X    ",
    "   X    ",
    "   X    ",
    "   X    ",
    "XXX XXX ")))

# Cursor to be displayed when over a button
BUTTON_CURSOR = ((24, 32), (10, 0), *pygame.cursors.compile((
    "         XX             ",
    "        X..X            ",
    "        X..X            ",
    "        X..X            ",
    "        X..X            ",
    "        X..X            ",
    "        X..X            ",
    "        X..XXX          ",
    "        X..X..XXXX      ",
    "        X..X..X..X      ",
    "        X..X..X..XX     ",
    "        X..X..X..X.X    ",
    "   XXXX X..X..X..X..X   ",
    "   X...XX...........X   ",
    "   X....X...........X   ",
    "    X...X...........X   ",
    "     X..............X   ",
    "     X..............X   ",
    "     X..............X   ",
    "      X.............X   ",
    "      X............X    ",
    "       X...........X    ",
    "       X...........X    ",
    "        X.........X     ",
    "        X.........X     ",
    "        XXXXXXXXXXX     ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",)))
