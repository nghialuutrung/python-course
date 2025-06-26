"""
Level Selection Screen UI
"""

import pygame
from ..core.constants import *


class LevelSelectScreen:
    """Beautiful level selection screen"""
    
    def __init__(self, level_manager):
        self.level_manager = level_manager
        # Start with first available level
        available_levels = self.level_manager.get_available_levels()
        self.selected_level = available_levels[0] if available_levels else 1
        self.scroll_offset = 0  # For scrolling through levels
        self.font_large = pygame.font.Font(None, 42)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
    def handle_key(self, key):
        """Handle keyboard input for level selection"""
        available_levels = self.level_manager.get_available_levels()

        if key == pygame.K_UP:
            current_index = available_levels.index(self.selected_level) if self.selected_level in available_levels else 0
            new_index = max(0, current_index - 1)
            self.selected_level = available_levels[new_index]

            # Auto-scroll if needed
            if new_index < self.scroll_offset:
                self.scroll_offset = new_index

        elif key == pygame.K_DOWN:
            current_index = available_levels.index(self.selected_level) if self.selected_level in available_levels else 0
            new_index = min(len(available_levels) - 1, current_index + 1)
            self.selected_level = available_levels[new_index]

            # Auto-scroll if needed
            max_visible = 5  # Approximate visible cards
            if new_index >= self.scroll_offset + max_visible:
                self.scroll_offset = new_index - max_visible + 1
            
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

        # Scroll indicators
        self.draw_scroll_indicators(screen)

        # Footer with instructions and progress
        self.draw_footer(screen)
    
    def draw_gradient_background(self, screen):
        """Draw gradient background"""
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
        shadow_text = self.font_large.render("WRO Robot Programming Academy", True, (20, 20, 20))
        main_text = self.font_large.render("WRO Robot Programming Academy", True, WHITE)
        
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
        
        # Subtitle with level count
        total_levels = len(self.level_manager.levels)
        available_levels = len(self.level_manager.get_available_levels())
        subtitle_text = f"Master Python Programming • {available_levels}/{total_levels} Levels Available"
        subtitle_surface = self.font_medium.render(subtitle_text, True, (150, 200, 255))
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH//2, 75))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Decorative line
        line_y = 95
        pygame.draw.line(screen, (100, 150, 200), (100, line_y), (SCREEN_WIDTH - 100, line_y), 2)
    
    def draw_level_cards(self, screen):
        """Draw beautiful level cards with detailed info"""
        start_y = 120
        card_height = 80  # Reduced height to fit more cards
        card_spacing = 6   # Reduced spacing
        card_width = SCREEN_WIDTH - 160

        # Calculate how many cards can fit on screen
        available_height = SCREEN_HEIGHT - start_y - 100  # Leave space for footer
        max_visible_cards = available_height // (card_height + card_spacing)

        # Get all levels and apply scrolling
        all_levels = sorted(self.level_manager.levels.keys())
        total_levels = len(all_levels)

        # Ensure scroll offset is within bounds
        max_scroll = max(0, total_levels - max_visible_cards)
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))

        # Only show visible levels
        visible_levels = all_levels[self.scroll_offset:self.scroll_offset + max_visible_cards]

        for i, level_id in enumerate(visible_levels):
            level = self.level_manager.get_level(level_id)
            is_unlocked = self.level_manager.is_level_unlocked(level_id)
            is_selected = level_id == self.selected_level
            
            # Card position using visible index
            card_y = start_y + i * (card_height + card_spacing)
            card_rect = pygame.Rect(80, card_y, card_width, card_height)
            
            # Draw the card
            self.draw_level_card(screen, card_rect, level, is_unlocked, is_selected)
    
    def draw_level_card(self, screen, card_rect, level, is_unlocked, is_selected):
        """Draw individual level card with modern styling"""
        # Card shadow
        shadow_rect = pygame.Rect(card_rect.x + 3, card_rect.y + 3, card_rect.width, card_rect.height)
        pygame.draw.rect(screen, (10, 10, 10), shadow_rect, border_radius=12)
        
        # Card background with gradient effect
        if is_selected and is_unlocked:
            self.draw_card_gradient(screen, card_rect, (70, 130, 220), (50, 110, 200))
            border_color = (255, 255, 255)
            border_width = 3
        elif is_unlocked:
            self.draw_card_gradient(screen, card_rect, (45, 55, 75), (35, 45, 65))
            border_color = (100, 150, 200)
            border_width = 2
        else:
            self.draw_card_gradient(screen, card_rect, (30, 30, 30), (20, 20, 20))
            border_color = (60, 60, 60)
            border_width = 1
        
        # Card border
        pygame.draw.rect(screen, border_color, card_rect, border_width, border_radius=12)
        
        # Level content
        self.draw_card_content(screen, card_rect, level, is_unlocked)
    
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
    
    def draw_card_content(self, screen, card_rect, level, is_unlocked):
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
            # Level title - more compact
            title_font = pygame.font.Font(None, 22)
            level_title = f"Level {level.level_id}: {level.name}"
            title_text = title_font.render(level_title, True, WHITE)
            screen.blit(title_text, (text_x, card_rect.y + 6))

            # Description - smaller font
            desc_text = self.font_small.render(level.description, True, (200, 200, 200))
            screen.blit(desc_text, (text_x, card_rect.y + 26))

            # Compact difficulty and type info
            stars = "⭐" * level.difficulty

            # Level type indicators - shorter
            level_types = {
                1: "🚀 Movement",
                2: "🔄 Navigation",
                3: "💎 Collection",
                4: "📡 Sensors",
                5: "🧭 Pathfinding",
                6: "⏱️ Speed"
            }

            type_indicator = level_types.get(level.level_id, "🎯 Challenge")
            difficulty_text = f"{type_indicator} • {stars}"
            stars_text = self.font_small.render(difficulty_text, True, (255, 215, 0))
            screen.blit(stars_text, (text_x, card_rect.y + 44))
            
            # Status and completion info - more compact
            if level.completed:
                status_text = self.font_small.render("✅ Done", True, (100, 255, 100))
                screen.blit(status_text, (text_x, card_rect.y + 60))

                # Best time - more compact
                if level.best_time:
                    time_text = self.font_small.render(f"{level.best_time:.1f}s", True, (150, 200, 255))
                    screen.blit(time_text, (card_rect.right - 80, card_rect.y + 60))
            else:
                status_text = self.font_small.render("🎯 Ready", True, (100, 200, 255))
                screen.blit(status_text, (text_x, card_rect.y + 60))
        else:
            # Locked level
            title_text = self.font_medium.render(f"Level {level.level_id}: ???", True, (120, 120, 120))
            screen.blit(title_text, (text_x, card_rect.y + 15))
            
            lock_desc = self.font_small.render("Complete previous level to unlock", True, (100, 100, 100))
            screen.blit(lock_desc, (text_x, card_rect.y + 40))

    def draw_scroll_indicators(self, screen):
        """Draw scroll indicators if needed"""
        all_levels = sorted(self.level_manager.levels.keys())
        total_levels = len(all_levels)

        # Calculate visible range
        available_height = SCREEN_HEIGHT - 120 - 100  # start_y to footer
        card_height = 80
        card_spacing = 6
        max_visible_cards = available_height // (card_height + card_spacing)

        if total_levels > max_visible_cards:
            # Show scroll up indicator
            if self.scroll_offset > 0:
                up_text = self.font_small.render("▲ More levels above", True, (150, 150, 255))
                screen.blit(up_text, (SCREEN_WIDTH - 200, 100))

            # Show scroll down indicator
            if self.scroll_offset + max_visible_cards < total_levels:
                down_text = self.font_small.render("▼ More levels below", True, (150, 150, 255))
                screen.blit(down_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150))

    def draw_footer(self, screen):
        """Draw footer with instructions and progress"""
        footer_y = SCREEN_HEIGHT - 120
        
        # Footer background
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
        progress = self.level_manager.get_progress()
        completed = progress['completed_levels']
        total = progress['total_levels']
        
        progress_text = self.font_small.render(f"Completed: {completed}/{total} levels", True, (200, 255, 200))
        screen.blit(progress_text, (progress_panel_rect.x + 15, progress_panel_rect.y + 30))
        
        # Progress bar
        bar_width = 200
        bar_height = 8
        bar_x = progress_panel_rect.x + 15
        bar_y = progress_panel_rect.y + 50
        
        # Background bar
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=4)
        
        # Progress bar fill
        if total > 0:
            fill_width = int((completed / total) * bar_width)
            if fill_width > 0:
                pygame.draw.rect(screen, (100, 255, 100), (bar_x, bar_y, fill_width, bar_height), border_radius=4)
        
        # Percentage
        percentage = int(progress['completion_percentage'])
        percent_text = self.font_small.render(f"{percentage}%", True, (150, 255, 150))
        screen.blit(percent_text, (bar_x + bar_width + 10, bar_y - 2))
