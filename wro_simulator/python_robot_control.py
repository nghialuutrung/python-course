#!/usr/bin/env python3
"""
WRO Python Control System
Interactive system cho học sinh điều khiển robot bằng Python commands
"""

import pygame
import math
import threading
import queue
import sys
import traceback
import time
import os
from io import StringIO

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
CONSOLE_WIDTH = 400
GAME_WIDTH = SCREEN_WIDTH - CONSOLE_WIDTH
FPS = 60

# Modern Color Palette
WHITE = (255, 255, 255)
BLACK = (33, 37, 41)
BLUE = (52, 144, 220)
RED = (231, 76, 60)
GREEN = (46, 204, 113)
YELLOW = (241, 196, 15)
ORANGE = (230, 126, 34)
PURPLE = (155, 89, 182)

# UI Colors
BACKGROUND = (248, 249, 250)
GRID_LIGHT = (233, 236, 239)
GRID_MAJOR = (206, 212, 218)
OBSTACLE_COLOR = (108, 117, 125)
ROBOT_COLOR = (52, 144, 220)
ROBOT_DIRECTION = (231, 76, 60)
ITEM_COLOR = (241, 196, 15)
TARGET_COLOR = (40, 167, 69)

# Console Colors
CONSOLE_BG = (33, 37, 41)
CONSOLE_BORDER = (52, 58, 64)
CONSOLE_TEXT = (248, 249, 250)
CONSOLE_PROMPT = (52, 144, 220)
CONSOLE_SUCCESS = (40, 167, 69)
CONSOLE_ERROR = (220, 53, 69)
CONSOLE_WARNING = (255, 193, 7)

# HUD Colors
HUD_BG = (255, 255, 255)  # White background
HUD_BORDER = (206, 212, 218)
HUD_TEXT = (33, 37, 41)

class Level:
    """Represents a game level with objectives and constraints"""

    def __init__(self, level_id, name, description, difficulty, objectives,
                 obstacles=None, items=None, target_area=None, time_limit=None,
                 allowed_commands=None, hints=None):
        self.level_id = level_id
        self.name = name
        self.description = description
        self.difficulty = difficulty  # 1-5 stars
        self.objectives = objectives  # List of objectives to complete
        self.obstacles = obstacles or []
        self.items = items or []
        self.target_area = target_area
        self.time_limit = time_limit  # seconds, None for unlimited
        self.allowed_commands = allowed_commands  # None for all commands
        self.hints = hints or []
        self.completed = False
        self.best_score = 0
        self.best_time = None

    def is_objective_completed(self, robot):
        """Check if level objectives are completed"""
        for objective in self.objectives:
            if not self._check_objective(objective, robot):
                return False
        return True

    def _check_objective(self, objective, robot):
        """Check individual objective"""
        obj_type = objective.get('type')

        if obj_type == 'reach_target':
            target = objective.get('target', (10, 10))
            tolerance = objective.get('tolerance', 1.0)
            robot_pos = (robot.x / 50, robot.y / 50)
            distance = math.sqrt((robot_pos[0] - target[0])**2 + (robot_pos[1] - target[1])**2)
            return distance <= tolerance

        elif obj_type == 'collect_items':
            required = objective.get('count', 1)
            return robot.items_collected >= required

        elif obj_type == 'avoid_obstacles':
            # Check if robot never hit obstacles (could track collisions)
            return True  # Simplified for now

        elif obj_type == 'use_sensors':
            required_calls = objective.get('sensor_calls', 1)
            return robot.sensor_calls >= required_calls

        elif obj_type == 'efficient_path':
            max_commands = objective.get('max_commands', 10)
            return robot.commands_executed <= max_commands

        return False

class LevelManager:
    """Manages game levels and progression"""

    def __init__(self):
        self.levels = self._create_levels()
        self.current_level = None
        self.unlocked_levels = [1]  # Level 1 is always unlocked

    def _create_levels(self):
        """Create all game levels"""
        levels = {}

        # Level 1: Basic Movement
        levels[1] = Level(
            level_id=1,
            name="First Steps",
            description="Learn basic robot movement commands",
            difficulty=1,
            objectives=[
                {'type': 'reach_target', 'target': (5, 5), 'tolerance': 1.0}
            ],
            obstacles=[],
            items=[],
            target_area={'x': 200, 'y': 200, 'width': 100, 'height': 100},
            hints=[
                "Use robot.forward() to move forward",
                "Use robot.right() to turn right",
                "Try: robot.forward(5); robot.right(); robot.forward(5)"
            ]
        )

        # Level 2: Turning and Navigation
        levels[2] = Level(
            level_id=2,
            name="Turn Around",
            description="Master turning and basic navigation",
            difficulty=1,
            objectives=[
                {'type': 'reach_target', 'target': (8, 2), 'tolerance': 1.0}
            ],
            obstacles=[
                {'x': 150, 'y': 150, 'width': 100, 'height': 50}
            ],
            items=[],
            target_area={'x': 350, 'y': 50, 'width': 100, 'height': 100},
            hints=[
                "You need to go around the obstacle",
                "Use robot.left() and robot.right() to turn",
                "Plan your path before coding"
            ]
        )

        # Level 3: Item Collection
        levels[3] = Level(
            level_id=3,
            name="Treasure Hunt",
            description="Collect items while navigating",
            difficulty=2,
            objectives=[
                {'type': 'collect_items', 'count': 2},
                {'type': 'reach_target', 'target': (10, 8), 'tolerance': 1.0}
            ],
            obstacles=[
                {'x': 100, 'y': 200, 'width': 50, 'height': 100}
            ],
            items=[
                {'x': 150, 'y': 100, 'type': 'coin'},
                {'x': 300, 'y': 300, 'type': 'coin'}
            ],
            target_area={'x': 450, 'y': 350, 'width': 100, 'height': 100},
            hints=[
                "Use robot.collect() when near items",
                "Items glow when you're close enough",
                "Collect all items before reaching target"
            ]
        )

        # Level 4: Sensor Usage
        levels[4] = Level(
            level_id=4,
            name="Sensor Navigation",
            description="Use sensors to navigate safely",
            difficulty=2,
            objectives=[
                {'type': 'use_sensors', 'sensor_calls': 3},
                {'type': 'reach_target', 'target': (9, 9), 'tolerance': 1.0},
                {'type': 'avoid_obstacles'}
            ],
            obstacles=[
                {'x': 200, 'y': 100, 'width': 50, 'height': 200},
                {'x': 350, 'y': 250, 'width': 100, 'height': 50}
            ],
            items=[],
            target_area={'x': 400, 'y': 400, 'width': 100, 'height': 100},
            hints=[
                "Use robot.sensor() to check distances",
                "Check sensors before moving",
                "if robot.front_sensor() < 1: robot.left()"
            ]
        )

        # Level 5: Efficient Programming
        levels[5] = Level(
            level_id=5,
            name="Code Golf",
            description="Reach target with minimal commands",
            difficulty=3,
            objectives=[
                {'type': 'reach_target', 'target': (8, 8), 'tolerance': 1.0},
                {'type': 'efficient_path', 'max_commands': 8}
            ],
            obstacles=[
                {'x': 150, 'y': 150, 'width': 200, 'height': 50},
                {'x': 300, 'y': 300, 'width': 50, 'height': 150}
            ],
            items=[],
            target_area={'x': 350, 'y': 350, 'width': 100, 'height': 100},
            hints=[
                "Use the shortest path possible",
                "Combine movements efficiently",
                "robot.move_to() might help"
            ]
        )

        return levels

    def get_level(self, level_id):
        """Get level by ID"""
        return self.levels.get(level_id)

    def is_level_unlocked(self, level_id):
        """Check if level is unlocked"""
        return level_id in self.unlocked_levels

    def unlock_level(self, level_id):
        """Unlock a level"""
        if level_id not in self.unlocked_levels:
            self.unlocked_levels.append(level_id)

    def complete_level(self, level_id, score, time_taken):
        """Mark level as completed"""
        level = self.get_level(level_id)
        if level:
            level.completed = True
            level.best_score = max(level.best_score, score)
            if level.best_time is None or time_taken < level.best_time:
                level.best_time = time_taken

            # Unlock next level
            next_level = level_id + 1
            if next_level in self.levels:
                self.unlock_level(next_level)

