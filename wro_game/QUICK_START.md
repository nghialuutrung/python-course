# [START] Quick Start Guide - WRO Game Practice

## Installation and Running

### Step 1: Setup Environment
```bash
./setup.sh
```

### Step 2: Run Game
```bash
./start_game.sh
```

## How to Play

### 1. Main Menu
- **Start Game**: Go to level selection screen
- **Instructions**: View detailed instructions
- **Exit**: Exit game

### 2. Select Level
- Choose level to play (only unlocked levels)
- Level 1 is always available to play

### 3. Playing Game
- **Click "[CODE] Editor"** to open code editor
- **Write code** to control robot
- **Click "[RUN] Code"** to execute
- **Watch robot** move in simulation area

### 4. Basic Commands (Level 1)
```python
robot.move_forward()    # Move forward
robot.move_backward()   # Move backward
robot.turn_left()       # Turn left 90 degrees
robot.turn_right()      # Turn right 90 degrees
robot.stop()           # Stop robot
```

### 5. Simple Code Example
```python
# Move robot in a square pattern
robot.move_forward()
robot.turn_right()
robot.move_forward()
robot.turn_right()
robot.move_forward()
robot.turn_right()
robot.move_forward()
robot.turn_right()
```

## Hotkeys
- **ESC**: Back to previous menu
- **C**: Open Code Editor (in playing mode)
- **R**: Reset level (in playing mode)

## Level 1 Objective
- Control robot to reach green target points
- Complete all target points to unlock next level

## Common Issues

### Game Won't Run
1. Check Python 3.8+ is installed
2. Run `./setup.sh` again
3. Check virtual environment: `source venv/bin/activate`

### Code Editor Won't Open
1. Ensure tkinter is available (usually comes with Python)
2. Try restarting game

### Robot Won't Move
1. Check code syntax
2. Make sure you clicked "🚀 Run Code"
3. Check console for errors

## For Teachers
- See `TEACHER_GUIDE.md` for detailed instructions
- Can customize levels in `game/levels/` directory

## Support
If you encounter issues, please:
1. Check README.md file
2. See TEACHER_GUIDE.md
3. Check console for error messages

---
**Happy Learning! [ROBOT][GAME]**
