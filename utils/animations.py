"""Animation system for sprite frame cycling."""
from __future__ import annotations

from pathlib import Path
import pygame


def load_image(path: str | Path) -> pygame.Surface | None:
    """Load an image file, return None if not found."""
    path_str = str(path)
    
    # Try PIL/Pillow first (more reliable for PNG)
    try:
        from PIL import Image
        pil_img = Image.open(path_str)
        if pil_img.mode != 'RGBA':
            pil_img = pil_img.convert('RGBA')
        # Convert to pygame Surface
        mode = pil_img.mode
        size = pil_img.size
        data = pil_img.tobytes()
        # Use frombuffer for newer pygame, fallback to fromstring
        try:
            img = pygame.image.frombuffer(data, size, mode)
        except AttributeError:
            img = pygame.image.fromstring(data, size, mode)
        return img
    except ImportError:
        # PIL not available, fall through to pygame
        pass
    except Exception:
        # PIL failed, try pygame
        pass
    
    # Fallback to pygame
    try:
        img = pygame.image.load(path_str)
        if img.get_flags() & pygame.SRCALPHA:
            return img.convert_alpha()
        return img.convert()
    except Exception:
        return None


class Animation:
    """Manages a sequence of sprite frames."""
    
    def __init__(self, frames: list[pygame.Surface], fps: float = 8.0) -> None:
        self.frames = frames
        self.fps = fps
        self.frame_time = 1.0 / fps if fps > 0 else 0
        self.current_frame = 0
        self.elapsed = 0.0
    
    def update(self, dt: float) -> None:
        """Update animation frame based on delta time."""
        if len(self.frames) <= 1:
            return
        if self.fps <= 0:  # fps=0 means static, don't animate
            return
        self.elapsed += dt
        if self.elapsed >= self.frame_time:
            self.elapsed = 0.0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def get_frame(self) -> pygame.Surface:
        """Get current animation frame."""
        return self.frames[self.current_frame] if self.frames else None
    
    def reset(self) -> None:
        """Reset animation to first frame."""
        self.current_frame = 0
        self.elapsed = 0.0


def split_sprite_sheet(image: pygame.Surface, frame_width: int, frame_height: int) -> list[pygame.Surface]:
    """Split a sprite sheet into individual frames."""
    frames = []
    img_w, img_h = image.get_size()
    cols = img_w // frame_width
    rows = img_h // frame_height
    
    for row in range(rows):
        for col in range(cols):
            x = col * frame_width
            y = row * frame_height
            frame = image.subsurface((x, y, frame_width, frame_height))
            frames.append(frame)
    
    return frames


def load_animation_sequence(base_path: Path, pattern: str, frame_count: int | None = None) -> list[pygame.Surface]:
    """Load animation frames from numbered files or sprite sheet.
    
    Tries:
    1. Numbered files: pattern1.png, pattern2.png, ...
    2. Single sprite sheet: pattern.png (tries to auto-detect frame count from filename)
    3. Single image as one frame
    4. Case-insensitive search
    """
    frames = []
    
    # Try numbered files first
    if frame_count:
        for i in range(1, frame_count + 1):
            path = base_path / f"{pattern}{i}.png"
            if not path.exists():
                path = base_path / f"{pattern}_{i}.png"
            if path.exists():
                img = load_image(path)
                if img:
                    frames.append(img)
    
    # If no numbered files, try single file (might be sprite sheet)
    if not frames:
        # Try exact match first
        single_path = base_path / f"{pattern}.png"
        if not single_path.exists():
            # Try case variations
            single_path_lower = base_path / f"{pattern.lower()}.png"
            single_path_upper = base_path / f"{pattern[0].upper() + pattern[1:]}.png"
            if single_path_lower.exists():
                single_path = single_path_lower
            elif single_path_upper.exists():
                single_path = single_path_upper
            else:
                # Try finding any file that starts with pattern (case-insensitive)
                pattern_lower = pattern.lower()
                for file in base_path.glob("*.png"):
                    file_stem_lower = file.stem.lower()
                    if file_stem_lower.startswith(pattern_lower) or pattern_lower in file_stem_lower:
                        single_path = file
                        break
                else:
                    single_path = None  # No file found
        
        if single_path and single_path.exists():
            try:
                img = load_image(single_path)
                if not img:
                    frames = []
                    return frames
                w, h = img.get_size()
                
                # Check filename for frame count hint (e.g., "Walk_6.png" or "Idle_4.png")
                frame_count_hint = None
                # Try from pattern first
                if "_" in pattern:
                    parts = pattern.split("_")
                    if parts[-1].isdigit():
                        frame_count_hint = int(parts[-1])
                # Also try from actual filename
                if not frame_count_hint and single_path:
                    filename_parts = single_path.stem.split("_")
                    if filename_parts[-1].isdigit():
                        frame_count_hint = int(filename_parts[-1])
                
                # If we have a hint, split sprite sheet horizontally
                if frame_count_hint and frame_count_hint > 1:
                    frame_w = w // frame_count_hint
                    if frame_w > 0 and frame_w <= w:
                        frames = split_sprite_sheet(img, frame_w, h)
                
                # If splitting failed or no hint, try common frame widths
                if not frames:
                    # Try common frame widths (16, 32, 48, 64)
                    for test_w in [32, 48, 64, 16]:
                        if w % test_w == 0:
                            frame_count = w // test_w
                            if frame_count > 1:
                                frames = split_sprite_sheet(img, test_w, h)
                                break
                
                # Last resort: single frame
                if not frames:
                    frames = [img]
            except Exception as e:
                # Silently fail - will use fallback
                import sys
                print(f"Warning: Could not load animation {pattern}: {e}", file=sys.stderr)
                frames = []
    
    return frames


class AnimationController:
    """Controls animations for an entity."""
    
    def __init__(self, animations: dict[str, Animation]) -> None:
        self.animations = animations
        self.current_anim = "idle"
        self.dt_accumulator = 0.0
    
    def set_animation(self, name: str) -> None:
        """Switch to a different animation."""
        if name in self.animations and name != self.current_anim:
            self.current_anim = name
            self.animations[name].reset()
    
    def update(self, dt: float) -> None:
        """Update current animation."""
        if self.current_anim in self.animations:
            self.animations[self.current_anim].update(dt)
    
    def get_frame(self) -> pygame.Surface | None:
        """Get current frame from current animation."""
        if self.current_anim in self.animations:
            return self.animations[self.current_anim].get_frame()
        return None

