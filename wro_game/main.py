#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WRO Game Practice - Main Entry Point
WRO robotics programming practice game for 8th grade students
"""

import pygame
import sys
import os

# Thêm thư mục game vào path
sys.path.append(os.path.join(os.path.dirname(__file__), 'game'))

from game.robot_game import WROGameManager

def main():
    """Main function to launch the game"""
    try:
        # Initialize pygame
        pygame.init()

        # Create game manager
        game_manager = WROGameManager()

        # Run game
        game_manager.run()

    except Exception as e:
        print(f"Error running game: {e}")
        input("Press Enter to exit...")

    finally:
        # Ensure pygame is properly closed
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("[ROBOT] Welcome to WRO Game Practice!")
    print("[GAME] Starting game...")
    main()
