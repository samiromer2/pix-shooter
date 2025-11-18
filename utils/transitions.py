"""Level transition effects."""
from __future__ import annotations

import pygame


class Transition:
    """Manages screen transitions."""
    
    def __init__(self):
        self.active = False
        self.fade_type = "fade_out"  # fade_out, fade_in
        self.alpha = 0
        self.speed = 8
        self.callback = None
    
    def start_fade_out(self, callback=None) -> None:
        """Start fade out transition."""
        self.active = True
        self.fade_type = "fade_out"
        self.alpha = 0
        self.callback = callback
    
    def start_fade_in(self, callback=None) -> None:
        """Start fade in transition."""
        self.active = True
        self.fade_type = "fade_in"
        self.alpha = 255
        self.callback = callback
    
    def update(self) -> bool:
        """Update transition. Returns True if complete."""
        if not self.active:
            return False
        
        if self.fade_type == "fade_out":
            self.alpha += self.speed
            if self.alpha >= 255:
                self.alpha = 255
                self.active = False
                if self.callback:
                    self.callback()
                return True
        else:  # fade_in
            self.alpha -= self.speed
            if self.alpha <= 0:
                self.alpha = 0
                self.active = False
                if self.callback:
                    self.callback()
                return True
        
        return False
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw transition overlay."""
        if self.active:
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, self.alpha))
            surface.blit(overlay, (0, 0))
    
    def is_active(self) -> bool:
        """Check if transition is active."""
        return self.active

