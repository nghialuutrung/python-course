"""
Level 4: Sensor-Based Navigation
Teaching sensor-based decision making and obstacle avoidance
"""

from ..core.level import BaseLevel

class Level04(BaseLevel):
    def __init__(self):
        super().__init__()
        self.level_id = 4
        self.name = "Sensor Navigation"
        self.description = "Learn to use sensors for smart navigation"
        self.difficulty = 4
        
        # Objectives - Multiple sensors and decision making
        self.add_objective(
            'reach_target',
            'Navigate to target using sensors (avoid obstacles)',
            target=(9, 7),
            tolerance=1.0
        )
        
        self.add_objective(
            'use_sensors',
            'Use sensors at least 5 times for navigation',
            min_sensor_calls=5
        )
        
        # Complex obstacle course requiring sensor navigation
        from ..core.constants import SIDEBAR_WIDTH
        
        # Maze-like obstacles
        self.add_obstacle(SIDEBAR_WIDTH + 150, 100, 100, 50)   # Top barrier
        self.add_obstacle(SIDEBAR_WIDTH + 300, 150, 50, 150)   # Vertical wall
        self.add_obstacle(SIDEBAR_WIDTH + 100, 250, 150, 50)   # Bottom barrier
        self.add_obstacle(SIDEBAR_WIDTH + 400, 200, 100, 100)  # Corner obstacle
        
        # No items - focus on navigation
        self.items = []
        
        # Target area - requires navigating through maze
        self.set_target_area(SIDEBAR_WIDTH + 450, 350, 100, 100)
        
        # Advanced hints for sensor programming
        self.add_hint("Use robot.sensor() to get all sensor readings")
        self.add_hint("Check robot.front_sensor() before moving forward")
        self.add_hint("Use if/elif/else for sensor-based decisions")
        self.add_hint("Example: if robot.front_sensor() < 2: robot.right()")
        self.add_hint("Create functions like is_path_clear() for reusable logic")
        
        # Programming examples for students
        self.programming_examples = [
            {
                "title": "Basic Sensor Check",
                "code": """
# Check if path is clear before moving
if robot.front_sensor() > 2:
    robot.forward()
else:
    robot.right()  # Turn if obstacle detected
"""
            },
            {
                "title": "Smart Navigation Function",
                "code": """
def navigate_safely():
    sensors = robot.sensor()
    
    if sensors['front'] > 2:
        robot.forward()
    elif sensors['left'] > sensors['right']:
        robot.left()
    else:
        robot.right()

# Use the function
for i in range(10):
    navigate_safely()
"""
            },
            {
                "title": "Obstacle Avoidance Loop",
                "code": """
# Navigate until target reached
while True:
    pos = robot.sensor()['position']
    if pos[0] >= 9 and pos[1] >= 7:
        break
    
    # Smart navigation logic
    if robot.front_sensor() < 1.5:
        # Obstacle ahead - choose best direction
        if robot.left_sensor() > robot.right_sensor():
            robot.left()
        else:
            robot.right()
    else:
        robot.forward()
"""
            }
        ]

    def setup_level(self):
        """Setup level-specific configuration"""
        pass

    def get_programming_examples(self):
        """Return programming examples for this level"""
        return self.programming_examples
    
    def check_sensor_usage(self, robot):
        """Check if student is using sensors appropriately"""
        return robot.sensor_calls >= 5
    
    def get_navigation_hints(self, robot):
        """Provide dynamic hints based on robot position and sensor readings"""
        sensors = robot.sensor()
        hints = []
        
        # Dynamic hints based on current situation
        if sensors['front'] < 2:
            hints.append("⚠️ Obstacle ahead! Use robot.left() or robot.right()")
        
        if robot.sensor_calls < 3:
            hints.append("💡 Try using robot.sensor() to check surroundings")
        
        if sensors['position'][0] < 5:  # Still in starting area
            hints.append("🧭 Use sensors to find the best path forward")
        
        return hints
    
    def get_level_specific_commands(self):
        """Return level-specific commands students should learn"""
        return [
            "robot.sensor() - Get all sensor readings",
            "robot.front_sensor() - Check distance ahead", 
            "robot.left_sensor() - Check distance to left",
            "robot.right_sensor() - Check distance to right",
            "sensors['position'] - Get current grid position",
            "sensors['angle'] - Get current robot angle"
        ]
