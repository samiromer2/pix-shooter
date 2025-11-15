"""Camera system for following the player."""
from __future__ import annotations

import pygame

import settings as S


class Camera:
    """Camera that follows a target (usually the player) with smooth movement."""
    
    def __init__(self, width: int = S.WIDTH, height: int = S.HEIGHT):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, width, height)
        self.target = None
        self.smooth_speed = 0.1  # Smooth following speed (0.0 to 1.0)
        self.deadzone_x = width // 4  # Deadzone before camera moves horizontally
        self.deadzone_y = height // 4  # Deadzone before camera moves vertically
        
        # Screen shake
        self.shake_offset = pygame.Vector2(0, 0)
        self.shake_intensity = 0.0
        self.shake_decay = 0.9
        
    def set_target(self, target: pygame.sprite.Sprite | None) -> None:
        """Set the sprite to follow."""
        self.target = target
    
    def add_screen_shake(self, intensity: float) -> None:
        """Add screen shake effect."""
        self.shake_intensity = max(self.shake_intensity, intensity)
    
    def update(self) -> None:
        """Update camera position to follow target."""
        if not self.target:
            return
        
        target_center = pygame.Vector2(self.target.rect.center)
        camera_center = pygame.Vector2(self.rect.center)
        
        # Calculate distance from camera center to target
        offset = target_center - camera_center
        
        # Check if target is outside deadzone
        move_x = abs(offset.x) > self.deadzone_x
        move_y = abs(offset.y) > self.deadzone_y
        
        # Smoothly move camera towards target
        if move_x:
            self.rect.centerx += int(offset.x * self.smooth_speed)
        if move_y:
            self.rect.centery += int(offset.y * self.smooth_speed)
        
        # Update screen shake
        if self.shake_intensity > 0.1:
            import random
            self.shake_offset.x = random.uniform(-self.shake_intensity, self.shake_intensity)
            self.shake_offset.y = random.uniform(-self.shake_intensity, self.shake_intensity)
            self.shake_intensity *= self.shake_decay
        else:
            self.shake_offset = pygame.Vector2(0, 0)
            self.shake_intensity = 0.0
        
        # Clamp camera to world bounds (optional - can be removed for infinite scrolling)
        # For now, we'll allow camera to go anywhere
        # self.rect.clamp_ip(world_rect)
    
    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        """Apply camera offset to a rect."""
        return rect.move(-self.rect.x, -self.rect.y)
    
    def apply_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        """Apply camera offset to a position."""
        return (pos[0] - self.rect.x, pos[1] - self.rect.y)
    
    def get_offset(self) -> tuple[int, int]:
        """Get the camera offset as (x, y), including screen shake."""
        return (int(-self.rect.x + self.shake_offset.x), int(-self.rect.y + self.shake_offset.y))

