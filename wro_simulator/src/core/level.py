"""
Base Level class for WRO Robot Control System
"""

import math
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class Objective:
    """Represents a level objective"""
    
    def __init__(self, obj_type: str, description: str, **kwargs):
        self.type = obj_type
        self.description = description
        self.params = kwargs
        self.completed = False
    
    def check_completion(self, robot) -> bool:
        """Check if objective is completed"""
        if self.type == 'reach_target':
            target = self.params.get('target', (10, 10))
            tolerance = self.params.get('tolerance', 1.0)

            # Convert robot pixel position to grid coordinates (accounting for sidebar)
            from .constants import UNIT_SIZE, SIDEBAR_WIDTH
            robot_grid_x = (robot.x - SIDEBAR_WIDTH) / UNIT_SIZE
            robot_grid_y = robot.y / UNIT_SIZE
            robot_pos = (robot_grid_x, robot_grid_y)

            distance = math.sqrt((robot_pos[0] - target[0])**2 + (robot_pos[1] - target[1])**2)
            return distance <= tolerance
            
        elif self.type == 'collect_items':
            required = self.params.get('count', 1)
            return robot.items_collected >= required
            
        elif self.type == 'avoid_obstacles':
            return True  # Simplified for now
            
        elif self.type == 'use_sensors':
            required_calls = self.params.get('sensor_calls', 1)
            return robot.sensor_calls >= required_calls
            
        elif self.type == 'efficient_path':
            max_commands = self.params.get('max_commands', 10)
            return robot.commands_executed <= max_commands
            
        return False


class BaseLevel(ABC):
    """Abstract base class for all levels"""
    
    def __init__(self):
        # These will be set in setup_level()
        self.level_id = 0
        self.name = ""
        self.description = ""
        self.difficulty = 1  # 1-5 stars
        self.objectives: List[Objective] = []
        self.obstacles: List[Dict] = []
        self.items: List[Dict] = []
        self.target_area: Optional[Dict] = None
        self.time_limit: Optional[float] = None
        self.allowed_commands: Optional[List[str]] = None
        self.hints: List[str] = []
        self.completed = False
        self.best_score = 0
        self.best_time: Optional[float] = None
        
        # Initialize level-specific content
        self.setup_level()
    
    @abstractmethod
    def setup_level(self):
        """Setup level-specific objectives, obstacles, items, etc."""
        pass
    
    def add_objective(self, obj_type: str, description: str, **kwargs):
        """Add an objective to the level"""
        objective = Objective(obj_type, description, **kwargs)
        self.objectives.append(objective)
    
    def add_obstacle(self, x: int, y: int, width: int, height: int):
        """Add an obstacle to the level"""
        self.obstacles.append({
            'x': x, 'y': y, 'width': width, 'height': height
        })
    
    def add_item(self, x: int, y: int, item_type: str = 'coin'):
        """Add a collectible item to the level"""
        self.items.append({
            'x': x, 'y': y, 'type': item_type
        })
    
    def set_target_area(self, x: int, y: int, width: int, height: int):
        """Set the target area for the level"""
        self.target_area = {
            'x': x, 'y': y, 'width': width, 'height': height
        }
    
    def add_hint(self, hint: str):
        """Add a hint for the level"""
        self.hints.append(hint)
    
    def is_completed(self, robot) -> bool:
        """Check if all objectives are completed"""
        return all(obj.check_completion(robot) for obj in self.objectives)
    
    def get_progress(self, robot) -> Dict[str, Any]:
        """Get current progress on objectives"""
        progress = {
            'total_objectives': len(self.objectives),
            'completed_objectives': 0,
            'objectives_status': []
        }
        
        for obj in self.objectives:
            completed = obj.check_completion(robot)
            if completed:
                progress['completed_objectives'] += 1
            
            progress['objectives_status'].append({
                'description': obj.description,
                'completed': completed,
                'type': obj.type
            })
        
        return progress
    
    def get_score(self, time_taken: float, robot) -> int:
        """Calculate score based on performance"""
        base_score = 100
        
        # Time bonus (faster = better)
        time_bonus = max(0, 50 - int(time_taken))
        
        # Efficiency bonus (fewer commands = better)
        efficiency_bonus = max(0, 20 - robot.commands_executed)
        
        # Sensor usage bonus (using sensors = better)
        sensor_bonus = min(10, robot.sensor_calls * 2)
        
        # Difficulty multiplier
        difficulty_multiplier = 1 + (self.difficulty - 1) * 0.2
        
        total_score = int((base_score + time_bonus + efficiency_bonus + sensor_bonus) * difficulty_multiplier)
        return total_score
    
    def reset(self):
        """Reset level state"""
        for obj in self.objectives:
            obj.completed = False
