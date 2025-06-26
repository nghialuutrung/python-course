"""
Level Manager for WRO Robot Control System
"""

import importlib
import os
from typing import Dict, List, Optional
from .level import BaseLevel


class LevelManager:
    """Manages game levels and progression"""
    
    def __init__(self):
        self.levels: Dict[int, BaseLevel] = {}
        self.unlocked_levels: List[int] = []  # Will be populated after loading
        self.load_levels()
        # Unlock all loaded levels for free exploration
        self.unlocked_levels = list(self.levels.keys())
    
    def load_levels(self):
        """Dynamically load all levels from the levels directory"""
        levels_dir = os.path.join(os.path.dirname(__file__), '..', 'levels')
        
        if not os.path.exists(levels_dir):
            print("Warning: Levels directory not found")
            return
        
        # Get all Python files in levels directory
        level_files = [f for f in os.listdir(levels_dir) 
                      if f.startswith('level_') and f.endswith('.py')]
        
        for level_file in sorted(level_files):
            try:
                # Extract level number from filename (e.g., level_01.py -> 1)
                level_num = int(level_file.split('_')[1].split('.')[0])
                
                # Import the level module
                module_name = f"src.levels.{level_file[:-3]}"
                module = importlib.import_module(module_name)
                
                # Get the level class (should be named like Level01, Level02, etc.)
                level_class_name = f"Level{level_num:02d}"
                if hasattr(module, level_class_name):
                    level_class = getattr(module, level_class_name)
                    level_instance = level_class()
                    self.levels[level_num] = level_instance
                    print(f"Loaded Level {level_num}: {level_instance.name}")
                else:
                    print(f"Warning: Level class {level_class_name} not found in {level_file}")
                    
            except Exception as e:
                print(f"Error loading level {level_file}: {e}")
    
    def get_level(self, level_id: int) -> Optional[BaseLevel]:
        """Get level by ID"""
        return self.levels.get(level_id)
    
    def is_level_unlocked(self, level_id: int) -> bool:
        """Check if level is unlocked"""
        return level_id in self.unlocked_levels
    
    def unlock_level(self, level_id: int):
        """Unlock a level"""
        if level_id not in self.unlocked_levels and level_id in self.levels:
            self.unlocked_levels.append(level_id)
            print(f"🔓 Level {level_id} unlocked!")
    
    def complete_level(self, level_id: int, score: int, time_taken: float):
        """Mark level as completed and unlock next level"""
        level = self.get_level(level_id)
        if not level:
            return
        
        level.completed = True
        level.best_score = max(level.best_score, score)
        if level.best_time is None or time_taken < level.best_time:
            level.best_time = time_taken
        
        # Unlock next level
        next_level = level_id + 1
        if next_level in self.levels:
            self.unlock_level(next_level)
    
    def get_progress(self) -> Dict:
        """Get overall progress statistics"""
        total_levels = len(self.levels)
        completed_levels = sum(1 for level in self.levels.values() if level.completed)
        unlocked_levels = len(self.unlocked_levels)
        
        return {
            'total_levels': total_levels,
            'completed_levels': completed_levels,
            'unlocked_levels': unlocked_levels,
            'completion_percentage': (completed_levels / total_levels * 100) if total_levels > 0 else 0
        }
    
    def get_available_levels(self) -> List[int]:
        """Get list of available (unlocked) level IDs"""
        return sorted([level_id for level_id in self.levels.keys() 
                      if self.is_level_unlocked(level_id)])
    
    def reset_progress(self):
        """Reset all progress (for testing/debugging)"""
        self.unlocked_levels = [1]
        for level in self.levels.values():
            level.completed = False
            level.best_score = 0
            level.best_time = None
            level.reset()
    
    def get_next_level(self, current_level_id: int) -> Optional[int]:
        """Get the next available level ID"""
        available_levels = self.get_available_levels()
        try:
            current_index = available_levels.index(current_level_id)
            if current_index + 1 < len(available_levels):
                return available_levels[current_index + 1]
        except ValueError:
            pass
        return None
    
    def get_level_summary(self) -> str:
        """Get a summary of all levels for debugging"""
        summary = "=== LEVEL SUMMARY ===\n"
        for level_id in sorted(self.levels.keys()):
            level = self.levels[level_id]
            status = "✅" if level.completed else ("🔓" if self.is_level_unlocked(level_id) else "🔒")
            summary += f"{status} Level {level_id}: {level.name} (Difficulty: {'⭐' * level.difficulty})\n"
        return summary
