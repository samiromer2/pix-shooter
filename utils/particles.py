"""Particle effects system for visual polish."""
from __future__ import annotations

import math
import random

import pygame


class Particle:
    """Single particle in a particle effect."""
    
    def __init__(
        self,
        x: float,
        y: float,
        vx: float,
        vy: float,
        color: tuple[int, int, int],
        lifetime: int,
        size: int = 2,
        fade: bool = True
    ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.fade = fade
        
    def update(self) -> bool:
        """Update particle. Returns False if particle should be removed."""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravity
        self.lifetime -= 1
        return self.lifetime > 0
    
    def draw(self, surface: pygame.Surface, camera_offset: tuple[int, int] = (0, 0)) -> None:
        """Draw the particle."""
        if self.lifetime <= 0:
            return
        
        offset_x, offset_y = camera_offset
        screen_x = int(self.x + offset_x)
        screen_y = int(self.y + offset_y)
        
        # Fade out over time
        if self.fade:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            color = (*self.color, alpha)
            # Create a surface with per-pixel alpha
            particle_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color, (self.size, self.size), self.size)
            surface.blit(particle_surf, (screen_x - self.size, screen_y - self.size))
        else:
            pygame.draw.circle(surface, self.color, (screen_x, screen_y), self.size)


class ParticleSystem:
    """Manages a collection of particles."""
    
    def __init__(self):
        self.particles: list[Particle] = []
    
    def add_particle(self, particle: Particle) -> None:
        """Add a particle to the system."""
        self.particles.append(particle)
    
    def create_explosion(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int] = (255, 200, 0),
        count: int = 15,
        speed: float = 3.0
    ) -> None:
        """Create an explosion effect at the given position."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed_variation = random.uniform(0.5, 1.5) * speed
            vx = math.cos(angle) * speed_variation
            vy = math.sin(angle) * speed_variation - 1.0  # Slight upward bias
            lifetime = random.randint(20, 40)
            size = random.randint(2, 4)
            self.add_particle(Particle(x, y, vx, vy, color, lifetime, size))
    
    def create_dust(
        self,
        x: float,
        y: float,
        direction: int = 1,
        count: int = 5
    ) -> None:
        """Create dust particles (for landing, running, etc.)."""
        for _ in range(count):
            vx = random.uniform(-1.0, 1.0) * direction + (direction * 0.5)
            vy = random.uniform(-2.0, 0.0)
            lifetime = random.randint(10, 20)
            size = random.randint(1, 2)
            color = (150, 150, 150)
            self.add_particle(Particle(x, y, vx, vy, color, lifetime, size))
    
    def create_impact(
        self,
        x: float,
        y: float,
        count: int = 8
    ) -> None:
        """Create impact particles (for bullet hits)."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1.0, 3.0)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            lifetime = random.randint(8, 15)
            size = random.randint(1, 2)
            color = (200, 150, 100)
            self.add_particle(Particle(x, y, vx, vy, color, lifetime, size))
    
    def create_muzzle_flash(
        self,
        x: float,
        y: float,
        direction: int = 1,
        count: int = 6
    ) -> None:
        """Create muzzle flash particles."""
        for _ in range(count):
            vx = direction * random.uniform(2.0, 4.0)
            vy = random.uniform(-1.0, 1.0)
            lifetime = random.randint(3, 8)
            size = random.randint(2, 3)
            color = (255, 255, 100)
            self.add_particle(Particle(x, y, vx, vy, color, lifetime, size, fade=False))
    
    def create_bullet_trail(
        self,
        x: float,
        y: float,
        direction: int = 1,
        color: tuple[int, int, int] = (255, 255, 200),
        count: int = 3
    ) -> None:
        """Create a trail effect behind a bullet."""
        for _ in range(count):
            vx = -direction * random.uniform(0.5, 1.5)
            vy = random.uniform(-0.5, 0.5)
            lifetime = random.randint(5, 10)
            size = random.randint(1, 2)
            self.add_particle(Particle(x, y, vx, vy, color, lifetime, size))
    
    def create_impact_sparks(
        self,
        x: float,
        y: float,
        count: int = 12,
        color: tuple[int, int, int] = (255, 200, 100)
    ) -> None:
        """Create spark particles on impact."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1.5, 3.5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 0.5  # Slight upward
            lifetime = random.randint(8, 15)
            size = random.randint(1, 2)
            self.add_particle(Particle(x, y, vx, vy, color, lifetime, size))
    
    def create_big_explosion(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int] = (255, 150, 0),
        count: int = 30,
        speed: float = 5.0
    ) -> None:
        """Create a large explosion effect."""
        # Outer ring
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed_variation = random.uniform(0.5, 1.5) * speed
            vx = math.cos(angle) * speed_variation
            vy = math.sin(angle) * speed_variation - 1.5
            lifetime = random.randint(25, 50)
            size = random.randint(3, 5)
            self.add_particle(Particle(x, y, vx, vy, color, lifetime, size))
        
        # Inner bright flash
        for _ in range(count // 2):
            angle = random.uniform(0, 2 * math.pi)
            speed_variation = random.uniform(0.3, 0.8) * speed
            vx = math.cos(angle) * speed_variation
            vy = math.sin(angle) * speed_variation
            lifetime = random.randint(10, 20)
            size = random.randint(4, 6)
            bright_color = (255, 255, 200)
            self.add_particle(Particle(x, y, vx, vy, bright_color, lifetime, size, fade=False))
    
    def update(self) -> None:
        """Update all particles."""
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self, surface: pygame.Surface, camera_offset: tuple[int, int] = (0, 0)) -> None:
        """Draw all particles."""
        for particle in self.particles:
            particle.draw(surface, camera_offset)
    
    def clear(self) -> None:
        """Clear all particles."""
        self.particles.clear()

