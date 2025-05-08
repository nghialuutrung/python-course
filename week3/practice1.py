import random
import time
x = 0
y = 0
direction = 0  # 0: bắc, 1: đông, 2: nam, 3: tây
speed = 1
left_sensor = False
center_sensor = True
right_sensor = False
is_running = False
direction_names = ["Bắc", "Đông", "Nam", "Tây"]

while True:
    print("\n===== MÔ PHỎNG ROBOT ĐI THEO LINE =====")
    print("1. Bật robot")
    print("2. Tắt robot")
    print("3. Di chuyển robot")
    print("4. Thiết lập tốc độ")
    print("5. Xem trạng thái robot")
    print("6. Reset robot")
    print("0. Thoát")
    
    user_input = input("Chọn số: ")
    
    if user_input == "1":
        print("Đã bật robot")
        is_running = True
    elif user_input == "2":
        print("Đã tắt robot")
        is_running = False
    elif user_input == "3":
        print("Đã di chuyển robot")
        if is_running == False:
            print("turn on robot")
        else:
            steps = input("Nhập số bước: ")
            if steps.isdigit() and int(steps) > 0:
                print("Đã bắt đầu di chuyển")
                for i in range(int(steps)):
                    print(f"---Bước {i+1}/{steps}---")
                    # Thiết lập ngẫu nhiên trạng thái cảm biến
                    # Đảm bảo chỉ có một cảm biến được kích hoạt (True)
                    sensor_choice = random.randint(0, 2)  # 0: trái, 1: giữa, 2: phải

                    left_sensor = (sensor_choice == 0)
                    center_sensor = (sensor_choice == 1)
                    right_sensor = (sensor_choice == 2)
                    print(f"Cảm biến: Trái={left_sensor}, Giữa={center_sensor}, Phải={right_sensor}")
                    if left_sensor:
                        direction = (direction - 1) % 4
                        print(f"Robot rẽ trái, hướng mới: {direction_names[direction]}")
                    elif right_sensor:
                        direction = (direction + 1) % 4
                        print(f"Robot rẽ phải, hướng mới: {direction_names[direction]}")
                    else:
                        print(f"Robot đi thẳng, hướng mới: {direction_names[direction]}")
                    if direction == 0:
                        y += speed
                    elif direction == 1:
                        x += speed
                    elif direction == 2:
                        y -= speed
                    else:
                        x -= speed
                    print(f"Vị trí mới: ({x,y})")
                    time.sleep(1)
                print("\n\n")
                print(f"\nRobot đã di chuyển xong {steps} bước.")
                print(f"Vị trí cuối cùng: ({x}, {y})")
                print(f"Hướng cuối cùng: {direction_names[direction]}")
            else:
                print("Số bước ko hợp lệ")
    elif user_input == "4":
        try:
            new_speed = float(input("Nhập tốc độ mới (0.1-5.0): "))
            if 0.1 <= new_speed <= 5.0:
                speed = new_speed
                print(f"Đã thiết lập tốc độ mới: {speed}")
            else:
                print("Tốc độ phải nằm trong khoảng từ 0.1 đến 5.0.")
        except ValueError:
            print("Vui lòng nhập một số hợp lệ.")
    elif user_input == "5":
        print(f"Vị trí: ({x},{y})")
        print(f"Hướng hiện tại: {direction_names[direction]}")
        print(f"Tốc độ hiện tại: {speed}")
        print(f"Cảm biến: Trái={left_sensor}, Giữa={center_sensor}, Phải={right_sensor}")
        if is_running:
            print("Robot đang bật")
        else:
            print("Robot đang tắt")
    elif user_input == "6":
        direction = 0  # 0: bắc, 1: đông, 2: nam, 3: tây
        speed = 0
        left_sensor = False
        center_sensor = False
        right_sensor = False
        is_running = False
        x = 0
        y = 0
        print("Đã reset robot")
    elif user_input == "0":
        print("bye")
        break
    else:
        print("invalid")