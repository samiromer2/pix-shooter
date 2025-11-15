from __future__ import annotations

from dataclasses import dataclass

import pygame

import settings as S
from utils.sprites import get_sprite_loader
from utils.animations import AnimationController


@dataclass
class Physics:
    gravity: float = 0.6
    move_speed: float = 4.0
    jump_velocity: float = -12.0
    max_fall_speed: float = 18.0
    friction: float = 0.8


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, physics: Physics | None = None) -> None:
        super().__init__()
        self.physics: Physics = physics or Physics()

        # Load animation controller
        self.sprite_loader = get_sprite_loader()
        self.anim_controller = self.sprite_loader.get_player_animation_controller()
        self.current_state = "idle"
        self._scale_factor = None  # Cache scale for all frames
        
        # Initialize first frame and determine scale
        sprite = self.anim_controller.get_frame()
        if sprite:
            w, h = sprite.get_size()
            if w > 64 or h > 96:
                self._scale_factor = min(64 / w, 96 / h)
            else:
                self._scale_factor = 1.0
            if self._scale_factor != 1.0:
                sprite = pygame.transform.scale(sprite, (int(w * self._scale_factor), int(h * self._scale_factor)))
            self.image = sprite
        else:
            # Fallback placeholder
            self.image = pygame.Surface((32, 48))
            self.image.fill(S.BLUE)
            self._scale_factor = 1.0
        self.rect = self.image.get_rect(topleft=(x, y))
        self._base_image = self.image.copy()  # Store for flipping

        # Sub-pixel precise position and velocity
        self.position = pygame.Vector2(self.rect.x, self.rect.y)
        self.velocity = pygame.Vector2(0, 0)

        self.on_ground = False
        self.facing = 1  # 1 right, -1 left
        self.shoot_cooldown_frames = 10
        self._cooldown_counter = 0

        # Health
        self.max_hp = 5
        self.hp = self.max_hp
        self.iframes_frames = 30
        self._iframes_counter = 0
        self.hp_upgrades = 0  # Track health upgrades

        # Ammo
        self.mag_capacity = 10
        self.ammo_in_mag = self.mag_capacity
        self.reserve_ammo = 50
        self.ammo_upgrades = 0  # Track ammo upgrades
        
        # Movement upgrades
        self.speed_multiplier = 1.0  # Speed upgrade multiplier
        self.jump_multiplier = 1.0  # Jump upgrade multiplier
        
        # Weapon system (Bitcoin mining tools)
        from entities.weapon import Weapon, Pistol
        self.weapons: list[Weapon] = [Pistol()]  # Start with Hash Power
        self.current_weapon_index = 0
        self.weapon_switch_cooldown = 0

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        # Horizontal movement
        move_dir = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_dir -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_dir += 1

        self.velocity.x = move_dir * self.physics.move_speed * self.speed_multiplier
        if move_dir != 0:
            self.facing = 1 if move_dir > 0 else -1

        # Jump (only if on ground) - with jump upgrade
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity.y = self.physics.jump_velocity * self.jump_multiplier
            self.on_ground = False

    def apply_gravity(self) -> None:
        if self.velocity.y < self.physics.max_fall_speed:
            self.velocity.y += self.physics.gravity
    
    def upgrade_health(self) -> None:
        """Upgrade max health."""
        self.max_hp += 1
        self.hp = self.max_hp  # Restore to new max
        self.hp_upgrades += 1
    
    def upgrade_ammo(self) -> None:
        """Upgrade magazine capacity."""
        self.mag_capacity += 2
        self.ammo_in_mag = self.mag_capacity  # Fill new capacity
        self.ammo_upgrades += 1
    
    def upgrade_speed(self) -> None:
        """Upgrade movement speed."""
        self.speed_multiplier += 0.1
    
    def upgrade_jump(self) -> None:
        """Upgrade jump height."""
        self.jump_multiplier += 0.15

    def apply_friction(self) -> None:
        if self.on_ground and abs(self.velocity.x) > 0:
            self.velocity.x *= self.physics.friction
            if abs(self.velocity.x) < 0.05:
                self.velocity.x = 0

    def take_damage(self, amount: int) -> None:
        if self._iframes_counter > 0 or amount <= 0:
            return
        self.hp = max(0, self.hp - amount)
        self._iframes_counter = self.iframes_frames

    def _collide_axis(self, solids: list[pygame.Rect], axis: str) -> None:
        hits = [r for r in solids if self.rect.colliderect(r)]
        for tile in hits:
            if axis == "x":
                if self.velocity.x > 0:
                    self.rect.right = tile.left
                elif self.velocity.x < 0:
                    self.rect.left = tile.right
                self.position.x = self.rect.x
                self.velocity.x = 0
            else:  # y axis
                if self.velocity.y > 0:
                    self.rect.bottom = tile.top
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = tile.bottom
                self.position.y = self.rect.y
                self.velocity.y = 0

    def _update_sprite(self, dt: float = 0.016) -> None:
        """Update sprite based on current state and animate frames."""
        state = "idle"
        if not self.on_ground:
            state = "jump"
        elif abs(self.velocity.x) > 2:
            state = "run"
        elif abs(self.velocity.x) > 0:
            state = "walk"
        if self._cooldown_counter > 0:
            state = "attack"
        
        # Switch animation if state changed
        if state != self.current_state:
            self.current_state = state
            self.anim_controller.set_animation(state)
        
        # Update animation frame
        self.anim_controller.update(dt)
        
        # Get current frame and scale if needed
        sprite = self.anim_controller.get_frame()
        if sprite:
            if self._scale_factor and self._scale_factor != 1.0:
                w, h = sprite.get_size()
                sprite = pygame.transform.scale(sprite, (int(w * self._scale_factor), int(h * self._scale_factor)))
            self._base_image = sprite
        else:
            # Fallback if animation failed
            self._base_image = pygame.Surface((32, 48))
            self._base_image.fill(S.BLUE)
        
        # Flip sprite based on facing direction
        self.image = pygame.transform.flip(self._base_image, self.facing < 0, False)
        # Keep rect size consistent
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
    
    def update(self, keys: pygame.key.ScancodeWrapper, solids: list[pygame.Rect] | None = None, moving_platforms: list | None = None) -> None:
        self.handle_input(keys)
        self.apply_gravity()
        self.apply_friction()

        if self._cooldown_counter > 0:
            self._cooldown_counter -= 1
        if self._iframes_counter > 0:
            self._iframes_counter -= 1
        if self.weapon_switch_cooldown > 0:
            self.weapon_switch_cooldown -= 1

        # Check if on a moving platform
        platform_velocity = pygame.Vector2(0, 0)
        if moving_platforms:
            for platform in moving_platforms:
                # Check if player is on top of platform
                if (self.rect.bottom <= platform.rect.top + 5 and
                    self.rect.right > platform.rect.left and
                    self.rect.left < platform.rect.right):
                    platform_velocity = platform.get_velocity()
                    # Move player with platform
                    self.position.x += platform_velocity.x
                    self.position.y += platform_velocity.y
                    break

        # Integrate with axis separation and resolve collisions if solids provided
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
            # Fallback: simple bottom-of-screen floor
            ground_y = S.HEIGHT - 32
            if self.rect.bottom >= ground_y:
                self.rect.bottom = ground_y
                self.position.y = self.rect.y
                self.velocity.y = 0
                self.on_ground = True
        
        # Update sprite appearance (dt is ~1/60 for 60 FPS)
        self._update_sprite(1.0 / 60.0)

    def can_shoot(self) -> bool:
        """Check if player can shoot with current weapon."""
        if self._cooldown_counter > 0:
            return False
        if not self.weapons or self.current_weapon_index >= len(self.weapons):
            return False
        weapon = self.weapons[self.current_weapon_index]
        return self.ammo_in_mag >= weapon.get_ammo_cost()

    def shoot(self, bullets_group: pygame.sprite.Group) -> bool:
        """Shoot using current weapon. Returns True if shot was fired, False otherwise."""
        if not self.can_shoot():
            return False
        
        weapon = self.weapons[self.current_weapon_index]
        
        # Spawn bullet from player's mid-body
        bx = self.rect.centerx + (self.facing * 20)
        by = self.rect.centery
        
        # Use weapon's shoot method
        if weapon.shoot(bx, by, self.facing, bullets_group):
            self._cooldown_counter = weapon.fire_rate
            self.ammo_in_mag = max(0, self.ammo_in_mag - weapon.get_ammo_cost())
            return True
        return False
    
    def switch_weapon(self, direction: int = 1) -> None:
        """Switch to next/previous weapon."""
        if self.weapon_switch_cooldown > 0:
            return
        if len(self.weapons) <= 1:
            return
        
        self.current_weapon_index = (self.current_weapon_index + direction) % len(self.weapons)
        self.weapon_switch_cooldown = 10  # Prevent rapid switching
    
    def add_weapon(self, weapon) -> None:
        """Add a weapon to inventory."""
        # Don't add duplicates
        for w in self.weapons:
            if w.name == weapon.name:
                return
        self.weapons.append(weapon)
    
    def get_current_weapon(self):
        """Get the currently equipped weapon."""
        if not self.weapons or self.current_weapon_index >= len(self.weapons):
            return None
        return self.weapons[self.current_weapon_index]

    def reload(self) -> None:
        if self.ammo_in_mag >= self.mag_capacity:
            return
        to_fill = self.mag_capacity - self.ammo_in_mag
        taken = min(to_fill, self.reserve_ammo)
        if taken <= 0:
            return
        self.ammo_in_mag += taken
        self.reserve_ammo -= taken


