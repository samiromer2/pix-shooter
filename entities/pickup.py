from __future__ import annotations

import pygame

import settings as S
from utils.animations import load_image


class AmmoPickup(pygame.sprite.Sprite):
    """Ammo pickup that restores player ammo when collected."""
    
    def __init__(self, x: int, y: int, ammo_amount: int = 30) -> None:
        super().__init__()
        self.ammo_amount = ammo_amount
        
        # Load ammo pack sprite
        pickup_path = "assets/sprites/pickups/ammo_pack.png"
        sprite = load_image(pickup_path)
        
        if sprite:
            w, h = sprite.get_size()
            # Scale if too large
            if w > 32 or h > 32:
                scale = min(32 / w, 32 / h)
                sprite = pygame.transform.scale(sprite, (int(w * scale), int(h * scale)))
            self.image = sprite
        else:
            # Fallback placeholder
            self.image = pygame.Surface((24, 24))
            self.image.fill((200, 200, 50))
            # Draw a simple "A" for ammo
            pygame.draw.rect(self.image, (255, 255, 0), (4, 4, 16, 16))
        
        self.rect = self.image.get_rect(center=(x, y))
        
        # Animation/bobbing
        self.bob_offset = 0.0
        self.bob_speed = 2.0
        self._base_y = y  # Store original Y position
        
    def update(self, *args, **kwargs) -> None:
        """Animate the pickup (bobbing motion)."""
        import math
        self.bob_offset += self.bob_speed
        # Reset offset to prevent overflow
        if self.bob_offset >= 360:
            self.bob_offset = 0.0
        
        # Bob up and down (sine wave)
        bob_amount = math.sin(math.radians(self.bob_offset)) * 3
        self.rect.y = int(self._base_y + bob_amount)
    
    def collect(self, player) -> bool:
        """Try to collect this pickup. Returns True if collected.
        
        Adds ammo directly to the current magazine (ammo_in_mag).
        No limits - just adds the amount directly to current ammo.
        """
        if self.rect.colliderect(player.rect):
            # Add directly to current magazine - increases current ammo count
            player.ammo_in_mag += self.ammo_amount
            return True
        return False


class HealthPickup(pygame.sprite.Sprite):
    """Health pickup that restores player HP when collected."""
    
    def __init__(self, x: int, y: int, health_amount: int = 2) -> None:
        super().__init__()
        self.health_amount = health_amount
        
        # Create a simple health pickup sprite (red cross)
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        # Draw red cross
        pygame.draw.rect(self.image, (255, 50, 50), (10, 4, 4, 16))
        pygame.draw.rect(self.image, (255, 50, 50), (4, 10, 16, 4))
        
        self.rect = self.image.get_rect(center=(x, y))
        
        # Animation/bobbing
        self.bob_offset = 0.0
        self.bob_speed = 2.0
        self._base_y = y
    
    def update(self, *args, **kwargs) -> None:
        """Animate the pickup (bobbing motion)."""
        import math
        self.bob_offset += self.bob_speed
        if self.bob_offset >= 360:
            self.bob_offset = 0.0
        
        bob_amount = math.sin(math.radians(self.bob_offset)) * 3
        self.rect.y = int(self._base_y + bob_amount)
    
    def collect(self, player) -> bool:
        """Try to collect this pickup. Returns True if collected."""
        if self.rect.colliderect(player.rect):
            # Restore health (up to max)
            player.hp = min(player.max_hp, player.hp + self.health_amount)
            return True
        return False


