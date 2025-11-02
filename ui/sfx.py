from __future__ import annotations

from pathlib import Path
import pygame


class Sounds:
    def __init__(self) -> None:
        self.click = None
        self.hover = None
        self.shoot = None
        self.hit = None
        self.explode = None
        self.bgm = None
        self.bgm_path = None
        self._bgm_playing = False

    def play_click(self) -> None:
        if self.click:
            try:
                self.click.play()
            except Exception:
                pass

    def play_hover(self) -> None:
        if self.hover:
            try:
                self.hover.play()
            except Exception:
                pass

    def play_shoot(self) -> None:
        if self.shoot:
            try:
                self.shoot.play()
            except Exception:
                pass

    def play_hit(self) -> None:
        if self.hit:
            try:
                self.hit.play()
            except Exception:
                pass

    def play_explode(self) -> None:
        if self.explode:
            try:
                self.explode.play()
            except Exception:
                pass

    def start_bgm(self, loops: int = -1) -> None:
        """Start background music (loops=-1 means infinite loop)."""
        if self._bgm_playing:
            return
        
        # Try mixer.music first (better for longer files)
        if self.bgm_path:
            try:
                pygame.mixer.music.load(self.bgm_path)
                pygame.mixer.music.play(loops=loops)
                self._bgm_playing = True
                return
            except Exception:
                pass
        
        # Fallback to Sound object
        if self.bgm and not self._bgm_playing:
            try:
                self.bgm.play(loops=loops)
                self._bgm_playing = True
            except Exception:
                pass

    def stop_bgm(self) -> None:
        """Stop background music."""
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        try:
            if self.bgm:
                self.bgm.stop()
        except Exception:
            pass
        self._bgm_playing = False


def load_sounds() -> Sounds:
    snd = Sounds()
    mixer_available = False
    
    # Try to initialize mixer
    try:
        # Check if mixer module exists
        if hasattr(pygame, 'mixer'):
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            mixer_available = True
        else:
            mixer_available = False
    except (NotImplementedError, AttributeError, Exception) as e:
        # Mixer not available - sounds will be disabled
        mixer_available = False
        import sys
        print(f"Note: Audio disabled (mixer not available: {type(e).__name__})", file=sys.stderr)
        return snd
    
    if not mixer_available:
        return snd
    
    base = Path("assets/sounds")
    
    # UI sounds
    try:
        if (base / "click.wav").exists():
            snd.click = pygame.mixer.Sound(str(base / "click.wav"))
        if (base / "hover.wav").exists():
            snd.hover = pygame.mixer.Sound(str(base / "hover.wav"))
    except Exception:
        pass
    
    # Gameplay sounds
    try:
        if (base / "shoot.wav").exists():
            snd.shoot = pygame.mixer.Sound(str(base / "shoot.wav"))
        if (base / "hit.mp3").exists():
            try:
                # Try MP3 (may not be supported)
                snd.hit = pygame.mixer.Sound(str(base / "hit.mp3"))
            except Exception:
                # MP3 not supported, try converting or skip
                pass
        if (base / "explode.ogg").exists():
            snd.explode = pygame.mixer.Sound(str(base / "explode.ogg"))
    except Exception:
        pass
    
    # Background music - use mixer.music (better for long files)
    try:
        if (base / "bgm.ogg").exists():
            # Store path for music.load() which works better than Sound
            snd.bgm_path = str(base / "bgm.ogg")
            # Also try as Sound for compatibility
            try:
                snd.bgm = pygame.mixer.Sound(snd.bgm_path)
            except Exception:
                snd.bgm = None
        else:
            snd.bgm_path = None
    except Exception:
        snd.bgm_path = None
    
    return snd


