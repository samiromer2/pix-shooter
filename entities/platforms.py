"""Moving platform entities."""
from __future__ import annotations

import pygame

import settings as S


class MovingPlatform(pygame.sprite.Sprite):
    """Platform that moves horizontally or vertically."""
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int = 90,
        height: int = 20,
        move_x: int = 0,
        move_y: int = 0,
        distance: int = 100,
        speed: float = 2.0
    ):
        super().__init__()
        self.width = width
        self.height = height
        
        # Create platform sprite
        self.image = pygame.Surface((width, height))
        # Draw platform with a simple pattern
        self.image.fill((100, 100, 120))
        # Add border
        pygame.draw.rect(self.image, (150, 150, 170), (0, 0, width, height), 2)
        # Add some detail lines
        for i in range(3):
            y_pos = (i + 1) * (height // 4)
            pygame.draw.line(self.image, (80, 80, 100), (0, y_pos), (width, y_pos), 1)
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.start_y = y
        self.move_x = move_x  # Direction: -1, 0, or 1
        self.move_y = move_y  # Direction: -1, 0, or 1
        self.distance = distance  # How far to move
        self.speed = speed
        self.position = pygame.Vector2(x, y)
        self.offset = 0.0  # Current offset from start position
        
    def update(self, *args, **kwargs) -> None:
        """Update platform position."""
        # Update offset
        self.offset += self.speed
        
        # Initialize offsets
        x_offset = 0
        y_offset = 0
        
        # Calculate new position based on movement direction
        if self.move_x != 0:
            # Horizontal movement
            max_offset = self.distance
            if self.offset >= max_offset * 2:
                self.offset = 0.0
            elif self.offset >= max_offset:
                # Moving back
                x_offset = (max_offset * 2 - self.offset) * self.move_x
            else:
                # Moving forward
                x_offset = self.offset * self.move_x
            self.position.x = self.start_x + x_offset
        
        if self.move_y != 0:
            # Vertical movement
            max_offset = self.distance
            if self.offset >= max_offset * 2:
                self.offset = 0.0
            elif self.offset >= max_offset:
                # Moving back
                y_offset = (max_offset * 2 - self.offset) * self.move_y
            else:
                # Moving forward
                y_offset = self.offset * self.move_y
            self.position.y = self.start_y + y_offset
        
        # Update rect
        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)
    
    def get_velocity(self) -> pygame.Vector2:
        """Get the platform's current velocity for player movement."""
        # Calculate velocity based on movement direction and speed
        vx = self.move_x * self.speed if self.move_x != 0 else 0
        vy = self.move_y * self.speed if self.move_y != 0 else 0
        
        # Reverse direction if moving back
        if self.move_x != 0:
            max_offset = self.distance
            if self.offset >= max_offset:
                vx = -vx
        if self.move_y != 0:
            max_offset = self.distance
            if self.offset >= max_offset:
                vy = -vy
        
        return pygame.Vector2(vx, vy)

