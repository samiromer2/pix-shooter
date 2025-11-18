"""Difficulty system for adjusting game parameters."""
from __future__ import annotations

from typing import Dict, Any


class DifficultySettings:
    """Difficulty settings that modify game parameters."""
    
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    
    def __init__(self, difficulty: str = "normal"):
        self.difficulty = difficulty
        self._apply_settings()
    
    def _apply_settings(self) -> None:
        """Apply difficulty settings."""
        if self.difficulty == self.EASY:
            self.enemy_hp_multiplier = 0.7  # Enemies have less HP
            self.enemy_damage_multiplier = 0.7  # Enemies do less damage
            self.enemy_speed_multiplier = 0.8  # Enemies slower
            self.player_hp_bonus = 2  # Player starts with more HP
            self.ammo_bonus = 20  # More starting ammo
            self.score_multiplier = 0.8  # Lower scores
        elif self.difficulty == self.HARD:
            self.enemy_hp_multiplier = 1.5  # Enemies have more HP
            self.enemy_damage_multiplier = 1.5  # Enemies do more damage
            self.enemy_speed_multiplier = 1.3  # Enemies faster
            self.player_hp_bonus = -1  # Player starts with less HP
            self.ammo_bonus = -10  # Less starting ammo
            self.score_multiplier = 1.5  # Higher scores
        else:  # NORMAL
            self.enemy_hp_multiplier = 1.0
            self.enemy_damage_multiplier = 1.0
            self.enemy_speed_multiplier = 1.0
            self.player_hp_bonus = 0
            self.ammo_bonus = 0
            self.score_multiplier = 1.0
    
    def apply_to_enemy(self, enemy) -> None:
        """Apply difficulty to an enemy."""
        enemy.max_hp = max(1, int(enemy.max_hp * self.enemy_hp_multiplier))
        enemy.hp = enemy.max_hp
        
        # Check if enemy is a Boss (Boss uses 'speed' instead of 'chase_speed'/'patrol_speed')
        from entities.boss import Boss
        if isinstance(enemy, Boss):
            # Boss uses 'speed' attribute
            if hasattr(enemy, 'speed'):
                enemy.speed *= self.enemy_speed_multiplier
        else:
            # Regular enemies use 'chase_speed' and 'patrol_speed'
            if hasattr(enemy, 'chase_speed'):
                enemy.chase_speed *= self.enemy_speed_multiplier
            if hasattr(enemy, 'patrol_speed'):
                enemy.patrol_speed *= self.enemy_speed_multiplier
    
    def apply_to_player(self, player) -> None:
        """Apply difficulty to player."""
        player.max_hp = max(1, player.max_hp + self.player_hp_bonus)
        player.hp = player.max_hp
        player.reserve_ammo = max(0, player.reserve_ammo + self.ammo_bonus)
    
    def get_score_multiplier(self) -> float:
        """Get score multiplier for this difficulty."""
        return self.score_multiplier
    
    def set_difficulty(self, difficulty: str) -> None:
        """Set difficulty level."""
        if difficulty in [self.EASY, self.NORMAL, self.HARD]:
            self.difficulty = difficulty
            self._apply_settings()

