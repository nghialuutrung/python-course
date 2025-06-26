"""
Programming Guide UI Component
Shows code examples and tutorials for each level
"""

import pygame
from ..core.constants import *

class ProgrammingGuide:
    """Display programming examples and tutorials"""
    
    def __init__(self, screen):
        self.screen = screen
        self.visible = False
        self.current_level = None
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Fonts
        self.title_font = pygame.font.Font(None, 24)
        self.subtitle_font = pygame.font.Font(None, 20)
        self.code_font = pygame.font.Font(None, 16)
        self.text_font = pygame.font.Font(None, 18)
        
        # Colors
        self.bg_color = (30, 30, 40, 240)
        self.title_color = (255, 215, 0)
        self.subtitle_color = (100, 200, 255)
        self.code_bg_color = (20, 20, 30)
        self.code_text_color = (200, 255, 200)
        self.comment_color = (150, 150, 150)
        self.keyword_color = (255, 150, 100)
        
        # Guide panel dimensions
        self.panel_width = 600
        self.panel_height = 500
        self.panel_x = (SCREEN_WIDTH - self.panel_width) // 2
        self.panel_y = (SCREEN_HEIGHT - self.panel_height) // 2
        
    def show(self, level):
        """Show programming guide for specific level"""
        self.current_level = level
        self.visible = True
        self.scroll_offset = 0
        
    def hide(self):
        """Hide programming guide"""
        self.visible = False
        
    def handle_event(self, event):
        """Handle input events"""
        if not self.visible:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_F1:
                self.hide()
                return True
            elif event.key == pygame.K_UP:
                self.scroll_offset = max(0, self.scroll_offset - 30)
                return True
            elif event.key == pygame.K_DOWN:
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + 30)
                return True
                
        elif event.type == pygame.MOUSEWHEEL:
            if self.is_mouse_over_panel():
                self.scroll_offset = max(0, min(self.max_scroll, 
                                               self.scroll_offset - event.y * 30))
                return True
                
        return False
    
    def is_mouse_over_panel(self):
        """Check if mouse is over the guide panel"""
        mouse_pos = pygame.mouse.get_pos()
        return (self.panel_x <= mouse_pos[0] <= self.panel_x + self.panel_width and
                self.panel_y <= mouse_pos[1] <= self.panel_y + self.panel_height)
    
    def draw(self):
        """Draw programming guide"""
        if not self.visible or not self.current_level:
            return
            
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Main panel background
        panel_surface = pygame.Surface((self.panel_width, self.panel_height), pygame.SRCALPHA)
        panel_surface.fill(self.bg_color)
        pygame.draw.rect(panel_surface, (100, 100, 120), 
                        (0, 0, self.panel_width, self.panel_height), 2)
        
        # Create scrollable content surface
        content_height = self.calculate_content_height()
        self.max_scroll = max(0, content_height - self.panel_height + 60)
        
        content_surface = pygame.Surface((self.panel_width - 40, content_height), pygame.SRCALPHA)
        self.draw_content(content_surface)
        
        # Clip content to panel area
        content_rect = pygame.Rect(20, 20 - self.scroll_offset, 
                                  self.panel_width - 40, self.panel_height - 40)
        panel_surface.blit(content_surface, (20, 20), 
                          (0, self.scroll_offset, self.panel_width - 40, self.panel_height - 40))
        
        # Draw scroll indicator
        if self.max_scroll > 0:
            self.draw_scroll_indicator(panel_surface)
        
        # Draw close instruction
        close_text = self.text_font.render("Press ESC or F1 to close", True, (200, 200, 200))
        panel_surface.blit(close_text, (10, self.panel_height - 25))
        
        self.screen.blit(panel_surface, (self.panel_x, self.panel_y))
    
    def calculate_content_height(self):
        """Calculate total height of content"""
        height = 0
        
        # Title
        height += 40
        
        # Level info
        height += 60
        
        # Programming examples
        if hasattr(self.current_level, 'get_programming_examples'):
            examples = self.current_level.get_programming_examples()
            for example in examples:
                height += 30  # Example title
                code_lines = example['code'].strip().split('\n')
                height += len(code_lines) * 20 + 40  # Code + padding
        
        # Level-specific commands
        if hasattr(self.current_level, 'get_level_specific_commands'):
            height += 40  # Commands title
            commands = self.current_level.get_level_specific_commands()
            height += len(commands) * 25 + 20
        
        return height + 100  # Extra padding
    
    def draw_content(self, surface):
        """Draw the scrollable content"""
        y = 0
        
        # Title
        title = f"Programming Guide - Level {self.current_level.level_id}"
        title_surface = self.title_font.render(title, True, self.title_color)
        surface.blit(title_surface, (0, y))
        y += 40
        
        # Level description
        desc_surface = self.text_font.render(self.current_level.description, True, WHITE)
        surface.blit(desc_surface, (0, y))
        y += 30
        
        difficulty_text = f"Difficulty: {'⭐' * self.current_level.difficulty}"
        diff_surface = self.text_font.render(difficulty_text, True, (255, 215, 0))
        surface.blit(diff_surface, (0, y))
        y += 40
        
        # Programming examples
        if hasattr(self.current_level, 'get_programming_examples'):
            examples = self.current_level.get_programming_examples()
            
            examples_title = self.subtitle_font.render("📚 Programming Examples:", True, self.subtitle_color)
            surface.blit(examples_title, (0, y))
            y += 35
            
            for example in examples:
                # Example title
                example_title = self.text_font.render(f"• {example['title']}", True, WHITE)
                surface.blit(example_title, (20, y))
                y += 30
                
                # Code block
                y = self.draw_code_block(surface, example['code'], 40, y)
                y += 20
        
        # Level-specific commands
        if hasattr(self.current_level, 'get_level_specific_commands'):
            commands = self.current_level.get_level_specific_commands()
            
            commands_title = self.subtitle_font.render("🔧 Key Commands for This Level:", True, self.subtitle_color)
            surface.blit(commands_title, (0, y))
            y += 35
            
            for command in commands:
                if command.startswith('#'):
                    # Comment
                    cmd_surface = self.code_font.render(command, True, self.comment_color)
                else:
                    # Command
                    cmd_surface = self.code_font.render(f"  {command}", True, self.code_text_color)
                surface.blit(cmd_surface, (20, y))
                y += 25
    
    def draw_code_block(self, surface, code, x, y):
        """Draw a syntax-highlighted code block"""
        lines = code.strip().split('\n')
        
        # Calculate code block dimensions
        max_width = max(self.code_font.size(line)[0] for line in lines) + 20
        block_height = len(lines) * 20 + 20
        
        # Draw code background
        code_bg = pygame.Rect(x, y, max_width, block_height)
        pygame.draw.rect(surface, self.code_bg_color, code_bg)
        pygame.draw.rect(surface, (60, 60, 80), code_bg, 1)
        
        # Draw code lines with basic syntax highlighting
        for i, line in enumerate(lines):
            line_y = y + 10 + i * 20
            self.draw_syntax_highlighted_line(surface, line, x + 10, line_y)
        
        return y + block_height
    
    def draw_syntax_highlighted_line(self, surface, line, x, y):
        """Draw a line with basic syntax highlighting"""
        # Simple syntax highlighting
        if line.strip().startswith('#'):
            # Comment
            text_surface = self.code_font.render(line, True, self.comment_color)
        elif any(keyword in line for keyword in ['def ', 'if ', 'elif ', 'else:', 'for ', 'while ', 'import ', 'from ']):
            # Keywords
            text_surface = self.code_font.render(line, True, self.keyword_color)
        else:
            # Regular code
            text_surface = self.code_font.render(line, True, self.code_text_color)
        
        surface.blit(text_surface, (x, y))
    
    def draw_scroll_indicator(self, surface):
        """Draw scroll indicator"""
        if self.max_scroll <= 0:
            return
            
        # Scroll bar background
        bar_x = self.panel_width - 15
        bar_y = 20
        bar_height = self.panel_height - 60
        pygame.draw.rect(surface, (60, 60, 80), (bar_x, bar_y, 10, bar_height))
        
        # Scroll thumb
        thumb_height = max(20, int(bar_height * (self.panel_height - 40) / (self.max_scroll + self.panel_height - 40)))
        thumb_y = bar_y + int((bar_height - thumb_height) * self.scroll_offset / self.max_scroll)
        pygame.draw.rect(surface, (120, 120, 140), (bar_x, thumb_y, 10, thumb_height))
