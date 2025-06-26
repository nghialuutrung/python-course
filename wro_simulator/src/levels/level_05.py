"""
Level 5: Pathfinding Algorithms
Teaching basic pathfinding and route optimization
"""

from ..core.level import BaseLevel

class Level05(BaseLevel):
    def __init__(self):
        super().__init__()
        self.level_id = 5
        self.name = "Smart Pathfinding"
        self.description = "Learn pathfinding algorithms and route optimization"
        self.difficulty = 5
        
        # Objectives - Pathfinding and efficiency
        self.add_objective(
            'reach_target',
            'Find optimal path to target (8, 8)',
            target=(8, 8),
            tolerance=1.0
        )
        
        self.add_objective(
            'collect_items',
            'Collect all 3 items efficiently',
            count=3
        )
        
        self.add_objective(
            'optimize_path',
            'Complete mission in under 25 commands',
            max_commands=25
        )
        
        # Strategic obstacle placement for pathfinding challenge
        from ..core.constants import SIDEBAR_WIDTH
        
        # Create a maze that requires smart pathfinding
        self.add_obstacle(SIDEBAR_WIDTH + 100, 150, 200, 50)   # Horizontal barrier
        self.add_obstacle(SIDEBAR_WIDTH + 350, 100, 50, 200)   # Vertical barrier
        self.add_obstacle(SIDEBAR_WIDTH + 150, 300, 150, 50)   # Lower barrier
        self.add_obstacle(SIDEBAR_WIDTH + 450, 250, 100, 100)  # Corner block
        
        # Strategic item placement requiring route optimization
        self.add_item(SIDEBAR_WIDTH + 250, 120, 'coin')  # Item 1: Behind first barrier
        self.add_item(SIDEBAR_WIDTH + 120, 380, 'coin')  # Item 2: Lower area
        self.add_item(SIDEBAR_WIDTH + 480, 150, 'coin')  # Item 3: Far corner
        
        # Target area - requires efficient pathfinding
        self.set_target_area(SIDEBAR_WIDTH + 400, 400, 100, 100)
        
        # Advanced programming hints
        self.add_hint("Plan your route before moving - think like GPS!")
        self.add_hint("Use lists to store waypoints: path = [(3,2), (5,2), (8,8)]")
        self.add_hint("Create functions for distance calculation")
        self.add_hint("Sort items by distance for efficient collection")
        self.add_hint("Use while loops for navigation to each waypoint")
        
        # Programming examples for pathfinding
        self.programming_examples = [
            {
                "title": "Distance Calculation Function",
                "code": """
def distance_to(target_x, target_y):
    pos = robot.sensor()['position']
    dx = target_x - pos[0]
    dy = target_y - pos[1]
    return (dx*dx + dy*dy)**0.5

# Find closest item
items = [(5, 2), (2, 7), (9, 3)]
closest = min(items, key=lambda item: distance_to(item[0], item[1]))
print(f"Closest item at: {closest}")
"""
            },
            {
                "title": "Waypoint Navigation",
                "code": """
def navigate_to(target_x, target_y):
    while True:
        pos = robot.sensor()['position']
        
        # Check if reached target
        if abs(pos[0] - target_x) < 0.5 and abs(pos[1] - target_y) < 0.5:
            break
        
        # Simple pathfinding logic
        if pos[0] < target_x:
            robot.forward()  # Move right
        elif pos[1] < target_y:
            robot.right()
            robot.forward()  # Move down
        else:
            robot.left()
            robot.forward()  # Move up

# Navigate to multiple waypoints
waypoints = [(3, 2), (5, 5), (8, 8)]
for point in waypoints:
    navigate_to(point[0], point[1])
"""
            },
            {
                "title": "Optimized Item Collection",
                "code": """
# Item positions (you need to find these with sensors!)
items = [(5, 2), (2, 7), (9, 3)]

# Sort items by distance for efficiency
def get_distance(item):
    pos = robot.sensor()['position']
    return ((item[0] - pos[0])**2 + (item[1] - pos[1])**2)**0.5

# Collect items in optimal order
while items:
    # Find closest item
    closest_item = min(items, key=get_distance)
    
    # Navigate to item
    navigate_to(closest_item[0], closest_item[1])
    robot.collect()
    
    # Remove collected item from list
    items.remove(closest_item)
"""
            }
        ]

    def setup_level(self):
        """Setup level-specific configuration"""
        pass

    def get_programming_examples(self):
        """Return programming examples for this level"""
        return self.programming_examples
    
    def check_path_efficiency(self, robot):
        """Check if student used efficient pathfinding"""
        return robot.commands_executed <= 25
    
    def get_pathfinding_hints(self, robot):
        """Provide dynamic pathfinding hints"""
        hints = []
        pos = robot.sensor()['position']
        
        # Efficiency hints
        if robot.commands_executed > 15:
            hints.append("🎯 Try planning your route more efficiently")
        
        if robot.items_collected == 0 and robot.commands_executed > 8:
            hints.append("💡 Consider collecting items in order of distance")
        
        if pos[0] < 4 and pos[1] < 4:  # Still in starting quadrant
            hints.append("🗺️ Explore systematically - map out the obstacles first")
        
        return hints
    
    def get_level_specific_commands(self):
        """Return pathfinding-specific commands"""
        return [
            "# Distance calculation",
            "distance = ((x2-x1)**2 + (y2-y1)**2)**0.5",
            "# List operations for waypoints", 
            "waypoints = [(3,2), (5,5), (8,8)]",
            "closest = min(items, key=distance_function)",
            "# Efficient loops",
            "for waypoint in waypoints:",
            "while not_at_target():"
        ]
