"""Sprite loading utilities for game assets."""
from __future__ import annotations

from pathlib import Path

import pygame
from utils.animations import load_animation_sequence, Animation, AnimationController, load_image as load_image_from_anim


class SpriteLoader:
    """Loads and manages sprite assets with animation support."""
    
    def __init__(self) -> None:
        self.base_path = Path("assets/sprites")
        self.player_animations: dict[str, Animation] = {}
        self.enemy_animations: dict[str, Animation] = {}
        self.enemy_types: list[dict[str, Animation]] = []  # Multiple enemy types
        self.bullet_sprites: list[pygame.Surface] = []
        self._load_all()
    
    def _load_all(self) -> None:
        """Load all sprite assets with animations."""
        # Player animations
        player_path = self.base_path / "player"
        if player_path.exists():
            # Load animations with frame detection from filename
            idle_frames = load_animation_sequence(player_path, "Owlet_Monster_Idle_4")
            walk_frames = load_animation_sequence(player_path, "Owlet_Monster_Walk_6")
            run_frames = load_animation_sequence(player_path, "Owlet_Monster_Run_6")
            jump_frames = load_animation_sequence(player_path, "Owlet_Monster_Jump_8")
            attack_frames = load_animation_sequence(player_path, "Owlet_Monster_Attack1_4")
            
            if idle_frames:
                self.player_animations["idle"] = Animation(idle_frames, fps=6.0)
            if walk_frames:
                self.player_animations["walk"] = Animation(walk_frames, fps=8.0)
            if run_frames:
                self.player_animations["run"] = Animation(run_frames, fps=10.0)
            if jump_frames:
                self.player_animations["jump"] = Animation(jump_frames, fps=8.0)
            if attack_frames:
                self.player_animations["attack"] = Animation(attack_frames, fps=12.0)
            
            # Fallback single frame
            if not self.player_animations:
                fallback = load_image_from_anim(player_path / "Owlet_Monster.png")
                if fallback:
                    self.player_animations["idle"] = Animation([fallback], fps=1.0)
        
        # Enemy animations - new farm animal sprites
        enemy_path = self.base_path / "enemy"
        if enemy_path.exists():
            # Look for farm animal animation spritesheets
            # Check common locations: PNG/With_shadow/, PNG/Without_shadow/, Tiled/
            possible_locations = [
                enemy_path / "craftpix-net-291971-free-top-down-animals-farm-pixel-art-sprites" / "PNG" / "With_shadow",
                enemy_path / "craftpix-net-291971-free-top-down-animals-farm-pixel-art-sprites" / "PNG" / "Without_shadow",
                enemy_path / "craftpix-net-291971-free-top-down-animals-farm-pixel-art-sprites" / "Tiled",
                enemy_path,  # Direct in enemy folder
            ]
            
            # Available enemy types (farm animals)
            enemy_types = ["Bull", "Calf", "Chick", "Lamb", "Piglet", "Rooster", "Sheep", "Turkey"]
            
            # Load all available enemy types
            for loc in possible_locations:
                if not loc.exists():
                    continue
                
                # Try to find enemy animation files for each type
                for enemy_type in enemy_types:
                    # Try with shadow first (looks better)
                    anim_file = loc / f"{enemy_type}_animation_with_shadow.png"
                    if not anim_file.exists():
                        anim_file = loc / f"{enemy_type}_animation_without_shadow.png"
                    if not anim_file.exists():
                        anim_file = loc / f"{enemy_type}_animation.png"
                    
                    if anim_file.exists():
                        img = load_image_from_anim(anim_file)
                        if img:
                            w, h = img.get_size()
                            # Try to detect frame size - common sizes: 128x128, 96x96, 64x64
                            frame_size = None
                            for size in [128, 96, 64, 48, 32]:
                                if w % size == 0 and h % size == 0:
                                    cols = w // size
                                    rows = h // size
                                    # Likely animation: should have multiple columns (directions) and rows (frames)
                                    if cols >= 3 and rows >= 2:
                                        frame_size = size
                                        break
                            
                            idle_frames = []
                            walk_frames = []
                            
                            if frame_size:
                                from utils.animations import split_sprite_sheet
                                all_frames = split_sprite_sheet(img, frame_size, frame_size)
                                # Animation spritesheets typically have 4 directions (front, back, left, right)
                                # and multiple frames per direction
                                # For simplicity, use all frames for walk, and first frame for idle
                                if len(all_frames) >= 8:
                                    # Use first 4 frames for idle (first direction, all frames)
                                    idle_frames = all_frames[:4] if len(all_frames) >= 4 else [all_frames[0]]
                                    # Use remaining frames for walk, or cycle all if not enough
                                    if len(all_frames) > 4:
                                        walk_frames = all_frames[4:8] if len(all_frames) >= 8 else all_frames[1:5]
                                    else:
                                        walk_frames = all_frames
                                elif len(all_frames) >= 4:
                                    # Split between idle and walk
                                    mid = len(all_frames) // 2
                                    idle_frames = all_frames[:mid]
                                    walk_frames = all_frames[mid:]
                                else:
                                    # Use all frames for both
                                    idle_frames = all_frames
                                    walk_frames = all_frames
                            else:
                                # Single frame or couldn't detect, use as is
                                idle_frames = [img]
                                walk_frames = [img]
                            
                            # Add this enemy type's animations
                            enemy_anims = {}
                            if idle_frames:
                                enemy_anims["idle"] = Animation(idle_frames, fps=4.0)
                            if walk_frames:
                                enemy_anims["walk"] = Animation(walk_frames, fps=6.0)
                            
                            if enemy_anims:
                                self.enemy_types.append(enemy_anims)
                                # Also use first loaded as default
                                if not self.enemy_animations:
                                    self.enemy_animations = enemy_anims.copy()
            
            # If we loaded multiple enemy types but no default, use first
            if not self.enemy_animations and self.enemy_types:
                self.enemy_animations = self.enemy_types[0].copy()
            
            # Fallback - try to load any PNG from enemy folder
            if not self.enemy_animations:
                for loc in possible_locations:
                    if loc.exists():
                        for png_file in loc.glob("*.png"):
                            # Skip shadow-only files and coupons
                            if "shadow" in png_file.name.lower() and "animation" not in png_file.name.lower():
                                continue
                            if "coupon" in png_file.name.lower() or "license" in png_file.name.lower():
                                continue
                            
                            img = load_image_from_anim(png_file)
                            if img:
                                w, h = img.get_size()
                                # Try to split if it looks like a spritesheet
                                if w > h * 2 or h > w * 2:  # Wide or tall sheet
                                    for size in [128, 96, 64]:
                                        if w % size == 0 and h % size == 0:
                                            from utils.animations import split_sprite_sheet
                                            frames = split_sprite_sheet(img, size, size)
                                            if len(frames) > 1:
                                                self.enemy_animations["idle"] = Animation([frames[0]], fps=1.0)
                                                self.enemy_animations["walk"] = Animation(frames[:4] if len(frames) >= 4 else frames, fps=6.0)
                                                break
                                else:
                                    # Single frame
                                    self.enemy_animations["idle"] = Animation([img], fps=1.0)
                                    self.enemy_animations["walk"] = Animation([img], fps=1.0)
                                break
                    if self.enemy_animations:
                        break
            
            # Final fallback - colored rectangle
            if not self.enemy_animations:
                fallback = pygame.Surface((32, 40))
                fallback.fill((180, 60, 60))
                self.enemy_animations["idle"] = Animation([fallback], fps=1.0)
                self.enemy_animations["walk"] = Animation([fallback], fps=1.0)
        
        # Bullet sprites (simple, no animation needed)
        bullet_path = self.base_path / "bullet"
        if bullet_path.exists():
            b1 = load_image_from_anim(bullet_path / "bullet1.png")
            b2 = load_image_from_anim(bullet_path / "bullet2.png")
            if b1:
                self.bullet_sprites.append(b1)
            if b2:
                self.bullet_sprites.append(b2)
    
    def get_player_animation_controller(self) -> AnimationController:
        """Get animation controller for player with cloned animations."""
        from utils.animations import Animation
        cloned = {}
        for name, anim in self.player_animations.items():
            # Create new Animation with same frames (surfaces are shared, state is separate)
            cloned[name] = Animation(anim.frames, fps=anim.fps)
        return AnimationController(cloned)
    
    def get_enemy_animation_controller(self, enemy_index: int | None = None) -> AnimationController:
        """Get animation controller for enemy with cloned animations.
        
        Args:
            enemy_index: Index of enemy type to use (None = random/default)
        """
        import random
        from utils.animations import Animation
        
        # Select enemy type
        if self.enemy_types:
            if enemy_index is None:
                # Randomly select an enemy type
                enemy_anims = random.choice(self.enemy_types)
            else:
                enemy_anims = self.enemy_types[enemy_index % len(self.enemy_types)]
        else:
            # Fallback to default
            enemy_anims = self.enemy_animations
        
        # Clone animations
        cloned = {}
        for name, anim in enemy_anims.items():
            # Create new Animation with same frames (surfaces are shared, state is separate)
            cloned[name] = Animation(anim.frames, fps=anim.fps)
        return AnimationController(cloned)
    
    def get_player_sprite(self, state: str = "idle") -> pygame.Surface | None:
        """Get player sprite for given state (backward compatibility)."""
        if state in self.player_animations:
            return self.player_animations[state].get_frame()
        return None
    
    def get_enemy_sprite(self, state: str = "idle") -> pygame.Surface | None:
        """Get enemy sprite for given state (backward compatibility)."""
        if state in self.enemy_animations:
            return self.enemy_animations[state].get_frame()
        return None
    
    def get_bullet_sprite(self, index: int = 0) -> pygame.Surface | None:
        """Get bullet sprite (cycles through available)."""
        if not self.bullet_sprites:
            return None
        return self.bullet_sprites[index % len(self.bullet_sprites)]


# Global sprite loader instance
_loader: SpriteLoader | None = None


def get_sprite_loader() -> SpriteLoader:
    """Get or create the global sprite loader.
    
    Note: Ensure pygame.init() has been called before first use.
    """
    global _loader
    if _loader is None:
        # Ensure pygame is initialized
        if not pygame.get_init():
            pygame.init()
        if not pygame.display.get_init():
            pygame.display.set_mode((1, 1))  # Dummy display for image loading
        _loader = SpriteLoader()
    return _loader

