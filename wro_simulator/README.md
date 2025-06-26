# WRO Python Robot Control System

## 🎯 Mô tả
Interactive Python system cho học sinh điều khiển robot WRO bằng code:
- **🐍 Python Console**: Gõ lệnh Python trực tiếp, thấy kết quả ngay
- **📐 Grid System**: Hệ tọa độ đơn giản (1 unit = 1 ô grid)
- **📡 Real-time Sensors**: Hiển thị sensor readings live
- **🎮 Visual Feedback**: Robot di chuyển theo code real-time
- **🎓 Educational**: Từ basic commands đến complex algorithms

## 🚀 Cách sử dụng

### Cài đặt và chạy:
```bash
cd wro_simulators/python_control
python3 -m venv venv
source venv/bin/activate
pip install pygame numpy
python python_robot_control.py
```

### Basic Commands:
```python
>>> robot.forward()         # Di chuyển 1 unit (đơn giản!)
>>> robot.left()            # Quay trái 90°
>>> robot.sensor()          # Đọc tất cả sensors
>>> robot.collect()         # Thu thập items
>>> robot.move_to(5, 3)     # Di chuyển đến vị trí (5, 3)
```

### Programming Examples:
```python
# Vẽ hình vuông
>>> for i in range(4): robot.forward(2); robot.right()

# Navigation thông minh
>>> if robot.front_sensor() < 1: robot.left()
... else: robot.forward()

# Function programming
>>> def explore():
...     while not robot.at_target():
...         if robot.front_sensor() < 0.5:
...             robot.avoid_obstacle()
...         else:
...             robot.forward()
>>> explore()
```

## ✨ Key Features
- ✅ **Simple Units**: 1 unit = 1 grid square (thay vì pixels)
- ✅ **Default Values**: `robot.forward()` thay vì `robot.forward(100)`
- ✅ **Interactive Console**: Python REPL với command history
- ✅ **Visual Grid**: Grid lines với coordinates
- ✅ **Real-time Display**: Robot coordinates và sensor readings
- ✅ **Educational Progression**: Từ basic đến advanced
- ✅ **WRO Ready**: Chuẩn bị tốt cho competitions

## 🎓 Learning Path
1. **Level 1**: `robot.forward()`, `robot.left()`, `robot.get_position()`
2. **Level 2**: `robot.sensor()`, conditionals, loops
3. **Level 3**: Functions, algorithms, `robot.move_to(x, y)`
4. **Level 4**: Complex navigation, obstacle avoidance

## 🎮 Controls
- **Type Python commands** trong console bên phải
- **↑↓ arrows**: Command history
- **help()**: Hiển thị tất cả commands
- **ESC**: Thoát program

## 🎯 Perfect for WRO Training
- **Beginner-friendly**: Đơn giản, dễ học
- **Visual learning**: Thấy ngay kết quả code
- **Real programming**: Python syntax thực tế
- **Competition prep**: Logic tương tự WRO robots