class IconRenderer:
    """Simple icon renderer using pygame shapes"""

    @staticmethod
    def draw_star(surface, center, size, color):
        """Draw a star icon"""
        x, y = center
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                radius = size
            else:
                radius = size * 0.5
            px = x + radius * math.cos(angle - math.pi/2)
            py = y + radius * math.sin(angle - math.pi/2)
            points.append((px, py))
        pygame.draw.polygon(surface, color, points)

    @staticmethod
    def draw_diamond(surface, center, size, color):
        """Draw a diamond icon"""
        x, y = center
        points = [
            (x, y - size),      # top
            (x + size, y),      # right
            (x, y + size),      # bottom
            (x - size, y)       # left
        ]
        pygame.draw.polygon(surface, color, points)

    @staticmethod
    def draw_lightning(surface, center, size, color):
        """Draw a lightning bolt icon"""
        x, y = center
        points = [
            (x - size//2, y - size),
            (x + size//4, y - size//4),
            (x - size//4, y - size//4),
            (x + size//2, y + size),
            (x - size//4, y + size//4),
            (x + size//4, y + size//4)
        ]
        pygame.draw.polygon(surface, color, points)

    @staticmethod
    def draw_location(surface, center, size, color):
        """Draw a location pin icon"""
        x, y = center
        # Pin body
        pygame.draw.circle(surface, color, (x, y - size//3), size//2)
        # Pin point
        points = [
            (x - size//3, y),
            (x, y + size//2),
            (x + size//3, y)
        ]
        pygame.draw.polygon(surface, color, points)

    @staticmethod
    def draw_compass(surface, center, size, color):
        """Draw a compass icon"""
        x, y = center
        # Outer circle
        pygame.draw.circle(surface, color, center, size, 2)
        # North arrow
        points = [
            (x, y - size + 2),
            (x - 3, y - 2),
            (x + 3, y - 2)
        ]
        pygame.draw.polygon(surface, color, points)
        # Center dot
        pygame.draw.circle(surface, color, center, 2)

class LevelSelectScreen:
    """Level selection screen for the game"""

    def __init__(self, level_manager):
        self.level_manager = level_manager
        self.selected_level = 1
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)

    def handle_key(self, key):
        """Handle keyboard input for level selection"""
        if key == pygame.K_UP:
            self.selected_level = max(1, self.selected_level - 1)
        elif key == pygame.K_DOWN:
            max_level = max(self.level_manager.unlocked_levels)
            self.selected_level = min(max_level, self.selected_level + 1)
        elif key == pygame.K_RETURN:
            if self.level_manager.is_level_unlocked(self.selected_level):
                return self.selected_level
        return None

    def draw(self, screen):
        """Draw beautiful level selection screen"""
        # Gradient background
        self.draw_gradient_background(screen)

        # Header section with modern styling
        self.draw_header(screen)

        # Level cards with improved design
        self.draw_level_cards(screen)

        # Footer with instructions and progress
        self.draw_footer(screen)

    def draw_gradient_background(self, screen):
        """Draw gradient background"""
        # Create gradient from dark blue to black
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(20 * (1 - ratio) + 10 * ratio)
            g = int(30 * (1 - ratio) + 15 * ratio)
            b = int(50 * (1 - ratio) + 25 * ratio)
            color = (r, g, b)
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

    def draw_header(self, screen):
        """Draw modern header section"""
        # Main title with shadow effect
        title_font = pygame.font.Font(None, 42)
        shadow_text = title_font.render("WRO Robot Programming Academy", True, (20, 20, 20))
        main_text = title_font.render("WRO Robot Programming Academy", True, WHITE)

        title_rect = main_text.get_rect(center=(SCREEN_WIDTH//2, 45))
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH//2 + 2, 47))

        screen.blit(shadow_text, shadow_rect)
        screen.blit(main_text, title_rect)

        # Robot icon
        robot_center = (SCREEN_WIDTH//2 - 200, 45)
        pygame.draw.circle(screen, BLUE, robot_center, 15)
        pygame.draw.circle(screen, WHITE, robot_center, 15, 2)
        pygame.draw.circle(screen, WHITE, (robot_center[0] - 5, robot_center[1] - 3), 3)
        pygame.draw.circle(screen, WHITE, (robot_center[0] + 5, robot_center[1] - 3), 3)

        # Subtitle with better styling
        subtitle_text = self.font_medium.render("Master Python Programming Through Interactive Challenges", True, (150, 200, 255))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, 75))
        screen.blit(subtitle_text, subtitle_rect)

        # Decorative line
        line_y = 95
        pygame.draw.line(screen, (100, 150, 200), (100, line_y), (SCREEN_WIDTH - 100, line_y), 2)

    def draw_level_cards(self, screen):
        """Draw beautiful level cards"""
        start_y = 120
        card_height = 90
        card_spacing = 8
        card_width = SCREEN_WIDTH - 160

        for level_id in sorted(self.level_manager.levels.keys()):
            level = self.level_manager.get_level(level_id)
            is_unlocked = self.level_manager.is_level_unlocked(level_id)
            is_selected = level_id == self.selected_level

            # Card position
            card_y = start_y + (level_id - 1) * (card_height + card_spacing)
            card_rect = pygame.Rect(80, card_y, card_width, card_height)

            # Card styling with modern effects
            self.draw_level_card(screen, card_rect, level, is_unlocked, is_selected)

    def draw_level_card(self, screen, card_rect, level, is_unlocked, is_selected):
        """Draw individual level card with modern styling"""
        # Card shadow
        shadow_rect = pygame.Rect(card_rect.x + 3, card_rect.y + 3, card_rect.width, card_rect.height)
        pygame.draw.rect(screen, (10, 10, 10), shadow_rect, border_radius=12)

        # Card background with gradient effect
        if is_selected and is_unlocked:
            # Bright blue gradient for selected unlocked
            self.draw_card_gradient(screen, card_rect, (70, 130, 220), (50, 110, 200))
            border_color = (255, 255, 255)
            border_width = 3
        elif is_unlocked:
            # Subtle blue gradient for unlocked
            self.draw_card_gradient(screen, card_rect, (45, 55, 75), (35, 45, 65))
            border_color = (100, 150, 200)
            border_width = 2
        else:
            # Dark gradient for locked
            self.draw_card_gradient(screen, card_rect, (30, 30, 30), (20, 20, 20))
            border_color = (60, 60, 60)
            border_width = 1

        # Card border
        pygame.draw.rect(screen, border_color, card_rect, border_width, border_radius=12)

        # Level content
        self.draw_card_content(screen, card_rect, level, is_unlocked, is_selected)

    def draw_card_gradient(self, screen, rect, color1, color2):
        """Draw gradient background for card"""
        for y in range(rect.height):
            ratio = y / rect.height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            color = (r, g, b)
            pygame.draw.line(screen, color,
                           (rect.x, rect.y + y),
                           (rect.x + rect.width, rect.y + y))

    def draw_card_content(self, screen, card_rect, level, is_unlocked, is_selected):
        """Draw content inside level card"""
        # Level icon/number circle
        icon_center = (card_rect.x + 35, card_rect.y + 30)
        icon_radius = 20

        if is_unlocked:
            # Colorful icon for unlocked levels
            icon_color = (255, 215, 0) if level.completed else (100, 200, 255)
            pygame.draw.circle(screen, icon_color, icon_center, icon_radius)
            pygame.draw.circle(screen, WHITE, icon_center, icon_radius, 2)

            # Level number
            number_font = pygame.font.Font(None, 28)
            number_text = number_font.render(str(level.level_id), True, BLACK)
            number_rect = number_text.get_rect(center=icon_center)
            screen.blit(number_text, number_rect)
        else:
            # Lock icon for locked levels
            pygame.draw.circle(screen, (60, 60, 60), icon_center, icon_radius)
            pygame.draw.circle(screen, (100, 100, 100), icon_center, icon_radius, 2)

            # Lock symbol
            lock_font = pygame.font.Font(None, 24)
            lock_text = lock_font.render("🔒", True, (150, 150, 150))
            lock_rect = lock_text.get_rect(center=icon_center)
            screen.blit(lock_text, lock_rect)

        # Level text content
        text_x = card_rect.x + 70  # Start after icon

        if is_unlocked:
            # Level title
            title_font = pygame.font.Font(None, 26)
            level_title = f"Level {level.level_id}: {level.name}"
            title_text = title_font.render(level_title, True, WHITE)
            screen.blit(title_text, (text_x, card_rect.y + 8))

            # Description
            desc_text = self.font_small.render(level.description, True, (200, 200, 200))
            screen.blit(desc_text, (text_x, card_rect.y + 30))

            # Difficulty stars
            stars = "⭐" * level.difficulty
            stars_text = self.font_small.render(f"Difficulty: {stars}", True, (255, 215, 0))
            screen.blit(stars_text, (text_x, card_rect.y + 50))

            # Status and completion info
            if level.completed:
                status_text = self.font_small.render("✅ Completed", True, (100, 255, 100))
                screen.blit(status_text, (text_x, card_rect.y + 68))

                # Best time
                if level.best_time:
                    time_text = self.font_small.render(f"Best: {level.best_time:.1f}s", True, (150, 200, 255))
                    screen.blit(time_text, (card_rect.right - 120, card_rect.y + 68))
            else:
                status_text = self.font_small.render("🎯 Ready to play", True, (100, 200, 255))
                screen.blit(status_text, (text_x, card_rect.y + 68))
        else:
            # Locked level
            title_text = self.font_medium.render(f"Level {level.level_id}: ???", True, (120, 120, 120))
            screen.blit(title_text, (text_x, card_rect.y + 15))

            lock_desc = self.font_small.render("Complete previous level to unlock", True, (100, 100, 100))
            screen.blit(lock_desc, (text_x, card_rect.y + 40))

    def draw_footer(self, screen):
        """Draw footer with instructions and progress"""
        footer_y = SCREEN_HEIGHT - 120

        # Footer background
        footer_rect = pygame.Rect(0, footer_y, SCREEN_WIDTH, 120)
        footer_surface = pygame.Surface((SCREEN_WIDTH, 120))
        footer_surface.set_alpha(180)
        footer_surface.fill((15, 25, 35))
        screen.blit(footer_surface, (0, footer_y))

        # Instructions panel
        inst_panel_rect = pygame.Rect(50, footer_y + 20, 300, 80)
        pygame.draw.rect(screen, (25, 35, 45), inst_panel_rect, border_radius=8)
        pygame.draw.rect(screen, (100, 150, 200), inst_panel_rect, 2, border_radius=8)

        # Instructions title
        inst_title = self.font_medium.render("🎮 Controls", True, (150, 200, 255))
        screen.blit(inst_title, (inst_panel_rect.x + 15, inst_panel_rect.y + 8))

        # Instructions
        instructions = [
            "↑↓  Navigate levels",
            "⏎   Select level",
            "⎋   Exit game"
        ]

        for i, instruction in enumerate(instructions):
            inst_text = self.font_small.render(instruction, True, (200, 200, 200))
            screen.blit(inst_text, (inst_panel_rect.x + 15, inst_panel_rect.y + 30 + i * 16))

        # Progress panel
        progress_panel_rect = pygame.Rect(SCREEN_WIDTH - 350, footer_y + 20, 300, 80)
        pygame.draw.rect(screen, (25, 35, 45), progress_panel_rect, border_radius=8)
        pygame.draw.rect(screen, (100, 200, 100), progress_panel_rect, 2, border_radius=8)

        # Progress title
        progress_title = self.font_medium.render("📊 Progress", True, (150, 255, 150))
        screen.blit(progress_title, (progress_panel_rect.x + 15, progress_panel_rect.y + 8))

        # Progress stats
        completed_levels = sum(1 for level in self.level_manager.levels.values() if level.completed)
        total_levels = len(self.level_manager.levels)

        progress_text = self.font_small.render(f"Completed: {completed_levels}/{total_levels} levels", True, (200, 255, 200))
        screen.blit(progress_text, (progress_panel_rect.x + 15, progress_panel_rect.y + 30))

        # Progress bar
        bar_width = 200
        bar_height = 8
        bar_x = progress_panel_rect.x + 15
        bar_y = progress_panel_rect.y + 50

        # Background bar
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=4)

        # Progress bar fill
        if total_levels > 0:
            fill_width = int((completed_levels / total_levels) * bar_width)
            if fill_width > 0:
                pygame.draw.rect(screen, (100, 255, 100), (bar_x, bar_y, fill_width, bar_height), border_radius=4)

        # Percentage
        percentage = int((completed_levels / total_levels) * 100) if total_levels > 0 else 0
        percent_text = self.font_small.render(f"{percentage}%", True, (150, 255, 150))
        screen.blit(percent_text, (bar_x + bar_width + 10, bar_y - 2))

class PythonRobot:
    """Robot class that students can control with Python commands"""
    
    def __init__(self, x=100, y=100):
        self.x = x
        self.y = y
        self.angle = 0  # degrees
        self.size = 20
        self.speed = 100  # pixels per second
        
        # Game state
        self.score = 0
        self.items_collected = 0
        self.commands_executed = 0
        self.sensor_calls = 0
        self.start_time = None
        self.level_start_time = None
        
        # Animation
        self.target_x = x
        self.target_y = y
        self.target_angle = 0
        self.animating = False
        self.animation_speed = 200
        
        # History for undo
        self.position_history = [(x, y, 0)]
        
        # Sensor simulation
        self.obstacles = []
        self.items = []
        
    def forward(self, distance=1):
        """Move robot forward by distance units (1 unit = 50 pixels)"""
        self.commands_executed += 1
        pixel_distance = distance * 50  # Convert units to pixels
        print(f">> Moving forward {distance} units ({pixel_distance} pixels)...")

        angle_rad = math.radians(self.angle)
        new_x = self.x + pixel_distance * math.cos(angle_rad)
        new_y = self.y + pixel_distance * math.sin(angle_rad)
        
        # Keep robot on screen
        new_x = max(self.size, min(GAME_WIDTH - self.size, new_x))
        new_y = max(self.size, min(SCREEN_HEIGHT - self.size, new_y))
        
        # Save current position for undo
        self.position_history.append((self.x, self.y, self.angle))
        if len(self.position_history) > 50:  # Limit history
            self.position_history.pop(0)
        
        # Set animation target
        self.target_x = new_x
        self.target_y = new_y
        self.animating = True
        self.commands_executed += 1
        
        return f"Moved to ({new_x:.1f}, {new_y:.1f}) - {distance} units"

    def backward(self, distance=1):
        """Move robot backward by distance units (1 unit = 50 pixels)"""
        return self.forward(-distance)
    
    def left(self, angle=90):
        """Turn robot left by angle degrees (default 90°)"""
        self.commands_executed += 1
        print(f">> Turning left {angle} degrees...")

        self.position_history.append((self.x, self.y, self.angle))
        if len(self.position_history) > 50:
            self.position_history.pop(0)

        self.target_angle = (self.angle - angle) % 360
        self.animating = True
        self.commands_executed += 1

        return f"Turned to {self.target_angle:.1f} degrees"

    def right(self, angle=90):
        """Turn robot right by angle degrees (default 90°)"""
        self.commands_executed += 1
        print(f">> Turning right {angle} degrees...")

        self.position_history.append((self.x, self.y, self.angle))
        if len(self.position_history) > 50:
            self.position_history.pop(0)

        self.target_angle = (self.angle + angle) % 360
        self.animating = True
        self.commands_executed += 1

        return f"Turned to {self.target_angle:.1f} degrees"
    
    def sensor(self):
        """Get sensor readings"""
        self.sensor_calls += 1
        readings = {
            'front': self.get_distance_to_obstacle(0),
            'left': self.get_distance_to_obstacle(-90),
            'right': self.get_distance_to_obstacle(90),
            'position': (round(self.x, 1), round(self.y, 1)),
            'angle': round(self.angle, 1)
        }
        print(f">> Sensor readings: {readings}")
        return readings

    def front_sensor(self):
        """Get front sensor reading only"""
        self.sensor_calls += 1
        distance = self.get_distance_to_obstacle(0)
        print(f">> Front sensor: {distance}")
        return distance

    def left_sensor(self):
        """Get left sensor reading only"""
        self.sensor_calls += 1
        distance = self.get_distance_to_obstacle(-90)
        print(f">> Left sensor: {distance}")
        return distance

    def right_sensor(self):
        """Get right sensor reading only"""
        self.sensor_calls += 1
        distance = self.get_distance_to_obstacle(90)
        print(f">> Right sensor: {distance}")
        return distance
    
    def collect(self):
        """Collect nearby items"""
        collected = 0
        for item in self.items[:]:  # Copy list to avoid modification during iteration
            distance = math.sqrt((self.x - item['x'])**2 + (self.y - item['y'])**2)
            if distance < self.size + 15:  # Collection radius
                self.items.remove(item)
                collected += 1
                self.items_collected += 1
                self.score += 10
        
        if collected > 0:
            print(f"OK: Collected {collected} items! Total: {self.items_collected}")
            return f"Collected {collected} items"
        else:
            print("ERROR: No items nearby to collect")
            return "No items nearby"
    
    def undo(self):
        """Undo last command"""
        if len(self.position_history) > 1:
            self.position_history.pop()  # Remove current position
            last_pos = self.position_history[-1]
            self.x, self.y, self.angle = last_pos
            self.target_x, self.target_y, self.target_angle = last_pos
            print("↩️ Undid last command")
            return "Undid last command"
        else:
            print("❌ Nothing to undo")
            return "Nothing to undo"
    
    def reset(self):
        """Reset robot to starting position"""
        self.x = self.target_x = 100
        self.y = self.target_y = 100
        self.angle = self.target_angle = 0
        self.position_history = [(100, 100, 0)]
        self.commands_executed = 0
        print("🔄 Robot reset to starting position")
        return "Robot reset"

    def reset_for_level(self, level):
        """Reset robot for a specific level"""
        self.x = self.target_x = 100
        self.y = self.target_y = 100
        self.angle = self.target_angle = 0
        self.position_history = [(100, 100, 0)]
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
            for hint in level.hints[:2]:  # Show first 2 hints
                print(f"   • {hint}")

        return f"Level {level.level_id} started"
    
    def status(self):
        """Get robot status"""
        status = {
            'position': (round(self.x, 1), round(self.y, 1)),
            'angle': round(self.angle, 1),
            'score': self.score,
            'items_collected': self.items_collected,
            'commands_executed': self.commands_executed
        }
        print(f"📊 Robot status: {status}")
        return status
    
    def at_target(self):
        """Check if robot is at target area"""
        # Define target area (green zone)
        target_x, target_y = GAME_WIDTH - 100, SCREEN_HEIGHT - 100
        distance = math.sqrt((self.x - target_x)**2 + (self.y - target_y)**2)
        at_target = distance < 50
        if at_target:
            print("OK: Robot is at target!")
        return at_target

    def move_to(self, x, y):
        """Move robot to specific coordinates (in units, 1 unit = 50 pixels)"""
        target_x = x * 50
        target_y = y * 50

        # Keep within bounds
        target_x = max(self.size, min(GAME_WIDTH - self.size, target_x))
        target_y = max(self.size, min(SCREEN_HEIGHT - self.size, target_y))

        print(f">> Moving to position ({x}, {y}) = pixel ({target_x}, {target_y})")

        # Save position for undo
        self.position_history.append((self.x, self.y, self.angle))
        if len(self.position_history) > 50:
            self.position_history.pop(0)

        # Set animation target
        self.target_x = target_x
        self.target_y = target_y
        self.animating = True
        self.commands_executed += 1

        return f"Moving to position ({x}, {y})"

    def get_position(self):
        """Get current position in unit coordinates"""
        pos_x = round(self.x / 50, 1)
        pos_y = round(self.y / 50, 1)
        print(f"📍 Current position: ({pos_x}, {pos_y})")
        return (pos_x, pos_y)

    def face_direction(self, direction):
        """Face a specific direction: 'north', 'south', 'east', 'west'"""
        direction_angles = {
            'north': 270,  # Up
            'south': 90,   # Down
            'east': 0,     # Right
            'west': 180    # Left
        }

        if direction.lower() in direction_angles:
            target_angle = direction_angles[direction.lower()]
            print(f"🧭 Facing {direction} (angle: {target_angle}°)")

            self.position_history.append((self.x, self.y, self.angle))
            if len(self.position_history) > 50:
                self.position_history.pop(0)

            self.target_angle = target_angle
            self.animating = True
            self.commands_executed += 1

            return f"Facing {direction}"
        else:
            print("❌ Invalid direction. Use: 'north', 'south', 'east', 'west'")
            return "Invalid direction"
    
    def avoid_obstacle(self):
        """Smart obstacle avoidance"""
        front = self.front_sensor()
        left = self.left_sensor()
        right = self.right_sensor()
        
        if front < 50:
            if left > right:
                self.left(45)
                print("🚧 Avoiding obstacle - turning left")
            else:
                self.right(45)
                print("🚧 Avoiding obstacle - turning right")
        
        return "Obstacle avoidance executed"
    
    def get_distance_to_obstacle(self, angle_offset):
        """Calculate distance to nearest obstacle in units (1 unit = 50 pixels)"""
        angle = math.radians(self.angle + angle_offset)
        max_range_pixels = 150

        for distance_pixels in range(1, max_range_pixels, 5):
            check_x = self.x + distance_pixels * math.cos(angle)
            check_y = self.y + distance_pixels * math.sin(angle)

            # Check boundaries
            if check_x < 0 or check_x >= GAME_WIDTH or check_y < 0 or check_y >= SCREEN_HEIGHT:
                return round(distance_pixels / 50, 1)  # Convert to units

            # Check obstacles
            for obstacle in self.obstacles:
                if (obstacle['x'] <= check_x <= obstacle['x'] + obstacle['width'] and
                    obstacle['y'] <= check_y <= obstacle['y'] + obstacle['height']):
                    return round(distance_pixels / 50, 1)  # Convert to units

        return round(max_range_pixels / 50, 1)  # Convert to units
    
    def update(self, dt):
        """Update robot animation"""
        if not self.animating:
            return
        
        # Animate position
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 1:
            move_distance = min(self.animation_speed * dt, distance)
            self.x += (dx / distance) * move_distance
            self.y += (dy / distance) * move_distance
        else:
            self.x = self.target_x
            self.y = self.target_y
        
        # Animate angle
        angle_diff = self.target_angle - self.angle
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360
        
        if abs(angle_diff) > 1:
            turn_speed = 180 * dt  # degrees per second
            if angle_diff > 0:
                self.angle += min(turn_speed, angle_diff)
            else:
                self.angle += max(-turn_speed, angle_diff)
        else:
            self.angle = self.target_angle
        
        # Check if animation is complete
        if distance <= 1 and abs(angle_diff) <= 1:
            self.animating = False

class PythonConsole:
    """Interactive Python console for robot control"""
    
    def __init__(self, robot):
        self.robot = robot
        self.command_history = []
        self.history_index = -1
        self.current_input = ""
        self.output_lines = [
            ">> Welcome to WRO Python Robot Control!",
            ">> Control your robot with simple Python commands:",
            "",
            ">> Quick Start:",
            "  robot.forward()     - Move forward 1 unit",
            "  robot.left()       - Turn left 90°",
            "  robot.sensor()     - Get sensor readings",
            "  robot.collect()    - Collect nearby items",
            "",
            ">> Type help() to see all commands",
            ">> Have fun programming your robot!",
            "",
            ">>> "
        ]
        self.cursor_blink = 0

        # Scroll functionality
        self.scroll_offset = 0
        self.max_visible_lines = 25  # Maximum lines visible in console
        self.line_height = 20
        
        # Create namespace for Python execution
        self.namespace = {
            'robot': robot,
            'help': self.show_help,
            'clear': self.clear_console,
            'math': math,
            'time': time
        }
    
    def show_help(self):
        """Show available commands"""
        help_text = """
>> Basic Robot Commands:
  robot.forward()            - Move forward 1 unit (default)
  robot.forward(2)           - Move forward 2 units
  robot.backward()           - Move backward 1 unit
  robot.left()               - Turn left 90° (default)
  robot.right()              - Turn right 90° (default)
  robot.left(45)             - Turn left 45°

>> Sensor Commands:
  robot.sensor()             - Get all sensor readings
  robot.front_sensor()       - Get front sensor only
  robot.left_sensor()        - Get left sensor only
  robot.right_sensor()       - Get right sensor only

>> Navigation Commands:
  robot.move_to(x, y)        - Move to coordinates (x, y)
  robot.get_position()       - Get current position
  robot.face_direction(dir)  - Face 'north', 'south', 'east', 'west'
  robot.collect()            - Collect nearby items
  robot.avoid_obstacle()     - Smart obstacle avoidance
  robot.at_target()          - Check if at target

🔧 Utility Commands:
  robot.status()             - Show robot status
  robot.undo()               - Undo last command
  robot.reset()              - Reset robot position

🎮 Console Commands:
  help()                     - Show this help
  clear()                    - Clear console

📐 Unit System:
  - 1 unit = 50 pixels (1 grid square)
  - Position (0,0) = top-left corner
  - Position (1,1) = 1 unit right, 1 unit down
  - Use robot.move_to(x, y) for precise positioning

🐍 Simple Examples:
  robot.forward()                    # Move 1 unit forward
  robot.forward(2)                   # Move 2 units forward
  robot.left(); robot.forward()      # Turn left, then move
  robot.move_to(5, 3)               # Go to position (5, 3)

🔄 Pattern Examples:
  # Draw a square
  for i in range(4): robot.forward(2); robot.right()

  # Navigate with sensors
  if robot.front_sensor() < 1: robot.left()
  else: robot.forward()
        """
        print(help_text)
        return help_text
    
    def clear_console(self):
        """Clear console output"""
        self.output_lines = ["Console cleared.", ">>> "]
        return "Console cleared"
    
    def execute_command(self, command):
        """Execute Python command"""
        if not command.strip():
            return
        
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            # Execute the command
            result = eval(command, self.namespace)
            
            # Get captured output
            output = captured_output.getvalue()
            
            # Add command to output
            self.output_lines.append(f">>> {command}")
            
            # Add any print output
            if output.strip():
                for line in output.strip().split('\n'):
                    self.output_lines.append(line)
            
            # Add result if not None
            if result is not None:
                self.output_lines.append(str(result))
                
        except Exception as e:
            self.output_lines.append(f">>> {command}")
            self.output_lines.append(f"❌ Error: {str(e)}")
            
        finally:
            sys.stdout = old_stdout
        
        # Add new prompt
        self.output_lines.append(">>> ")
        
        # Limit output lines (keep more for scrolling)
        if len(self.output_lines) > 100:
            self.output_lines = self.output_lines[-100:]

        # Auto-scroll to bottom when new content is added
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        """Scroll to the bottom of the console"""
        max_scroll = max(0, len(self.output_lines) - self.max_visible_lines)
        self.scroll_offset = max_scroll

    def handle_scroll(self, direction):
        """Handle scroll wheel input"""
        scroll_speed = 3  # Lines to scroll per wheel event

        if direction > 0:  # Scroll up
            self.scroll_offset = max(0, self.scroll_offset - scroll_speed)
        else:  # Scroll down
            max_scroll = max(0, len(self.output_lines) - self.max_visible_lines)
            self.scroll_offset = min(max_scroll, self.scroll_offset + scroll_speed)

    def handle_key(self, key, unicode_char):
        """Handle keyboard input"""
        if key == pygame.K_RETURN:
            if self.current_input.strip():
                self.execute_command(self.current_input)
                self.current_input = ""
        
        elif key == pygame.K_BACKSPACE:
            self.current_input = self.current_input[:-1]
        
        elif key == pygame.K_UP:
            if self.command_history and self.history_index > 0:
                self.history_index -= 1
                self.current_input = self.command_history[self.history_index]
        
        elif key == pygame.K_DOWN:
            if self.command_history and self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.current_input = self.command_history[self.history_index]
            else:
                self.history_index = len(self.command_history)
                self.current_input = ""

        # Scroll controls
        elif key == pygame.K_PAGEUP:
            self.handle_scroll(5)  # Scroll up

        elif key == pygame.K_PAGEDOWN:
            self.handle_scroll(-5)  # Scroll down

        elif key == pygame.K_HOME:
            self.scroll_offset = 0  # Go to top

        elif key == pygame.K_END:
            self.scroll_to_bottom()  # Go to bottom

        elif unicode_char and ord(unicode_char) >= 32:  # Printable characters
            self.current_input += unicode_char
    
    def update(self, dt):
        """Update console (for cursor blinking)"""
        self.cursor_blink += dt
    
    def draw(self, screen):
        """Draw modern console"""
        # Console background with gradient effect
        console_rect = pygame.Rect(GAME_WIDTH, 0, CONSOLE_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(screen, CONSOLE_BG, console_rect)

        # Console border
        pygame.draw.line(screen, CONSOLE_BORDER, (GAME_WIDTH, 0), (GAME_WIDTH, SCREEN_HEIGHT), 3)

        # Console header
        header_rect = pygame.Rect(GAME_WIDTH, 0, CONSOLE_WIDTH, 40)
        pygame.draw.rect(screen, CONSOLE_BORDER, header_rect)

        header_font = pygame.font.Font(None, 24)
        header_text = header_font.render("Python Console", True, CONSOLE_TEXT)
        header_rect_center = header_text.get_rect(center=(GAME_WIDTH + CONSOLE_WIDTH//2 + 10, 20))

        # Draw Python snake icon
        snake_center = (GAME_WIDTH + 25, 20)
        pygame.draw.circle(screen, GREEN, snake_center, 8)
        pygame.draw.circle(screen, WHITE, snake_center, 8, 1)
        # Snake pattern
        pygame.draw.circle(screen, WHITE, (snake_center[0] - 2, snake_center[1] - 2), 2)
        pygame.draw.circle(screen, WHITE, (snake_center[0] + 2, snake_center[1] + 2), 2)

        screen.blit(header_text, header_rect_center)

        # Console content area
        content_y_start = 50

        # Font
        font = pygame.font.Font(None, 18)

        # Calculate scrollable area
        scrollable_height = SCREEN_HEIGHT - content_y_start - 60  # Leave space for footer
        self.max_visible_lines = scrollable_height // self.line_height

        # Draw output lines with syntax highlighting and scrolling
        y_offset = content_y_start

        # Calculate which lines to show based on scroll offset
        start_line = self.scroll_offset
        end_line = min(len(self.output_lines) - 1, start_line + self.max_visible_lines)

        # Draw visible lines
        for i in range(start_line, end_line):
            line = self.output_lines[i]

            if y_offset > SCREEN_HEIGHT - 60:
                break

            # Color coding for different line types
            if line.startswith(">>>"):
                color = CONSOLE_PROMPT
            elif line.startswith(">>") or line.startswith("OK:") or line.startswith("SUCCESS:"):
                color = CONSOLE_SUCCESS
            elif line.startswith("ERROR:") or line.startswith("Error:"):
                color = CONSOLE_ERROR
            elif line.startswith("WARNING:") or line.startswith("Warning:"):
                color = CONSOLE_WARNING
            else:
                color = CONSOLE_TEXT

            # Word wrap for long lines
            if len(line) > 45:
                words = line.split(' ')
                current_line = ""
                for word in words:
                    if len(current_line + word) < 45:
                        current_line += word + " "
                    else:
                        if current_line:
                            text_surface = font.render(current_line.strip(), True, color)
                            screen.blit(text_surface, (GAME_WIDTH + 15, y_offset))
                            y_offset += self.line_height
                        current_line = word + " "

                if current_line:
                    text_surface = font.render(current_line.strip(), True, color)
                    screen.blit(text_surface, (GAME_WIDTH + 15, y_offset))
                    y_offset += self.line_height
            else:
                text_surface = font.render(line, True, color)
                screen.blit(text_surface, (GAME_WIDTH + 15, y_offset))
                y_offset += self.line_height

        # Draw current input line at bottom (always visible)
        input_y = SCREEN_HEIGHT - 55
        if self.output_lines:
            # Input background
            input_rect = pygame.Rect(GAME_WIDTH + 10, input_y - 2, CONSOLE_WIDTH - 20, 24)
            pygame.draw.rect(screen, (40, 44, 52), input_rect, border_radius=4)
            pygame.draw.rect(screen, CONSOLE_PROMPT, input_rect, 1, border_radius=4)

            prompt_line = self.output_lines[-1] + self.current_input

            # Add blinking cursor
            if self.cursor_blink % 1.0 < 0.5:
                prompt_line += "█"

            text_surface = font.render(prompt_line, True, CONSOLE_TEXT)
            screen.blit(text_surface, (GAME_WIDTH + 15, input_y))

        # Draw scroll indicator
        self.draw_scroll_indicator(screen, font)

        # Console footer with help hint
        footer_y = SCREEN_HEIGHT - 25

        # Light bulb icon
        bulb_center = (GAME_WIDTH + 25, footer_y + 8)
        pygame.draw.circle(screen, CONSOLE_WARNING, bulb_center, 6)
        pygame.draw.circle(screen, WHITE, bulb_center, 6, 1)
        # Bulb lines
        for i in range(3):
            angle = (i - 1) * 0.5
            start_x = bulb_center[0] + 8 * math.cos(angle)
            start_y = bulb_center[1] + 8 * math.sin(angle)
            end_x = bulb_center[0] + 12 * math.cos(angle)
            end_y = bulb_center[1] + 12 * math.sin(angle)
            pygame.draw.line(screen, CONSOLE_WARNING, (start_x, start_y), (end_x, end_y), 1)

        # Show different footer text based on scroll state
        if len(self.output_lines) > self.max_visible_lines:
            footer_text = font.render("Scroll: Mouse wheel, PgUp/PgDn, Home/End", True, CONSOLE_PROMPT)
        else:
            footer_text = font.render("Type help() for commands", True, CONSOLE_PROMPT)
        screen.blit(footer_text, (GAME_WIDTH + 40, footer_y))

    def draw_scroll_indicator(self, screen, _):
        """Draw scroll indicator and instructions"""
        # Only show if there's content to scroll
        if len(self.output_lines) <= self.max_visible_lines:
            return

        # Scroll bar area
        scroll_bar_x = GAME_WIDTH + CONSOLE_WIDTH - 15
        scroll_bar_y = 50
        scroll_bar_height = SCREEN_HEIGHT - 120

        # Background track
        pygame.draw.rect(screen, (60, 60, 60),
                        (scroll_bar_x, scroll_bar_y, 8, scroll_bar_height))

        # Calculate thumb position and size
        total_lines = len(self.output_lines)
        visible_ratio = self.max_visible_lines / total_lines
        thumb_height = max(20, scroll_bar_height * visible_ratio)

        scroll_ratio = self.scroll_offset / max(1, total_lines - self.max_visible_lines)
        thumb_y = scroll_bar_y + (scroll_bar_height - thumb_height) * scroll_ratio

        # Scroll thumb
        pygame.draw.rect(screen, CONSOLE_PROMPT,
                        (scroll_bar_x, thumb_y, 8, thumb_height), border_radius=4)

        # Scroll instructions (small text)
        if self.scroll_offset > 0 or len(self.output_lines) > self.max_visible_lines:
            scroll_font = pygame.font.Font(None, 14)
            scroll_text = scroll_font.render("Mouse wheel to scroll", True, (150, 150, 150))
            screen.blit(scroll_text, (GAME_WIDTH + 10, SCREEN_HEIGHT - 20))

class WROPythonControl:
    """Main application class"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("WRO Python Robot Control - Level-based Learning")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

        # Game state management
        self.game_state = "LEVEL_SELECT"  # LEVEL_SELECT, PLAYING, LEVEL_COMPLETE
        self.level_manager = LevelManager()
        self.level_select_screen = LevelSelectScreen(self.level_manager)
        self.current_level = None
        self.level_start_time = None

        # Create robot and console
        self.robot = PythonRobot()
        self.console = PythonConsole(self.robot)

        # Add level management to console namespace
        self.console.namespace['levels'] = self.level_manager
        self.console.namespace['start_level'] = self.start_level
        self.console.namespace['check_objectives'] = self.check_level_objectives

        self.running = True

    def start_level(self, level_id):
        """Start a specific level"""
        level = self.level_manager.get_level(level_id)
        if not level:
            print(f"ERROR: Level {level_id} not found")
            return

        if not self.level_manager.is_level_unlocked(level_id):
            print(f"ERROR: Level {level_id} is locked")
            return

        self.current_level = level
        self.game_state = "PLAYING"
        self.level_start_time = time.time()

        # Setup level environment
        self.setup_level_environment(level)

        # Reset robot for this level
        self.robot.reset_for_level(level)

        return f"Started Level {level_id}: {level.name}"

    def setup_level_environment(self, level):
        """Setup environment for specific level"""
        # Set obstacles from level
        self.robot.obstacles = level.obstacles.copy()

        # Set items from level
        self.robot.items = level.items.copy()

        print(f"🎮 Level environment loaded: {len(level.obstacles)} obstacles, {len(level.items)} items")

    def check_level_objectives(self):
        """Check if current level objectives are completed"""
        if not self.current_level:
            print("ERROR: No level is currently active")
            return False

        if self.current_level.is_objective_completed(self.robot):
            self.complete_level()
            return True
        else:
            # Show progress
            self.show_level_progress()
            return False

    def complete_level(self):
        """Complete current level"""
        if not self.current_level:
            return

        # Calculate score and time
        time_taken = time.time() - self.level_start_time
        score = self.calculate_level_score(time_taken)

        # Mark level as completed
        self.level_manager.complete_level(self.current_level.level_id, score, time_taken)

        print(f"🎉 LEVEL {self.current_level.level_id} COMPLETED!")
        print(f"⏱️  Time: {time_taken:.1f} seconds")
        print(f"⭐ Score: {score}")
        print(f"🤖 Commands used: {self.robot.commands_executed}")
        print(f"📡 Sensor calls: {self.robot.sensor_calls}")

        # Check if next level is unlocked
        next_level = self.current_level.level_id + 1
        if next_level in self.level_manager.levels:
            print(f"🔓 Level {next_level} unlocked!")

        self.game_state = "LEVEL_COMPLETE"

    def calculate_level_score(self, time_taken):
        """Calculate score based on performance"""
        base_score = 100

        # Time bonus (faster = better)
        time_bonus = max(0, 50 - int(time_taken))

        # Efficiency bonus (fewer commands = better)
        efficiency_bonus = max(0, 20 - self.robot.commands_executed)

        # Sensor usage bonus (using sensors = better)
        sensor_bonus = min(10, self.robot.sensor_calls * 2)

        total_score = base_score + time_bonus + efficiency_bonus + sensor_bonus
        return total_score

    def show_level_progress(self):
        """Show current level progress"""
        level = self.current_level
        print(f"📊 Level {level.level_id} Progress:")

        for i, objective in enumerate(level.objectives):
            completed = level._check_objective(objective, self.robot)
            status = "✅" if completed else "❌"
            obj_type = objective.get('type', 'unknown')

            if obj_type == 'reach_target':
                target = objective.get('target')
                print(f"  {status} Reach target position {target}")
            elif obj_type == 'collect_items':
                required = objective.get('count', 1)
                current = self.robot.items_collected
                print(f"  {status} Collect items: {current}/{required}")
            elif obj_type == 'use_sensors':
                required = objective.get('sensor_calls', 1)
                current = self.robot.sensor_calls
                print(f"  {status} Use sensors: {current}/{required}")
            elif obj_type == 'efficient_path':
                max_commands = objective.get('max_commands', 10)
                current = self.robot.commands_executed
                print(f"  {status} Efficient path: {current}/{max_commands} commands")

    def setup_environment(self):
        """Setup obstacles and items"""
        # Add obstacles
        self.robot.obstacles = [
            {'x': 200, 'y': 150, 'width': 80, 'height': 60},
            {'x': 400, 'y': 300, 'width': 100, 'height': 50},
            {'x': 600, 'y': 100, 'width': 60, 'height': 120},
            {'x': 300, 'y': 500, 'width': 120, 'height': 40}
        ]
        
        # Add collectible items
        self.robot.items = [
            {'x': 150, 'y': 250, 'type': 'coin'},
            {'x': 350, 'y': 200, 'type': 'coin'},
            {'x': 550, 'y': 400, 'type': 'coin'},
            {'x': 750, 'y': 300, 'type': 'coin'},
            {'x': 450, 'y': 450, 'type': 'coin'}
        ]
    
    def handle_events(self):
        """Handle pygame events based on game state"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "PLAYING":
                        self.game_state = "LEVEL_SELECT"
                    else:
                        self.running = False

                elif self.game_state == "LEVEL_SELECT":
                    # Handle level selection
                    selected_level = self.level_select_screen.handle_key(event.key)
                    if selected_level:
                        self.start_level(selected_level)

                elif self.game_state == "PLAYING":
                    # Handle game input
                    if event.key == pygame.K_F1:
                        # Quick objective check
                        self.check_level_objectives()
                    else:
                        # Pass key to console
                        self.console.handle_key(event.key, event.unicode)

                elif self.game_state == "LEVEL_COMPLETE":
                    # Any key to return to level select
                    self.game_state = "LEVEL_SELECT"

            elif event.type == pygame.MOUSEWHEEL and self.game_state == "PLAYING":
                # Handle mouse wheel for console scrolling
                mouse_x, _ = pygame.mouse.get_pos()
                # Check if mouse is over console area
                if mouse_x >= GAME_WIDTH:
                    self.console.handle_scroll(event.y)
    
    def update(self, dt):
        """Update game state"""
        self.robot.update(dt)
        self.console.update(dt)
    
    def draw(self):
        """Draw everything based on game state"""
        if self.game_state == "LEVEL_SELECT":
            self.level_select_screen.draw(self.screen)

        elif self.game_state == "PLAYING":
            self.draw_game()

        elif self.game_state == "LEVEL_COMPLETE":
            self.draw_level_complete()

        pygame.display.flip()

    def draw_game(self):
        """Draw the main game screen"""
        # Clear screen with modern background
        self.screen.fill(BACKGROUND)

        # Draw game area background
        game_rect = pygame.Rect(0, 0, GAME_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, game_rect)

        # Draw grid lines
        self.draw_grid()
        
        # Draw obstacles with modern styling
        for obstacle in self.robot.obstacles:
            # Main obstacle
            pygame.draw.rect(self.screen, OBSTACLE_COLOR,
                           (obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']))
            # Subtle border
            pygame.draw.rect(self.screen, BLACK,
                           (obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']), 1)
            # Inner highlight for 3D effect
            pygame.draw.rect(self.screen, WHITE,
                           (obstacle['x']+1, obstacle['y']+1, obstacle['width']-2, obstacle['height']-2), 1)

        # Draw items with glow effect
        for item in self.robot.items:
            # Glow effect
            for i in range(3):
                glow_size = 15 - i * 2
                glow_alpha = 50 - i * 15
                glow_surface = pygame.Surface((glow_size*2, glow_size*2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*ITEM_COLOR, glow_alpha), (glow_size, glow_size), glow_size)
                self.screen.blit(glow_surface, (int(item['x']) - glow_size, int(item['y']) - glow_size))

            # Main item
            pygame.draw.circle(self.screen, ITEM_COLOR, (int(item['x']), int(item['y'])), 10)
            pygame.draw.circle(self.screen, WHITE, (int(item['x']), int(item['y'])), 10, 2)
        
        # Draw target area with modern styling
        target_rect = pygame.Rect(GAME_WIDTH - 150, SCREEN_HEIGHT - 150, 100, 100)

        # Target background with gradient effect
        target_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(target_surface, (*TARGET_COLOR, 100), (0, 0, 100, 100))
        self.screen.blit(target_surface, (GAME_WIDTH - 150, SCREEN_HEIGHT - 150))

        # Target border
        pygame.draw.rect(self.screen, TARGET_COLOR, target_rect, 3)

        # Target text with background
        target_text = self.font.render("TARGET", True, WHITE)
        text_rect = target_text.get_rect(center=(GAME_WIDTH - 100, SCREEN_HEIGHT - 100))

        # Text background
        bg_rect = text_rect.inflate(8, 4)
        pygame.draw.rect(self.screen, TARGET_COLOR, bg_rect)
        pygame.draw.rect(self.screen, WHITE, bg_rect, 1)

        self.screen.blit(target_text, text_rect)
        
        # Draw robot
        self.draw_robot()
        
        # Draw sensor beams
        self.draw_sensors()
        
        # Draw HUD
        self.draw_hud()
        
        # Draw console
        self.console.draw(self.screen)

        # Draw level info overlay
        if self.current_level:
            self.draw_level_info()

    def draw_level_complete(self):
        """Draw level completion screen"""
        self.screen.fill(BLACK)

        # Title
        title_text = pygame.font.Font(None, 48).render("🎉 LEVEL COMPLETED!", True, CONSOLE_SUCCESS)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title_text, title_rect)

        if self.current_level:
            # Level info
            level_text = pygame.font.Font(None, 32).render(f"Level {self.current_level.level_id}: {self.current_level.name}", True, WHITE)
            level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, 200))
            self.screen.blit(level_text, level_rect)

            # Stats
            time_taken = time.time() - self.level_start_time if self.level_start_time else 0
            score = self.calculate_level_score(time_taken)

            stats = [
                f"⏱️  Time: {time_taken:.1f} seconds",
                f"⭐ Score: {score}",
                f"🤖 Commands: {self.robot.commands_executed}",
                f"📡 Sensors: {self.robot.sensor_calls}"
            ]

            for i, stat in enumerate(stats):
                stat_text = pygame.font.Font(None, 24).render(stat, True, CONSOLE_TEXT)
                stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH//2, 280 + i * 30))
                self.screen.blit(stat_text, stat_rect)

        # Instructions
        instruction_text = pygame.font.Font(None, 24).render("Press any key to continue", True, CONSOLE_PROMPT)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100))
        self.screen.blit(instruction_text, instruction_rect)

    def draw_level_info(self):
        """Draw current level information overlay"""
        if not self.current_level:
            return

        # Level info panel
        panel_width = 250
        panel_height = 120
        panel_x = GAME_WIDTH - panel_width - 10
        panel_y = 10

        # Semi-transparent background
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(200)
        panel_surface.fill((40, 40, 40))
        self.screen.blit(panel_surface, (panel_x, panel_y))

        # Border
        pygame.draw.rect(self.screen, CONSOLE_BORDER, (panel_x, panel_y, panel_width, panel_height), 2)

        # Level info
        font_small = pygame.font.Font(None, 18)
        font_medium = pygame.font.Font(None, 20)

        # Title
        title_text = font_medium.render(f"Level {self.current_level.level_id}: {self.current_level.name}", True, WHITE)
        self.screen.blit(title_text, (panel_x + 10, panel_y + 10))

        # Difficulty
        stars = "⭐" * self.current_level.difficulty
        diff_text = font_small.render(f"Difficulty: {stars}", True, CONSOLE_WARNING)
        self.screen.blit(diff_text, (panel_x + 10, panel_y + 30))

        # Time
        if self.level_start_time:
            elapsed = time.time() - self.level_start_time
            time_text = font_small.render(f"Time: {elapsed:.1f}s", True, CONSOLE_TEXT)
            self.screen.blit(time_text, (panel_x + 10, panel_y + 50))

        # Commands
        cmd_text = font_small.render(f"Commands: {self.robot.commands_executed}", True, CONSOLE_TEXT)
        self.screen.blit(cmd_text, (panel_x + 10, panel_y + 70))

        # Quick help
        help_text = font_small.render("F1: Check objectives", True, CONSOLE_PROMPT)
        self.screen.blit(help_text, (panel_x + 10, panel_y + 90))

    def draw_grid(self):
        """Draw modern grid lines for better visualization"""
        grid_size = 50  # 50 pixel grid

        # Light grid lines
        for x in range(0, GAME_WIDTH, grid_size):
            pygame.draw.line(self.screen, GRID_LIGHT, (x, 0), (x, SCREEN_HEIGHT), 1)

        for y in range(0, SCREEN_HEIGHT, grid_size):
            pygame.draw.line(self.screen, GRID_LIGHT, (0, y), (GAME_WIDTH, y), 1)

        # Major grid lines every 100 pixels
        for x in range(0, GAME_WIDTH, 100):
            pygame.draw.line(self.screen, GRID_MAJOR, (x, 0), (x, SCREEN_HEIGHT), 1)

            # Add coordinate labels
            if x > 0:
                coord_text = self.font.render(str(x//50), True, GRID_MAJOR)
                text_rect = coord_text.get_rect()

                # Background for text
                bg_rect = text_rect.inflate(4, 2)
                bg_rect.topleft = (x + 2, 5)
                pygame.draw.rect(self.screen, WHITE, bg_rect)
                pygame.draw.rect(self.screen, GRID_MAJOR, bg_rect, 1)

                self.screen.blit(coord_text, (x + 4, 6))

        for y in range(0, SCREEN_HEIGHT, 100):
            pygame.draw.line(self.screen, GRID_MAJOR, (0, y), (GAME_WIDTH, y), 1)

            # Add coordinate labels
            if y > 0:
                coord_text = self.font.render(str(y//50), True, GRID_MAJOR)
                text_rect = coord_text.get_rect()

                # Background for text
                bg_rect = text_rect.inflate(4, 2)
                bg_rect.topleft = (5, y + 2)
                pygame.draw.rect(self.screen, WHITE, bg_rect)
                pygame.draw.rect(self.screen, GRID_MAJOR, bg_rect, 1)

                self.screen.blit(coord_text, (6, y + 3))

        # Draw origin marker with modern styling
        pygame.draw.circle(self.screen, RED, (0, 0), 4)
        pygame.draw.circle(self.screen, WHITE, (0, 0), 4, 1)

        origin_text = self.font.render("(0,0)", True, WHITE)
        text_rect = origin_text.get_rect()
        bg_rect = text_rect.inflate(6, 4)
        bg_rect.topleft = (8, 8)

        pygame.draw.rect(self.screen, RED, bg_rect)
        pygame.draw.rect(self.screen, WHITE, bg_rect, 1)
        self.screen.blit(origin_text, (10, 9))

    def draw_robot(self):
        """Draw robot with modern styling and coordinates"""
        robot_x, robot_y = int(self.robot.x), int(self.robot.y)

        # Robot shadow for depth
        shadow_offset = 3
        pygame.draw.circle(self.screen, (0, 0, 0, 50),
                          (robot_x + shadow_offset, robot_y + shadow_offset), self.robot.size)

        # Robot body with gradient effect
        pygame.draw.circle(self.screen, ROBOT_COLOR, (robot_x, robot_y), self.robot.size)
        pygame.draw.circle(self.screen, WHITE, (robot_x, robot_y), self.robot.size, 2)

        # Inner circle for 3D effect
        inner_size = self.robot.size - 6
        pygame.draw.circle(self.screen, (255, 255, 255, 100), (robot_x, robot_y), inner_size)

        # Direction indicator with arrow
        angle_rad = math.radians(self.robot.angle)
        arrow_length = self.robot.size - 5
        end_x = self.robot.x + arrow_length * math.cos(angle_rad)
        end_y = self.robot.y + arrow_length * math.sin(angle_rad)

        # Arrow shaft
        pygame.draw.line(self.screen, ROBOT_DIRECTION, (self.robot.x, self.robot.y), (end_x, end_y), 4)

        # Arrow head
        arrow_size = 8
        left_angle = angle_rad + 2.5
        right_angle = angle_rad - 2.5

        left_x = end_x - arrow_size * math.cos(left_angle)
        left_y = end_y - arrow_size * math.sin(left_angle)
        right_x = end_x - arrow_size * math.cos(right_angle)
        right_y = end_y - arrow_size * math.sin(right_angle)

        pygame.draw.polygon(self.screen, ROBOT_DIRECTION, [(end_x, end_y), (left_x, left_y), (right_x, right_y)])

        # Robot coordinates with modern styling
        pos_x = round(self.robot.x / 50, 1)
        pos_y = round(self.robot.y / 50, 1)
        coord_text = f"({pos_x}, {pos_y})"

        text_surface = self.font.render(coord_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.robot.x, self.robot.y - self.robot.size - 20))

        # Modern text background
        bg_rect = text_rect.inflate(12, 6)
        pygame.draw.rect(self.screen, ROBOT_COLOR, bg_rect, border_radius=8)
        pygame.draw.rect(self.screen, WHITE, bg_rect, 1, border_radius=8)

        self.screen.blit(text_surface, text_rect)
    
    def draw_sensors(self):
        """Draw modern sensor beams with visual effects"""
        sensors = [('front', 0), ('left', -90), ('right', 90)]

        for _, angle_offset in sensors:
            distance_units = self.robot.get_distance_to_obstacle(angle_offset)
            distance_pixels = distance_units * 50  # Convert to pixels for drawing
            angle = math.radians(self.robot.angle + angle_offset)

            end_x = self.robot.x + distance_pixels * math.cos(angle)
            end_y = self.robot.y + distance_pixels * math.sin(angle)

            # Color based on distance (in units)
            if distance_units < 1:
                color = RED
                beam_width = 3
            elif distance_units < 2:
                color = ORANGE
                beam_width = 2
            else:
                color = GREEN
                beam_width = 1

            # Main beam with transparency
            pygame.draw.line(self.screen, color, (self.robot.x, self.robot.y), (end_x, end_y), beam_width)

            # Beam endpoint indicator
            pygame.draw.circle(self.screen, color, (int(end_x), int(end_y)), 4)
            pygame.draw.circle(self.screen, WHITE, (int(end_x), int(end_y)), 4, 1)

            # Distance label
            if distance_units < 3:  # Only show label for close objects
                dist_text = f"{distance_units:.1f}"
                text_surface = pygame.font.Font(None, 20).render(dist_text, True, WHITE)
                text_rect = text_surface.get_rect(center=(end_x, end_y - 15))

                # Text background
                bg_rect = text_rect.inflate(6, 4)
                pygame.draw.rect(self.screen, color, bg_rect, border_radius=4)
                pygame.draw.rect(self.screen, WHITE, bg_rect, 1, border_radius=4)

                self.screen.blit(text_surface, text_rect)
    
    def draw_hud(self):
        """Draw modern heads-up display"""
        # Convert position to units
        pos_x = round(self.robot.x / 50, 1)
        pos_y = round(self.robot.y / 50, 1)

        # HUD background
        hud_width = 220
        hud_height = 140
        hud_surface = pygame.Surface((hud_width, hud_height), pygame.SRCALPHA)
        hud_surface.fill((*HUD_BG, 220))  # Add alpha for transparency

        # HUD border
        pygame.draw.rect(hud_surface, HUD_BORDER, (0, 0, hud_width, hud_height), 2, border_radius=10)

        # HUD items with text icons
        hud_items = [
            ("star", f"Score: {self.robot.score}", PURPLE),
            ("diamond", f"Items: {self.robot.items_collected}", ITEM_COLOR),
            ("lightning", f"Commands: {self.robot.commands_executed}", BLUE),
            ("location", f"Position: ({pos_x}, {pos_y})", ROBOT_COLOR),
            ("compass", f"Angle: {self.robot.angle:.0f}°", GREEN)
        ]

        for i, (icon_type, text, color) in enumerate(hud_items):
            y_pos = 15 + i * 22

            # Icon background circle
            icon_center = (18, y_pos + 9)
            pygame.draw.circle(hud_surface, color, icon_center, 12)
            pygame.draw.circle(hud_surface, WHITE, icon_center, 12, 1)

            # Draw custom icon
            if icon_type == "star":
                IconRenderer.draw_star(hud_surface, icon_center, 7, WHITE)
            elif icon_type == "diamond":
                IconRenderer.draw_diamond(hud_surface, icon_center, 6, WHITE)
            elif icon_type == "lightning":
                IconRenderer.draw_lightning(hud_surface, icon_center, 8, WHITE)
            elif icon_type == "location":
                IconRenderer.draw_location(hud_surface, icon_center, 8, WHITE)
            elif icon_type == "compass":
                IconRenderer.draw_compass(hud_surface, icon_center, 8, WHITE)

            # Text
            text_surface = pygame.font.Font(None, 20).render(text, True, HUD_TEXT)
            hud_surface.blit(text_surface, (38, y_pos))

        # Blit HUD to main screen
        self.screen.blit(hud_surface, (10, 10))
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()

def main():
    app = WROPythonControl()
    app.run()

if __name__ == "__main__":
    main()
