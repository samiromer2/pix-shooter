"""Save and load system for game progress."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any


SAVE_FILE = Path("save_game.json")


class SaveData:
    """Manages game save data."""
    
    def __init__(self):
        self.data: Dict[str, Any] = {
            "player": {
                "max_hp": 5,
                "hp_upgrades": 0,
                "ammo_upgrades": 0,
                "speed_multiplier": 1.0,
                "jump_multiplier": 1.0,
            },
            "progress": {
                "levels_completed": [],
                "current_level": "level1",
            },
            "currency": {
                "coins": 0,
            },
            "scores": {
                "high_scores": {},  # level_name -> score
                "global_high_score": 0,
            },
            "achievements": [],
            "settings": {
                "difficulty": "normal",  # easy, normal, hard
                "master_volume": 1.0,
                "sfx_volume": 1.0,
                "music_volume": 1.0,
            },
        }
    
    def save(self) -> bool:
        """Save game data to file."""
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(self.data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load(self) -> bool:
        """Load game data from file."""
        if not SAVE_FILE.exists():
            return False
        try:
            with open(SAVE_FILE, 'r') as f:
                self.data = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
    
    def reset(self) -> None:
        """Reset save data to defaults."""
        self.__init__()
        self.save()
    
    def get_player_data(self) -> Dict[str, Any]:
        """Get player save data."""
        return self.data.get("player", {})
    
    def set_player_data(self, player_data: Dict[str, Any]) -> None:
        """Set player save data."""
        self.data["player"] = player_data
    
    def complete_level(self, level_name: str) -> None:
        """Mark a level as completed."""
        completed = self.data["progress"]["levels_completed"]
        if level_name not in completed:
            completed.append(level_name)
        self.save()
    
    def is_level_completed(self, level_name: str) -> bool:
        """Check if a level is completed."""
        return level_name in self.data["progress"]["levels_completed"]
    
    def add_coins(self, amount: int) -> None:
        """Add coins to save data."""
        self.data["currency"]["coins"] = self.data["currency"].get("coins", 0) + amount
        self.save()
    
    def get_coins(self) -> int:
        """Get current coin count."""
        return self.data["currency"].get("coins", 0)
    
    def set_coins(self, amount: int) -> None:
        """Set coin count."""
        self.data["currency"]["coins"] = amount
        self.save()
    
    def set_high_score(self, level_name: str, score: int) -> bool:
        """Set high score for a level. Returns True if new record."""
        high_scores = self.data["scores"]["high_scores"]
        current_best = high_scores.get(level_name, 0)
        if score > current_best:
            high_scores[level_name] = score
            if score > self.data["scores"]["global_high_score"]:
                self.data["scores"]["global_high_score"] = score
            self.save()
            return True
        return False
    
    def get_high_score(self, level_name: str) -> int:
        """Get high score for a level."""
        return self.data["scores"]["high_scores"].get(level_name, 0)
    
    def get_global_high_score(self) -> int:
        """Get global high score."""
        return self.data["scores"].get("global_high_score", 0)
    
    def unlock_achievement(self, achievement_id: str) -> bool:
        """Unlock an achievement. Returns True if newly unlocked."""
        achievements = self.data["achievements"]
        if achievement_id not in achievements:
            achievements.append(achievement_id)
            self.save()
            return True
        return False
    
    def has_achievement(self, achievement_id: str) -> bool:
        """Check if achievement is unlocked."""
        return achievement_id in self.data["achievements"]
    
    def get_difficulty(self) -> str:
        """Get current difficulty setting."""
        return self.data["settings"].get("difficulty", "normal")
    
    def set_difficulty(self, difficulty: str) -> None:
        """Set difficulty setting."""
        if difficulty in ["easy", "normal", "hard"]:
            self.data["settings"]["difficulty"] = difficulty
            self.save()


# Global save data instance
_save_data: SaveData | None = None


def get_save_data() -> SaveData:
    """Get or create the global save data instance."""
    global _save_data
    if _save_data is None:
        _save_data = SaveData()
        _save_data.load()
    return _save_data

