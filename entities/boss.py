"""Boss entity with multi-phase behavior."""
from __future__ import annotations

import math
import random

import pygame

import settings as S
from entities.bullet import Bullet
from utils.sprites import get_sprite_loader


class Boss(pygame.sprite.Sprite):
    """Boss enemy with multiple phases and attack patterns."""
    
    def __init__(self, x: int, y: int):
        super().__init__()
        
        # Load animation controller
        self.sprite_loader = get_sprite_loader()
        self.anim_controller = self.sprite_loader.get_enemy_animation_controller(0)
        self.current_state = "idle"
        self.facing = 1
        self._scale_factor = None
        
        sprite = self.anim_controller.get_frame()
        if sprite:
            w, h = sprite.get_size()
            # Boss is larger than regular enemies
            if w > 128 or h > 128:
                self._scale_factor = min(128 / w, 128 / h)
            else:
                self._scale_factor = 1.5  # Scale up boss
            if self._scale_factor != 1.0:
                sprite = pygame.transform.scale(sprite, (int(w * self._scale_factor), int(h * self._scale_factor)))
            self.image = sprite
        else:
            # Fallback placeholder - larger for boss
            self.image = pygame.Surface((80, 100))
            self.image.fill((200, 0, 0))  # Red boss
            self._scale_factor = 1.0
        
        self.rect = self.image.get_rect(center=(x, y))
        self._base_image = self.image.copy()
        self.position = pygame.Vector2(self.rect.x, self.rect.y)
        self.velocity = pygame.Vector2(0, 0)
        
        # Boss stats
        self.max_hp = 20  # Much more health than regular enemies
        self.hp = self.max_hp
        self.speed = 1.5
        
        # Phase system
        self.phase = 1  # 1, 2, or 3
        self.phase_thresholds = [0.66, 0.33]  # Phase 2 at 66% HP, Phase 3 at 33% HP
        
        # Attack patterns
        self.attack_cooldown = 0
        self.attack_pattern = 0  # Which attack pattern to use
        self.pattern_cooldown = 0
        
        # Movement bounds
        self.left_bound = x - 200
        self.right_bound = x + 200
        self.patrol_direction = 1
        
        # Player reference
        self.player_target = None
        
        # Animation
        self.animation_frame = 0
    
    def take_damage(self, amount: int) -> None:
        """Take damage and check for phase transitions."""
        if amount <= 0:
            return
        old_hp_ratio = self.hp / self.max_hp
        self.hp = max(0, self.hp - amount)
        new_hp_ratio = self.hp / self.max_hp if self.max_hp > 0 else 0
        
        # Check phase transitions
        if self.phase == 1 and new_hp_ratio <= self.phase_thresholds[0]:
            self.phase = 2
            self.speed = 2.0  # Faster in phase 2
        elif self.phase == 2 and new_hp_ratio <= self.phase_thresholds[1]:
            self.phase = 3
            self.speed = 2.5  # Even faster in phase 3
        
        if self.hp == 0:
            self.kill()
    
    def update(self, keys, solids: list[pygame.Rect] | None = None, player=None, bullets_group=None) -> None:
        """Update boss behavior."""
        self.player_target = player
        self.animation_frame += 1
        
        # Update attack cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.pattern_cooldown > 0:
            self.pattern_cooldown -= 1
        
        # Face player
        if player and player.hp > 0:
            if player.rect.centerx > self.rect.centerx:
                self.facing = 1
            else:
                self.facing = -1
        
        # Movement - patrol back and forth
        self.velocity.x = self.patrol_direction * self.speed
        self.position.x += self.velocity.x
        
        # Bounce at bounds
        if self.position.x <= self.left_bound:
            self.position.x = self.left_bound
            self.patrol_direction = 1
        elif self.position.x >= self.right_bound:
            self.position.x = self.right_bound
            self.patrol_direction = -1
        
        self.rect.x = int(self.position.x)
        
        # Attack patterns based on phase
        if player and player.hp > 0 and bullets_group:
            if self.attack_cooldown == 0:
                self._perform_attack(bullets_group)
    
    def _perform_attack(self, bullets_group: pygame.sprite.Group) -> None:
        """Perform attack based on current phase."""
        if not self.player_target:
            return
        
        if self.phase == 1:
            # Phase 1: Simple shots
            self._attack_single_shot(bullets_group)
            self.attack_cooldown = 60  # 1 second at 60 FPS
        elif self.phase == 2:
            # Phase 2: Spread shots
            if self.pattern_cooldown == 0:
                self._attack_spread(bullets_group)
                self.attack_cooldown = 45
                self.pattern_cooldown = 120
            else:
                self._attack_single_shot(bullets_group)
                self.attack_cooldown = 40
        else:  # Phase 3
            # Phase 3: Rapid fire and spread
            if self.pattern_cooldown == 0:
                self._attack_rapid_spread(bullets_group)
                self.attack_cooldown = 30
                self.pattern_cooldown = 90
            else:
                self._attack_single_shot(bullets_group)
                self.attack_cooldown = 30
    
    def _attack_single_shot(self, bullets_group: pygame.sprite.Group) -> None:
        """Fire a single bullet at player."""
        if not self.player_target:
            return
        dx = self.player_target.rect.centerx - self.rect.centerx
        dy = self.player_target.rect.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > 0:
            direction = 1 if dx > 0 else -1
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction=direction, speed=8.0, is_enemy=True)
            bullets_group.add(bullet)
    
    def _attack_spread(self, bullets_group: pygame.sprite.Group) -> None:
        """Fire multiple bullets in a spread pattern."""
        if not self.player_target:
            return
        dx = self.player_target.rect.centerx - self.rect.centerx
        dy = self.player_target.rect.centery - self.rect.centery
        angle = math.atan2(dy, dx)
        
        # Fire 5 bullets in a spread
        for i in range(5):
            spread_angle = angle + math.radians((i - 2) * 15)  # 15 degree spread
            speed = 7.0
            vx = math.cos(spread_angle) * speed
            vy = math.sin(spread_angle) * speed
            
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction=1 if vx >= 0 else -1, speed=abs(vx), is_enemy=True)
            bullet._custom_velocity = pygame.Vector2(vx, vy)
            bullets_group.add(bullet)
    
    def _attack_rapid_spread(self, bullets_group: pygame.sprite.Group) -> None:
        """Fire rapid spread shots in all directions."""
        # Fire 8 bullets in a circle
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            speed = 6.0
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction=1 if vx >= 0 else -1, speed=abs(vx), is_enemy=True)
            bullet._custom_velocity = pygame.Vector2(vx, vy)
            bullets_group.add(bullet)

