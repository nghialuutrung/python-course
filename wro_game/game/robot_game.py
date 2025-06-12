#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WRO Robot Game - Main Game Logic
Main class managing WRO Practice game
"""

import pygame
import sys
from typing import Dict, List, Tuple
from enum import Enum

# Try to import clipboard support
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    print("pyperclip not available - using internal clipboard only")

# Import required modules
from .levels.level_1_basic_movement import Level1BasicMovement

class GameState(Enum):
    MENU = "menu"
    LEVEL_SELECT = "level_select"
    PLAYING = "playing"
    CODE_EDITOR = "code_editor"
    RESULTS = "results"
    INSTRUCTIONS = "instructions"

class WROGameManager:
    """Main class managing WRO Practice game"""

    def __init__(self):
        """Initialize game manager"""
        # Screen settings
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("WRO Game Practice - Robotics Training")
        
        # Colors
        self.COLORS = {
            'WHITE': (255, 255, 255),
            'BLACK': (0, 0, 0),
            'BLUE': (0, 100, 200),
            'GREEN': (0, 200, 0),
            'RED': (200, 0, 0),
            'YELLOW': (255, 255, 0),
            'GRAY': (128, 128, 128),
            'LIGHT_GRAY': (200, 200, 200),
            'DARK_BLUE': (0, 50, 100),
            'PURPLE': (128, 0, 128)
        }
        
        # Font with fallback system
        self.fonts = self.setup_fonts()
        
        # Game state
        self.current_state = GameState.MENU
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Level data
        self.levels = [
            {"name": "Level 1: Basic Movement", "description": "Learn how to control robot", "unlocked": True},
            {"name": "Level 2: Line Following", "description": "Robot follows a straight line", "unlocked": False},
            {"name": "Level 3: Obstacle Avoidance", "description": "Avoid obstacles", "unlocked": False},
            {"name": "Level 4: Color Sorting", "description": "Sort by colors", "unlocked": False},
            {"name": "Level 5: WRO Challenge", "description": "Comprehensive challenge", "unlocked": False}
        ]
        
        self.current_level = 0
        self.player_progress = {"completed_levels": [], "current_score": 0}

        # Advanced code editor state
        self.current_code = ""
        self.code_lines = []
        self.cursor_line = 0
        self.cursor_pos = 0
        self.code_input_active = False
        self.blink_timer = 0

        # Text selection
        self.selection_start_line = -1
        self.selection_start_pos = -1
        self.selection_end_line = -1
        self.selection_end_pos = -1
        self.selecting = False

        # Undo/Redo system
        self.undo_stack = []
        self.redo_stack = []
        self.max_undo_steps = 50

        # Clipboard
        self.clipboard = ""
        self.clipboard_feedback = ""
        self.clipboard_feedback_timer = 0

        # Syntax highlighting colors
        self.syntax_colors = {
            'keyword': (0, 0, 255),      # Blue for keywords
            'string': (0, 128, 0),       # Green for strings
            'comment': (128, 128, 128),  # Gray for comments
            'function': (128, 0, 128),   # Purple for functions
            'normal': (0, 0, 0)          # Black for normal text
        }

        # Current level instance
        self.current_level_instance = None

        # Code editor state (back to original implementation)
        self.code_lines = ["# Write your Python code here", "robot.move_forward()"]
        self.cursor_line = 1
        self.cursor_pos = len(self.code_lines[1])
        self.code_input_active = False
        self.selecting = False
        self.selection_start = None
        self.selection_end = None
        self.undo_stack = []
        self.redo_stack = []

    def setup_fonts(self):
        """Setup fonts with fallback system"""
        # Try to use system fonts that support more characters
        font_names = [
            'Arial',
            'DejaVu Sans',
            'Liberation Sans',
            'Helvetica',
            'sans-serif'
        ]

        fonts = {}

        # Try each font name until one works
        for font_name in font_names:
            try:
                fonts = {
                    'title': pygame.font.SysFont(font_name, 48),
                    'subtitle': pygame.font.SysFont(font_name, 32),
                    'normal': pygame.font.SysFont(font_name, 24),
                    'small': pygame.font.SysFont(font_name, 18)
                }
                break
            except:
                continue

        # Fallback to default pygame font if no system font works
        if not fonts:
            fonts = {
                'title': pygame.font.Font(None, 48),
                'subtitle': pygame.font.Font(None, 32),
                'normal': pygame.font.Font(None, 24),
                'small': pygame.font.Font(None, 18)
            }

        return fonts
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            self.handle_events()

            # Update game logic
            self.update()

            # Render graphics
            self.render()

            # Control frame rate
            self.clock.tick(60)
    
    def handle_events(self):
        """Handle user events"""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_state == GameState.CODE_EDITOR:
                        self.close_code_editor()
                    elif self.current_state != GameState.MENU:
                        self.current_state = GameState.MENU
                    else:
                        self.running = False
                elif self.current_state == GameState.PLAYING:
                    self.handle_playing_keys(event.key)
                elif self.current_state == GameState.CODE_EDITOR:
                    self.handle_code_editor_keys(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.current_state == GameState.CODE_EDITOR:
                    self.selecting = False

            elif event.type == pygame.MOUSEMOTION:
                if self.current_state == GameState.CODE_EDITOR and self.selecting:
                    self.handle_mouse_drag(event.pos)
    
    def handle_mouse_click(self, pos: Tuple[int, int]):
        """Handle mouse clicks"""
        x, y = pos

        if self.current_state == GameState.MENU:
            self.handle_menu_click(x, y)
        elif self.current_state == GameState.LEVEL_SELECT:
            self.handle_level_select_click(x, y)
        elif self.current_state == GameState.PLAYING:
            self.handle_playing_click(x, y)
        elif self.current_state == GameState.INSTRUCTIONS:
            self.handle_instructions_click(x, y)
        elif self.current_state == GameState.CODE_EDITOR:
            self.handle_code_editor_click(x, y)
    
    def handle_menu_click(self, x: int, y: int):
        """Handle clicks in main menu"""
        # "Start Game" button
        if 450 <= x <= 750 and 300 <= y <= 350:
            self.current_state = GameState.LEVEL_SELECT

        # "Instructions" button
        elif 450 <= x <= 750 and 370 <= y <= 420:
            self.show_instructions()

        # "Exit" button
        elif 450 <= x <= 750 and 440 <= y <= 490:
            self.running = False
    
    def handle_level_select_click(self, x: int, y: int):
        """Xử lý click trong màn hình chọn level"""
        # Back button
        if 50 <= x <= 150 and 50 <= y <= 90:
            self.current_state = GameState.MENU
            return
        
        # Level buttons
        for i, level in enumerate(self.levels):
            button_y = 200 + i * 80
            if 300 <= x <= 900 and button_y <= y <= button_y + 60:
                if level["unlocked"]:
                    self.current_level = i
                    self.start_level(i)
    
    def start_level(self, level_index: int):
        """Start a level"""
        print(f"Starting {self.levels[level_index]['name']}")

        # Create corresponding level instance
        if level_index == 0:  # Level 1: Basic Movement
            self.current_level_instance = Level1BasicMovement(self.SCREEN_WIDTH - 200, self.SCREEN_HEIGHT - 150)

        self.current_state = GameState.PLAYING
    
    def handle_playing_keys(self, key):
        """Handle keys in playing mode"""
        if key == pygame.K_c:  # Open code editor
            self.open_code_editor()
        elif key == pygame.K_r:  # Reset level
            if self.current_level_instance:
                self.current_level_instance.reset()

    def handle_playing_click(self, x: int, y: int):
        """Handle clicks in playing mode"""
        # Back button
        if 50 <= x <= 150 and 50 <= y <= 90:
            self.current_state = GameState.LEVEL_SELECT

        # Code Editor button
        elif 200 <= x <= 350 and 50 <= y <= 90:
            self.open_code_editor()

        # Reset button
        elif 370 <= x <= 470 and 50 <= y <= 90:
            if self.current_level_instance:
                self.current_level_instance.reset()

        # Grid toggle button
        elif 490 <= x <= 570 and 50 <= y <= 90:
            if hasattr(self.current_level_instance, 'show_grid'):
                self.current_level_instance.show_grid = not self.current_level_instance.show_grid

        # Hints toggle button
        elif 580 <= x <= 660 and 50 <= y <= 90:
            if hasattr(self.current_level_instance, 'show_path_hints'):
                self.current_level_instance.show_path_hints = not self.current_level_instance.show_path_hints

    def open_code_editor(self):
        """Open code editor"""
        self.current_state = GameState.CODE_EDITOR

    def close_code_editor(self):
        """Close code editor and return to playing"""
        self.current_state = GameState.PLAYING

    def execute_user_code(self, code: str):
        """Execute user code"""
        if self.current_level_instance:
            success, message = self.current_level_instance.execute_code(code)
            print(f"User code execution: {message}")
            if success:
                print("✅ Code executed successfully!")
            else:
                print(f"❌ Error: {message}")

    def handle_instructions_click(self, x: int, y: int):
        """Handle clicks in instructions screen"""
        # Back button
        if 50 <= x <= 150 and 50 <= y <= 90:
            self.current_state = GameState.MENU

    def handle_code_editor_click(self, x: int, y: int):
        """Handle clicks in code editor screen"""
        # Run Code button
        if 50 <= x <= 170 and 540 <= y <= 580:
            if self.current_level_instance and self.code_lines:
                user_code = '\n'.join(self.code_lines)
                success, message = self.current_level_instance.execute_code(user_code)
                print(f"User code execution: {message}")

        # Reset button
        elif 180 <= x <= 280 and 540 <= y <= 580:
            if self.current_level_instance:
                self.current_level_instance.reset()

        # Sample button
        elif 290 <= x <= 390 and 540 <= y <= 580:
            if self.current_level_instance:
                self.save_undo_state()
                sample_code = self.current_level_instance.get_sample_code()
                self.code_lines = sample_code.split('\n')
                self.cursor_line = len(self.code_lines) - 1
                self.cursor_pos = len(self.code_lines[self.cursor_line]) if self.code_lines else 0
                self.code_input_active = True
                self.clear_selection()

        # Save button
        elif 400 <= x <= 480 and 540 <= y <= 580:
            if self.code_lines:
                self.save_code_to_file()
                print("Code saved to file!")

        # Back button
        elif 50 <= x <= 150 and 700 <= y <= 740:
            self.current_state = GameState.PLAYING

        # Click on code input area to activate
        elif 50 <= x <= 550 and 320 <= y <= 520:
            self.code_input_active = True

            # Initialize code_lines if empty
            if not self.code_lines:
                if self.current_level_instance:
                    sample_code = self.current_level_instance.get_sample_code()
                    self.code_lines = sample_code.split('\n')
                else:
                    self.code_lines = ["# Write your code here", "robot.move_forward()"]

            # Clear previous selection
            self.clear_selection()

            # Calculate which line was clicked
            line_number_width = 40
            line_clicked = (y - 330) // 20
            if line_clicked < len(self.code_lines):
                self.cursor_line = line_clicked
                # Estimate cursor position based on x coordinate
                clicked_x = x - (50 + line_number_width + 10)
                if clicked_x > 0:
                    line_text = self.code_lines[self.cursor_line]
                    # Rough estimation of character position
                    char_width = 7  # Approximate character width
                    self.cursor_pos = min(len(line_text), max(0, clicked_x // char_width))
                else:
                    self.cursor_pos = 0
            else:
                # Clicked below existing lines, add to end
                self.cursor_line = len(self.code_lines) - 1
                self.cursor_pos = len(self.code_lines[self.cursor_line])

            # Start selection for potential drag
            self.selection_start_line = self.cursor_line
            self.selection_start_pos = self.cursor_pos
            self.selecting = True

        # Click outside to deactivate
        else:
            self.code_input_active = False
            self.clear_selection()

    def handle_mouse_drag(self, pos):
        """Handle mouse drag for text selection"""
        x, y = pos
        line_number_width = 40

        # Check if dragging in code area
        if 50 + line_number_width <= x <= 550 and 320 <= y <= 520:
            # Calculate which line was dragged to
            line_clicked = (y - 330) // 20
            if line_clicked < len(self.code_lines):
                self.selection_end_line = line_clicked
                # Estimate cursor position based on x coordinate
                clicked_x = x - (50 + line_number_width + 10)
                if clicked_x > 0:
                    line_text = self.code_lines[line_clicked]
                    # Rough estimation of character position
                    char_width = 7  # Approximate character width
                    self.selection_end_pos = min(len(line_text), max(0, clicked_x // char_width))
                else:
                    self.selection_end_pos = 0
            else:
                # Dragged below existing lines
                self.selection_end_line = len(self.code_lines) - 1
                self.selection_end_pos = len(self.code_lines[self.selection_end_line])

    def save_undo_state(self):
        """Save current state for undo"""
        state = {
            'code_lines': [line for line in self.code_lines],
            'cursor_line': self.cursor_line,
            'cursor_pos': self.cursor_pos
        }
        self.undo_stack.append(state)
        if len(self.undo_stack) > self.max_undo_steps:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def undo(self):
        """Undo last action"""
        if self.undo_stack:
            # Save current state to redo stack
            current_state = {
                'code_lines': [line for line in self.code_lines],
                'cursor_line': self.cursor_line,
                'cursor_pos': self.cursor_pos
            }
            self.redo_stack.append(current_state)

            # Restore previous state
            state = self.undo_stack.pop()
            self.code_lines = state['code_lines']
            self.cursor_line = state['cursor_line']
            self.cursor_pos = state['cursor_pos']

    def redo(self):
        """Redo last undone action"""
        if self.redo_stack:
            # Save current state to undo stack
            current_state = {
                'code_lines': [line for line in self.code_lines],
                'cursor_line': self.cursor_line,
                'cursor_pos': self.cursor_pos
            }
            self.undo_stack.append(current_state)

            # Restore next state
            state = self.redo_stack.pop()
            self.code_lines = state['code_lines']
            self.cursor_line = state['cursor_line']
            self.cursor_pos = state['cursor_pos']

    def clear_selection(self):
        """Clear text selection"""
        self.selection_start_line = -1
        self.selection_start_pos = -1
        self.selection_end_line = -1
        self.selection_end_pos = -1
        self.selecting = False

    def has_selection(self):
        """Check if there's an active selection"""
        return (self.selection_start_line >= 0 and self.selection_start_pos >= 0 and
                self.selection_end_line >= 0 and self.selection_end_pos >= 0)

    def get_selected_text(self):
        """Get currently selected text"""
        if not self.has_selection():
            return ""

        start_line = min(self.selection_start_line, self.selection_end_line)
        end_line = max(self.selection_start_line, self.selection_end_line)
        start_pos = self.selection_start_pos if self.selection_start_line <= self.selection_end_line else self.selection_end_pos
        end_pos = self.selection_end_pos if self.selection_start_line <= self.selection_end_line else self.selection_start_pos

        if start_line == end_line:
            return self.code_lines[start_line][start_pos:end_pos]

        result = []
        for i in range(start_line, end_line + 1):
            if i == start_line:
                result.append(self.code_lines[i][start_pos:])
            elif i == end_line:
                result.append(self.code_lines[i][:end_pos])
            else:
                result.append(self.code_lines[i])

        return '\n'.join(result)

    def delete_selected_text(self):
        """Delete currently selected text"""
        if not self.has_selection():
            return

        self.save_undo_state()

        start_line = min(self.selection_start_line, self.selection_end_line)
        end_line = max(self.selection_start_line, self.selection_end_line)
        start_pos = self.selection_start_pos if self.selection_start_line <= self.selection_end_line else self.selection_end_pos
        end_pos = self.selection_end_pos if self.selection_start_line <= self.selection_end_line else self.selection_start_pos

        if start_line == end_line:
            # Single line selection
            line = self.code_lines[start_line]
            self.code_lines[start_line] = line[:start_pos] + line[end_pos:]
            self.cursor_line = start_line
            self.cursor_pos = start_pos
        else:
            # Multi-line selection
            start_part = self.code_lines[start_line][:start_pos]
            end_part = self.code_lines[end_line][end_pos:]

            # Remove lines in between
            for _ in range(end_line - start_line):
                del self.code_lines[start_line + 1]

            # Combine start and end parts
            self.code_lines[start_line] = start_part + end_part
            self.cursor_line = start_line
            self.cursor_pos = start_pos

        self.clear_selection()

    def insert_text(self, text):
        """Insert text at cursor position"""
        lines = text.split('\n')
        if len(lines) == 1:
            # Single line insert
            line = self.code_lines[self.cursor_line]
            self.code_lines[self.cursor_line] = line[:self.cursor_pos] + text + line[self.cursor_pos:]
            self.cursor_pos += len(text)
        else:
            # Multi-line insert
            current_line = self.code_lines[self.cursor_line]
            before_cursor = current_line[:self.cursor_pos]
            after_cursor = current_line[self.cursor_pos:]

            # First line
            self.code_lines[self.cursor_line] = before_cursor + lines[0]

            # Insert middle lines
            for i, line in enumerate(lines[1:-1], 1):
                self.code_lines.insert(self.cursor_line + i, line)

            # Last line
            if len(lines) > 1:
                self.code_lines.insert(self.cursor_line + len(lines) - 1, lines[-1] + after_cursor)
                self.cursor_line += len(lines) - 1
                self.cursor_pos = len(lines[-1])

    def handle_code_editor_keys(self, event):
        """Handle keyboard input in code editor"""
        if not self.code_input_active:
            return

        # Initialize code_lines if empty
        if not self.code_lines:
            if self.current_level_instance:
                sample_code = self.current_level_instance.get_sample_code()
                self.code_lines = sample_code.split('\n')
            else:
                self.code_lines = ["# Write your code here", "robot.move_forward()"]
            self.cursor_line = 0
            self.cursor_pos = 0

        # Ensure cursor is within bounds
        if self.cursor_line >= len(self.code_lines):
            self.cursor_line = len(self.code_lines) - 1
        if self.cursor_line < 0:
            self.cursor_line = 0
        if self.cursor_pos > len(self.code_lines[self.cursor_line]):
            self.cursor_pos = len(self.code_lines[self.cursor_line])
        if self.cursor_pos < 0:
            self.cursor_pos = 0

        # Check for modifier keys
        keys = pygame.key.get_pressed()
        ctrl_pressed = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        # Handle Ctrl combinations first
        if ctrl_pressed:
            if event.key == pygame.K_z and not shift_pressed:
                self.undo()
                return
            elif event.key == pygame.K_y or (event.key == pygame.K_z and shift_pressed):
                self.redo()
                return
            elif event.key == pygame.K_c:
                if self.has_selection():
                    selected_text = self.get_selected_text()
                    self.clipboard = selected_text
                    # Try to copy to system clipboard
                    if CLIPBOARD_AVAILABLE:
                        try:
                            pyperclip.copy(selected_text)
                            self.clipboard_feedback = f"✅ Copied {len(selected_text)} chars to clipboard"
                        except:
                            self.clipboard_feedback = "⚠️ Copied to internal clipboard only"
                    else:
                        self.clipboard_feedback = "📋 Copied to internal clipboard"
                    self.clipboard_feedback_timer = 180  # Show for 3 seconds at 60fps
                return
            elif event.key == pygame.K_x:
                if self.has_selection():
                    selected_text = self.get_selected_text()
                    self.clipboard = selected_text
                    # Try to copy to system clipboard
                    if CLIPBOARD_AVAILABLE:
                        try:
                            pyperclip.copy(selected_text)
                            self.clipboard_feedback = f"✂️ Cut {len(selected_text)} chars to clipboard"
                        except:
                            self.clipboard_feedback = "⚠️ Cut to internal clipboard only"
                    else:
                        self.clipboard_feedback = "✂️ Cut to internal clipboard"
                    self.clipboard_feedback_timer = 180
                    self.delete_selected_text()
                return
            elif event.key == pygame.K_v:
                # Try to get from system clipboard first
                paste_text = self.clipboard
                from_system = False

                if CLIPBOARD_AVAILABLE:
                    try:
                        system_clipboard = pyperclip.paste()
                        if system_clipboard and system_clipboard.strip():
                            paste_text = system_clipboard
                            from_system = True
                    except:
                        pass

                if paste_text:
                    self.save_undo_state()
                    if self.has_selection():
                        self.delete_selected_text()
                    self.insert_text(paste_text)

                    # Show feedback
                    source = "system" if from_system else "internal"
                    self.clipboard_feedback = f"📋 Pasted {len(paste_text)} chars from {source} clipboard"
                    self.clipboard_feedback_timer = 180
                else:
                    self.clipboard_feedback = "❌ Nothing to paste"
                    self.clipboard_feedback_timer = 120
                return
            elif event.key == pygame.K_a:
                # Select all
                self.selection_start_line = 0
                self.selection_start_pos = 0
                self.selection_end_line = len(self.code_lines) - 1
                self.selection_end_pos = len(self.code_lines[-1])
                return

        # Handle selection with Shift + Arrow keys
        if shift_pressed and not self.selecting:
            self.selection_start_line = self.cursor_line
            self.selection_start_pos = self.cursor_pos
            self.selecting = True
        elif not shift_pressed and self.selecting:
            self.clear_selection()

        if event.key == pygame.K_RETURN:
            # Enter key - new line
            self.save_undo_state()
            if self.has_selection():
                self.delete_selected_text()

            current_line = self.code_lines[self.cursor_line]
            new_line = current_line[self.cursor_pos:]
            self.code_lines[self.cursor_line] = current_line[:self.cursor_pos]
            self.code_lines.insert(self.cursor_line + 1, new_line)
            self.cursor_line += 1
            self.cursor_pos = 0

        elif event.key == pygame.K_BACKSPACE:
            # Backspace
            if self.has_selection():
                self.delete_selected_text()
            else:
                self.save_undo_state()
                if self.cursor_pos > 0:
                    line = self.code_lines[self.cursor_line]
                    self.code_lines[self.cursor_line] = line[:self.cursor_pos-1] + line[self.cursor_pos:]
                    self.cursor_pos -= 1
                elif self.cursor_line > 0:
                    # Join with previous line
                    prev_line = self.code_lines[self.cursor_line - 1]
                    current_line = self.code_lines[self.cursor_line]
                    self.cursor_pos = len(prev_line)
                    self.code_lines[self.cursor_line - 1] = prev_line + current_line
                    del self.code_lines[self.cursor_line]
                    self.cursor_line -= 1

        elif event.key == pygame.K_DELETE:
            # Delete key
            if self.has_selection():
                self.delete_selected_text()
            else:
                self.save_undo_state()
                line = self.code_lines[self.cursor_line]
                if self.cursor_pos < len(line):
                    self.code_lines[self.cursor_line] = line[:self.cursor_pos] + line[self.cursor_pos+1:]
                elif self.cursor_line < len(self.code_lines) - 1:
                    # Join with next line
                    next_line = self.code_lines[self.cursor_line + 1]
                    self.code_lines[self.cursor_line] = line + next_line
                    del self.code_lines[self.cursor_line + 1]

        elif event.key == pygame.K_UP:
            # Arrow up
            if self.cursor_line > 0:
                self.cursor_line -= 1
                self.cursor_pos = min(self.cursor_pos, len(self.code_lines[self.cursor_line]))
                if shift_pressed and self.selecting:
                    self.selection_end_line = self.cursor_line
                    self.selection_end_pos = self.cursor_pos

        elif event.key == pygame.K_DOWN:
            # Arrow down
            if self.cursor_line < len(self.code_lines) - 1:
                self.cursor_line += 1
                self.cursor_pos = min(self.cursor_pos, len(self.code_lines[self.cursor_line]))
                if shift_pressed and self.selecting:
                    self.selection_end_line = self.cursor_line
                    self.selection_end_pos = self.cursor_pos

        elif event.key == pygame.K_LEFT:
            # Arrow left
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
            elif self.cursor_line > 0:
                self.cursor_line -= 1
                self.cursor_pos = len(self.code_lines[self.cursor_line])
            if shift_pressed and self.selecting:
                self.selection_end_line = self.cursor_line
                self.selection_end_pos = self.cursor_pos

        elif event.key == pygame.K_RIGHT:
            # Arrow right
            if self.cursor_pos < len(self.code_lines[self.cursor_line]):
                self.cursor_pos += 1
            elif self.cursor_line < len(self.code_lines) - 1:
                self.cursor_line += 1
                self.cursor_pos = 0
            if shift_pressed and self.selecting:
                self.selection_end_line = self.cursor_line
                self.selection_end_pos = self.cursor_pos

        else:
            # Regular character input
            if event.unicode and event.unicode.isprintable():
                self.save_undo_state()
                if self.has_selection():
                    self.delete_selected_text()

                line = self.code_lines[self.cursor_line]
                self.code_lines[self.cursor_line] = line[:self.cursor_pos] + event.unicode + line[self.cursor_pos:]
                self.cursor_pos += 1

    def get_syntax_highlighting(self, line):
        """Get syntax highlighting for a line of code"""
        tokens = []
        i = 0
        current_token = ""
        current_color = self.syntax_colors['normal']

        # Keywords to highlight
        keywords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'import', 'from', 'return']
        robot_functions = ['robot.move_forward', 'robot.move_backward', 'robot.turn_left', 'robot.turn_right', 'robot.stop']

        while i < len(line):
            char = line[i]

            if char == '#':
                # Comment - rest of line
                if current_token:
                    tokens.append((current_token, current_color))
                    current_token = ""
                tokens.append((line[i:], self.syntax_colors['comment']))
                break
            elif char == '"' or char == "'":
                # String literal
                if current_token:
                    tokens.append((current_token, current_color))
                    current_token = ""

                quote = char
                string_token = char
                i += 1
                while i < len(line) and line[i] != quote:
                    string_token += line[i]
                    i += 1
                if i < len(line):
                    string_token += line[i]

                tokens.append((string_token, self.syntax_colors['string']))
                i += 1
                continue
            elif char.isalnum() or char == '_' or char == '.':
                current_token += char
            else:
                if current_token:
                    # Check if token is a keyword or function
                    if current_token in keywords:
                        color = self.syntax_colors['keyword']
                    elif any(current_token.startswith(func) for func in robot_functions):
                        color = self.syntax_colors['function']
                    else:
                        color = self.syntax_colors['normal']

                    tokens.append((current_token, color))
                    current_token = ""

                if char != ' ':
                    tokens.append((char, self.syntax_colors['normal']))
                else:
                    tokens.append((char, self.syntax_colors['normal']))

            i += 1

        # Handle remaining token
        if current_token:
            if current_token in keywords:
                color = self.syntax_colors['keyword']
            elif any(current_token.startswith(func) for func in robot_functions):
                color = self.syntax_colors['function']
            else:
                color = self.syntax_colors['normal']
            tokens.append((current_token, color))

        return tokens

    def save_code_to_file(self):
        """Save current code to a file"""
        try:
            import os
            save_dir = "saved_code"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # Generate filename with timestamp
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{save_dir}/level_{self.current_level}_code_{timestamp}.py"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.code_lines))

            print(f"Code saved to: {filename}")
            return True
        except Exception as e:
            print(f"Error saving code: {e}")
            return False

    def load_code_from_file(self, filename):
        """Load code from a file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()

            self.save_undo_state()
            self.code_lines = content.split('\n')
            self.cursor_line = 0
            self.cursor_pos = 0
            self.clear_selection()
            return True
        except Exception as e:
            print(f"Error loading code: {e}")
            return False

    def show_instructions(self):
        """Show game instructions"""
        self.current_state = GameState.INSTRUCTIONS
    
    def update(self):
        """Update game logic"""
        if self.current_state == GameState.PLAYING and self.current_level_instance:
            self.current_level_instance.update()

            # Check if level is completed
            if self.current_level_instance.is_completed():
                # Unlock next level
                if self.current_level + 1 < len(self.levels):
                    self.levels[self.current_level + 1]["unlocked"] = True

                # Add to completed list
                if self.current_level not in self.player_progress["completed_levels"]:
                    self.player_progress["completed_levels"].append(self.current_level)
                    self.player_progress["current_score"] += 100
    
    def render(self):
        """Render graphics"""
        self.screen.fill(self.COLORS['WHITE'])
        
        if self.current_state == GameState.MENU:
            self.render_menu()
        elif self.current_state == GameState.LEVEL_SELECT:
            self.render_level_select()
        elif self.current_state == GameState.PLAYING:
            self.render_playing()
        elif self.current_state == GameState.CODE_EDITOR:
            self.render_code_editor()
        elif self.current_state == GameState.INSTRUCTIONS:
            self.render_instructions()
        
        pygame.display.flip()
    
    def render_menu(self):
        """Render main menu"""
        # Title
        title_text = self.fonts['title'].render("WRO Game Practice", True, self.COLORS['DARK_BLUE'])
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH//2, 150))
        self.screen.blit(title_text, title_rect)

        # Subtitle
        subtitle_text = self.fonts['subtitle'].render("Robotics Programming Practice", True, self.COLORS['BLUE'])
        subtitle_rect = subtitle_text.get_rect(center=(self.SCREEN_WIDTH//2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Buttons
        buttons = [
            ("Start Game", 300),
            ("Instructions", 370),
            ("Exit", 440)
        ]

        for text, y in buttons:
            self.draw_button(text, 450, y, 300, 50, self.COLORS['BLUE'], self.COLORS['WHITE'])
    
    def render_level_select(self):
        """Render level selection screen"""
        # Title
        title_text = self.fonts['title'].render("Select Level", True, self.COLORS['DARK_BLUE'])
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)

        # Back button
        self.draw_button("< Back", 50, 50, 100, 40, self.COLORS['GRAY'], self.COLORS['WHITE'])
        
        # Level buttons
        for i, level in enumerate(self.levels):
            y = 200 + i * 80
            color = self.COLORS['GREEN'] if level["unlocked"] else self.COLORS['GRAY']
            
            self.draw_button(level["name"], 300, y, 600, 60, color, self.COLORS['WHITE'])
            
            # Description
            desc_text = self.fonts['small'].render(level["description"], True, self.COLORS['BLACK'])
            self.screen.blit(desc_text, (320, y + 35))

    def render_playing(self):
        """Render game playing screen"""
        if not self.current_level_instance:
            return

        # Draw level
        # Add DARK_GREEN color if not exists
        if 'DARK_GREEN' not in self.COLORS:
            self.COLORS['DARK_GREEN'] = (0, 150, 0)

        self.current_level_instance.draw(self.screen, self.COLORS)

        # Control panel
        # Back button
        self.draw_button("< Back", 50, 50, 100, 40, self.COLORS['GRAY'], self.COLORS['WHITE'])

        # Code Editor button
        self.draw_button("[CODE] Editor", 200, 50, 150, 40, self.COLORS['BLUE'], self.COLORS['WHITE'])

        # Reset button
        self.draw_button("[RESET]", 370, 50, 100, 40, self.COLORS['RED'], self.COLORS['WHITE'])

        # Visualization toggle buttons
        if hasattr(self.current_level_instance, 'show_grid'):
            grid_color = self.COLORS['GREEN'] if self.current_level_instance.show_grid else self.COLORS['GRAY']
            self.draw_button("[GRID]", 490, 50, 80, 40, grid_color, self.COLORS['WHITE'])

        if hasattr(self.current_level_instance, 'show_path_hints'):
            hints_color = self.COLORS['GREEN'] if self.current_level_instance.show_path_hints else self.COLORS['GRAY']
            self.draw_button("[HINTS]", 580, 50, 80, 40, hints_color, self.COLORS['WHITE'])

        # Instructions
        instructions_text = [
            "🎮 Controls:",
            "C - Code Editor",
            "R - Reset Level",
            "[GRID] - Toggle grid lines",
            "[HINTS] - Toggle path hints",
            "ESC - Back to menu"
        ]

        for i, text in enumerate(instructions_text):
            text_surface = self.fonts['small'].render(text, True, self.COLORS['BLACK'])
            self.screen.blit(text_surface, (self.SCREEN_WIDTH - 200, 100 + i * 20))

        # Score
        score_text = f"Score: {self.player_progress['current_score']}"
        score_surface = self.fonts['normal'].render(score_text, True, self.COLORS['BLACK'])
        self.screen.blit(score_surface, (self.SCREEN_WIDTH - 200, 200))
    
    def render_code_editor(self):
        """Render code editor screen"""
        # Title
        title_text = self.fonts['subtitle'].render(f"Code Editor - {self.levels[self.current_level]['name']}", True, self.COLORS['DARK_BLUE'])
        self.screen.blit(title_text, (50, 50))

        # Instructions area
        pygame.draw.rect(self.screen, self.COLORS['LIGHT_GRAY'], (50, 100, 500, 200))
        pygame.draw.rect(self.screen, self.COLORS['BLACK'], (50, 100, 500, 200), 2)

        if self.current_level_instance:
            instructions = self.current_level_instance.get_instructions()
            for i, line in enumerate(instructions[:8]):  # Show first 8 lines
                if i < 8:
                    text_surface = self.fonts['small'].render(line[:60], True, self.COLORS['BLACK'])  # Limit line length
                    self.screen.blit(text_surface, (60, 110 + i * 20))

        # Code area with line numbers
        line_number_width = 40
        code_bg_color = self.COLORS['WHITE'] if self.code_input_active else self.COLORS['LIGHT_GRAY']

        # Line number area
        pygame.draw.rect(self.screen, (240, 240, 240), (50, 320, line_number_width, 200))
        pygame.draw.rect(self.screen, self.COLORS['GRAY'], (50 + line_number_width - 1, 320, 1, 200))

        # Code area
        pygame.draw.rect(self.screen, code_bg_color, (50 + line_number_width, 320, 500 - line_number_width, 200))
        border_color = self.COLORS['BLUE'] if self.code_input_active else self.COLORS['BLACK']
        pygame.draw.rect(self.screen, border_color, (50, 320, 500, 200), 3 if self.code_input_active else 2)

        # Initialize code_lines if empty
        if not self.code_lines and self.current_level_instance:
            sample_code = self.current_level_instance.get_sample_code()
            self.code_lines = sample_code.split('\n')
            self.cursor_line = len(self.code_lines) - 1
            self.cursor_pos = len(self.code_lines[self.cursor_line]) if self.code_lines else 0

        # Display editable code with syntax highlighting
        for i, line in enumerate(self.code_lines[:8]):  # Show first 8 lines
            y_pos = 330 + i * 20

            # Line number
            line_num_text = str(i + 1).rjust(2)
            line_num_surface = self.fonts['small'].render(line_num_text, True, self.COLORS['GRAY'])
            self.screen.blit(line_num_surface, (55, y_pos))

            # Highlight current line
            if i == self.cursor_line and self.code_input_active:
                pygame.draw.rect(self.screen, (240, 240, 255), (50 + line_number_width, y_pos - 2, 500 - line_number_width, 18))

            # Draw selection background
            if self.has_selection():
                start_line = min(self.selection_start_line, self.selection_end_line)
                end_line = max(self.selection_start_line, self.selection_end_line)
                if start_line <= i <= end_line:
                    start_pos = 0
                    end_pos = len(line)

                    if i == start_line and i == end_line:
                        start_pos = min(self.selection_start_pos, self.selection_end_pos)
                        end_pos = max(self.selection_start_pos, self.selection_end_pos)
                    elif i == start_line:
                        start_pos = self.selection_start_pos if self.selection_start_line <= self.selection_end_line else self.selection_end_pos
                    elif i == end_line:
                        end_pos = self.selection_end_pos if self.selection_start_line <= self.selection_end_line else self.selection_start_pos

                    if start_pos < end_pos:
                        start_x = self.fonts['small'].size(line[:start_pos])[0] if start_pos > 0 else 0
                        end_x = self.fonts['small'].size(line[:end_pos])[0] if end_pos > 0 else 0
                        pygame.draw.rect(self.screen, (173, 216, 230),
                                       (50 + line_number_width + 10 + start_x, y_pos - 2, end_x - start_x, 18))

            # Render line text with syntax highlighting
            tokens = self.get_syntax_highlighting(line[:60])
            x_offset = 50 + line_number_width + 10

            for token, color in tokens:
                if token:
                    text_surface = self.fonts['small'].render(token, True, color)
                    self.screen.blit(text_surface, (x_offset, y_pos))
                    x_offset += self.fonts['small'].size(token)[0]

            # Draw cursor
            if i == self.cursor_line and self.code_input_active:
                # Calculate cursor position
                cursor_text = line[:self.cursor_pos]
                cursor_width = self.fonts['small'].size(cursor_text)[0] if cursor_text else 0

                # Blink cursor
                self.blink_timer += 1
                if self.blink_timer % 60 < 30:  # Blink every 30 frames
                    pygame.draw.line(self.screen, self.COLORS['BLACK'],
                                   (50 + line_number_width + 10 + cursor_width, y_pos),
                                   (50 + line_number_width + 10 + cursor_width, y_pos + 16), 2)

        # Simulation area
        pygame.draw.rect(self.screen, self.COLORS['WHITE'], (600, 100, 550, 420))
        pygame.draw.rect(self.screen, self.COLORS['BLACK'], (600, 100, 550, 420), 2)

        # Draw level in simulation area if available
        if self.current_level_instance:
            # Save current screen area
            original_screen = self.screen
            # Create a subsurface for the simulation area
            sim_surface = self.screen.subsurface((600, 100, 550, 420))
            # Temporarily set the screen to the simulation area
            self.screen = sim_surface
            # Draw the level
            self.current_level_instance.draw(sim_surface, self.COLORS)
            # Restore original screen
            self.screen = original_screen
        else:
            sim_text = self.fonts['normal'].render("Simulation Area", True, self.COLORS['BLACK'])
            self.screen.blit(sim_text, (750, 300))

        # Control buttons
        self.draw_button("[RUN] Code", 50, 540, 120, 40, self.COLORS['GREEN'], self.COLORS['WHITE'])
        self.draw_button("[RESET]", 180, 540, 100, 40, self.COLORS['RED'], self.COLORS['WHITE'])
        self.draw_button("[SAMPLE]", 290, 540, 100, 40, self.COLORS['BLUE'], self.COLORS['WHITE'])
        self.draw_button("[SAVE]", 400, 540, 80, 40, self.COLORS['PURPLE'], self.COLORS['WHITE'])
        self.draw_button("< Back", 50, 700, 100, 40, self.COLORS['GRAY'], self.COLORS['WHITE'])

        # Instructions
        if self.code_input_active:
            info_text = "✏️ EDITING: Type code, Shift+Arrows=Select, Ctrl+C/V/X=Copy/Paste/Cut, Ctrl+Z/Y=Undo/Redo"
        else:
            info_text = "👆 Click in code area to edit. [SAMPLE] for example. Line numbers & syntax highlighting enabled!"
        text_surface = self.fonts['small'].render(info_text[:95], True, self.COLORS['BLACK'])
        self.screen.blit(text_surface, (50, 600))

        # Additional help
        help_text = "📝 Commands: robot.move_forward(), robot.turn_left(), robot.turn_right(), robot.move_backward()"
        help_surface = self.fonts['small'].render(help_text[:95], True, self.COLORS['GRAY'])
        self.screen.blit(help_surface, (50, 620))

        # Show current line info and selection when editing
        if self.code_input_active and self.code_lines:
            line_info = f"Line {self.cursor_line + 1}/{len(self.code_lines)}, Col {self.cursor_pos + 1}"
            if self.has_selection():
                line_info += f" | Selection: {len(self.get_selected_text())} chars"
            if len(self.undo_stack) > 0:
                line_info += f" | Undo: {len(self.undo_stack)}"
            line_surface = self.fonts['small'].render(line_info, True, self.COLORS['BLUE'])
            self.screen.blit(line_surface, (50, 640))

        # Show clipboard feedback
        if self.clipboard_feedback_timer > 0:
            feedback_surface = self.fonts['small'].render(self.clipboard_feedback, True, self.COLORS['GREEN'])
            self.screen.blit(feedback_surface, (50, 660))
            self.clipboard_feedback_timer -= 1
    
    def render_instructions(self):
        """Render instructions screen"""
        # Title
        title_text = self.fonts['title'].render("Instructions", True, self.COLORS['DARK_BLUE'])
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH//2, 80))
        self.screen.blit(title_text, title_rect)

        # Back button
        self.draw_button("< Back", 50, 50, 100, 40, self.COLORS['GRAY'], self.COLORS['WHITE'])

        # Instructions content
        instructions = [
            "[GAME] OVERVIEW",
            "WRO Game Practice helps students learn robotics programming through interactive challenges.",
            "",
            "[HOW TO] PLAY",
            "1. MAIN MENU",
            "   * Start Game: Begin playing and select levels",
            "   * Instructions: View this help",
            "   * Exit: Close the game",
            "",
            "2. LEVEL SELECTION",
            "   * Choose from available levels (unlocked levels only)",
            "   * Level 1 is always available to start",
            "",
            "3. PLAYING THE GAME",
            "   * Click '[CODE] Editor' to open the programming interface",
            "   * Write Python code to control the robot",
            "   * Click '[RUN] Code' to execute your program",
            "   * Watch the robot move in the simulation area",
            "",
            "[ROBOT] BASIC COMMANDS (Level 1)",
            "robot.move_forward()    # Move robot forward",
            "robot.move_backward()   # Move robot backward",
            "robot.turn_left()       # Turn robot left 90 degrees",
            "robot.turn_right()      # Turn robot right 90 degrees",
            "robot.stop()           # Stop the robot",
            "",
            "[KEYS] KEYBOARD SHORTCUTS",
            "* ESC: Go back to previous menu",
            "* C: Open Code Editor (while playing)",
            "* R: Reset current level (while playing)",
            "",
            "[GOAL] LEVEL 1 OBJECTIVES",
            "* Learn basic robot movement commands",
            "* Control robot to reach green target points in order",
            "* Complete all targets to unlock Level 2"
        ]

        # Display instructions with scrolling
        start_y = 130
        line_height = 20
        max_lines = (self.SCREEN_HEIGHT - start_y - 50) // line_height

        for i, line in enumerate(instructions[:max_lines]):
            if line.startswith("[") and "]" in line:
                # Section headers
                text_surface = self.fonts['subtitle'].render(line, True, self.COLORS['DARK_BLUE'])
            elif line.startswith("   *") or line.startswith("robot.") or line.startswith("* "):
                # Code or bullet points
                text_surface = self.fonts['small'].render(line, True, self.COLORS['BLACK'])
            else:
                # Regular text
                text_surface = self.fonts['normal'].render(line, True, self.COLORS['BLACK'])

            self.screen.blit(text_surface, (100, start_y + i * line_height))

    def draw_button(self, text: str, x: int, y: int, width: int, height: int, bg_color: Tuple[int, int, int], text_color: Tuple[int, int, int]):
        """Draw button"""
        pygame.draw.rect(self.screen, bg_color, (x, y, width, height))
        pygame.draw.rect(self.screen, self.COLORS['BLACK'], (x, y, width, height), 2)

        text_surface = self.fonts['normal'].render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + width//2, y + height//2))
        self.screen.blit(text_surface, text_rect)
