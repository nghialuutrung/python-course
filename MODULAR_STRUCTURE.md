# 🏗️ WRO Robot Control - Modular Architecture

## 📁 Project Structure

```
wro_simulator/
├── src/                          # Source code
│   ├── core/                     # Core game logic
│   │   ├── __init__.py
│   │   ├── constants.py          # Game constants and colors
│   │   ├── robot.py              # Robot class with all commands
│   │   ├── level.py              # Base level class and objectives
│   │   └── level_manager.py      # Level loading and progression
│   │
│   ├── ui/                       # User interface components
│   │   ├── __init__.py
│   │   ├── level_select.py       # Beautiful level selection screen
│   │   ├── console.py            # Interactive Python console
│   │   └── game_renderer.py      # Game graphics and HUD
│   │
│   ├── levels/                   # Individual level definitions
│   │   ├── __init__.py           # Level creation guide
│   │   ├── level_01.py           # Level 1: First Steps
│   │   ├── level_02.py           # Level 2: Turn Around
│   │   ├── level_03.py           # Level 3: Treasure Hunt
│   │   └── level_XX.py           # Add new levels here
│   │
│   ├── utils/                    # Utility functions (future)
│   │   └── __init__.py
│   │
│   ├── __init__.py
│   └── main.py                   # Main application class
│
├── run_game.py                   # Main launcher script
├── requirements.txt              # Dependencies
├── setup.sh                     # Setup script
├── run.sh                       # Run script
└── README.md                    # Documentation
```

## 🎯 How to Add New Levels

### Step 1: Create Level File
Create a new file in `src/levels/` following the naming convention:
```
src/levels/level_04.py  # For level 4
src/levels/level_05.py  # For level 5
```

### Step 2: Implement Level Class
```python
# src/levels/level_04.py
from ..core.level import BaseLevel

class Level04(BaseLevel):
    """Level 4: Your Level Name"""
    
    def setup_level(self):
        """Setup Level 4 content"""
        # Basic info
        self.level_id = 4
        self.name = "Sensor Navigation"
        self.description = "Use sensors to navigate safely"
        self.difficulty = 2  # 1-5 stars
        
        # Add objectives
        self.add_objective(
            'use_sensors',
            'Use sensors at least 3 times',
            sensor_calls=3
        )
        
        self.add_objective(
            'reach_target',
            'Reach the target position (9, 9)',
            target=(9, 9),
            tolerance=1.0
        )
        
        # Add obstacles
        self.add_obstacle(200, 100, 50, 200)
        self.add_obstacle(350, 250, 100, 50)
        
        # Add items (optional)
        self.add_item(150, 150, 'coin')
        
        # Set target area
        self.set_target_area(400, 400, 100, 100)
        
        # Add hints
        self.add_hint("Use robot.sensor() to check distances")
        self.add_hint("Check sensors before moving")
        self.add_hint("if robot.front_sensor() < 1: robot.left()")
```

### Step 3: Level Auto-Loading
The level will be automatically loaded by `LevelManager` when the game starts. No additional configuration needed!

## 🎮 Available Objective Types

### 1. Reach Target
```python
self.add_objective(
    'reach_target',
    'Reach position (x, y)',
    target=(x, y),
    tolerance=1.0  # Distance tolerance
)
```

### 2. Collect Items
```python
self.add_objective(
    'collect_items',
    'Collect N items',
    count=N
)
```

### 3. Use Sensors
```python
self.add_objective(
    'use_sensors',
    'Use sensors N times',
    sensor_calls=N
)
```

### 4. Efficient Path
```python
self.add_objective(
    'efficient_path',
    'Complete with max N commands',
    max_commands=N
)
```

### 5. Avoid Obstacles
```python
self.add_objective(
    'avoid_obstacles',
    'Don\'t hit any obstacles'
)
```

## 🏗️ Level Building Methods

### Add Obstacles
```python
self.add_obstacle(x, y, width, height)
```

### Add Items
```python
self.add_item(x, y, 'coin')  # Item type: 'coin', 'gem', etc.
```

### Set Target Area
```python
self.set_target_area(x, y, width, height)
```

### Add Hints
```python
self.add_hint("Helpful tip for students")
```

### Set Difficulty
```python
self.difficulty = 1  # 1=Easy, 2=Medium, 3=Hard, 4=Expert, 5=Master
```

## 🎨 Customization Options

### Time Limits
```python
self.time_limit = 60.0  # 60 seconds, None for unlimited
```

### Restricted Commands
```python
self.allowed_commands = ['forward', 'left', 'right', 'sensor']
```

### Custom Scoring
Override the `get_score()` method for custom scoring logic.

## 🚀 Example: Complete Level Template

```python
# src/levels/level_05.py
from ..core.level import BaseLevel

class Level05(BaseLevel):
    """Level 5: Advanced Challenge"""
    
    def setup_level(self):
        # Basic setup
        self.level_id = 5
        self.name = "Maze Master"
        self.description = "Navigate through a complex maze"
        self.difficulty = 3
        
        # Multiple objectives
        self.add_objective('reach_target', 'Reach the exit', target=(15, 12))
        self.add_objective('collect_items', 'Collect 3 keys', count=3)
        self.add_objective('efficient_path', 'Use max 20 commands', max_commands=20)
        
        # Complex maze
        self.add_obstacle(100, 100, 300, 50)   # Top wall
        self.add_obstacle(100, 100, 50, 200)   # Left wall
        self.add_obstacle(200, 200, 200, 50)   # Middle barrier
        
        # Key items
        self.add_item(150, 250, 'key')
        self.add_item(350, 150, 'key')
        self.add_item(450, 300, 'key')
        
        # Exit area
        self.set_target_area(700, 550, 80, 80)
        
        # Progressive hints
        self.add_hint("Plan your route to collect all keys")
        self.add_hint("Use sensors to avoid walls")
        self.add_hint("Try to minimize backtracking")
        
        # Optional: Time challenge
        self.time_limit = 120.0  # 2 minutes
```

## 🔧 Advanced Features

### Custom Objective Types
Extend the `Objective.check_completion()` method to create custom objectives.

### Dynamic Environments
Modify obstacles/items during gameplay by overriding level methods.

### Interactive Elements
Add moving obstacles, switches, or other interactive elements.

### Branching Paths
Create levels that unlock different paths based on performance.

## 📚 Educational Progression

### Beginner Levels (1-2 ⭐)
- Basic movement commands
- Simple navigation
- Introduction to sensors

### Intermediate Levels (3 ⭐)
- Complex navigation
- Item collection
- Basic programming concepts

### Advanced Levels (4-5 ⭐)
- Algorithm optimization
- Complex problem solving
- Advanced programming patterns

## 🎯 Best Practices

1. **Progressive Difficulty**: Each level should build on previous concepts
2. **Clear Objectives**: Make goals obvious and achievable
3. **Helpful Hints**: Provide guidance without giving away solutions
4. **Visual Clarity**: Use appropriate obstacle and item placement
5. **Testing**: Test levels thoroughly for different solution approaches

## 🚀 Getting Started

1. **Run the game**: `python run_game.py`
2. **Create your level**: Copy `level_03.py` as a template
3. **Test and iterate**: Adjust difficulty and objectives
4. **Share with students**: Levels auto-load on restart

Happy level creating! 🎮✨
