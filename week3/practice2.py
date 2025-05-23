import random
import time
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow

x = 0
y = 0
direction = 0  # 0: bắc, 1: đông, 2: nam, 3: tây
speed = 1
front_sensor = False
left_sensor = False
right_sensor = False
is_running = True
battery = 100  # Pin robot (%)


# Khai báo biến cho môi trường
obstacles = []  # Danh sách vị trí các vật cản [(x1, y1), (x2, y2), ...]
target_position = (10, 10)  # Vị trí đích
direction_names = ["Bắc", "Đông", "Nam", "Tây"]
# Biến để theo dõi trạng thái đồ thị
graph_figure = None
auto_update_graph = False

def display_map_on_graph(block=True, update_only=False):
    global graph_figure

    # Nếu đang cập nhật và không có figure, tạo mới
    if update_only and graph_figure is None:
        graph_figure = plt.figure(figsize=(10, 8))
    # Nếu không phải cập nhật, tạo figure mới
    elif not update_only:
        # Đóng figure cũ nếu có
        if graph_figure is not None:
            plt.close(graph_figure)
        graph_figure = plt.figure(figsize=(10, 8))
    # Nếu đang cập nhật và có figure, xóa nội dung cũ
    else:
        plt.clf()

    # Thiết lập giới hạn trục x và y
    min_x, max_x = min(min(ox for ox, _ in obstacles) if obstacles else 0, x, target_position[0]) - 5, max(max(ox for ox, _ in obstacles) if obstacles else 0, x, target_position[0]) + 5
    min_y, max_y = min(min(oy for _, oy in obstacles) if obstacles else 0, y, target_position[1]) - 5, max(max(oy for _, oy in obstacles) if obstacles else 0, y, target_position[1]) + 5

    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)

    # Vẽ lưới với khoảng cách dựa trên giá trị speed
    # Tạo các điểm lưới dựa trên speed
    x_ticks = []
    y_ticks = []

    # Tính toán các điểm lưới dựa trên speed
    x_start = int(min_x) - (int(min_x) % speed)
    x_end = int(max_x) + speed
    y_start = int(min_y) - (int(min_y) % speed)
    y_end = int(max_y) + speed

    # Tạo các điểm lưới theo speed
    x_ticks = [i for i in range(x_start, x_end, speed)]
    y_ticks = [i for i in range(y_start, y_end, speed)]

    # Thiết lập các điểm lưới
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)

    # Vẽ lưới
    plt.grid(True, linestyle='--', alpha=0.7)

    # Vẽ các vật cản
    if obstacles:
        obstacle_x = [ox for ox, _ in obstacles]
        obstacle_y = [oy for _, oy in obstacles]
        plt.scatter(obstacle_x, obstacle_y, color='red', marker='s', s=100, label='Vật cản')

    # Vẽ đích
    plt.scatter(target_position[0], target_position[1], color='green', marker='*', s=200, label='Đích')

    # Vẽ robot
    plt.scatter(x, y, color='blue', marker='o', s=150, label='Robot')

    # Vẽ mũi tên chỉ hướng của robot
    arrow_length = 0.5 * speed  # Điều chỉnh độ dài mũi tên theo speed
    dx, dy = 0, 0

    if direction == 0:  # Bắc
        dx, dy = 0, arrow_length
    elif direction == 1:  # Đông
        dx, dy = arrow_length, 0
    elif direction == 2:  # Nam
        dx, dy = 0, -arrow_length
    else:  # Tây
        dx, dy = -arrow_length, 0

    plt.arrow(x, y, dx, dy, head_width=0.3 * speed, head_length=0.3 * speed, fc='blue', ec='blue')

    # Thêm chú thích
    plt.title(f'Bản đồ môi trường Robot (Speed: {speed})')
    plt.xlabel('Trục X')
    plt.ylabel('Trục Y')
    plt.legend()

    # Hiển thị thông tin robot
    info_text = f"Vị trí: ({x}, {y})\n"
    info_text += f"Hướng: {direction_names[direction]}\n"
    info_text += f"Tốc độ: {speed}\n"
    info_text += f"Pin: {battery}%\n"
    info_text += f"Cảm biến: Trước={front_sensor}, Trái={left_sensor}, Phải={right_sensor}"

    plt.annotate(info_text, xy=(0.02, 0.02), xycoords='figure fraction',
                 bbox=dict(boxstyle="round,pad=0.5", fc="lightyellow", alpha=0.8))

    # Hiển thị đồ thị
    plt.tight_layout()

    # Cập nhật đồ thị
    if update_only:
        plt.draw()
        plt.pause(0.001)  # Tạm dừng ngắn để cập nhật đồ thị
    else:
        plt.show(block=block)  # block=False cho phép chương trình tiếp tục chạy

