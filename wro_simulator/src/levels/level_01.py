"""
Level 1: First Steps
Basic robot movement commands
"""

from ..core.level import BaseLevel


class Level01(BaseLevel):
    """Level 1: Learn basic robot movement commands"""
    
    def setup_level(self):
        """Setup Level 1 content"""
        # Basic level info
        self.level_id = 1
        self.name = "First Steps"
        self.description = "Learn basic robot movement commands"
        self.difficulty = 1
        
        # Objectives
        self.add_objective(
            'reach_target',
            'Reach the target position (5, 5)',
            target=(5, 5),
            tolerance=1.0
        )
        
        # No obstacles for first level
        self.obstacles = []
        
        # No items for first level
        self.items = []
        
        # Target area (visual indicator) - offset by sidebar
        from ..core.constants import SIDEBAR_WIDTH
        # Target at grid (5, 5) = pixel (450, 250)
        self.set_target_area(SIDEBAR_WIDTH + 200, 200, 100, 100)
        
        # Hints for beginners
        self.add_hint("Use robot.forward() to move forward")
        self.add_hint("Use robot.right() to turn right")
        self.add_hint("Try: robot.forward(5); robot.right(); robot.forward(5)")
        self.add_hint("Check your position with robot.sensor()")
        
        # No time limit for first level
        self.time_limit = None
        
        # All commands allowed
        self.allowed_commands = None
