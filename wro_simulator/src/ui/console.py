"""
Python Console UI Component
"""

import pygame
import math
import sys
import time
from io import StringIO
from ..core.constants import *
from .icon_manager import icon_manager


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
        self.max_visible_lines = MAX_VISIBLE_CONSOLE_LINES
        self.line_height = CONSOLE_LINE_HEIGHT
        
        # Create namespace for Python execution
        self.namespace = {
            'robot': robot,
            'help': self.show_help,
            'clear': self.clear_console,
            'math': math,
            'time': time
        }
    
    def execute_command(self, command):
        """Execute Python command and capture output"""
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Add command to output
        self.output_lines.append(f">>> {command}")
        
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            # Execute the command
            result = eval(command, self.namespace)
            if result is not None:
                print(result)
        except:
            try:
                exec(command, self.namespace)
            except Exception as e:
                print(f"ERROR: {e}")
        
        # Restore stdout and get output
        sys.stdout = old_stdout
        output = captured_output.getvalue()
        
        # Add output to console
        if output.strip():
            for line in output.strip().split('\n'):
                self.output_lines.append(line)

        # Add new prompt for next command
        self.output_lines.append(">>> ")

        # Limit output lines and auto-scroll
        if len(self.output_lines) > MAX_OUTPUT_LINES:
            self.output_lines = self.output_lines[-MAX_OUTPUT_LINES:]

        self.scroll_to_bottom()
    
    def show_help(self):
        """Show help information"""
        help_text = """
>> Basic Robot Commands:
  robot.forward()           - Move forward 1 unit
  robot.forward(distance)   - Move forward specified distance
  robot.backward()          - Move backward 1 unit
  robot.left()              - Turn left 90° (default)
  robot.right()             - Turn right 90° (default)
  robot.left(45)            - Turn left 45°

>> Sensor Commands:
  robot.sensor()            - Get all sensor readings
  robot.front_sensor()      - Get front sensor only
  robot.left_sensor()       - Get left sensor only
  robot.right_sensor()      - Get right sensor only

>> Navigation Commands:
  robot.move_to(x, y)       - Move to coordinates (x, y)
  robot.get_position()      - Get current position
  robot.face_direction(dir) - Face 'north', 'south', 'east', 'west'
  robot.collect()           - Collect nearby items
  robot.avoid_obstacle()    - Smart obstacle avoidance

>> Utility Commands:
  help()                    - Show this help
  clear()                   - Clear console
  robot.reset()             - Reset robot position

>> Level Commands:
  check_objectives()        - Check current level progress
  start_level(n)           - Start level n (if unlocked)

>> Programming Tips:
  - Use loops: for i in range(4): robot.forward()
  - Use conditions: if robot.front_sensor() < 1: robot.left()
  - Define functions: def square(): ...
  - Check position: x, y = robot.get_position()
"""
        print(help_text)
    
    def clear_console(self):
        """Clear console output"""
        self.output_lines = [">>> "]
        self.scroll_offset = 0
        print("Console cleared")
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the console"""
        max_scroll = max(0, len(self.output_lines) - self.max_visible_lines)
        self.scroll_offset = max_scroll
    
    def handle_scroll(self, direction):
        """Handle scroll wheel input"""
        scroll_speed = 3
        
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
            self.handle_scroll(5)
        elif key == pygame.K_PAGEDOWN:
            self.handle_scroll(-5)
        elif key == pygame.K_HOME:
            self.scroll_offset = 0
        elif key == pygame.K_END:
            self.scroll_to_bottom()
        
        elif unicode_char and ord(unicode_char) >= 32:  # Printable characters
            self.current_input += unicode_char
    
    def update(self, dt):
        """Update console (for cursor blinking)"""
        self.cursor_blink += dt
    
    def draw(self, screen):
        """Draw modern console (offset by sidebar)"""
        console_x = SIDEBAR_WIDTH + GAME_WIDTH

        # Console background
        console_rect = pygame.Rect(console_x, 0, CONSOLE_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(screen, CONSOLE_BG, console_rect)

        # Console border
        pygame.draw.line(screen, CONSOLE_BORDER, (console_x, 0), (console_x, SCREEN_HEIGHT), 3)
        
        # Console header
        header_rect = pygame.Rect(console_x, 0, CONSOLE_WIDTH, 40)
        pygame.draw.rect(screen, CONSOLE_BORDER, header_rect)

        header_font = pygame.font.Font(None, 24)
        header_text = header_font.render("Python Console", True, CONSOLE_TEXT)
        header_rect_center = header_text.get_rect(center=(console_x + CONSOLE_WIDTH//2 + 10, 20))

        # Draw Python snake icon
        snake_center = (console_x + 25, 20)
        pygame.draw.circle(screen, GREEN, snake_center, 8)
        pygame.draw.circle(screen, WHITE, snake_center, 8, 1)
        pygame.draw.circle(screen, WHITE, (snake_center[0] - 2, snake_center[1] - 2), 2)
        pygame.draw.circle(screen, WHITE, (snake_center[0] + 2, snake_center[1] + 2), 2)
        
        screen.blit(header_text, header_rect_center)
        
        # Console content
        self.draw_console_content(screen, console_x)

        # Console footer
        self.draw_console_footer(screen, console_x)
    
    def draw_console_content(self, screen, console_x):
        """Draw console content with scrolling"""
        content_y_start = 50
        scrollable_height = SCREEN_HEIGHT - content_y_start - 60
        self.max_visible_lines = scrollable_height // self.line_height
        
        font = pygame.font.Font(None, 18)
        y_offset = content_y_start
        
        # Calculate visible lines (exclude the last line if it's a prompt)
        total_lines = len(self.output_lines)
        if total_lines > 0 and self.output_lines[-1].strip() == ">>>":
            # Don't show the last line if it's just a prompt
            display_lines = total_lines - 1
        else:
            display_lines = total_lines

        start_line = self.scroll_offset
        end_line = min(display_lines, start_line + self.max_visible_lines)

        # Draw visible lines
        for i in range(start_line, end_line):
            line = self.output_lines[i]
            
            if y_offset > SCREEN_HEIGHT - 60:
                break
            
            # Color coding
            if line.startswith(">>>"):
                color = CONSOLE_PROMPT
            elif line.startswith(">>") or line.startswith("OK:"):
                color = CONSOLE_SUCCESS
            elif line.startswith("ERROR:"):
                color = CONSOLE_ERROR
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
                            screen.blit(text_surface, (console_x + 15, y_offset))
                            y_offset += self.line_height
                        current_line = word + " "
                
                if current_line:
                    text_surface = font.render(current_line.strip(), True, color)
                    screen.blit(text_surface, (console_x + 15, y_offset))
                    y_offset += self.line_height
            else:
                text_surface = font.render(line, True, color)
                screen.blit(text_surface, (console_x + 15, y_offset))
                y_offset += self.line_height
        
        # Draw current input line at bottom
        input_y = SCREEN_HEIGHT - 55
        input_rect = pygame.Rect(console_x + 10, input_y - 2, CONSOLE_WIDTH - 20, 24)
        pygame.draw.rect(screen, (40, 44, 52), input_rect, border_radius=4)
        pygame.draw.rect(screen, CONSOLE_PROMPT, input_rect, 1, border_radius=4)

        # Always use ">>> " as prompt, regardless of output_lines content
        prompt_line = ">>> " + self.current_input

        # Add blinking cursor
        if self.cursor_blink % 1.0 < 0.5:
            prompt_line += "█"

        text_surface = font.render(prompt_line, True, CONSOLE_TEXT)
        screen.blit(text_surface, (console_x + 15, input_y))
        
        # Draw scroll indicator
        self.draw_scroll_indicator(screen, console_x)
    
    def draw_scroll_indicator(self, screen, console_x):
        """Draw scroll indicator"""
        if len(self.output_lines) <= self.max_visible_lines:
            return

        # Scroll bar
        scroll_bar_x = console_x + CONSOLE_WIDTH - 15
        scroll_bar_y = 50
        scroll_bar_height = SCREEN_HEIGHT - 120
        
        # Background track
        pygame.draw.rect(screen, (60, 60, 60), (scroll_bar_x, scroll_bar_y, 8, scroll_bar_height))
        
        # Calculate thumb
        total_lines = len(self.output_lines)
        visible_ratio = self.max_visible_lines / total_lines
        thumb_height = max(20, scroll_bar_height * visible_ratio)
        
        scroll_ratio = self.scroll_offset / max(1, total_lines - self.max_visible_lines)
        thumb_y = scroll_bar_y + (scroll_bar_height - thumb_height) * scroll_ratio
        
        # Scroll thumb
        pygame.draw.rect(screen, CONSOLE_PROMPT, (scroll_bar_x, thumb_y, 8, thumb_height), border_radius=4)
    
    def draw_console_footer(self, screen, console_x):
        """Draw console footer"""
        footer_y = SCREEN_HEIGHT - 25
        font = pygame.font.Font(None, 18)

        # Info icon using Font Awesome
        icon_manager.draw_icon(screen, 'info', (console_x + 25, footer_y + 8), size=12, color=CONSOLE_WARNING)
        
        # Footer text
        if len(self.output_lines) > self.max_visible_lines:
            footer_text = font.render("Scroll: Mouse wheel, PgUp/PgDn, Home/End", True, CONSOLE_PROMPT)
        else:
            footer_text = font.render("Type help() for commands", True, CONSOLE_PROMPT)
        screen.blit(footer_text, (console_x + 40, footer_y))
