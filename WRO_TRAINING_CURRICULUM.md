# 🏆 WRO Robot Programming Training Curriculum

## 📚 **Học sinh đã biết (Python Fundamentals):**
- ✅ Điều kiện (if/elif/else)
- ✅ Vòng lặp (for/while)
- ✅ So sánh và toán tử logic
- ✅ Functions và parameters
- ✅ Dữ liệu phức tạp (lists, dictionaries)

## 🎯 **Mục tiêu: Áp dụng vào WRO Competition Programming**

---

## 📖 **PHASE 1: WRO Programming Fundamentals (Levels 4-6)**

### 🤖 **Level 4: Sensor-Based Navigation**
**Objective**: Học sử dụng sensors để điều hướng

**Python Concepts Applied**:
```python
# Điều kiện với sensor readings
sensor_data = robot.sensor()
if sensor_data['front'] < 2:
    robot.right()
    robot.forward()

# Function để check obstacles
def is_path_clear():
    return robot.front_sensor() > 1.5

# Vòng lặp với sensor feedback
while not is_path_clear():
    robot.right()
```

**WRO Skills Learned**:
- Sensor-based decision making
- Obstacle avoidance algorithms
- Real-time environment analysis

---

### 🎯 **Level 5: Pathfinding Algorithms**
**Objective**: Tìm đường tối ưu đến target

**Python Concepts Applied**:
```python
# Lists để lưu path
path = []
visited = []

# Function để tìm đường
def find_path_to_target():
    current_pos = robot.sensor()['position']
    target_pos = (8, 8)
    
    # Algorithm logic using loops and conditions
    while current_pos != target_pos:
        # Decision making logic
        pass

# Dictionary để map directions
directions = {
    'north': (0, -1),
    'south': (0, 1),
    'east': (1, 0),
    'west': (-1, 0)
}
```

**WRO Skills Learned**:
- Basic pathfinding algorithms
- Grid-based navigation
- Optimal route planning

---

### 🏃 **Level 6: Time-Optimized Missions**
**Objective**: Hoàn thành nhiệm vụ trong thời gian giới hạn

**Python Concepts Applied**:
```python
import time

# Function với time tracking
def timed_mission(time_limit):
    start_time = time.time()
    
    while time.time() - start_time < time_limit:
        # Mission logic
        if mission_completed():
            return True
    
    return False

# Optimization với loops
def optimize_collection_route(items):
    # Sort items by distance for efficiency
    sorted_items = sorted(items, key=lambda x: distance_to(x))
    
    for item in sorted_items:
        navigate_to(item)
        robot.collect()
```

**WRO Skills Learned**:
- Time management in competitions
- Route optimization
- Performance measurement

---

## 🚀 **PHASE 2: Advanced WRO Strategies (Levels 7-9)**

### 🧭 **Level 7: Multi-Sensor Fusion**
**Objective**: Kết hợp nhiều sensor để ra quyết định

**Python Concepts Applied**:
```python
# Dictionary để store sensor history
sensor_history = {
    'front': [],
    'left': [],
    'right': []
}

# Function phân tích sensor data
def analyze_environment():
    sensors = robot.sensor()
    
    # Update history (lists)
    for direction in sensor_history:
        sensor_history[direction].append(sensors[direction])
        if len(sensor_history[direction]) > 5:
            sensor_history[direction].pop(0)
    
    # Decision making với multiple conditions
    if all(reading > 3 for reading in sensor_history['front']):
        return "safe_forward"
    elif min(sensor_history['left']) > min(sensor_history['right']):
        return "turn_left"
    else:
        return "turn_right"
```

**WRO Skills Learned**:
- Sensor data fusion
- Historical data analysis
- Complex decision trees

---

### 🎪 **Level 8: Dynamic Obstacle Courses**
**Objective**: Xử lý môi trường thay đổi động

**Python Concepts Applied**:
```python
# Class để model environment state
class EnvironmentMap:
    def __init__(self):
        self.obstacles = []
        self.safe_zones = []
        self.items = []
    
    def update_from_sensors(self, sensor_data):
        # Update map based on new sensor readings
        pass
    
    def find_safe_path(self, start, end):
        # Pathfinding algorithm
        pass

# Main navigation loop
env_map = EnvironmentMap()

while not mission_complete():
    # Continuous environment mapping
    sensor_data = robot.sensor()
    env_map.update_from_sensors(sensor_data)
    
    # Adaptive navigation
    next_move = env_map.find_safe_path(
        robot.sensor()['position'], 
        target_position
    )
    
    execute_move(next_move)
```

**WRO Skills Learned**:
- Dynamic environment mapping
- Adaptive algorithms
- Real-time strategy adjustment

---

### 🏆 **Level 9: Competition Simulation**
**Objective**: Mô phỏng thi đấu WRO thực tế

**Python Concepts Applied**:
```python
# Competition strategy class
class WROStrategy:
    def __init__(self):
        self.mission_priorities = [
            'collect_items',
            'avoid_obstacles', 
            'reach_target',
            'optimize_time'
        ]
        self.backup_plans = {}
    
    def execute_mission(self):
        for priority in self.mission_priorities:
            try:
                success = self.execute_task(priority)
                if not success:
                    self.execute_backup_plan(priority)
            except Exception as e:
                self.handle_emergency(e)
    
    def execute_backup_plan(self, failed_task):
        # Fallback strategies
        pass

# Main competition loop
strategy = WROStrategy()
strategy.execute_mission()
```

**WRO Skills Learned**:
- Competition strategy development
- Error handling and recovery
- Mission prioritization

---

## 🎖️ **PHASE 3: Competition Mastery (Level 10+)**

### 🥇 **Level 10: Advanced Competition Challenges**
**Real WRO scenarios**:
- Multi-robot coordination
- Complex scoring systems
- Advanced sensor integration
- Machine learning basics

---

## 📊 **Assessment & Progress Tracking**

### 🎯 **Performance Metrics**:
1. **Completion Time** - Tối ưu hóa thời gian
2. **Code Efficiency** - Số lệnh tối thiểu
3. **Reliability** - Tỷ lệ thành công
4. **Adaptability** - Xử lý tình huống bất ngờ

### 📈 **Skill Progression**:
```
Level 1-3: Basic Movement ✅ (Completed)
Level 4-6: WRO Fundamentals 🎯 (Next Phase)
Level 7-9: Advanced Strategies 🚀 (Future)
Level 10+: Competition Mastery 🏆 (Expert)
```

---

## 🎓 **Learning Outcomes**

Sau khi hoàn thành curriculum này, học sinh sẽ có thể:

✅ **Apply Python fundamentals** to robot programming
✅ **Develop sensor-based algorithms** for navigation
✅ **Create optimization strategies** for time-critical missions
✅ **Handle complex scenarios** similar to WRO competitions
✅ **Debug and improve** robot performance systematically
✅ **Compete confidently** in WRO programming challenges

---

## 🚀 **Next Steps**

1. **Implement Levels 4-6** với curriculum này
2. **Add performance tracking** system
3. **Create assessment tools** cho từng level
4. **Develop competition scenarios** realistic với WRO
5. **Build mentor dashboard** để track student progress