def toggle_auto_update():
    global auto_update_graph
    auto_update_graph = not auto_update_graph
    return auto_update_graph

def resett(new_x,new_y):
    direction = 0  # 0: bắc, 1: đông, 2: nam, 3: tây
    speed = 1
    left_sensor = False
    front_sensor = False
    right_sensor = False
    is_running = False
    battery = 100
    x = new_x
    y = new_y
    print("Đã reset robot")
    
def setmode(running):
    is_running = running
    if running:
        print("Đã bật robot")
    else:
        print("Đã tắt robot")

def randomm():
    # Thiết lập ngẫu nhiên trạng thái cảm biến
    # Đảm bảo chỉ có một cảm biến được kích hoạt (True)
    sensor_choice = random.randint(0, 2)  # 0: trái, 1: giữa, 2: phải

    left_sensor = (sensor_choice == 0)
    center_sensor = (sensor_choice == 1)
    right_sensor = (sensor_choice == 2)
    print(f"Cảm biến: Trái={left_sensor}, Giữa={center_sensor}, Phải={right_sensor}")

def state():
    print(f"Vị trí: ({x},{y})")
    print(f"Hướng hiện tại: {direction_names[direction]}")
    print(f"Tốc độ hiện tại: {speed}")
    print(f"Cảm biến: Trái={left_sensor}, Giữa={front_sensor}, Phải={right_sensor}")
        
