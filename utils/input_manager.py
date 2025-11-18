"""Input management system with customizable controls."""
from __future__ import annotations

from typing import Dict, Callable
import pygame


class InputManager:
    """Manages input with customizable key bindings."""
    
    def __init__(self):
        self.key_bindings: Dict[str, int] = {
            "move_left": pygame.K_a,
            "move_right": pygame.K_d,
            "jump": pygame.K_SPACE,
            "shoot": pygame.K_f,
            "reload": pygame.K_r,
            "weapon_next": pygame.K_q,
            "weapon_prev": pygame.K_e,
            "pause": pygame.K_ESCAPE,
        }
        self.controller_enabled = False
        self.controller = None
        self._init_controller()
    
    def _init_controller(self) -> None:
        """Initialize controller if available."""
        try:
            if pygame.joystick.get_count() > 0:
                self.controller = pygame.joystick.Joystick(0)
                self.controller.init()
                self.controller_enabled = True
        except Exception:
            self.controller_enabled = False
    
    def is_pressed(self, action: str, keys: pygame.key.ScancodeWrapper | None = None) -> bool:
        """Check if an action is pressed."""
        if action not in self.key_bindings:
            return False
        
        key = self.key_bindings[action]
        
        # Check keyboard
        if keys is not None:
            if keys[key]:
                return True
        
        # Check controller
        if self.controller_enabled and self.controller:
            if action == "move_left":
                return self.controller.get_axis(0) < -0.5
            elif action == "move_right":
                return self.controller.get_axis(0) > 0.5
            elif action == "jump":
                return self.controller.get_button(0)  # A button
            elif action == "shoot":
                return self.controller.get_button(1)  # B button
        
        return False
    
    def get_move_direction(self, keys: pygame.key.ScancodeWrapper | None = None) -> int:
        """Get horizontal movement direction (-1 left, 0 none, 1 right)."""
        move_dir = 0
        if self.is_pressed("move_left", keys):
            move_dir -= 1
        if self.is_pressed("move_right", keys):
            move_dir += 1
        
        # Controller support
        if self.controller_enabled and self.controller:
            axis = self.controller.get_axis(0)
            if axis < -0.5:
                move_dir -= 1
            elif axis > 0.5:
                move_dir += 1
        
        return move_dir
    
    def set_binding(self, action: str, key: int) -> None:
        """Set a key binding."""
        self.key_bindings[action] = key
    
    def get_binding(self, action: str) -> int:
        """Get key binding for an action."""
        return self.key_bindings.get(action, 0)


# Global input manager
_input_manager: InputManager | None = None


def get_input_manager() -> InputManager:
    """Get or create the global input manager."""
    global _input_manager
    if _input_manager is None:
        _input_manager = InputManager()
    return _input_manager

