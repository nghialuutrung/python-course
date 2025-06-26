"""
Level 6: Time-Optimized Missions
Teaching time management and performance optimization for WRO competitions
"""

import time
from ..core.level import BaseLevel

class Level06(BaseLevel):
    def __init__(self):
        super().__init__()
        self.level_id = 6
        self.name = "Speed Challenge"
        self.description = "Master time-critical missions like real WRO competitions"
        self.difficulty = 6
        
        # Time-critical objectives
        self.add_objective(
            'reach_target',
            'Reach target within time limit',
            target=(10, 6),
            tolerance=1.0
        )
        
        self.add_objective(
            'collect_items',
            'Collect at least 4 out of 6 items',
            count=4
        )
        
        self.add_objective(
            'time_challenge',
            'Complete mission in under 60 seconds',
            time_limit=60
        )
        
        self.add_objective(
            'efficiency_bonus',
            'Bonus: Use fewer than 30 commands',
            max_commands=30
        )
        
        # Competition-style obstacle course
        from ..core.constants import SIDEBAR_WIDTH
        
        # Multiple paths with different difficulties
        self.add_obstacle(SIDEBAR_WIDTH + 150, 100, 50, 150)   # Path blocker 1
        self.add_obstacle(SIDEBAR_WIDTH + 300, 200, 100, 50)   # Path blocker 2
        self.add_obstacle(SIDEBAR_WIDTH + 450, 100, 50, 200)   # Path blocker 3
        self.add_obstacle(SIDEBAR_WIDTH + 200, 350, 200, 50)   # Bottom barrier
        
        # Strategic item placement - some easier, some harder to reach
        self.add_item(SIDEBAR_WIDTH + 120, 180, 'coin')  # Easy item 1
        self.add_item(SIDEBAR_WIDTH + 250, 120, 'coin')  # Medium item 2
        self.add_item(SIDEBAR_WIDTH + 380, 180, 'coin')  # Easy item 3
        self.add_item(SIDEBAR_WIDTH + 180, 300, 'coin')  # Hard item 4
        self.add_item(SIDEBAR_WIDTH + 420, 320, 'coin')  # Hard item 5
        self.add_item(SIDEBAR_WIDTH + 520, 180, 'coin')  # Bonus item 6
        
        # Target area
        self.set_target_area(SIDEBAR_WIDTH + 500, 300, 100, 100)
        
        # Competition strategy hints
        self.add_hint("⏱️ Time is critical! Plan your strategy first")
        self.add_hint("🎯 You don't need ALL items - prioritize easy ones")
        self.add_hint("🚀 Use functions to avoid repeating code")
        self.add_hint("📊 Track your performance: time, commands, items")
        self.add_hint("🏃 Sometimes the fastest path isn't the shortest!")
        
        # Competition programming examples
        self.programming_examples = [
            {
                "title": "Time-Aware Mission Control",
                "code": """
import time

def timed_mission():
    start_time = time.time()
    time_limit = 60  # seconds
    
    # Mission priorities (easy items first)
    easy_items = [(2, 3), (7, 3), (10, 3)]
    hard_items = [(3, 6), (8, 6)]
    
    # Collect easy items first
    for item in easy_items:
        if time.time() - start_time > time_limit * 0.7:
            break  # Save time for reaching target
        navigate_to_item(item)
    
    # Go to target
    navigate_to(10, 6)
    
    total_time = time.time() - start_time
    print(f"Mission completed in {total_time:.1f} seconds")

timed_mission()
"""
            },
            {
                "title": "Efficient Route Planning",
                "code": """
def plan_optimal_route():
    # Current position
    pos = robot.sensor()['position']
    
    # Available items with difficulty scores
    items = [
        {'pos': (2, 3), 'difficulty': 1},
        {'pos': (5, 2), 'difficulty': 2}, 
        {'pos': (8, 3), 'difficulty': 1},
        {'pos': (3, 6), 'difficulty': 3},
        {'pos': (8, 6), 'difficulty': 3},
        {'pos': (10, 3), 'difficulty': 2}
    ]
    
    # Sort by efficiency (distance vs difficulty)
    def efficiency_score(item):
        distance = calculate_distance(pos, item['pos'])
        return distance * item['difficulty']  # Lower is better
    
    sorted_items = sorted(items, key=efficiency_score)
    
    # Collect top 4 most efficient items
    for i in range(min(4, len(sorted_items))):
        item = sorted_items[i]
        navigate_to(item['pos'][0], item['pos'][1])
        robot.collect()

plan_optimal_route()
"""
            },
            {
                "title": "Performance Monitoring",
                "code": """
class PerformanceTracker:
    def __init__(self):
        self.start_time = time.time()
        self.commands_used = 0
        self.items_collected = 0
        self.checkpoints = []
    
    def log_checkpoint(self, description):
        elapsed = time.time() - self.start_time
        self.checkpoints.append({
            'time': elapsed,
            'description': description,
            'commands': self.commands_used
        })
        print(f"⏱️ {description}: {elapsed:.1f}s, {self.commands_used} commands")
    
    def get_performance_report(self):
        total_time = time.time() - self.start_time
        efficiency = self.items_collected / max(1, self.commands_used)
        
        print(f"📊 Performance Report:")
        print(f"   Total Time: {total_time:.1f}s")
        print(f"   Commands Used: {self.commands_used}")
        print(f"   Items Collected: {self.items_collected}")
        print(f"   Efficiency: {efficiency:.2f} items/command")

# Usage
tracker = PerformanceTracker()
tracker.log_checkpoint("Started mission")
# ... mission code ...
tracker.log_checkpoint("Completed mission")
tracker.get_performance_report()
"""
            }
        ]
        
        # Track mission start time
        self.mission_start_time = None

    def setup_level(self):
        """Setup level-specific configuration"""
        pass

    def start_mission_timer(self):
        """Start the mission timer"""
        self.mission_start_time = time.time()
    
    def get_mission_time(self):
        """Get elapsed mission time"""
        if self.mission_start_time:
            return time.time() - self.mission_start_time
        return 0
    
    def check_time_limit(self, robot):
        """Check if mission completed within time limit"""
        return self.get_mission_time() <= 60
    
    def get_programming_examples(self):
        """Return programming examples for this level"""
        return self.programming_examples
    
    def get_performance_hints(self, robot):
        """Provide performance optimization hints"""
        hints = []
        elapsed_time = self.get_mission_time()
        
        # Time-based hints
        if elapsed_time > 30:
            hints.append("⏰ Time running out! Focus on easy items and target")
        
        if robot.commands_executed > 20 and robot.items_collected < 2:
            hints.append("🎯 Try collecting easier items first")
        
        if elapsed_time > 45:
            hints.append("🏃 Consider going straight to target now!")
        
        # Efficiency hints
        efficiency = robot.items_collected / max(1, robot.commands_executed)
        if efficiency < 0.1:
            hints.append("📈 Improve efficiency: plan your route better")
        
        return hints
    
    def get_level_specific_commands(self):
        """Return time-optimization specific commands"""
        return [
            "import time",
            "start_time = time.time()",
            "elapsed = time.time() - start_time",
            "# Priority-based collection",
            "easy_items = [...]",
            "hard_items = [...]",
            "# Efficiency calculations",
            "efficiency = items / commands",
            "# Time limits",
            "if elapsed > time_limit: break"
        ]
