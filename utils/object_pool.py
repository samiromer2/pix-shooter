"""Object pooling system for performance optimization."""
from __future__ import annotations

from typing import TypeVar, Generic, Callable
import pygame

T = TypeVar('T')


class ObjectPool(Generic[T]):
    """Generic object pool for reusing objects."""
    
    def __init__(self, factory: Callable[[], T], initial_size: int = 10, max_size: int = 100):
        """
        Create an object pool.
        
        Args:
            factory: Function that creates new objects
            initial_size: Initial number of objects to create
            max_size: Maximum pool size
        """
        self.factory = factory
        self.max_size = max_size
        self.pool: list[T] = []
        self.active: list[T] = []
        
        # Pre-populate pool
        for _ in range(initial_size):
            self.pool.append(self.factory())
    
    def get(self) -> T:
        """Get an object from the pool."""
        if self.pool:
            obj = self.pool.pop()
        else:
            obj = self.factory()
        self.active.append(obj)
        return obj
    
    def release(self, obj: T) -> None:
        """Return an object to the pool."""
        if obj in self.active:
            self.active.remove(obj)
            if len(self.pool) < self.max_size:
                # Reset object if it has a reset method
                if hasattr(obj, 'reset'):
                    obj.reset()
                self.pool.append(obj)
    
    def release_all(self) -> None:
        """Release all active objects back to pool."""
        while self.active:
            self.release(self.active[0])
    
    def clear(self) -> None:
        """Clear the pool."""
        self.pool.clear()
        self.active.clear()


class BulletPool:
    """Specialized pool for bullets."""
    
    def __init__(self, initial_size: int = 20, max_size: int = 200):
        from entities.bullet import Bullet
        self.pool = ObjectPool(
            lambda: Bullet(0, 0, direction=1, speed=10.0, is_enemy=False),
            initial_size=initial_size,
            max_size=max_size
        )
    
    def get_bullet(self, x: int, y: int, direction: int = 1, speed: float = 10.0, is_enemy: bool = False, damage: int = 1) -> 'Bullet':
        """Get a bullet from the pool."""
        bullet = self.pool.get()
        # Reset bullet properties
        bullet.rect.center = (x, y)
        bullet.direction = 1 if direction >= 0 else -1
        bullet.speed = abs(speed)
        bullet.is_enemy = is_enemy
        bullet.damage = damage
        bullet.is_rocket = False
        bullet._custom_velocity = None
        bullet._trail_positions = []
        return bullet
    
    def release_bullet(self, bullet) -> None:
        """Return a bullet to the pool."""
        self.pool.release(bullet)
    
    def release_all(self) -> None:
        """Release all bullets."""
        self.pool.release_all()

