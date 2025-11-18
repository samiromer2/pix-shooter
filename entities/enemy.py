from __future__ import annotations

import pygame

import settings as S
from utils.sprites import get_sprite_loader
from utils.animations import AnimationController


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, left_bound: int, right_bound: int, speed: float = 2.0, enemy_type_index: int | None = None):
        super().__init__()
        # Load animation controller (randomly select enemy type if not specified)
        self.sprite_loader = get_sprite_loader()
        self.anim_controller = self.sprite_loader.get_enemy_animation_controller(enemy_type_index)
        self.current_state = "idle"
        self.facing = 1 if speed >= 0 else -1
        self._scale_factor = None
        
        sprite = self.anim_controller.get_frame()
        if sprite:
            w, h = sprite.get_size()
            # Better scaling - maintain aspect ratio, target size around 48x48 to 64x64
            target_size = 56  # Good size for enemies
            if w > target_size or h > target_size:
                self._scale_factor = min(target_size / w, target_size / h)
            elif w < target_size * 0.7 or h < target_size * 0.7:
                # Scale up if too small
                self._scale_factor = max(target_size * 0.8 / w, target_size * 0.8 / h)
            else:
                self._scale_factor = 1.0
            
            if self._scale_factor != 1.0:
                new_w = int(w * self._scale_factor)
                new_h = int(h * self._scale_factor)
                # Use smoothscale for better quality
                sprite = pygame.transform.smoothscale(sprite, (new_w, new_h))
            
            # Apply red tint to make enemies look more menacing
            sprite = self._apply_enemy_tint(sprite)
            self.image = sprite
        else:
            # Better fallback placeholder - more detailed
            self.image = self._create_fallback_sprite()
            self._scale_factor = 1.0
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self._base_image = self.image.copy()
        self.position = pygame.Vector2(self.rect.x, self.rect.y)
        self.velocity = pygame.Vector2(speed, 0)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.on_ground = False

        # Health
        self.max_hp = 2
        self.hp = self.max_hp
        
        # AI behavior
        self.detection_radius = 200  # Distance to detect player
        self.chase_speed = 3.0  # Speed when chasing player
        self.patrol_speed = speed  # Original patrol speed
        self.shoot_range = 150  # Distance to start shooting
        self.shoot_cooldown_frames = 60  # Frames between shots
        self._shoot_cooldown = 0
        self.player_target = None  # Reference to player when detected
    
    def _apply_enemy_tint(self, sprite: pygame.Surface) -> pygame.Surface:
        """Apply a red/menacing tint to enemy sprite."""
        # Create a tinted copy
        tinted = sprite.copy()
        # Create a red overlay with alpha
        overlay = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
        # Red tint (subtle - 20% opacity)
        overlay.fill((255, 50, 50, 50))
        tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return tinted
    
    def _create_fallback_sprite(self) -> pygame.Surface:
        """Create a better-looking fallback sprite."""
        size = 48
        sprite = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Body (rounded rectangle)
        body_rect = pygame.Rect(8, 12, 32, 28)
        pygame.draw.ellipse(sprite, (200, 60, 60), body_rect)
        pygame.draw.ellipse(sprite, (150, 40, 40), body_rect, 2)
        
        # Head
        head_rect = pygame.Rect(16, 8, 16, 16)
        pygame.draw.circle(sprite, (220, 80, 80), (24, 16), 8)
        pygame.draw.circle(sprite, (150, 40, 40), (24, 16), 8, 2)
        
        # Eyes (glowing red)
        pygame.draw.circle(sprite, (255, 0, 0), (22, 14), 2)
        pygame.draw.circle(sprite, (255, 0, 0), (26, 14), 2)
        pygame.draw.circle(sprite, (255, 150, 150), (22, 14), 1)
        pygame.draw.circle(sprite, (255, 150, 150), (26, 14), 1)
        
        # Legs
        pygame.draw.rect(sprite, (180, 50, 50), (12, 36, 6, 8))
        pygame.draw.rect(sprite, (180, 50, 50), (30, 36, 6, 8))
        
        return sprite

    def take_damage(self, amount: int) -> None:
        if amount <= 0:
            return
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.kill()

    def _collide_axis(self, solids: list[pygame.Rect], axis: str) -> None:
        hits = [r for r in solids if self.rect.colliderect(r)]
        for tile in hits:
            if axis == "x":
                if self.velocity.x > 0:
                    self.rect.right = tile.left
                elif self.velocity.x < 0:
                    self.rect.left = tile.right
                self.position.x = self.rect.x
                self.velocity.x *= -1  # bounce/flip on walls
            else:
                if self.velocity.y > 0:
                    self.rect.bottom = tile.top
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = tile.bottom
                self.position.y = self.rect.y
                self.velocity.y = 0

    def detect_player(self, player) -> bool:
        """Check if player is within detection radius."""
        if not player or player.hp <= 0:
            return False
        
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = (dx * dx + dy * dy) ** 0.5
        
        return distance <= self.detection_radius
    
    def can_shoot(self) -> bool:
        """Check if enemy can shoot."""
        return self._shoot_cooldown == 0
    
    def shoot(self, bullets_group: pygame.sprite.Group) -> None:
        """Shoot a bullet towards the player."""
        if not self.can_shoot() or not self.player_target:
            return
        
        from entities.bullet import Bullet
        
        # Calculate direction to player
        dx = self.player_target.rect.centerx - self.rect.centerx
        direction = 1 if dx >= 0 else -1
        
        # Spawn bullet from enemy
        bx = self.rect.centerx + (direction * 20)
        by = self.rect.centery
        bullet = Bullet(bx, by, direction=direction, speed=8.0, is_enemy=True)
        bullets_group.add(bullet)
        self._shoot_cooldown = self.shoot_cooldown_frames
    
    def update(self, _keys, solids: list[pygame.Rect] | None = None, player=None, bullets_group=None) -> None:
        """Update enemy AI and movement.
        
        Args:
            _keys: Unused (for compatibility with sprite group update)
            solids: List of solid rectangles for collision
            player: Player sprite to detect and engage
            bullets_group: Group to add bullets to when shooting
        """
        self.player_target = player
        
        # Update shoot cooldown
        if self._shoot_cooldown > 0:
            self._shoot_cooldown -= 1
        
        # Detect player
        player_detected = self.detect_player(player)
        
        if player_detected:
            # Calculate distance to player
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = (dx * dx + dy * dy) ** 0.5
            
            # Face player
            self.facing = 1 if dx >= 0 else -1
            
            # If in shoot range, shoot
            if distance <= self.shoot_range and bullets_group:
                if self.can_shoot():
                    self.shoot(bullets_group)
                # Stop moving when shooting
                self.velocity.x = 0
            else:
                # Chase player (move towards player)
                chase_dir = 1 if dx > 0 else -1
                self.velocity.x = chase_dir * self.chase_speed
        else:
            # Patrol AI: flip direction at bounds
            if self.rect.left <= self.left_bound:
                self.velocity.x = abs(self.patrol_speed)
                self.facing = 1
            elif self.rect.right >= self.right_bound:
                self.velocity.x = -abs(self.patrol_speed)
                self.facing = -1
            else:
                # Continue patrol
                self.velocity.x = self.patrol_speed if self.facing > 0 else -self.patrol_speed

        # Gravity
        if self.velocity.y < 18:
            self.velocity.y += 0.6

        self.on_ground = False
        # Move X
        self.position.x += self.velocity.x
        self.rect.x = round(self.position.x)
        if solids:
            self._collide_axis(solids, "x")

        # Move Y
        self.position.y += self.velocity.y
        self.rect.y = round(self.position.y)
        if solids:
            self._collide_axis(solids, "y")
        else:
            ground_y = S.HEIGHT - 32
            if self.rect.bottom >= ground_y:
                self.rect.bottom = ground_y
                self.position.y = self.rect.y
                self.velocity.y = 0
                self.on_ground = True
        
        # Update sprite animation
        state = "idle"
        if abs(self.velocity.x) > 1:
            state = "walk"
        
        if state != self.current_state:
            self.current_state = state
            self.anim_controller.set_animation(state)
        
        # Update animation frame
        self.anim_controller.update(1.0 / 60.0)
        
        sprite = self.anim_controller.get_frame()
        if sprite:
            # Only scale if needed and cache the scaled version
            if self._scale_factor and self._scale_factor != 1.0:
                w, h = sprite.get_size()
                new_w = int(w * self._scale_factor)
                new_h = int(h * self._scale_factor)
                # Only use smoothscale if significantly different size, otherwise use regular scale for performance
                if abs(new_w - w) > 2 or abs(new_h - h) > 2:
                    sprite = pygame.transform.smoothscale(sprite, (new_w, new_h))
                elif new_w != w or new_h != h:
                    sprite = pygame.transform.scale(sprite, (new_w, new_h))
            # Apply tint each frame
            sprite = self._apply_enemy_tint(sprite)
            self._base_image = sprite
        else:
            # Use fallback sprite
            self._base_image = self._create_fallback_sprite()
        
        # Flip based on facing
        self.image = pygame.transform.flip(self._base_image, self.facing < 0, False)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center


