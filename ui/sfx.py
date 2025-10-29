from __future__ import annotations

from pathlib import Path
import pygame


class Sounds:
    def __init__(self) -> None:
        self.click = None
        self.hover = None

    def play_click(self) -> None:
        if self.click:
            self.click.play()

    def play_hover(self) -> None:
        if self.hover:
            self.hover.play()


def load_sounds() -> Sounds:
    snd = Sounds()
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except Exception:
        return snd
    try:
        click_path = Path("assets/sounds/click.wav")
        hover_path = Path("assets/sounds/hover.wav")
        if click_path.exists():
            snd.click = pygame.mixer.Sound(str(click_path))
        if hover_path.exists():
            snd.hover = pygame.mixer.Sound(str(hover_path))
    except Exception:
        pass
    return snd


