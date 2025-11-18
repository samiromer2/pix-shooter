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
                # Use regular scale for boss (smoothscale is expensive)
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
        self.attack_sequence = []  # For complex attack sequences
        self.sequence_index = 0
        
        # Movement bounds
        self.left_bound = x - 200
        self.right_bound = x + 200
        self.patrol_direction = 1
        
        # Player reference
        self.player_target = None
        
        # Animation
        self.animation_frame = 0
        
        # Visual indicators
        self.charge_timer = 0  # For charge-up attacks
        self.flash_timer = 0  # For visual flash effects
        self.phase_transition_timer = 0  # Visual effect on phase change
    
    def take_damage(self, amount: int) -> None:
        """Take damage and check for phase transitions."""
        if amount <= 0:
            return
        old_hp_ratio = self.hp / self.max_hp
        self.hp = max(0, self.hp - amount)
        new_hp_ratio = self.hp / self.max_hp if self.max_hp > 0 else 0
        
        # Check phase transitions
        old_phase = self.phase
        if self.phase == 1 and new_hp_ratio <= self.phase_thresholds[0]:
            self.phase = 2
            self.speed = 2.0  # Faster in phase 2
            self.phase_transition_timer = 60  # Visual effect duration
        elif self.phase == 2 and new_hp_ratio <= self.phase_thresholds[1]:
            self.phase = 3
            self.speed = 2.5  # Even faster in phase 3
            self.phase_transition_timer = 60  # Visual effect duration
        
        if self.phase != old_phase:
            # Reset attack patterns on phase change
            self.attack_cooldown = 0
            self.pattern_cooldown = 0
        
        if self.hp == 0:
            self.kill()
    
    def update(self, keys, solids: list[pygame.Rect] | None = None, player=None, bullets_group=None) -> None:
        """Update boss behavior."""
        self.player_target = player
        self.animation_frame += 1
        
        # Update visual timers
        if self.charge_timer > 0:
            self.charge_timer -= 1
        if self.flash_timer > 0:
            self.flash_timer -= 1
        if self.phase_transition_timer > 0:
            self.phase_transition_timer -= 1
        
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
        
        # Update sprite with visual effects
        self._update_sprite()
        
        # Attack patterns based on phase
        if player and player.hp > 0 and bullets_group:
            if self.attack_cooldown == 0:
                self._perform_attack(bullets_group)
    
    def _update_sprite(self) -> None:
        """Update boss sprite with visual effects."""
        # Update animation controller
        self.anim_controller.update(1.0 / 60.0)
        sprite = self.anim_controller.get_frame()
        if sprite:
            if self._scale_factor and self._scale_factor != 1.0:
                w, h = sprite.get_size()
                new_w = int(w * self._scale_factor)
                new_h = int(h * self._scale_factor)
                sprite = pygame.transform.scale(sprite, (new_w, new_h))
            
            # Apply visual effects
            if self.phase_transition_timer > 0:
                # Flash white during phase transition
                flash_surf = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
                flash_alpha = int(100 * (self.phase_transition_timer / 60))
                flash_surf.fill((255, 255, 255, flash_alpha))
                sprite.blit(flash_surf, (0, 0), special_flags=pygame.BLEND_ADD)
            
            if self.charge_timer > 0:
                # Red glow when charging
                charge_surf = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
                charge_alpha = int(80 * (self.charge_timer / 20))
                charge_surf.fill((255, 100, 100, charge_alpha))
                sprite.blit(charge_surf, (0, 0), special_flags=pygame.BLEND_ADD)
            
            if self.flash_timer > 0:
                # Yellow flash when attacking
                flash_surf = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
                flash_alpha = int(120 * (self.flash_timer / 15))
                flash_surf.fill((255, 255, 100, flash_alpha))
                sprite.blit(flash_surf, (0, 0), special_flags=pygame.BLEND_ADD)
            
            # Phase-based tint
            if self.phase == 3:
                # Red tint for phase 3
                tint_surf = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
                tint_surf.fill((255, 50, 50, 30))
                sprite.blit(tint_surf, (0, 0), special_flags=pygame.BLEND_MULT)
            elif self.phase == 2:
                # Orange tint for phase 2
                tint_surf = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
                tint_surf.fill((255, 150, 50, 20))
                sprite.blit(tint_surf, (0, 0), special_flags=pygame.BLEND_MULT)
            
            self._base_image = sprite
        
        # Flip sprite based on facing
        self.image = pygame.transform.flip(self._base_image, self.facing < 0, False)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
    
    def _perform_attack(self, bullets_group: pygame.sprite.Group) -> None:
        """Perform attack based on current phase."""
        if not self.player_target:
            return
        
        # Randomly select attack pattern for variety
        attack_choice = random.randint(0, 2)
        
        if self.phase == 1:
            # Phase 1: Simple shots with occasional burst
            if attack_choice == 0 and self.pattern_cooldown == 0:
                self._attack_burst(bullets_group, count=3)
                self.attack_cooldown = 50
                self.pattern_cooldown = 180
            else:
                self._attack_single_shot(bullets_group)
                self.attack_cooldown = 60
        elif self.phase == 2:
            # Phase 2: Spread shots, burst, and charge attacks
            if attack_choice == 0 and self.pattern_cooldown == 0:
                self._attack_spread(bullets_group)
                self.attack_cooldown = 45
                self.pattern_cooldown = 120
            elif attack_choice == 1:
                self._attack_burst(bullets_group, count=5)
                self.attack_cooldown = 50
            else:
                self._attack_single_shot(bullets_group)
                self.attack_cooldown = 35
        else:  # Phase 3
            # Phase 3: All attacks, including rapid spread and wave
            if attack_choice == 0 and self.pattern_cooldown == 0:
                self._attack_rapid_spread(bullets_group)
                self.attack_cooldown = 30
                self.pattern_cooldown = 90
            elif attack_choice == 1:
                self._attack_wave(bullets_group)
                self.attack_cooldown = 40
            else:
                self._attack_burst(bullets_group, count=7)
                self.attack_cooldown = 25
    
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
        self.flash_timer = 10  # Visual flash
    
    def _attack_burst(self, bullets_group: pygame.sprite.Group, count: int = 3) -> None:
        """Fire multiple bullets in quick succession at player."""
        if not self.player_target:
            return
        dx = self.player_target.rect.centerx - self.rect.centerx
        dy = self.player_target.rect.centery - self.rect.centery
        angle = math.atan2(dy, dx)
        
        # Fire burst of bullets
        for i in range(count):
            spread = math.radians((i - count // 2) * 8)  # Small spread
            bullet_angle = angle + spread
            speed = 8.0
            vx = math.cos(bullet_angle) * speed
            vy = math.sin(bullet_angle) * speed
            
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction=1 if vx >= 0 else -1, speed=abs(vx), is_enemy=True)
            bullet._custom_velocity = pygame.Vector2(vx, vy)
            bullets_group.add(bullet)
        self.charge_timer = 20  # Charge-up visual
    
    def _attack_wave(self, bullets_group: pygame.sprite.Group) -> None:
        """Fire bullets in a wave pattern."""
        # Fire bullets in a sine wave pattern
        for i in range(12):
            base_angle = (i / 12) * math.pi  # Half circle
            wave_offset = math.sin(i * 0.5) * 0.3  # Wave effect
            angle = base_angle + wave_offset
            speed = 7.0
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 2.0  # Upward bias
            
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction=1 if vx >= 0 else -1, speed=abs(vx), is_enemy=True)
            bullet._custom_velocity = pygame.Vector2(vx, vy)
            bullets_group.add(bullet)
        self.flash_timer = 15  # Visual flash

