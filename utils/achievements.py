"""Achievement system."""
from __future__ import annotations

from typing import Dict, List, Callable
from utils.save_system import get_save_data


class Achievement:
    """Represents an achievement."""
    
    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        check_func: Callable[[], bool] | None = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.check_func = check_func
    
    def check(self) -> bool:
        """Check if achievement should be unlocked."""
        if self.check_func:
            return self.check_func()
        return False


class AchievementSystem:
    """Manages achievements."""
    
    def __init__(self):
        self.achievements: Dict[str, Achievement] = {}
        self._initialize_achievements()
    
    def _initialize_achievements(self) -> None:
        """Initialize all achievements."""
        # Level completion achievements
        self.achievements["complete_level1"] = Achievement(
            "complete_level1",
            "First Steps",
            "Complete Level 1"
        )
        self.achievements["complete_level2"] = Achievement(
            "complete_level2",
            "Getting Better",
            "Complete Level 2"
        )
        self.achievements["complete_level3"] = Achievement(
            "complete_level3",
            "Platform Master",
            "Complete Level 3"
        )
        self.achievements["complete_level4"] = Achievement(
            "complete_level4",
            "Boss Slayer",
            "Defeat the Boss"
        )
        self.achievements["complete_all_levels"] = Achievement(
            "complete_all_levels",
            "Champion",
            "Complete all levels"
        )
        
        # Combat achievements
        self.achievements["kill_10_enemies"] = Achievement(
            "kill_10_enemies",
            "Enemy Hunter",
            "Kill 10 enemies"
        )
        self.achievements["kill_50_enemies"] = Achievement(
            "kill_50_enemies",
            "Massacre",
            "Kill 50 enemies"
        )
        self.achievements["no_damage_level"] = Achievement(
            "no_damage_level",
            "Perfect Run",
            "Complete a level without taking damage"
        )
        self.achievements["boss_no_damage"] = Achievement(
            "boss_no_damage",
            "Untouchable",
            "Defeat boss without taking damage"
        )
        
        # Collection achievements
        self.achievements["collect_10_coins"] = Achievement(
            "collect_10_coins",
            "Coin Collector",
            "Collect 10 coins"
        )
        self.achievements["collect_100_coins"] = Achievement(
            "collect_100_coins",
            "Rich Miner",
            "Collect 100 coins"
        )
        self.achievements["collect_all_coins"] = Achievement(
            "collect_all_coins",
            "Treasure Hunter",
            "Collect all coins in a level"
        )
        
        # Score achievements
        self.achievements["score_1000"] = Achievement(
            "score_1000",
            "High Scorer",
            "Score 1000 points"
        )
        self.achievements["score_5000"] = Achievement(
            "score_5000",
            "Score Master",
            "Score 5000 points"
        )
        self.achievements["score_10000"] = Achievement(
            "score_10000",
            "Legendary Score",
            "Score 10000 points"
        )
        
        # Weapon achievements
        self.achievements["use_all_weapons"] = Achievement(
            "use_all_weapons",
            "Weapon Master",
            "Use all weapon types"
        )
        
        # Speed achievements
        self.achievements["fast_completion"] = Achievement(
            "fast_completion",
            "Speed Runner",
            "Complete a level quickly"
        )
        
        # Secret achievements
        self.achievements["find_secret"] = Achievement(
            "find_secret",
            "Secret Finder",
            "Discover a secret area"
        )
        self.achievements["find_bonus_room"] = Achievement(
            "find_bonus_room",
            "Explorer",
            "Enter a bonus room"
        )
        self.achievements["find_all_secrets"] = Achievement(
            "find_all_secrets",
            "Master Explorer",
            "Find all secrets in the game"
        )
    
    def check_achievements(
        self,
        level_name: str | None = None,
        enemies_killed: int = 0,
        coins_collected: int = 0,
        score: int = 0,
        damage_taken: int = 0,
        weapons_used: List[str] | None = None,
        secret_found: bool = False,
        bonus_room_found: bool = False
    ) -> List[str]:
        """Check and unlock achievements. Returns list of newly unlocked achievement IDs."""
        save_data = get_save_data()
        newly_unlocked = []
        
        # Secret checks
        if secret_found:
            if save_data.unlock_achievement("find_secret"):
                newly_unlocked.append("find_secret")
        
        if bonus_room_found:
            if save_data.unlock_achievement("find_bonus_room"):
                newly_unlocked.append("find_bonus_room")
        
        # Level completion checks
        if level_name:
            level_id = level_name.replace("levels/", "").replace(".csv", "")
            achievement_id = f"complete_{level_id}"
            if achievement_id in self.achievements:
                if save_data.unlock_achievement(achievement_id):
                    newly_unlocked.append(achievement_id)
            
            # Check if all levels completed
            if save_data.is_level_completed("level1") and \
               save_data.is_level_completed("level2") and \
               save_data.is_level_completed("level3") and \
               save_data.is_level_completed("level4"):
                if save_data.unlock_achievement("complete_all_levels"):
                    newly_unlocked.append("complete_all_levels")
        
        # Combat checks
        if enemies_killed >= 10:
            if save_data.unlock_achievement("kill_10_enemies"):
                newly_unlocked.append("kill_10_enemies")
        if enemies_killed >= 50:
            if save_data.unlock_achievement("kill_50_enemies"):
                newly_unlocked.append("kill_50_enemies")
        
        if level_name and damage_taken == 0:
            if save_data.unlock_achievement("no_damage_level"):
                newly_unlocked.append("no_damage_level")
        
        if level_name and "level4" in level_name and damage_taken == 0:
            if save_data.unlock_achievement("boss_no_damage"):
                newly_unlocked.append("boss_no_damage")
        
        # Collection checks
        total_coins = save_data.get_coins()
        if total_coins >= 10:
            if save_data.unlock_achievement("collect_10_coins"):
                newly_unlocked.append("collect_10_coins")
        if total_coins >= 100:
            if save_data.unlock_achievement("collect_100_coins"):
                newly_unlocked.append("collect_100_coins")
        
        # Score checks
        if score >= 1000:
            if save_data.unlock_achievement("score_1000"):
                newly_unlocked.append("score_1000")
        if score >= 5000:
            if save_data.unlock_achievement("score_5000"):
                newly_unlocked.append("score_5000")
        if score >= 10000:
            if save_data.unlock_achievement("score_10000"):
                newly_unlocked.append("score_10000")
        
        # Weapon checks
        if weapons_used and len(set(weapons_used)) >= 4:
            if save_data.unlock_achievement("use_all_weapons"):
                newly_unlocked.append("use_all_weapons")
        
        return newly_unlocked
    
    def get_achievement(self, achievement_id: str) -> Achievement | None:
        """Get an achievement by ID."""
        return self.achievements.get(achievement_id)
    
    def get_all_achievements(self) -> List[Achievement]:
        """Get all achievements."""
        return list(self.achievements.values())
    
    def get_unlocked_achievements(self) -> List[str]:
        """Get list of unlocked achievement IDs."""
        save_data = get_save_data()
        return save_data.data.get("achievements", [])


# Global achievement system instance
_achievement_system: AchievementSystem | None = None


def get_achievement_system() -> AchievementSystem:
    """Get or create the global achievement system."""
    global _achievement_system
    if _achievement_system is None:
        _achievement_system = AchievementSystem()
    return _achievement_system

