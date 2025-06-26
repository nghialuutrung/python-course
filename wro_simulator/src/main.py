"""
Main application entry point for WRO Robot Control System
"""

import pygame
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .core.constants import *
from .core.robot import PythonRobot
from .core.level_manager import LevelManager
from .ui.level_select import LevelSelectScreen


class WROPythonControl:
    """Main application class with modular architecture"""
    
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
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
        
        # Create robot
        self.robot = PythonRobot()
        
        # Import console and sidebar here to avoid circular imports
        from .ui.console import PythonConsole
        from .ui.sidebar import Sidebar
        self.console = PythonConsole(self.robot)
        self.sidebar = Sidebar()
        
        # Add level management to console namespace
        self.console.namespace['levels'] = self.level_manager
        self.console.namespace['start_level'] = self.start_level
        self.console.namespace['check_objectives'] = self.check_level_objectives
        
        self.running = True
    
    def start_level(self, level_id: int) -> str:
        """Start a specific level"""
        level = self.level_manager.get_level(level_id)
        if not level:
            print(f"ERROR: Level {level_id} not found")
            return f"Level {level_id} not found"
        
        if not self.level_manager.is_level_unlocked(level_id):
            print(f"ERROR: Level {level_id} is locked")
            return f"Level {level_id} is locked"
        
        self.current_level = level
        self.game_state = "PLAYING"
        self.level_start_time = pygame.time.get_ticks() / 1000.0
        
        # Setup level environment
        self.setup_level_environment(level)
        
        # Reset robot for this level
        self.robot.reset_for_level(level)

        # Set callback for auto-checking objectives
        self.robot.objective_check_callback = self.auto_check_objectives

        return f"Started Level {level_id}: {level.name}"
    
    def setup_level_environment(self, level):
        """Setup environment for specific level"""
        # Set obstacles from level
        self.robot.obstacles = level.obstacles.copy()
        
        # Set items from level
        self.robot.items = level.items.copy()
        
        print(f"🎮 Level environment loaded: {len(level.obstacles)} obstacles, {len(level.items)} items")

    def auto_check_objectives(self):
        """Automatically check objectives after robot movement"""
        if not self.current_level:
            return

        # Debug: Show robot position
        from .core.constants import UNIT_SIZE, SIDEBAR_WIDTH
        robot_grid_x = (self.robot.x - SIDEBAR_WIDTH) / UNIT_SIZE
        robot_grid_y = self.robot.y / UNIT_SIZE
        print(f"🤖 Robot at pixel ({self.robot.x:.1f}, {self.robot.y:.1f}) = grid ({robot_grid_x:.1f}, {robot_grid_y:.1f})")

        if self.current_level.is_completed(self.robot):
            print("🎯 OBJECTIVES COMPLETED!")
            print("✨ Level completed automatically!")
            self.complete_level()
        else:
            # Check individual objectives and give feedback
            progress = self.current_level.get_progress(self.robot)
            completed_count = progress['completed_objectives']
            total_count = progress['total_objectives']

            if completed_count > 0:
                print(f"📊 Progress: {completed_count}/{total_count} objectives completed")

                # Show which objectives are completed
                for obj_status in progress['objectives_status']:
                    if obj_status['completed']:
                        print(f"✅ {obj_status['description']}")
            else:
                # Show target info for debugging
                for obj in self.current_level.objectives:
                    if obj.type == 'reach_target':
                        target = obj.params.get('target', (10, 10))
                        tolerance = obj.params.get('tolerance', 1.0)
                        distance = ((robot_grid_x - target[0])**2 + (robot_grid_y - target[1])**2)**0.5
                        print(f"🎯 Target: {target}, Distance: {distance:.2f}, Tolerance: {tolerance}")
                        break

    def check_level_objectives(self) -> bool:
        """Check if current level objectives are completed"""
        if not self.current_level:
            print("ERROR: No level is currently active")
            return False
        
        if self.current_level.is_completed(self.robot):
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
        current_time = pygame.time.get_ticks() / 1000.0
        time_taken = current_time - self.level_start_time if self.level_start_time else 0
        score = self.current_level.get_score(time_taken, self.robot)
        
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
    
    def show_level_progress(self):
        """Show current level progress"""
        if not self.current_level:
            return
        
        progress = self.current_level.get_progress(self.robot)
        print(f"📊 Level {self.current_level.level_id} Progress:")
        
        for obj_status in progress['objectives_status']:
            status = "✅" if obj_status['completed'] else "❌"
            print(f"  {status} {obj_status['description']}")
    
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
                console_start_x = SIDEBAR_WIDTH + GAME_WIDTH
                if mouse_x >= console_start_x:
                    self.console.handle_scroll(event.y)
    
    def update(self, dt: float):
        """Update game state"""
        if self.game_state == "PLAYING":
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
        # Import game renderer here to avoid circular imports
        from .ui.game_renderer import GameRenderer
        
        renderer = GameRenderer(self.screen, self.font)
        renderer.draw_game(self.robot, self.console, self.current_level, self.level_start_time, self.sidebar)
    
    def draw_level_complete(self):
        """Draw level completion screen"""
        self.screen.fill(BLACK)
        
        # Title
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("🎉 LEVEL COMPLETED!", True, CONSOLE_SUCCESS)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title_text, title_rect)
        
        if self.current_level:
            # Level info
            level_font = pygame.font.Font(None, 32)
            level_text = level_font.render(f"Level {self.current_level.level_id}: {self.current_level.name}", True, WHITE)
            level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, 200))
            self.screen.blit(level_text, level_rect)
            
            # Stats
            current_time = pygame.time.get_ticks() / 1000.0
            time_taken = current_time - self.level_start_time if self.level_start_time else 0
            score = self.current_level.get_score(time_taken, self.robot)
            
            stats = [
                f"⏱️  Time: {time_taken:.1f} seconds",
                f"⭐ Score: {score}",
                f"🤖 Commands: {self.robot.commands_executed}",
                f"📡 Sensors: {self.robot.sensor_calls}"
            ]
            
            for i, stat in enumerate(stats):
                stat_text = self.font.render(stat, True, CONSOLE_TEXT)
                stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH//2, 280 + i * 30))
                self.screen.blit(stat_text, stat_rect)
        
        # Instructions
        instruction_text = self.font.render("Press any key to continue", True, CONSOLE_PROMPT)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100))
        self.screen.blit(instruction_text, instruction_rect)
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()


def main():
    """Main entry point"""
    app = WROPythonControl()
    app.run()


if __name__ == "__main__":
    main()
