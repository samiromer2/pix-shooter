"""Additional enemy types with different behaviors."""
from __future__ import annotations

import pygame

import settings as S
from entities.enemy import Enemy


class FlyingEnemy(Enemy):
    """Flying enemy that hovers and shoots from above."""
    
    def __init__(self, x: int, y: int, left_bound: int, right_bound: int, speed: float = 2.0):
        super().__init__(x, y, left_bound, right_bound, speed)
        self.max_hp = 1  # Lower HP
        self.hp = self.max_hp
        self.flying_height = y  # Store flying height
        self.hover_offset = 0.0
        self.hover_speed = 0.1
    
    def update(self, _keys, solids: list[pygame.Rect] | None = None, player=None, bullets_group=None) -> None:
        """Update flying enemy - hovers and doesn't use gravity."""
        self.player_target = player
        
        # Update shoot cooldown
        if self._shoot_cooldown > 0:
            self._shoot_cooldown -= 1
        
        # Hover animation
        self.hover_offset += self.hover_speed
        if self.hover_offset >= 360:
            self.hover_offset = 0.0
        
        import math
        hover_amount = math.sin(math.radians(self.hover_offset)) * 5
        self.position.y = self.flying_height + hover_amount
        
        # Detect player
        player_detected = self.detect_player(player)
        
        if player_detected:
            dx = player.rect.centerx - self.rect.centerx
            self.facing = 1 if dx >= 0 else -1
            
            # Fly towards player horizontally
            if abs(dx) > 50:  # Don't get too close
                chase_dir = 1 if dx > 0 else -1
                self.velocity.x = chase_dir * self.chase_speed
            else:
                self.velocity.x = 0
            
            # Shoot if in range
            distance = (dx * dx + (player.rect.centery - self.rect.centery) ** 2) ** 0.5
            if distance <= self.shoot_range and bullets_group:
                if self.can_shoot():
                    self.shoot(bullets_group)
                    self.velocity.x = 0
        else:
            # Patrol horizontally
            if self.position.x <= self.left_bound:
                self.velocity.x = abs(self.patrol_speed)
                self.facing = 1
            elif self.position.x >= self.right_bound:
                self.velocity.x = -abs(self.patrol_speed)
                self.facing = -1
        
        # Move X (no gravity for flying enemies)
        self.position.x += self.velocity.x
        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)
        
        # Update animation
        state = "idle"
        if abs(self.velocity.x) > 1:
            state = "walk"
        
        if state != self.current_state:
            self.current_state = state
            self.anim_controller.set_animation(state)
        
        self.anim_controller.update(1.0 / 60.0)
        sprite = self.anim_controller.get_frame()
        if sprite:
            if self._scale_factor and self._scale_factor != 1.0:
                w, h = sprite.get_size()
                new_w = int(w * self._scale_factor)
                new_h = int(h * self._scale_factor)
                if abs(new_w - w) > 2 or abs(new_h - h) > 2:
                    sprite = pygame.transform.smoothscale(sprite, (new_w, new_h))
                elif new_w != w or new_h != h:
                    sprite = pygame.transform.scale(sprite, (new_w, new_h))
            sprite = self._apply_enemy_tint(sprite)
            self._base_image = sprite
        else:
            self._base_image = self._create_fallback_sprite()
        
        self.image = pygame.transform.flip(self._base_image, self.facing < 0, False)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center


class TankEnemy(Enemy):
    """Slow, high-HP tank enemy."""
    
    def __init__(self, x: int, y: int, left_bound: int, right_bound: int, speed: float = 1.0):
        super().__init__(x, y, left_bound, right_bound, speed)
        self.max_hp = 5  # High HP
        self.hp = self.max_hp
        self.chase_speed = 1.5  # Slower chase
        self.patrol_speed = speed
        self.shoot_cooldown_frames = 90  # Slower shooting but more damage


class FastEnemy(Enemy):
    """Fast, low-HP enemy."""
    
    def __init__(self, x: int, y: int, left_bound: int, right_bound: int, speed: float = 4.0):
        super().__init__(x, y, left_bound, right_bound, speed)
        self.max_hp = 1  # Low HP
        self.hp = self.max_hp
        self.chase_speed = 5.0  # Very fast chase
        self.patrol_speed = speed
        self.detection_radius = 250  # Larger detection radius
        self.shoot_cooldown_frames = 40  # Faster shooting