while True:
    print("\n===== MÔ PHỎNG ROBOT ĐI THEO LINE =====")
    print("1. Bật robot")
    print("2. Tắt robot")
    print("3. Di chuyển robot")
    print("4. Thiết lập tốc độ")
    print("5. Xem trạng thái robot")
    print("6. Tạo vật cản ngẫu nhiên")
    print("7. Thiết lập vị trí đích")
    print("8. Reset robot")
    print(f"10. {'Tắt' if auto_update_graph else 'Bật'} tự động cập nhật đồ thị")
    print("0. Thoát")
    
    user_input = input("Chọn số: ")
    
    if user_input == "1":
        setmode(True)
    elif user_input == "2":
        setmode(False)
    elif user_input == "3":
        print("Cbi di chuyển robot")
        if not is_running:
            print("turn on robot")
        else:
            steps = input("Nhập số bước: ")
            if steps.isdigit() and int(steps) > 0:
                print("Đã bắt đầu di chuyển")
                for i in range(int(steps)):
                    
                    if battery < 1:
                        print("robot het pin roi. Sạc pin đi")
                        break
                    print(f"---Bước {i+1}/{steps}---")
                    
                    # if left_sensor:
                    #     direction = (direction - 1) % 4
                    #     print(f"Robot rẽ trái, hướng mới: {direction_names[direction]}")
                    # elif right_sensor:
                    #     direction = (direction + 1) % 4
                    #     print(f"Robot rẽ phải, hướng mới: {direction_names[direction]}")
                    # else:
                    #     print(f"Robot đi thẳng, hướng mới: {direction_names[direction]}")
                    
                    
                    #xác định cảm biến xem đằng trc có vật cản hay ko
                    
                    next_x, next_y = x, y
                    if direction == 0:
                        next_y += speed
                    elif direction == 1:
                        next_x += speed
                    elif direction == 2:
                        next_y -= speed  
                    else:
                        next_x -= speed
                    front_sensor = (next_x, next_y) in obstacles

                    #xác định cbien bên phải có gặp vật cản hay ko
                    right_direction = (direction + 1) % 4
                    right_x, right_y = x, y  # Vị trí hiện tại
                    if right_direction == 0:  # Bắc
                        right_y += speed
                    elif right_direction == 1:  # Đông
                        right_x += speed
                    elif right_direction == 2:  # Nam
                        right_y -= speed
                    else:  # Tây
                        right_x -= speed
                    # Kiểm tra xem vị trí này có vật cản không
                    right_sensor = (right_x, right_y) in obstacles
                    
                    #xác định cbien bên trái có gặp vật cản hay ko
                    left_direction = (direction - 1) % 4
                    left_x, left_y = x, y  # Vị trí hiện tại
                    if left_direction == 0:  # Bắc
                        left_y += speed
                    elif left_direction == 1:  # Đông
                        left_x += speed
                    elif left_direction == 2:  # Nam
                        left_y -= speed
                    else:  # Tây
                        left_x -= speed
                    # Kiểm tra xem vị trí này có vật cản không
                    left_sensor = (left_x, left_y) in obstacles
                    if not front_sensor:
                        if direction == 0:
                            y += speed
                        elif direction == 1:
                            x += speed
                        elif direction == 2:
                            y -= speed  
                        else:
                            x -= speed
                    else:
                        if not right_sensor:
                            direction = (direction + 1) % 4
                            if direction == 0:
                                y += speed
                            elif direction == 1:
                                x += speed
                            elif direction == 2:
                                y -= speed  
                            else:
                                x -= speed
                        else:
                            if not left_sensor:
                                direction = (direction - 1) % 4
                                if direction == 0:
                                    y += speed
                                elif direction == 1:
                                    x += speed
                                elif direction == 2:
                                    y -= speed  
                                else:
                                    x -= speed
                            else:
                                direction = (direction + 2) % 4
                                if direction == 0:
                                    y += speed
                                elif direction == 1:
                                    x += speed
                                elif direction == 2:
                                    y -= speed  
                                else:
                                    x -= speed
                    battery = battery - 1
                    print(f"Pin: {battery}%")
                    print(f"Vị trí mới: ({x,y})")
                    # Cập nhật đồ thị nếu chế độ tự động cập nhật được bật
                    if auto_update_graph and graph_figure is not None:
                        try:
                            display_map_on_graph(block=False, update_only=True)
                        except Exception as e:
                            print(f"Lỗi khi cập nhật đồ thị: {e}")
                    time.sleep(1)
                    if (x,y) == target_position:
                        print(f"Đã đến đích")
                        break
                    state()
            else:
                print("Số bước ko hợp lệ")
        # print(f"\nRobot đã di chuyển xong {min(i+1, steps)} bước.") CẦN SỬA!!!
        print(f"Vị trí cuối cùng: ({x}, {y})")
        print(f"Hướng cuối cùng: {direction_names[direction]}")
        print(f"Pin còn lại: {battery}%")
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
        state()
        if is_running:
            print("Robot đang bật")
        else:
            print("Robot đang tắt")
    elif user_input == "8":
        resett(0,0) #new_x, new_y
    elif user_input == "10":
        # Bật/tắt tự động cập nhật đồ thị
        is_enabled = toggle_auto_update()
        status = "bật" if is_enabled else "tắt"
        print(f"Đã {status} chế độ tự động cập nhật đồ thị.")

        # Nếu bật chế độ tự động cập nhật, mở đồ thị ngay
        if auto_update_graph:
            try:
                print("Đang mở cửa sổ đồ thị (không chặn)...")
                display_map_on_graph(block=False)
            except Exception as e:
                print(f"Lỗi khi hiển thị đồ thị: {e}")
                auto_update_graph = False
                print("Đã tắt chế độ tự động cập nhật đồ thị.")
        else:
            # Nếu tắt chế độ tự động cập nhật, đóng đồ thị nếu đang mở
            if graph_figure is not None:
                plt.close(graph_figure)
                graph_figure = None
                print("Đã đóng cửa sổ đồ thị.")
    elif user_input == "0":
        print("bye")
        break
    else:
        print("invalid")