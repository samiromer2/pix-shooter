"""Secret areas and bonus rooms."""
from __future__ import annotations

import pygame

import settings as S
from entities.collectibles import Coin


class SecretArea(pygame.sprite.Sprite):
    """Hidden area that reveals bonus collectibles when entered."""
    
    def __init__(self, x: int, y: int, width: int, height: int, reward_type: str = "coins", reward_amount: int = 5):
        super().__init__()
        self.reward_type = reward_type  # "coins", "health", "ammo"
        self.reward_amount = reward_amount
        self.activated = False
        
        # Invisible trigger area
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Invisible
        
        # Visual indicator when discovered (subtle)
        self.indicator_timer = 0
    
    def check_activation(self, player) -> bool:
        """Check if player entered secret area. Returns True if newly activated."""
        if not self.activated and self.rect.colliderect(player.rect):
            self.activated = True
            self.indicator_timer = 180  # Show indicator for 3 seconds
            return True
        return False
    
    def update(self, *args, **kwargs) -> None:
        """Update secret area."""
        if self.indicator_timer > 0:
            self.indicator_timer -= 1
    
    def draw_indicator(self, surface: pygame.Surface, camera_offset: tuple[int, int] = (0, 0)) -> None:
        """Draw visual indicator when secret is discovered."""
        if self.activated and self.indicator_timer > 0:
            offset_x, offset_y = camera_offset
            screen_x = self.rect.centerx + offset_x
            screen_y = self.rect.top + offset_y - 20
            
            # Draw "SECRET!" text indicator
            try:
                import pygame.freetype as ft
                font = ft.Font(None, 20)
                alpha = int(255 * (self.indicator_timer / 180))
                text_surf, _ = font.render("SECRET!", (255, 255, 0))
                text_surf.set_alpha(alpha)
                surface.blit(text_surf, (screen_x - text_surf.get_width() // 2, screen_y))
            except Exception:
                # Fallback: draw simple indicator
                import math
                pulse = int(20 * abs(math.sin(self.indicator_timer * 0.1)))
                pygame.draw.circle(surface, (255, 255, 0), (screen_x, screen_y), 5 + pulse)


class BonusRoom:
    """A bonus room with rewards."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.entered = False
        self.rewards_spawned = False
        self.coins: list[Coin] = []
    
    def check_entry(self, player) -> bool:
        """Check if player entered bonus room. Returns True if newly entered."""
        if not self.entered and self.rect.colliderect(player.rect):
            self.entered = True
            return True
        return False
    
    def spawn_rewards(self, collectibles_group: pygame.sprite.Group) -> None:
        """Spawn reward coins in the bonus room."""
        if not self.rewards_spawned:
            self.rewards_spawned = True
            # Spawn coins in a pattern
            center_x = self.rect.centerx
            center_y = self.rect.centery
            coin_positions = [
                (center_x - 40, center_y - 20),
                (center_x, center_y - 20),
                (center_x + 40, center_y - 20),
                (center_x - 20, center_y),
                (center_x + 20, center_y),
                (center_x - 40, center_y + 20),
                (center_x, center_y + 20),
                (center_x + 40, center_y + 20),
            ]
            for pos in coin_positions:
                coin = Coin(pos[0], pos[1], value=20)  # Higher value coins
                collectibles_group.add(coin)
                self.coins.append(coin)

