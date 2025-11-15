"""Weapon system with multiple weapon types."""
from __future__ import annotations

import math
import random

import pygame

from entities.bullet import Bullet


class Weapon:
    """Base class for weapons."""
    
    def __init__(
        self,
        name: str,
        fire_rate: int = 10,  # Frames between shots
        ammo_per_shot: int = 1,
        damage: int = 1,
        bullet_speed: float = 10.0
    ):
        self.name = name
        self.fire_rate = fire_rate
        self.ammo_per_shot = ammo_per_shot
        self.damage = damage
        self.bullet_speed = bullet_speed
    
    def shoot(
        self,
        x: int,
        y: int,
        direction: int,
        bullets_group: pygame.sprite.Group
    ) -> bool:
        """Shoot bullets. Returns True if shot was fired."""
        raise NotImplementedError("Subclasses must implement shoot()")
    
    def get_ammo_cost(self) -> int:
        """Get ammo cost per shot."""
        return self.ammo_per_shot


class Pistol(Weapon):
    """Default mining tool - Basic Hash Power."""
    
    def __init__(self):
        super().__init__(
            name="Hash Power",
            fire_rate=10,
            ammo_per_shot=1,
            damage=1,
            bullet_speed=10.0
        )
    
    def shoot(
        self,
        x: int,
        y: int,
        direction: int,
        bullets_group: pygame.sprite.Group
    ) -> bool:
        """Shoot a single bullet."""
        bullet = Bullet(x, y, direction=direction, speed=self.bullet_speed, is_enemy=False)
        bullets_group.add(bullet)
        return True


class Shotgun(Weapon):
    """Mining Rig that fires multiple hashes in a spread."""
    
    def __init__(self):
        super().__init__(
            name="Mining Rig",
            fire_rate=30,  # Slower fire rate
            ammo_per_shot=2,  # Uses more ammo
            damage=1,
            bullet_speed=8.0
        )
        self.spread_count = 5  # Number of pellets
        self.spread_angle = 30  # Degrees of spread
    
    def shoot(
        self,
        x: int,
        y: int,
        direction: int,
        bullets_group: pygame.sprite.Group
    ) -> bool:
        """Shoot multiple bullets in a spread pattern."""
        base_angle = 0 if direction > 0 else 180
        
        for i in range(self.spread_count):
            # Calculate spread angle
            angle_offset = (i - self.spread_count // 2) * (self.spread_angle / self.spread_count)
            angle_rad = math.radians(base_angle + angle_offset)
            
            # Calculate velocity components
            vx = math.cos(angle_rad) * self.bullet_speed
            vy = math.sin(angle_rad) * self.bullet_speed
            
            # Create bullet with custom velocity
            bullet = Bullet(x, y, direction=direction, speed=abs(vx), is_enemy=False)
            # Override bullet's direction-based movement with angle-based
            bullet.direction = 1 if vx >= 0 else -1
            bullet.speed = abs(vx)
            # Store custom velocity for angled movement
            bullet._custom_velocity = pygame.Vector2(vx, vy)
            bullets_group.add(bullet)
        
        return True


class Laser(Weapon):
    """Lightning Network - fast transaction processing."""
    
    def __init__(self):
        super().__init__(
            name="Lightning",
            fire_rate=5,  # Very fast fire rate
            ammo_per_shot=1,
            damage=1,
            bullet_speed=20.0  # Very fast
        )
    
    def shoot(
        self,
        x: int,
        y: int,
        direction: int,
        bullets_group: pygame.sprite.Group
    ) -> bool:
        """Shoot a fast laser bullet."""
        bullet = Bullet(x, y, direction=direction, speed=self.bullet_speed, is_enemy=False)
        bullets_group.add(bullet)
        return True


class Rocket(Weapon):
    """ASIC Miner - powerful but expensive mining hardware."""
    
    def __init__(self):
        super().__init__(
            name="ASIC Miner",
            fire_rate=60,  # Slow fire rate
            ammo_per_shot=3,  # Expensive ammo
            damage=2,  # More damage
            bullet_speed=6.0  # Slower but powerful
        )
    
    def shoot(
        self,
        x: int,
        y: int,
        direction: int,
        bullets_group: pygame.sprite.Group
    ) -> bool:
        """Shoot a rocket."""
        bullet = Bullet(x, y, direction=direction, speed=self.bullet_speed, is_enemy=False)
        bullet.is_rocket = True  # Mark as rocket for explosion effect
        bullets_group.add(bullet)
        return True

