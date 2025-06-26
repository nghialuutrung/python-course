"""
Level 2: Turn Around
Master turning and basic navigation
"""

from ..core.level import BaseLevel


class Level02(BaseLevel):
    """Level 2: Master turning and basic navigation"""
    
    def setup_level(self):
        """Setup Level 2 content"""
        # Basic level info
        self.level_id = 2
        self.name = "Turn Around"
        self.description = "Master turning and basic navigation"
        self.difficulty = 1
        
        # Objectives
        self.add_objective(
            'reach_target',
            'Navigate around the obstacle to reach (8, 2)',
            target=(8, 2),
            tolerance=1.0
        )
        
        # Add obstacle to navigate around (offset by sidebar)
        from ..core.constants import SIDEBAR_WIDTH
        self.add_obstacle(SIDEBAR_WIDTH + 150, 150, 100, 50)

        # No items yet
        self.items = []

        # Target area (offset by sidebar)
        self.set_target_area(SIDEBAR_WIDTH + 350, 50, 100, 100)
        
        # Hints for navigation
        self.add_hint("You need to go around the obstacle")
        self.add_hint("Use robot.left() and robot.right() to turn")
        self.add_hint("Plan your path before coding")
        self.add_hint("Try going up first, then right, then down")
        
        # No time limit
        self.time_limit = None
        
        # All commands allowed
        self.allowed_commands = None
