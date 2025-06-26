"""
Sidebar UI Component for Robot Status and Level Info
"""

import pygame
import time
from ..core.constants import *


class Sidebar:
    """Beautiful sidebar for robot status and level information"""
    
    def __init__(self):
        self.font_large = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 20)
        self.font_small = pygame.font.Font(None, 16)
        
    def draw(self, screen, robot, current_level, level_start_time):
        """Draw the complete sidebar"""
        # Sidebar background
        sidebar_rect = pygame.Rect(0, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
        
        # Gradient background
        self.draw_gradient_background(screen, sidebar_rect)
        
        # Sidebar border
        pygame.draw.line(screen, (100, 100, 120), (SIDEBAR_WIDTH, 0), (SIDEBAR_WIDTH, SCREEN_HEIGHT), 2)
        
        # Draw sections
        y_offset = 20
        
        # Robot status section
        y_offset = self.draw_robot_status(screen, robot, y_offset)
        y_offset += 20
        
        # Level info section
        if current_level:
            y_offset = self.draw_level_info(screen, current_level, level_start_time, y_offset)
            y_offset += 20
        
        # Objectives section
        if current_level:
            y_offset = self.draw_objectives(screen, current_level, robot, y_offset)
            y_offset += 20
        
        # Controls help section
        self.draw_controls_help(screen, y_offset)
    
    def draw_gradient_background(self, screen, rect):
        """Draw gradient background for sidebar"""
        for y in range(rect.height):
            ratio = y / rect.height
            r = int(25 * (1 - ratio) + 35 * ratio)
            g = int(30 * (1 - ratio) + 40 * ratio)
            b = int(45 * (1 - ratio) + 55 * ratio)
            color = (r, g, b)
            pygame.draw.line(screen, color, (rect.x, rect.y + y), (rect.x + rect.width, rect.y + y))
    
    def draw_section_header(self, screen, title, y, icon=None):
        """Draw section header with icon"""
        # Header background
        header_rect = pygame.Rect(10, y, SIDEBAR_WIDTH - 20, 25)
        pygame.draw.rect(screen, (50, 60, 80), header_rect, border_radius=5)
        pygame.draw.rect(screen, (100, 120, 160), header_rect, 1, border_radius=5)
        
        # Icon
        if icon:
            icon_text = self.font_medium.render(icon, True, (150, 200, 255))
            screen.blit(icon_text, (15, y + 3))
            title_x = 35
        else:
            title_x = 15
        
        # Title
        title_text = self.font_medium.render(title, True, WHITE)
        screen.blit(title_text, (title_x, y + 3))
        
        return y + 30
    
    def draw_robot_status(self, screen, robot, y_start):
        """Draw robot status section"""
        y = self.draw_section_header(screen, "Robot Status", y_start, "🤖")
        
        # Status items
        status_items = [
            ("Position", f"({robot.x/UNIT_SIZE:.1f}, {robot.y/UNIT_SIZE:.1f})", (100, 200, 255)),
            ("Angle", f"{robot.angle:.1f}°", (150, 255, 150)),
            ("Score", str(robot.score), (255, 215, 0)),
            ("Items", str(robot.items_collected), (255, 150, 100)),
            ("Commands", str(robot.commands_executed), (200, 150, 255)),
            ("Sensors", str(robot.sensor_calls), (150, 255, 200))
        ]
        
        for label, value, color in status_items:
            y = self.draw_status_item(screen, label, value, color, y)
        
        return y
    
    def draw_status_item(self, screen, label, value, color, y):
        """Draw individual status item"""
        # Label
        label_text = self.font_small.render(f"{label}:", True, (200, 200, 200))
        screen.blit(label_text, (15, y))
        
        # Value with color
        value_text = self.font_small.render(str(value), True, color)
        value_rect = value_text.get_rect()
        screen.blit(value_text, (SIDEBAR_WIDTH - value_rect.width - 15, y))
        
        return y + 18
    
    def draw_level_info(self, screen, level, level_start_time, y_start):
        """Draw level information section"""
        y = self.draw_section_header(screen, f"Level {level.level_id}", y_start, "🎯")
        
        # Level name
        name_text = self.font_small.render(level.name, True, (150, 200, 255))
        screen.blit(name_text, (15, y))
        y += 18
        
        # Difficulty stars
        stars = "⭐" * level.difficulty
        diff_text = self.font_small.render(f"Difficulty: {stars}", True, (255, 215, 0))
        screen.blit(diff_text, (15, y))
        y += 18
        
        # Time
        if level_start_time:
            elapsed = time.time() - level_start_time
            time_text = self.font_small.render(f"Time: {elapsed:.1f}s", True, (200, 200, 200))
            screen.blit(time_text, (15, y))
            y += 18
        
        # Description (wrapped)
        desc_words = level.description.split()
        line = ""
        for word in desc_words:
            test_line = line + word + " "
            if len(test_line) > 22:  # Wrap at ~22 characters
                if line:
                    desc_text = self.font_small.render(line.strip(), True, (180, 180, 180))
                    screen.blit(desc_text, (15, y))
                    y += 16
                line = word + " "
            else:
                line = test_line
        
        if line:
            desc_text = self.font_small.render(line.strip(), True, (180, 180, 180))
            screen.blit(desc_text, (15, y))
            y += 16
        
        return y
    
    def draw_objectives(self, screen, level, robot, y_start):
        """Draw objectives section"""
        y = self.draw_section_header(screen, "Objectives", y_start, "📋")
        
        progress = level.get_progress(robot)
        
        # Progress bar
        completed = progress['completed_objectives']
        total = progress['total_objectives']
        
        # Progress text
        progress_text = self.font_small.render(f"Progress: {completed}/{total}", True, (200, 200, 200))
        screen.blit(progress_text, (15, y))
        y += 18
        
        # Progress bar
        bar_width = SIDEBAR_WIDTH - 30
        bar_height = 8
        bar_rect = pygame.Rect(15, y, bar_width, bar_height)
        
        # Background
        pygame.draw.rect(screen, (60, 60, 60), bar_rect, border_radius=4)
        
        # Progress fill
        if total > 0:
            fill_width = int((completed / total) * bar_width)
            if fill_width > 0:
                fill_rect = pygame.Rect(15, y, fill_width, bar_height)
                pygame.draw.rect(screen, (100, 255, 100), fill_rect, border_radius=4)
        
        y += 20
        
        # Individual objectives
        for obj_status in progress['objectives_status']:
            status_icon = "✅" if obj_status['completed'] else "⏳"
            
            # Objective text (wrapped)
            obj_text = f"{status_icon} {obj_status['description']}"
            words = obj_text.split()
            line = ""
            
            for word in words:
                test_line = line + word + " "
                if len(test_line) > 20:  # Wrap objectives text
                    if line:
                        color = (150, 255, 150) if obj_status['completed'] else (200, 200, 200)
                        text_surface = self.font_small.render(line.strip(), True, color)
                        screen.blit(text_surface, (15, y))
                        y += 16
                    line = word + " "
                else:
                    line = test_line
            
            if line:
                color = (150, 255, 150) if obj_status['completed'] else (200, 200, 200)
                text_surface = self.font_small.render(line.strip(), True, color)
                screen.blit(text_surface, (15, y))
                y += 16
            
            y += 5  # Small gap between objectives
        
        return y
    
    def draw_controls_help(self, screen, y_start):
        """Draw controls help section"""
        y = self.draw_section_header(screen, "Quick Help", y_start, "💡")
        
        help_items = [
            "F1: Programming Guide",
            "F2: Check objectives",
            "ESC: Back to menu",
            "Mouse wheel: Scroll console",
            "",
            "Robot Commands:",
            "robot.forward()",
            "robot.left()",
            "robot.right()",
            "robot.sensor()",
            "robot.collect()",
            "",
            "help() for more info"
        ]
        
        for item in help_items:
            if item == "":
                y += 8  # Small gap
                continue
                
            if item.startswith("robot."):
                color = (150, 200, 255)  # Blue for commands
            elif item.endswith(":"):
                color = (255, 200, 150)  # Orange for categories
            else:
                color = (180, 180, 180)  # Gray for normal text
            
            help_text = self.font_small.render(item, True, color)
            screen.blit(help_text, (15, y))
            y += 14
        
        return y