class ShieldPickup(pygame.sprite.Sprite):
    """Shield pickup that grants temporary invincibility when collected."""
    
    def __init__(self, x: int, y: int, shield_duration: int = 300) -> None:
        super().__init__()
        self.shield_duration = shield_duration  # Frames of shield
        
        # Create a simple shield pickup sprite (blue shield)
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        # Draw blue shield shape
        pygame.draw.circle(self.image, (100, 150, 255), (12, 12), 10, 2)
        pygame.draw.arc(self.image, (150, 200, 255), (4, 4, 16, 16), 0, 3.14, 2)
        
        self.rect = self.image.get_rect(center=(x, y))
        
        # Animation/bobbing
        self.bob_offset = 0.0
        self.bob_speed = 2.0
        self._base_y = y
    
    def update(self, *args, **kwargs) -> None:
        """Animate the pickup (bobbing motion)."""
        import math
        self.bob_offset += self.bob_speed
        if self.bob_offset >= 360:
            self.bob_offset = 0.0
        
        bob_amount = math.sin(math.radians(self.bob_offset)) * 3
        self.rect.y = int(self._base_y + bob_amount)
    
    def collect(self, player) -> bool:
        """Try to collect this pickup. Returns True if collected."""
        if self.rect.colliderect(player.rect):
            # Grant shield (extend iframes significantly)
            player._iframes_counter = max(player._iframes_counter, self.shield_duration)
            return True
        return False


class SpeedPickup(pygame.sprite.Sprite):
    """Speed boost pickup that temporarily increases movement speed."""
    
    def __init__(self, x: int, y: int, duration: int = 600, speed_multiplier: float = 1.5) -> None:
        super().__init__()
        self.duration = duration
        self.speed_multiplier = speed_multiplier
        
        # Create speed pickup sprite (green arrow)
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        # Draw green arrow pointing right
        pygame.draw.polygon(self.image, (50, 255, 50), [(4, 12), (16, 6), (16, 10), (20, 10), (20, 14), (16, 14), (16, 18)])
        
        self.rect = self.image.get_rect(center=(x, y))
        self.bob_offset = 0.0
        self.bob_speed = 2.0
        self._base_y = y
    
    def update(self, *args, **kwargs) -> None:
        """Animate the pickup."""
        import math
        self.bob_offset += self.bob_speed
        if self.bob_offset >= 360:
            self.bob_offset = 0.0
        bob_amount = math.sin(math.radians(self.bob_offset)) * 3
        self.rect.y = int(self._base_y + bob_amount)
    
    def collect(self, player) -> bool:
        """Try to collect this pickup."""
        if self.rect.colliderect(player.rect):
            # Apply speed boost
            if not hasattr(player, '_speed_boost_end'):
                player._speed_boost_end = 0
            player._speed_boost_end = max(player._speed_boost_end, pygame.time.get_ticks() + self.duration * 16)  # Convert frames to ms
            player.speed_multiplier *= self.speed_multiplier
            return True
        return False


class DamageBoostPickup(pygame.sprite.Sprite):
    """Damage boost pickup that temporarily increases weapon damage."""
    
    def __init__(self, x: int, y: int, duration: int = 600, damage_multiplier: float = 2.0) -> None:
        super().__init__()
        self.duration = duration
        self.damage_multiplier = damage_multiplier
        
        # Create damage boost sprite (red star)
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        # Draw red star
        import math
        center = (12, 12)
        outer_radius = 10
        inner_radius = 5
        points = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(self.image, (255, 50, 50), points)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.bob_offset = 0.0
        self.bob_speed = 2.0
        self._base_y = y
    
    def update(self, *args, **kwargs) -> None:
        """Animate the pickup."""
        import math
        self.bob_offset += self.bob_speed
        if self.bob_offset >= 360:
            self.bob_offset = 0.0
        bob_amount = math.sin(math.radians(self.bob_offset)) * 3
        self.rect.y = int(self._base_y + bob_amount)
    
    def collect(self, player) -> bool:
        """Try to collect this pickup."""
        if self.rect.colliderect(player.rect):
            # Apply damage boost
            if not hasattr(player, '_damage_boost_end'):
                player._damage_boost_end = 0
            player._damage_boost_end = max(player._damage_boost_end, pygame.time.get_ticks() + self.duration * 16)
            if not hasattr(player, '_damage_multiplier'):
                player._damage_multiplier = 1.0
            player._damage_multiplier *= self.damage_multiplier
            return True
        return False


