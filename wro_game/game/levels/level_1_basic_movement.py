#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Level 1: Basic Movement
Students learn how to control basic robot movement
"""

import pygame
from typing import Tuple, List

class Robot:
    """Class representing robot in the game"""

    def __init__(self, x: int, y: int):
        """Initialize robot at position (x, y)"""
        self.x = x
        self.y = y
        self.angle = 0  # Rotation angle (degrees) - 0=East, 90=South, 180=West, 270=North
        self.grid_size = 50  # One unit = 50 pixels (matches grid)
        self.size = 20
        self.trail = []  # Store robot's trail
        
    def move_forward(self, units: int = 1):
        """Move robot forward by specified grid units (default 1 unit = 50px)"""
        # Store current position for trail
        old_pos = (self.x, self.y)

        # Calculate movement distance
        distance = units * self.grid_size

        # Move based on current direction (angle)
        if self.angle == 0:    # East (Right)
            self.x += distance
        elif self.angle == 90:  # South (Down)
            self.y += distance
        elif self.angle == 180: # West (Left)
            self.x -= distance
        elif self.angle == 270: # North (Up)
            self.y -= distance
        else:
            # For non-cardinal directions, use trigonometry
            import math
            rad = math.radians(self.angle)
            self.x += distance * math.cos(rad)
            self.y += distance * math.sin(rad)

        # Store trail
        self.trail.append(old_pos)
        if len(self.trail) > 50:  # Limit trail length
            self.trail.pop(0)

    def move_backward(self, units: int = 1):
        """Move robot backward by specified grid units"""
        self.move_forward(-units)

    def turn_left(self):
        """Turn left 90 degrees (counter-clockwise)"""
        self.angle -= 90
        self.angle %= 360
        # Ensure angle is always one of: 0, 90, 180, 270
        self.angle = round(self.angle / 90) * 90 % 360

    def turn_right(self):
        """Turn right 90 degrees (clockwise)"""
        self.angle += 90
        self.angle %= 360
        # Ensure angle is always one of: 0, 90, 180, 270
        self.angle = round(self.angle / 90) * 90 % 360

    def stop(self):
        """Stop robot"""
        pass

    def get_position(self) -> Tuple[int, int]:
        """Get current robot position"""
        return (int(self.x), int(self.y))
    
    def draw(self, screen, colors):
        """Draw robot on screen"""
        # Draw trail with step numbers
        if len(self.trail) > 1:
            # Draw trail lines with fading effect
            for i in range(len(self.trail) - 1):
                # Calculate alpha for fading effect
                alpha_factor = (i + 1) / len(self.trail)
                line_width = max(1, int(3 * alpha_factor))

                start_pos = self.trail[i]
                end_pos = self.trail[i + 1]
                pygame.draw.line(screen, colors['BLUE'], start_pos, end_pos, line_width)

                # Draw step numbers
                if i % 3 == 0:  # Show every 3rd step to avoid clutter
                    font = pygame.font.Font(None, 16)
                    step_text = str(i + 1)
                    text_surface = font.render(step_text, True, (0, 0, 150))
                    # Position text slightly offset from trail point
                    text_pos = (start_pos[0] + 10, start_pos[1] - 10)
                    screen.blit(text_surface, text_pos)

        # Draw robot body (circle) with gradient
        pos = self.get_position()

        # Draw shadow
        shadow_offset = 3
        pygame.draw.circle(screen, (100, 100, 100), (pos[0] + shadow_offset, pos[1] + shadow_offset), self.size)

        # Draw main body
        pygame.draw.circle(screen, colors['RED'], pos, self.size)
        pygame.draw.circle(screen, (150, 0, 0), pos, self.size - 3)  # Inner circle
        pygame.draw.circle(screen, colors['BLACK'], pos, self.size, 2)

        # Draw robot direction (enhanced arrow)
        import math
        rad = math.radians(self.angle)

        # Main direction line
        end_x = self.x + (self.size - 3) * math.cos(rad)
        end_y = self.y + (self.size - 3) * math.sin(rad)
        pygame.draw.line(screen, colors['WHITE'], pos, (int(end_x), int(end_y)), 4)

        # Arrow head
        arrow_length = 8
        arrow_angle = 30  # degrees

        # Left arrow line
        left_angle = rad + math.radians(180 - arrow_angle)
        left_x = end_x + arrow_length * math.cos(left_angle)
        left_y = end_y + arrow_length * math.sin(left_angle)
        pygame.draw.line(screen, colors['WHITE'], (int(end_x), int(end_y)), (int(left_x), int(left_y)), 3)

        # Right arrow line
        right_angle = rad + math.radians(180 + arrow_angle)
        right_x = end_x + arrow_length * math.cos(right_angle)
        right_y = end_y + arrow_length * math.sin(right_angle)
        pygame.draw.line(screen, colors['WHITE'], (int(end_x), int(end_y)), (int(right_x), int(right_y)), 3)

        # Draw angle indicator
        font = pygame.font.Font(None, 16)
        angle_text = f"{int(self.angle)}°"
        text_surface = font.render(angle_text, True, colors['BLACK'])
        text_rect = text_surface.get_rect(center=(pos[0], pos[1] + self.size + 15))
        screen.blit(text_surface, text_rect)

class Level1BasicMovement:
    """Level 1: Learn basic movement"""

    def __init__(self, screen_width: int, screen_height: int):
        """Initialize level 1"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Align positions with grid (multiples of 50)
        self.robot = Robot(100, 100)  # Starting position (2,2 in grid coordinates)
        self.target_positions = [(300, 200), (450, 300), (350, 450)]  # Target points aligned to grid
        self.current_target = 0
        self.completed = False

        # Movement visualization
        self.movement_steps = []  # Store each movement step for visualization
        self.show_grid = True
        self.show_path_hints = True

        # Camera system for auto-follow
        self.camera_x = 0
        self.camera_y = 0
        self.viewport_width = 550  # Simulation area width
        self.viewport_height = 420  # Simulation area height
        self.instructions = [
            "Level 1 Instructions: Grid-Based Movement",
            "",
            "Objective: Control robot to reach target points (green)",
            "",
            "🎯 Movement System:",
            "- Each move_forward() = 1 grid unit (50 pixels)",
            "- Robot moves in cardinal directions only",
            "- Turns are exactly 90 degrees",
            "",
            "📍 Starting Position: (100,100) facing East →",
            "📍 Target 1: (300,200) - 4 units right, 2 units down",
            "",
            "Available commands:",
            "- robot.move_forward()  # Move 1 grid unit forward",
            "- robot.move_backward() # Move 1 grid unit backward",
            "- robot.turn_left()     # Turn left 90° (↑→↓←)",
            "- robot.turn_right()    # Turn right 90° (↑←↓→)",
            "- robot.stop()          # Stop robot",
            "",
            "💡 Tip: Count grid squares to plan your path!",
        ]
        
        # Sample code for students
        self.sample_code = """# Sample code Level 1
# Move robot to the first target point
# Robot starts at (100,100) facing East (right)
# Target 1 is at (300,200) - that's 4 units right, 2 units down

robot.move_forward()  # Move 1 unit right (to 150,100)
robot.move_forward()  # Move 1 unit right (to 200,100)
robot.move_forward()  # Move 1 unit right (to 250,100)
robot.move_forward()  # Move 1 unit right (to 300,100)
robot.turn_right()    # Turn to face South (down)
robot.move_forward()  # Move 1 unit down (to 300,150)
robot.move_forward()  # Move 1 unit down (to 300,200) - Target reached!
"""
    
    def reset(self):
        """Reset level to initial state"""
        self.robot = Robot(100, 100)  # Reset to grid position (2,2)
        self.current_target = 0
        self.completed = False

    def update(self):
        """Update level state"""
        # Update camera to follow robot
        self.update_camera()

        if self.current_target < len(self.target_positions):
            target_x, target_y = self.target_positions[self.current_target]
            robot_x, robot_y = self.robot.get_position()

            # Check if robot is near target point
            distance = ((robot_x - target_x) ** 2 + (robot_y - target_y) ** 2) ** 0.5
            if distance < 30:  # Within 30 pixels
                self.current_target += 1
                if self.current_target >= len(self.target_positions):
                    self.completed = True

    def update_camera(self):
        """Update camera position to follow robot"""
        robot_x, robot_y = self.robot.get_position()

        # Center camera on robot (instant follow)
        self.camera_x = robot_x - self.viewport_width // 2
        self.camera_y = robot_y - self.viewport_height // 2

        # Keep camera within reasonable bounds
        self.camera_x = max(-100, min(self.camera_x, 1500))
        self.camera_y = max(-100, min(self.camera_y, 1500))
    
    def draw(self, screen, colors):
        """Draw level on screen with camera offset"""
        # Create a surface for the world (larger than viewport)
        world_surface = pygame.Surface((2000, 2000))  # Large world surface
        world_surface.fill((255, 255, 255))  # White background

        # Draw everything on world surface first
        world_rect = world_surface.get_rect()

        # Draw grid lines for better visualization
        if self.show_grid:
            self.draw_grid(world_surface, colors, world_rect)

        # Draw path suggestions (optional helper lines)
        if self.show_path_hints:
            self.draw_path_hints(world_surface, colors)

        # Draw movement guides
        self.draw_movement_guides(world_surface, colors)

        # Draw target points
        for i, (x, y) in enumerate(self.target_positions):
            if i == self.current_target:
                # Current target (bright green)
                pygame.draw.circle(world_surface, colors['GREEN'], (x, y), 25)
                pygame.draw.circle(world_surface, colors['BLACK'], (x, y), 25, 3)
                # Number
                font = pygame.font.Font(None, 24)
                text = font.render(str(i + 1), True, colors['WHITE'])
                text_rect = text.get_rect(center=(x, y))
                world_surface.blit(text, text_rect)
            elif i < self.current_target:
                # Completed point (dark green)
                pygame.draw.circle(world_surface, colors['DARK_GREEN'], (x, y), 20)
                pygame.draw.circle(world_surface, colors['BLACK'], (x, y), 20, 2)
                # Check mark
                pygame.draw.line(world_surface, colors['WHITE'], (x-8, y), (x-3, y+5), 3)
                pygame.draw.line(world_surface, colors['WHITE'], (x-3, y+5), (x+8, y-5), 3)
            else:
                # Unreached point (gray)
                pygame.draw.circle(world_surface, colors['GRAY'], (x, y), 20)
                pygame.draw.circle(world_surface, colors['BLACK'], (x, y), 20, 2)
                # Number
                font = pygame.font.Font(None, 20)
                text = font.render(str(i + 1), True, colors['BLACK'])
                text_rect = text.get_rect(center=(x, y))
                world_surface.blit(text, text_rect)

        # Draw robot on world surface
        self.robot.draw(world_surface, colors)

        # Calculate viewport rectangle in world coordinates
        viewport_rect = pygame.Rect(
            int(self.camera_x),
            int(self.camera_y),
            self.viewport_width,
            self.viewport_height
        )

        # Blit the visible portion of world to screen
        screen.blit(world_surface, (0, 0), viewport_rect)

        # Draw UI elements (status) on top (not affected by camera)
        font = pygame.font.Font(None, 24)
        status_text = f"Target: {self.current_target + 1}/{len(self.target_positions)}"
        if self.completed:
            status_text = "*** Level 1 Completed! ***"

        text_surface = font.render(status_text, True, colors['BLACK'])
        screen.blit(text_surface, (10, 10))

        # Draw camera info
        robot_x, robot_y = self.robot.get_position()
        camera_info = f"Robot: ({robot_x},{robot_y}) Camera: ({int(self.camera_x)},{int(self.camera_y)})"
        info_surface = pygame.font.Font(None, 16).render(camera_info, True, (100, 100, 100))
        screen.blit(info_surface, (10, 30))

    def draw_grid(self, screen, colors, screen_rect):
        """Draw grid lines to help visualize movement"""
        # Grid spacing
        grid_size = 50

        # Add light gray color if not exists
        light_gray = (230, 230, 230)

        # Draw vertical lines
        for x in range(0, screen_rect.width, grid_size):
            pygame.draw.line(screen, light_gray, (x, 0), (x, screen_rect.height), 1)

        # Draw horizontal lines
        for y in range(0, screen_rect.height, grid_size):
            pygame.draw.line(screen, light_gray, (0, y), (screen_rect.width, y), 1)

        # Draw coordinate labels every 100 pixels
        font = pygame.font.Font(None, 16)
        for x in range(0, screen_rect.width, 100):
            if x > 0:  # Skip origin
                text = font.render(str(x), True, (180, 180, 180))
                screen.blit(text, (x + 2, 2))

        for y in range(0, screen_rect.height, 100):
            if y > 0:  # Skip origin
                text = font.render(str(y), True, (180, 180, 180))
                screen.blit(text, (2, y + 2))

    def draw_path_hints(self, screen, colors):
        """Draw subtle path hints to help students understand movement"""
        # Only show hints for current target
        if self.current_target < len(self.target_positions):
            robot_pos = self.robot.get_position()
            target_pos = self.target_positions[self.current_target]

            # Draw dotted line hint (very subtle)
            hint_color = (200, 255, 200)  # Very light green

            # Draw dotted line from robot to target
            self.draw_dotted_line(screen, hint_color, robot_pos, target_pos)

            # Draw distance info
            distance = ((robot_pos[0] - target_pos[0]) ** 2 + (robot_pos[1] - target_pos[1]) ** 2) ** 0.5
            font = pygame.font.Font(None, 18)
            distance_text = f"Distance to target {self.current_target + 1}: {int(distance)}px"
            text_surface = font.render(distance_text, True, (100, 100, 100))
            screen.blit(text_surface, (10, 35))

    def draw_dotted_line(self, screen, color, start_pos, end_pos):
        """Draw a dotted line between two points"""
        import math

        # Calculate line parameters
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        distance = math.sqrt(dx * dx + dy * dy)

        if distance == 0:
            return

        # Normalize direction
        dx /= distance
        dy /= distance

        # Draw dots along the line
        dot_spacing = 10
        dot_size = 2

        for i in range(0, int(distance), dot_spacing):
            x = start_pos[0] + dx * i
            y = start_pos[1] + dy * i
            pygame.draw.circle(screen, color, (int(x), int(y)), dot_size)

    def draw_movement_guides(self, screen, colors):
        """Draw movement guides and distance indicators"""
        robot_pos = self.robot.get_position()

        # Draw compass directions from robot
        compass_length = 40
        compass_colors = {
            'N': (255, 100, 100),  # Red for North (up)
            'E': (100, 255, 100),  # Green for East (right)
            'S': (100, 100, 255),  # Blue for South (down)
            'W': (255, 255, 100)   # Yellow for West (left)
        }

        # North (up)
        north_end = (robot_pos[0], robot_pos[1] - compass_length)
        pygame.draw.line(screen, compass_colors['N'], robot_pos, north_end, 2)

        # East (right)
        east_end = (robot_pos[0] + compass_length, robot_pos[1])
        pygame.draw.line(screen, compass_colors['E'], robot_pos, east_end, 2)

        # South (down)
        south_end = (robot_pos[0], robot_pos[1] + compass_length)
        pygame.draw.line(screen, compass_colors['S'], robot_pos, south_end, 2)

        # West (left)
        west_end = (robot_pos[0] - compass_length, robot_pos[1])
        pygame.draw.line(screen, compass_colors['W'], robot_pos, west_end, 2)

        # Draw direction labels
        font = pygame.font.Font(None, 16)

        # North label
        n_text = font.render("N", True, compass_colors['N'])
        screen.blit(n_text, (robot_pos[0] - 5, robot_pos[1] - compass_length - 15))

        # East label
        e_text = font.render("E", True, compass_colors['E'])
        screen.blit(e_text, (robot_pos[0] + compass_length + 5, robot_pos[1] - 8))

        # South label
        s_text = font.render("S", True, compass_colors['S'])
        screen.blit(s_text, (robot_pos[0] - 5, robot_pos[1] + compass_length + 5))

        # West label
        w_text = font.render("W", True, compass_colors['W'])
        screen.blit(w_text, (robot_pos[0] - compass_length - 15, robot_pos[1] - 8))

        # Draw movement step size indicator (1 grid unit = 50px)
        step_size = self.robot.grid_size  # 50 pixels = 1 grid unit
        step_color = (150, 150, 150)

        # Show next step preview based on robot's current angle
        if self.robot.angle == 0:    # East
            next_pos = (robot_pos[0] + step_size, robot_pos[1])
        elif self.robot.angle == 90:  # South
            next_pos = (robot_pos[0], robot_pos[1] + step_size)
        elif self.robot.angle == 180: # West
            next_pos = (robot_pos[0] - step_size, robot_pos[1])
        elif self.robot.angle == 270: # North
            next_pos = (robot_pos[0], robot_pos[1] - step_size)
        else:
            next_pos = robot_pos

        # Draw dotted line to show next step
        if next_pos != robot_pos:
            self.draw_dotted_line(screen, step_color, robot_pos, next_pos)

        # Draw step size indicator
        step_text = font.render("Next step: 1 grid unit (50px)", True, step_color)
        screen.blit(step_text, (robot_pos[0] + 25, robot_pos[1] + 25))

        # Draw current grid position
        grid_x = robot_pos[0] // 50
        grid_y = robot_pos[1] // 50
        pos_text = font.render(f"Grid pos: ({grid_x},{grid_y})", True, step_color)
        screen.blit(pos_text, (robot_pos[0] + 25, robot_pos[1] + 40))
    
    def execute_code(self, code: str):
        """Execute student's code"""
        try:
            # Create safe namespace for code execution
            namespace = {
                'robot': self.robot,
                '__builtins__': {}  # Restrict built-in functions
            }

            # Execute code
            exec(code, namespace)

            # Update camera after code execution
            self.update_camera()

            return True, "Code executed successfully!"

        except Exception as e:
            return False, f"Error in code: {str(e)}"

    def get_instructions(self) -> List[str]:
        """Get instructions for this level"""
        return self.instructions

    def get_sample_code(self) -> str:
        """Get sample code for this level"""
        return self.sample_code

    def is_completed(self) -> bool:
        """Check if level is completed"""
        return self.completed
