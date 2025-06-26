"""
Robot class for WRO Robot Control System
"""

import math
import time
from typing import List, Dict, Tuple, Optional
from .constants import *


class PythonRobot:
    """Robot class that students can control with Python commands"""
    
    def __init__(self, x: float = SIDEBAR_WIDTH + 100, y: float = 100):
        # Position and orientation
        self.x = x
        self.y = y
        self.angle = 0  # degrees
        self.size = ROBOT_SIZE
        self.speed = ROBOT_SPEED
        
        # Game state
        self.score = 0
        self.items_collected = 0
        self.commands_executed = 0
        self.sensor_calls = 0
        self.start_time: Optional[float] = None
        self.level_start_time: Optional[float] = None
        
        # Animation
        self.target_x = x
        self.target_y = y
        self.target_angle = 0
        self.animating = False
        self.animation_speed = ANIMATION_SPEED
        
        # History for undo functionality
        self.position_history: List[Tuple[float, float, float]] = [(x, y, 0)]
        
        # Environment
        self.obstacles: List[Dict] = []
        self.items: List[Dict] = []

        # Callback for objective checking
        self.objective_check_callback = None

        # Visual effects
        self.trail_positions = []
        self.max_trail_length = 10
    
    def forward(self, distance: float = 1) -> str:
        """Move robot forward by distance units"""
        self.commands_executed += 1
        pixel_distance = distance * UNIT_SIZE
        print(f">> Moving forward {distance} units ({pixel_distance} pixels)...")

        angle_rad = math.radians(self.angle)
        new_x = self.x + pixel_distance * math.cos(angle_rad)
        new_y = self.y + pixel_distance * math.sin(angle_rad)

        # Keep within bounds
        new_x = max(self.size, min(GAME_WIDTH - self.size, new_x))
        new_y = max(self.size, min(SCREEN_HEIGHT - self.size, new_y))

        # Save position for undo
        self.position_history.append((self.x, self.y, self.angle))
        if len(self.position_history) > MAX_HISTORY:
            self.position_history.pop(0)

        self.target_x = new_x
        self.target_y = new_y
        self.animating = True

        return f"Moved to ({new_x/UNIT_SIZE:.1f}, {new_y/UNIT_SIZE:.1f})"
    
    def backward(self, distance: float = 1) -> str:
        """Move robot backward by distance units"""
        return self.forward(-distance)
    
    def left(self, angle: float = 90) -> str:
        """Turn robot left by angle degrees"""
        self.commands_executed += 1
        print(f">> Turning left {angle} degrees...")

        self.position_history.append((self.x, self.y, self.angle))
        if len(self.position_history) > MAX_HISTORY:
            self.position_history.pop(0)

        self.target_angle = (self.angle - angle) % 360
        self.animating = True

        return f"Turned to {self.target_angle:.1f} degrees"
    
    def right(self, angle: float = 90) -> str:
        """Turn robot right by angle degrees"""
        self.commands_executed += 1
        print(f">> Turning right {angle} degrees...")

        self.position_history.append((self.x, self.y, self.angle))
        if len(self.position_history) > MAX_HISTORY:
            self.position_history.pop(0)

        self.target_angle = (self.angle + angle) % 360
        self.animating = True

        return f"Turned to {self.target_angle:.1f} degrees"
    
    def sensor(self) -> Dict:
        """Get sensor readings"""
        self.sensor_calls += 1
        readings = {
            'front': self.get_distance_to_obstacle(0),
            'left': self.get_distance_to_obstacle(-90),
            'right': self.get_distance_to_obstacle(90),
            'position': (round(self.x / UNIT_SIZE, 1), round(self.y / UNIT_SIZE, 1)),
            'angle': round(self.angle, 1)
        }
        print(f">> Sensor readings: {readings}")
        return readings
    
    def front_sensor(self) -> float:
        """Get front sensor reading only"""
        self.sensor_calls += 1
        distance = self.get_distance_to_obstacle(0)
        print(f">> Front sensor: {distance}")
        return distance
    
    def left_sensor(self) -> float:
        """Get left sensor reading only"""
        self.sensor_calls += 1
        distance = self.get_distance_to_obstacle(-90)
        print(f">> Left sensor: {distance}")
        return distance
    
    def right_sensor(self) -> float:
        """Get right sensor reading only"""
        self.sensor_calls += 1
        distance = self.get_distance_to_obstacle(90)
        print(f">> Right sensor: {distance}")
        return distance
    
    def collect(self) -> str:
        """Collect nearby items"""
        collected = 0
        items_to_remove = []
        
        for i, item in enumerate(self.items):
            distance = math.sqrt((self.x - item['x'])**2 + (self.y - item['y'])**2)
            if distance < 40:  # Collection radius
                items_to_remove.append(i)
                collected += 1
                self.items_collected += 1
                self.score += 10
        
        # Remove collected items (reverse order to maintain indices)
        for i in reversed(items_to_remove):
            self.items.pop(i)
        
        if collected > 0:
            print(f"OK: Collected {collected} items! Total: {self.items_collected}")
            return f"Collected {collected} items"
        else:
            print("ERROR: No items nearby to collect")
            return "No items nearby"
    
    def get_distance_to_obstacle(self, angle_offset: float) -> float:
        """Get distance to nearest obstacle in given direction"""
        sensor_angle = math.radians(self.angle + angle_offset)
        sensor_range = 200  # pixels
        
        # Cast ray to find obstacles
        for distance in range(1, sensor_range, 5):
            check_x = self.x + distance * math.cos(sensor_angle)
            check_y = self.y + distance * math.sin(sensor_angle)
            
            # Check bounds
            if check_x <= 0 or check_x >= GAME_WIDTH or check_y <= 0 or check_y >= SCREEN_HEIGHT:
                return distance / UNIT_SIZE
            
            # Check obstacles
            for obstacle in self.obstacles:
                if (obstacle['x'] <= check_x <= obstacle['x'] + obstacle['width'] and
                    obstacle['y'] <= check_y <= obstacle['y'] + obstacle['height']):
                    return distance / UNIT_SIZE
        
        return sensor_range / UNIT_SIZE
    
    def reset_for_level(self, level):
        """Reset robot for a specific level"""
        # Position robot in game area (offset by sidebar)
        start_x = SIDEBAR_WIDTH + 100  # 100 pixels from left edge of game area
        start_y = 100  # 100 pixels from top

        self.x = self.target_x = start_x
        self.y = self.target_y = start_y
        self.angle = self.target_angle = 0
        self.position_history = [(start_x, start_y, 0)]
        self.animating = False
        
        # Reset game metrics
        self.score = 0
        self.items_collected = 0
        self.commands_executed = 0
        self.sensor_calls = 0
        self.level_start_time = time.time()
        
        print(f"🎯 Starting Level {level.level_id}: {level.name}")
        print(f"📝 Objective: {level.description}")
        
        # Show hints for difficulty 1-2 levels
        if level.difficulty <= 2 and level.hints:
            print("💡 Hints:")
            for hint in level.hints[:2]:
                print(f"   • {hint}")
        
        return f"Level {level.level_id} started"
    
    def update(self, dt: float):
        """Update robot animation"""
        if not self.animating:
            return
        
        # Move towards target position
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 1:
            move_distance = self.animation_speed * dt
            if move_distance >= distance:
                self.x = self.target_x
                self.y = self.target_y
            else:
                self.x += (dx / distance) * move_distance
                self.y += (dy / distance) * move_distance
        else:
            self.x = self.target_x
            self.y = self.target_y
        
        # Rotate towards target angle
        angle_diff = self.target_angle - self.angle
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360
        
        if abs(angle_diff) > 1:
            rotation_speed = 180 * dt  # degrees per second
            if abs(angle_diff) <= rotation_speed:
                self.angle = self.target_angle
            else:
                self.angle += rotation_speed if angle_diff > 0 else -rotation_speed
        else:
            self.angle = self.target_angle
        
        # Update trail positions during movement
        if self.animating:
            self.trail_positions.append((self.x, self.y))
            if len(self.trail_positions) > self.max_trail_length:
                self.trail_positions.pop(0)

        # Check if animation is complete
        if distance <= 1 and abs(angle_diff) <= 1:
            self.animating = False
            # Clear trail when movement stops
            self.trail_positions = []
            # Auto-check objectives when movement is complete
            if self.objective_check_callback:
                self.objective_check_callback()
