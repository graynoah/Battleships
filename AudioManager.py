import pygame

""" A class that controls the audio in this game. All the audio files used here 
are credited to the Youtube Audio Library.

=== Private Attributes ===
_pause: true if the background music is paused, false otherwise.
"""
def __init__():
    """Initialize the audio in the game. Load all the audio files."""
    self._pause = False
    pygame.mixer.music.load('audio/backgroundMusic.wav')
    canonShot = pygame.mixer.Sound("canonShot.wav")
    shipHit = pygame.mixer.Sound("shipHit.wav")
    
def start():
    """ Start the background music from the beginning.
    """
    pygame.mixer.music.play(-1) # play the music infinitely 

def shoot():
    """ Play the canon shot sound effect.
    """
    canonShot.play()

def shipHit():
    """ Play the sound effect for a ship that just got hit.
    """
    shipHit.play()
    
def pause():
    """ Pause the background music."""
    if (not self._pause):
        pygame.mixer.music.pause()
        self._pause = True 

def unpause():
    """Resume the background music."""
    pygame.mixer.unpause()

def setMusicVolume(value:float):
    """Set the volume of the music. Precondition: 0.0<= value <= 1.0 """
    pygame.mixer.music.set_volume(value)

def getMusicVolume():
    """Return the current music volume, which is between 0.0 and 1.0."""
    pygame.mixer.music.get_volume()

def stopMusic():
    """Stop the background music from playing."""
    pygame.mixer.music.stop()
