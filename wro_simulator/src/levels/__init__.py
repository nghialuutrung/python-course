"""
Level definitions for WRO Robot Control System

To add a new level:
1. Create a new file: level_XX.py (where XX is the level number with leading zero)
2. Create a class named LevelXX that inherits from BaseLevel
3. Implement the setup_level() method
4. The level will be automatically loaded by the LevelManager

Example:
    # level_04.py
    from ..core.level import BaseLevel
    
    class Level04(BaseLevel):
        def setup_level(self):
            self.level_id = 4
            self.name = "My New Level"
            self.description = "Description of the level"
            self.difficulty = 2
            
            # Add objectives, obstacles, items, etc.
            self.add_objective('reach_target', 'Reach (10, 10)', target=(10, 10))
            self.add_obstacle(100, 100, 50, 50)
            self.add_item(200, 200, 'coin')
"""
