"""
Level 3: Treasure Hunt
Collect items while navigating
"""

from ..core.level import BaseLevel


class Level03(BaseLevel):
    """Level 3: Collect items while navigating"""
    
    def setup_level(self):
        """Setup Level 3 content"""
        # Basic level info
        self.level_id = 3
        self.name = "Treasure Hunt"
        self.description = "Collect items while navigating"
        self.difficulty = 2
        
        # Multiple objectives
        self.add_objective(
            'collect_items',
            'Collect at least 2 items',
            count=2
        )
        
        self.add_objective(
            'reach_target',
            'Reach the final target position (10, 8)',
            target=(10, 8),
            tolerance=1.0
        )
        
        # Add obstacle (offset by sidebar)
        from ..core.constants import SIDEBAR_WIDTH
        self.add_obstacle(SIDEBAR_WIDTH + 100, 200, 50, 100)

        # Add collectible items (offset by sidebar)
        self.add_item(SIDEBAR_WIDTH + 150, 100, 'coin')
        self.add_item(SIDEBAR_WIDTH + 300, 300, 'coin')
        self.add_item(SIDEBAR_WIDTH + 450, 150, 'coin')  # Extra item for bonus

        # Target area (offset by sidebar)
        self.set_target_area(SIDEBAR_WIDTH + 450, 350, 100, 100)
        
        # Hints for item collection
        self.add_hint("Use robot.collect() when near items")
        self.add_hint("Items glow when you're close enough")
        self.add_hint("Collect all items before reaching target")
        self.add_hint("Plan an efficient route to collect items")
        
        # No time limit
        self.time_limit = None
        
        # All commands allowed
        self.allowed_commands = None
