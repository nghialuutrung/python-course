"""
Game Renderer for WRO Robot Control System
"""

import pygame
import math
import time
from ..core.constants import *


class IconRenderer:
    """Renders custom icons for the UI"""
    
    @staticmethod
    def draw_star(surface, center, size, color):
        """Draw a star icon"""
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                radius = size
            else:
                radius = size * 0.5
            x = center[0] + radius * math.cos(angle - math.pi/2)
            y = center[1] + radius * math.sin(angle - math.pi/2)
            points.append((x, y))
        pygame.draw.polygon(surface, color, points)
    
    @staticmethod
    def draw_diamond(surface, center, size, color):
        """Draw a diamond icon"""
        points = [
            (center[0], center[1] - size),
            (center[0] + size, center[1]),
            (center[0], center[1] + size),
            (center[0] - size, center[1])
        ]
        pygame.draw.polygon(surface, color, points)
    
    @staticmethod
    def draw_lightning(surface, center, size, color):
        """Draw a lightning bolt icon"""
        points = [
            (center[0] - size//2, center[1] - size),
            (center[0] + size//4, center[1] - size//4),
            (center[0] - size//4, center[1]),
            (center[0] + size//2, center[1] + size)
        ]
        pygame.draw.lines(surface, color, False, points, 3)


class GameRenderer:
    """Renders the main game screen"""
    
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.icon_renderer = IconRenderer()
    
    def draw_game(self, robot, console, current_level, level_start_time, sidebar):
        """Draw the complete game screen with sidebar layout"""
        # Clear screen
        self.screen.fill(BACKGROUND)

        # Draw sidebar
        sidebar.draw(self.screen, robot, current_level, level_start_time)

        # Draw game area background (offset by sidebar)
        game_rect = pygame.Rect(SIDEBAR_WIDTH, 0, GAME_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, game_rect)

        # Draw grid (offset by sidebar)
        self.draw_grid()

        # Draw level environment
        if current_level:
            self.draw_level_environment(current_level, robot)

        # Draw robot
        self.draw_robot(robot)

        # Draw console
        console.draw(self.screen)
    
    def draw_grid(self):
        """Draw coordinate grid (offset by sidebar)"""
        # Light grid lines (every unit)
        for x in range(SIDEBAR_WIDTH, SIDEBAR_WIDTH + GAME_WIDTH, UNIT_SIZE):
            pygame.draw.line(self.screen, GRID_LIGHT, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, UNIT_SIZE):
            pygame.draw.line(self.screen, GRID_LIGHT, (SIDEBAR_WIDTH, y), (SIDEBAR_WIDTH + GAME_WIDTH, y))

        # Major grid lines (every 5 units)
        for x in range(SIDEBAR_WIDTH, SIDEBAR_WIDTH + GAME_WIDTH, UNIT_SIZE * 5):
            pygame.draw.line(self.screen, GRID_MAJOR, (x, 0), (x, SCREEN_HEIGHT), 2)
        for y in range(0, SCREEN_HEIGHT, UNIT_SIZE * 5):
            pygame.draw.line(self.screen, GRID_MAJOR, (SIDEBAR_WIDTH, y), (SIDEBAR_WIDTH + GAME_WIDTH, y), 2)

        # Coordinate labels
        font_small = pygame.font.Font(None, 16)
        for x in range(SIDEBAR_WIDTH, SIDEBAR_WIDTH + GAME_WIDTH, UNIT_SIZE * 5):
            grid_x = (x - SIDEBAR_WIDTH) // UNIT_SIZE
            if grid_x > 0:
                label = font_small.render(str(grid_x), True, GRID_MAJOR)
                self.screen.blit(label, (x + 2, 2))
        for y in range(0, SCREEN_HEIGHT, UNIT_SIZE * 5):
            if y > 0:
                label = font_small.render(str(y // UNIT_SIZE), True, GRID_MAJOR)
                self.screen.blit(label, (SIDEBAR_WIDTH + 2, y + 2))
    
    def draw_level_environment(self, level, robot=None):
        """Draw level-specific environment"""
        # Draw beautiful target point
        if level.target_area:
            # Calculate target center point
            target_center = (
                level.target_area['x'] + level.target_area['width'] // 2,
                level.target_area['y'] + level.target_area['height'] // 2
            )

            # Check if robot is near target
            robot_near_target = False
            distance_to_target = float('inf')
            if robot:
                dx = robot.x - target_center[0]
                dy = robot.y - target_center[1]
                distance_to_target = math.sqrt(dx*dx + dy*dy)
                robot_near_target = distance_to_target <= 50  # Within 50 pixels

            # Draw beautiful target point
            self.draw_target_point(target_center, robot_near_target, distance_to_target)

        # Draw obstacles
        for obstacle in level.obstacles:
            obstacle_rect = pygame.Rect(
                obstacle['x'], obstacle['y'],
                obstacle['width'], obstacle['height']
            )
            pygame.draw.rect(self.screen, OBSTACLE_COLOR, obstacle_rect)
            pygame.draw.rect(self.screen, BLACK, obstacle_rect, 2)

        # Draw items
        for item in level.items:
            item_center = (item['x'], item['y'])

            # Glow effect
            glow_radius = 25 + 5 * math.sin(time.time() * 3)
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*ITEM_COLOR, 30), (glow_radius, glow_radius), glow_radius)
            self.screen.blit(glow_surface, (item_center[0] - glow_radius, item_center[1] - glow_radius))

            # Item
            pygame.draw.circle(self.screen, ITEM_COLOR, item_center, 8)
            pygame.draw.circle(self.screen, BLACK, item_center, 8, 2)

    def draw_target_point(self, center, robot_near, distance):
        """Draw beautiful animated target point"""
        # Animation based on time
        pulse = math.sin(time.time() * 3) * 0.3 + 0.7  # Pulse between 0.4 and 1.0

        # Base colors
        if robot_near:
            # Bright colors when robot is near
            primary_color = (255, 215, 0)  # Gold
            secondary_color = (255, 255, 100)  # Light yellow
            glow_color = (255, 255, 0, 80)  # Yellow glow
            status_text = "REACHED!"
        else:
            # Normal colors
            primary_color = (100, 255, 100)  # Green
            secondary_color = (150, 255, 150)  # Light green
            glow_color = (100, 255, 100, 60)  # Green glow
            status_text = "TARGET"

        # Outer glow effect (multiple layers)
        for i in range(5):
            glow_radius = 30 + i * 8 + pulse * 10
            alpha = max(0, glow_color[3] - i * 15)
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*glow_color[:3], alpha),
                             (glow_radius, glow_radius), glow_radius)
            self.screen.blit(glow_surface,
                           (center[0] - glow_radius, center[1] - glow_radius))

        # Main target rings (animated)
        base_radius = 20

        # Outer ring
        outer_radius = int(base_radius + pulse * 5)
        pygame.draw.circle(self.screen, primary_color, center, outer_radius, 3)

        # Middle ring
        middle_radius = int(base_radius * 0.7 + pulse * 3)
        pygame.draw.circle(self.screen, secondary_color, center, middle_radius, 2)

        # Inner filled circle
        inner_radius = int(base_radius * 0.4 + pulse * 2)
        pygame.draw.circle(self.screen, primary_color, center, inner_radius)

        # Center dot (always visible)
        pygame.draw.circle(self.screen, WHITE, center, 3)

        # Crosshair lines
        line_length = outer_radius + 10
        line_width = 2

        # Horizontal line
        pygame.draw.line(self.screen, primary_color,
                        (center[0] - line_length, center[1]),
                        (center[0] + line_length, center[1]), line_width)

        # Vertical line
        pygame.draw.line(self.screen, primary_color,
                        (center[0], center[1] - line_length),
                        (center[0], center[1] + line_length), line_width)

        # Target label (floating above)
        font = pygame.font.Font(None, 18)
        text_surface = font.render(status_text, True, primary_color)
        text_rect = text_surface.get_rect(center=(center[0], center[1] - 40))

        # Text background
        bg_rect = text_rect.inflate(10, 4)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (0, 0, 0, 120), (0, 0, bg_rect.width, bg_rect.height), border_radius=5)
        self.screen.blit(bg_surface, bg_rect)

        # Text
        self.screen.blit(text_surface, text_rect)

        # Distance indicator (when robot is close)
        if robot_near and distance < 100:
            distance_text = f"{distance:.0f}px"
            dist_surface = font.render(distance_text, True, (200, 200, 200))
            dist_rect = dist_surface.get_rect(center=(center[0], center[1] + 40))
            self.screen.blit(dist_surface, dist_rect)
    
    def draw_robot(self, robot):
        """Draw beautiful, detailed robot with modern styling"""
        robot_center = (int(robot.x), int(robot.y))
        angle_rad = math.radians(robot.angle)

        # Enhanced shadow with gradient effect
        self.draw_robot_shadow(robot_center, robot.size)

        # Main robot body with gradient and details
        self.draw_robot_body(robot_center, robot.size, angle_rad)

        # Advanced direction indicator
        self.draw_robot_direction(robot_center, robot.size, angle_rad)

        # Beautiful robot face
        self.draw_robot_face(robot_center, robot.size, angle_rad)

        # Robot details and decorations
        self.draw_robot_details(robot_center, robot.size, angle_rad)

        # Enhanced sensor beams
        self.draw_sensor_beams(robot)

        # Movement trail effect
        if robot.animating:
            self.draw_movement_trail(robot)

    def draw_robot_shadow(self, center, size):
        """Draw realistic shadow with gradient"""
        shadow_center = (center[0] + 3, center[1] + 3)

        # Multiple shadow layers for depth
        for i in range(3):
            alpha = 40 - i * 10
            radius = size + i
            shadow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shadow_surface, (0, 0, 0, alpha), (radius, radius), radius)
            self.screen.blit(shadow_surface, (shadow_center[0] - radius, shadow_center[1] - radius))

    def draw_robot_body(self, center, size, angle_rad):
        """Draw detailed robot body with gradient and metallic look"""
        # Outer ring (metallic border)
        pygame.draw.circle(self.screen, (180, 180, 200), center, size + 2)

        # Main body with gradient effect
        for i in range(size):
            ratio = i / size
            # Blue gradient from light to dark
            r = int(100 + (150 - 100) * (1 - ratio))
            g = int(150 + (200 - 150) * (1 - ratio))
            b = int(255 * (1 - ratio * 0.3))
            color = (r, g, b)
            pygame.draw.circle(self.screen, color, center, size - i)

        # Inner highlight circle
        highlight_radius = size // 3
        highlight_center = (
            center[0] - size // 4,
            center[1] - size // 4
        )
        pygame.draw.circle(self.screen, (200, 220, 255), highlight_center, highlight_radius)

        # Metallic border
        pygame.draw.circle(self.screen, (220, 220, 240), center, size, 3)
        pygame.draw.circle(self.screen, (160, 160, 180), center, size, 1)

    def draw_robot_direction(self, center, size, angle_rad):
        """Draw advanced direction indicator"""
        # Main direction arrow
        arrow_length = size - 3
        arrow_end = (
            center[0] + arrow_length * math.cos(angle_rad),
            center[1] + arrow_length * math.sin(angle_rad)
        )

        # Arrow shaft
        pygame.draw.line(self.screen, (255, 255, 255), center, arrow_end, 5)
        pygame.draw.line(self.screen, (100, 150, 255), center, arrow_end, 3)

        # Arrow head
        head_size = 8
        head_angle1 = angle_rad + 2.8
        head_angle2 = angle_rad - 2.8

        head_point1 = (
            arrow_end[0] + head_size * math.cos(head_angle1),
            arrow_end[1] + head_size * math.sin(head_angle1)
        )
        head_point2 = (
            arrow_end[0] + head_size * math.cos(head_angle2),
            arrow_end[1] + head_size * math.sin(head_angle2)
        )

        # Draw arrow head
        pygame.draw.polygon(self.screen, (255, 255, 255), [arrow_end, head_point1, head_point2])
        pygame.draw.polygon(self.screen, (100, 150, 255), [arrow_end, head_point1, head_point2])

    def draw_robot_face(self, center, size, angle_rad):
        """Draw expressive robot face"""
        # Eye positions relative to direction
        eye_distance = size // 2.5
        eye_offset_angle = 0.6

        eye1_angle = angle_rad + eye_offset_angle
        eye2_angle = angle_rad - eye_offset_angle

        eye1_pos = (
            int(center[0] + eye_distance * math.cos(eye1_angle)),
            int(center[1] + eye_distance * math.sin(eye1_angle))
        )
        eye2_pos = (
            int(center[0] + eye_distance * math.cos(eye2_angle)),
            int(center[1] + eye_distance * math.sin(eye2_angle))
        )

        # Eye design
        eye_size = 4

        # Eye background (white)
        pygame.draw.circle(self.screen, WHITE, eye1_pos, eye_size)
        pygame.draw.circle(self.screen, WHITE, eye2_pos, eye_size)

        # Eye pupils (blue)
        pygame.draw.circle(self.screen, (0, 100, 255), eye1_pos, eye_size - 1)
        pygame.draw.circle(self.screen, (0, 100, 255), eye2_pos, eye_size - 1)

        # Eye highlights
        highlight_offset = 1
        highlight1 = (eye1_pos[0] - highlight_offset, eye1_pos[1] - highlight_offset)
        highlight2 = (eye2_pos[0] - highlight_offset, eye2_pos[1] - highlight_offset)
        pygame.draw.circle(self.screen, WHITE, highlight1, 1)
        pygame.draw.circle(self.screen, WHITE, highlight2, 1)

        # Mouth (optional, based on robot state)
        mouth_pos = (
            int(center[0] + (size // 3) * math.cos(angle_rad)),
            int(center[1] + (size // 3) * math.sin(angle_rad))
        )
        pygame.draw.circle(self.screen, (255, 200, 100), mouth_pos, 2)

    def draw_robot_details(self, center, size, angle_rad):
        """Draw additional robot details and decorations"""
        # Side panels
        panel_distance = size * 0.7
        panel_angle1 = angle_rad + math.pi/2
        panel_angle2 = angle_rad - math.pi/2

        panel1_pos = (
            int(center[0] + panel_distance * math.cos(panel_angle1)),
            int(center[1] + panel_distance * math.sin(panel_angle1))
        )
        panel2_pos = (
            int(center[0] + panel_distance * math.cos(panel_angle2)),
            int(center[1] + panel_distance * math.sin(panel_angle2))
        )

        # Draw side panels
        pygame.draw.circle(self.screen, (150, 150, 170), panel1_pos, 3)
        pygame.draw.circle(self.screen, (150, 150, 170), panel2_pos, 3)
        pygame.draw.circle(self.screen, (200, 200, 220), panel1_pos, 2)
        pygame.draw.circle(self.screen, (200, 200, 220), panel2_pos, 2)

        # Center logo/emblem
        pygame.draw.circle(self.screen, (255, 215, 0), center, 4)
        pygame.draw.circle(self.screen, (255, 255, 255), center, 4, 1)

        # Small decorative elements
        for i in range(4):
            deco_angle = angle_rad + (i * math.pi / 2) + math.pi/4
            deco_distance = size * 0.8
            deco_pos = (
                int(center[0] + deco_distance * math.cos(deco_angle)),
                int(center[1] + deco_distance * math.sin(deco_angle))
            )
            pygame.draw.circle(self.screen, (180, 200, 255), deco_pos, 1)

    def draw_movement_trail(self, robot):
        """Draw trail effect when robot is moving"""
        if hasattr(robot, 'trail_positions'):
            for i, pos in enumerate(robot.trail_positions):
                alpha = int(50 * (i / len(robot.trail_positions)))
                trail_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, (100, 150, 255, alpha), (5, 5), 5)
                self.screen.blit(trail_surface, (pos[0] - 5, pos[1] - 5))
    
    def draw_sensor_beams(self, robot):
        """Draw beautiful sensor beams with effects"""
        sensor_configs = [
            {'angle': 0, 'color': (255, 100, 100), 'name': 'FRONT'},    # Red
            {'angle': -90, 'color': (100, 255, 100), 'name': 'LEFT'},   # Green
            {'angle': 90, 'color': (100, 100, 255), 'name': 'RIGHT'}    # Blue
        ]

        for config in sensor_configs:
            angle_offset = config['angle']
            base_color = config['color']

            sensor_angle = math.radians(robot.angle + angle_offset)
            distance = robot.get_distance_to_obstacle(angle_offset)
            beam_length = min(distance * UNIT_SIZE, 150)

            beam_start = (robot.x, robot.y)
            beam_end = (
                robot.x + beam_length * math.cos(sensor_angle),
                robot.y + beam_length * math.sin(sensor_angle)
            )

            # Dynamic color based on distance
            if distance < 1:
                intensity = 255  # Bright red zone
                beam_color = (255, 50, 50)
                glow_color = (255, 100, 100, 80)
            elif distance < 2:
                intensity = 200  # Warning yellow zone
                beam_color = (255, 200, 50)
                glow_color = (255, 255, 100, 60)
            else:
                intensity = 150  # Safe green zone
                beam_color = base_color
                glow_color = (*base_color, 40)

            # Draw beam glow effect
            glow_surface = pygame.Surface((beam_length * 2, 20), pygame.SRCALPHA)
            for i in range(5):
                alpha = glow_color[3] // (i + 1)
                glow_width = 6 - i
                if glow_width > 0:
                    # Calculate glow line positions
                    start_offset = (beam_start[0] - beam_length, beam_start[1] - 10)
                    end_offset = (beam_end[0] - beam_length, beam_end[1] - 10)

                    # Draw glow on surface
                    if start_offset[0] >= 0 and end_offset[0] >= 0:
                        try:
                            pygame.draw.line(glow_surface, (*glow_color[:3], alpha),
                                           (start_offset[0], 10), (end_offset[0], 10), glow_width)
                        except:
                            pass

            # Blit glow surface
            self.screen.blit(glow_surface, (beam_start[0] - beam_length, beam_start[1] - 10))

            # Draw main beam line
            pygame.draw.line(self.screen, beam_color, beam_start, beam_end, 3)
            pygame.draw.line(self.screen, WHITE, beam_start, beam_end, 1)

            # Draw sensor indicator at robot
            sensor_pos = (
                robot.x + (robot.size - 5) * math.cos(sensor_angle),
                robot.y + (robot.size - 5) * math.sin(sensor_angle)
            )
            pygame.draw.circle(self.screen, beam_color, (int(sensor_pos[0]), int(sensor_pos[1])), 3)
            pygame.draw.circle(self.screen, WHITE, (int(sensor_pos[0]), int(sensor_pos[1])), 3, 1)

            # Draw distance indicator at beam end
            if beam_length > 20:  # Only if beam is long enough
                pygame.draw.circle(self.screen, beam_color, (int(beam_end[0]), int(beam_end[1])), 4)
                pygame.draw.circle(self.screen, WHITE, (int(beam_end[0]), int(beam_end[1])), 4, 1)
    
    def draw_hud(self, robot):
        """Draw HUD with robot information"""
        hud_rect = pygame.Rect(10, 10, 300, 120)
        
        # HUD background
        hud_surface = pygame.Surface((300, 120))
        hud_surface.set_alpha(200)
        hud_surface.fill(HUD_BG)
        self.screen.blit(hud_surface, (10, 10))
        
        # HUD border
        pygame.draw.rect(self.screen, HUD_BORDER, hud_rect, 2, border_radius=8)
        
        # HUD content
        font_small = pygame.font.Font(None, 18)
        
        # Icons and values
        hud_items = [
            ("Score", robot.score, PURPLE, self.icon_renderer.draw_star),
            ("Items", robot.items_collected, YELLOW, self.icon_renderer.draw_diamond),
            ("Commands", robot.commands_executed, BLUE, self.icon_renderer.draw_lightning),
            ("Position", f"({robot.x/UNIT_SIZE:.1f}, {robot.y/UNIT_SIZE:.1f})", ROBOT_COLOR, None),
            ("Angle", f"{robot.angle:.1f}°", GREEN, None)
        ]
        
        for i, (label, value, color, icon_func) in enumerate(hud_items):
            y_pos = 25 + i * 20
            
            # Icon
            if icon_func:
                icon_center = (25, y_pos)
                icon_func(self.screen, icon_center, 6, color)
            else:
                pygame.draw.circle(self.screen, color, (25, y_pos), 6)
            
            # Label and value
            label_text = font_small.render(f"{label}:", True, WHITE)
            value_text = font_small.render(str(value), True, color)
            
            self.screen.blit(label_text, (40, y_pos - 8))
            self.screen.blit(value_text, (120, y_pos - 8))
    
    def draw_level_info(self, level, level_start_time, robot):
        """Draw current level information overlay"""
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
        title_text = font_medium.render(f"Level {level.level_id}: {level.name}", True, WHITE)
        self.screen.blit(title_text, (panel_x + 10, panel_y + 10))
        
        # Difficulty
        stars = "⭐" * level.difficulty
        diff_text = font_small.render(f"Difficulty: {stars}", True, CONSOLE_WARNING)
        self.screen.blit(diff_text, (panel_x + 10, panel_y + 30))
        
        # Time
        if level_start_time:
            elapsed = time.time() - level_start_time
            time_text = font_small.render(f"Time: {elapsed:.1f}s", True, CONSOLE_TEXT)
            self.screen.blit(time_text, (panel_x + 10, panel_y + 50))
        
        # Commands
        cmd_text = font_small.render(f"Commands: {robot.commands_executed}", True, CONSOLE_TEXT)
        self.screen.blit(cmd_text, (panel_x + 10, panel_y + 70))
        
        # Quick help
        help_text = font_small.render("F1: Check objectives", True, CONSOLE_PROMPT)
        self.screen.blit(help_text, (panel_x + 10, panel_y + 90))
