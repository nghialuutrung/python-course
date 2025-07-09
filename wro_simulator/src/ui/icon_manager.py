"""
Font Awesome Icon Manager for WRO Simulator
"""

import pygame
import os

class FontAwesomeIcon:
    """Font Awesome icon renderer using TTF font"""
    
    def __init__(self):
        self.font_path = None
        self.fonts = {}
        self.initialized = False
        
        # Font Awesome icon codes (Unicode)
        self.icons = {
            # Movement and navigation
            'rocket': '\uf135',           # fa-rocket
            'arrows': '\uf047',           # fa-arrows
            'compass': '\uf14e',          # fa-compass
            'location-arrow': '\uf124',   # fa-location-arrow
            'route': '\uf4d7',           # fa-route
            
            # Collection and items
            'gem': '\uf3a5',             # fa-gem
            'diamond': '\uf219',         # fa-diamond
            'treasure-chest': '\uf507',   # fa-treasure-chest
            
            # Technology and sensors
            'wifi': '\uf1eb',            # fa-wifi
            'radar': '\uf924',           # fa-radar (Font Awesome Pro)
            'satellite': '\uf7bf',       # fa-satellite
            'microchip': '\uf2db',       # fa-microchip
            
            # Speed and time
            'clock': '\uf017',           # fa-clock
            'stopwatch': '\uf2f2',       # fa-stopwatch
            'tachometer': '\uf0e4',      # fa-tachometer
            'bolt': '\uf0e7',            # fa-bolt
            
            # General UI
            'star': '\uf005',            # fa-star
            'check': '\uf00c',           # fa-check
            'lock': '\uf023',            # fa-lock
            'play': '\uf04b',            # fa-play
            'cog': '\uf013',             # fa-cog
            'info': '\uf129',            # fa-info
            'question': '\uf128',        # fa-question
            
            # Arrows and directions
            'arrow-up': '\uf062',        # fa-arrow-up
            'arrow-down': '\uf063',      # fa-arrow-down
            'chevron-up': '\uf077',      # fa-chevron-up
            'chevron-down': '\uf078',    # fa-chevron-down

            # Additional icons
            'list': '\uf03a',            # fa-list
            'clipboard': '\uf328',       # fa-clipboard-list
            'lightbulb': '\uf0eb',       # fa-lightbulb
        }
    
    def load_font_awesome(self):
        """Load Font Awesome font file"""
        # Try to find Font Awesome font in common locations
        possible_paths = [
            # Local project paths (relative to wro_simulator directory)
            'assets/fonts/fa-solid-900.ttf',
            'assets/fonts/fontawesome-webfont.ttf',
            'fonts/fa-solid-900.ttf',

            # Absolute paths from project root
            os.path.join(os.path.dirname(__file__), '../../assets/fonts/fa-solid-900.ttf'),

            # System paths (macOS) - fallback
            '/System/Library/Fonts/Helvetica.ttc',  # Fallback
            '/Library/Fonts/Arial.ttf',             # Fallback

            # Try to use system default
            None  # Will use pygame default
        ]
        
        for path in possible_paths:
            try:
                if path is None:
                    # Use pygame default font as fallback
                    self.fonts[16] = pygame.font.Font(None, 16)
                    self.fonts[18] = pygame.font.Font(None, 18)
                    self.fonts[20] = pygame.font.Font(None, 20)
                    self.fonts[24] = pygame.font.Font(None, 24)
                    print("Using pygame default font (Font Awesome not available)")
                    break
                elif os.path.exists(path):
                    self.font_path = path
                    # Load different sizes
                    self.fonts[16] = pygame.font.Font(path, 16)
                    self.fonts[18] = pygame.font.Font(path, 18)
                    self.fonts[20] = pygame.font.Font(path, 20)
                    self.fonts[24] = pygame.font.Font(path, 24)
                    print(f"Loaded Font Awesome from: {path}")
                    break
            except Exception as e:
                continue
        
        # If no font loaded, use fallback
        if not self.fonts:
            self.fonts[16] = pygame.font.Font(None, 16)
            self.fonts[18] = pygame.font.Font(None, 18)
            self.fonts[20] = pygame.font.Font(None, 20)
            self.fonts[24] = pygame.font.Font(None, 24)
            print("Using fallback font")
    
    def get_icon_text(self, icon_name):
        """Get icon unicode character or fallback text"""
        if self.font_path and icon_name in self.icons:
            return self.icons[icon_name]
        else:
            # Fallback to better text representations
            fallbacks = {
                'rocket': '▲',        # Movement
                'arrows': '↔',        # Navigation
                'compass': '⊕',       # Pathfinding
                'location-arrow': '→', # Direction
                'route': '~',         # Route
                'gem': '◆',           # Collection
                'diamond': '♦',       # Diamond
                'treasure-chest': '■', # Treasure
                'wifi': '≈',          # Sensors/Wifi
                'radar': '◉',         # Radar
                'satellite': '●',     # Satellite
                'microchip': '▣',     # Microchip
                'clock': '○',         # Time
                'stopwatch': '◐',     # Stopwatch
                'tachometer': '⊙',    # Speed
                'bolt': '⚡',         # Lightning/Speed
                'star': '★',          # Star
                'check': '✓',         # Check mark
                'lock': '⚿',          # Lock
                'play': '▶',          # Play
                'cog': '⚙',           # Settings/Cog
                'info': 'ⓘ',          # Info
                'question': '?',      # Question
                'arrow-up': '▲',      # Up arrow
                'arrow-down': '▼',    # Down arrow
                'chevron-up': '▲',    # Chevron up
                'chevron-down': '▼',  # Chevron down
                'list': '≡',          # List
                'clipboard': '📋',    # Clipboard
                'lightbulb': '💡',    # Lightbulb
            }
            return fallbacks.get(icon_name, '•')
    
    def render_icon(self, icon_name, size=20, color=(255, 255, 255)):
        """Render an icon and return the surface"""
        if not self.initialized:
            self.load_font_awesome()
            self.initialized = True

        font = self.fonts.get(size, self.fonts.get(20, self.fonts[16]))
        icon_text = self.get_icon_text(icon_name)
        return font.render(icon_text, True, color)
    
    def draw_icon(self, surface, icon_name, pos, size=20, color=(255, 255, 255)):
        """Draw an icon directly to a surface"""
        if not self.initialized:
            self.load_font_awesome()
            self.initialized = True

        icon_surface = self.render_icon(icon_name, size, color)
        icon_rect = icon_surface.get_rect(center=pos)
        surface.blit(icon_surface, icon_rect)
        return icon_rect

# Global icon manager instance
icon_manager = FontAwesomeIcon()

def get_level_icon(level_id):
    """Get appropriate icon for each level"""
    level_icons = {
        1: 'rocket',           # Movement
        2: 'arrows',           # Navigation  
        3: 'gem',              # Collection
        4: 'wifi',             # Sensors
        5: 'compass',          # Pathfinding
        6: 'bolt',             # Speed
    }
    return level_icons.get(level_id, 'cog')

def get_level_icon_color(level_id, completed=False):
    """Get appropriate color for each level icon"""
    if completed:
        return (100, 255, 100)  # Green for completed
    
    level_colors = {
        1: (100, 150, 255),    # Blue for movement
        2: (255, 150, 100),    # Orange for navigation
        3: (255, 215, 0),      # Gold for collection
        4: (150, 255, 150),    # Light green for sensors
        5: (255, 100, 255),    # Magenta for pathfinding
        6: (255, 255, 100),    # Yellow for speed
    }
    return level_colors.get(level_id, (200, 200, 200))
