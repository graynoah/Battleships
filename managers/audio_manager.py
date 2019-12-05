import pygame


class AudioManager(object):
    """A Singleton that manages the audio of the game. The static instance
    variable can be used to access this object. This class must be created
    atleast once. All the audio files used here are credited to the Youtube
    Audio Library.

    === Private Attributes ===
        _canon_shot:
            The cannon shot sound file.
        _ship_hit:
            The sound file for when a ship is hit.
        _music_volume:
            The volume of the music.
        _fx_volume:
            The volume of the sound fx.
    """
    instance = None

    _canon_shot: pygame.mixer.Sound
    _ship_hit: pygame.mixer.Sound
    _music_volume: float
    _fx_volume: float

    def __init__(self):
        """Create a new Audio Manager and setup the static instance variable.
        This functionwill load all the audio files.
        """
        if(AudioManager.instance is None):
            AudioManager.instance = self

        pygame.mixer.init()
        pygame.mixer.music.load('audio/backgroundMusic.wav')
        self._canon_shot = pygame.mixer.Sound("audio/canonShot.wav")
        self._ship_hit = pygame.mixer.Sound("audio/shipHit.wav")
        self._music_volume = 1
        self._fx_volume = 1
        self.start()

    def start(self):
        """ Start the background music from the beginning.
        """
        pygame.mixer.music.play(-1)

    def shoot(self):
        """ Play the canon shot sound effect.
        """
        self._canon_shot.play()

    def ship_hit(self):
        """ Play the sound effect for a ship that just got hit.
        """
        self._ship_hit.play()

    def set_music_volume(self, value: float):
        """Set the volume of the music. Precondition: 0.0 <= value <= 1.0 """
        self._music_volume = value
        pygame.mixer.music.set_volume(self._music_volume)

    def get_music_volume(self):
        """Return the current music volume, which is between 0.0 and 1.0."""
        return self._music_volume

    def set_fx_volume(self, value: float):
        """Set the volume of the sound effects.
        Precondition: 0.0 <= value <= 1.0
        """
        self._fx_volume = value
        self._ship_hit.set_volume(self._fx_volume)
        self._canon_shot.set_volume(self._fx_volume)

    def get_fx_volume(self):
        """Return the current music volume, which is between 0.0 and 1.0."""
        return self._fx_volume
