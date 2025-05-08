# ĐỀ BÀI: MÔ PHỎNG ROBOT TRÁNH VẬT CẢN

## YÊU CẦU:

Viết chương trình mô phỏng một robot tránh vật cản và tìm đường đến đích với các chức năng cơ bản:
- Chương trình phải có menu cho phép người dùng thực hiện các thao tác với robot
- Sử dụng các cấu trúc điều khiển: for, while, if-else
- Tên biến và cấu trúc điều khiển sử dụng tiếng Anh, nội dung hiển thị sử dụng tiếng Việt
- Robot có khả năng phát hiện vật cản và tìm đường đi đến đích

## CHI TIẾT CƠ CHẾ DI CHUYỂN ROBOT:

### 1. Mô hình robot:
- Robot di chuyển trên mặt phẳng tọa độ (x, y)
- Robot có vị trí (x, y) và hướng di chuyển (0: Bắc, 1: Đông, 2: Nam, 3: Tây)
- Robot có 3 cảm biến: phía trước, bên trái và bên phải
- Robot có pin với mức năng lượng ban đầu là 100%
- Mỗi bước di chuyển tiêu tốn 1% pin

### 2. Cảm biến và phát hiện vật cản:
- Cảm biến trước: Kiểm tra vị trí phía trước robot theo hướng hiện tại
- Cảm biến trái: Kiểm tra vị trí bên trái robot (hướng hiện tại - 1) % 4
- Cảm biến phải: Kiểm tra vị trí bên phải robot (hướng hiện tại + 1) % 4
- Mỗi cảm biến trả về True nếu phát hiện vật cản, False nếu không

### 3. Quy tắc di chuyển:
- **Nếu không có vật cản phía trước (front_sensor = False):**
  - Robot đi thẳng theo hướng hiện tại
  - Cập nhật vị trí dựa trên hướng và tốc độ
  - Ví dụ: Nếu robot ở (3, 4), hướng Bắc, tốc độ 1, vị trí mới sẽ là (3, 5)

- **Nếu có vật cản phía trước (front_sensor = True):**
  - **Nếu không có vật cản bên phải (right_sensor = False):**
    - Robot rẽ phải: direction = (direction + 1) % 4
    - Ví dụ: Nếu hướng hiện tại là Bắc (0), hướng mới sẽ là Đông (1)

  - **Nếu có vật cản bên phải nhưng không có vật cản bên trái (left_sensor = False):**
    - Robot rẽ trái: direction = (direction - 1) % 4
    - Ví dụ: Nếu hướng hiện tại là Bắc (0), hướng mới sẽ là Tây (3)

  - **Nếu cả ba hướng đều có vật cản:**
    - Robot quay đầu: direction = (direction + 2) % 4
    - Ví dụ: Nếu hướng hiện tại là Bắc (0), hướng mới sẽ là Nam (2)

- **Thứ tự ưu tiên trong quyết định:**
  1. Đi thẳng (nếu không có vật cản phía trước)
  2. Rẽ phải (nếu có vật cản phía trước nhưng không có vật cản bên phải)
  3. Rẽ trái (nếu có vật cản phía trước và bên phải nhưng không có vật cản bên trái)
  4. Quay đầu (nếu cả ba hướng đều có vật cản)

> **Lưu ý:** Xem file `quy_tac_di_chuyen_robot.md` để biết thêm chi tiết và ví dụ minh họa.

### 4. Cập nhật vị trí:
- **Nếu hướng là Bắc (direction = 0):**
  - y += speed (di chuyển lên trên)
- **Nếu hướng là Đông (direction = 1):**
  - x += speed (di chuyển sang phải)
- **Nếu hướng là Nam (direction = 2):**
  - y -= speed (di chuyển xuống dưới)
- **Nếu hướng là Tây (direction = 3):**
  - x -= speed (di chuyển sang trái)

### 5. Điều kiện dừng:
- Robot đến đích: (x, y) == target_position
- Robot hết pin: battery <= 0
- Hoàn thành số bước di chuyển đã chỉ định

### 6. Hiển thị thông tin sau mỗi bước:
- Trạng thái cảm biến (True/False cho mỗi cảm biến)
- Quyết định di chuyển (đi thẳng, rẽ trái, rẽ phải, quay đầu)
- Vị trí mới sau khi di chuyển
- Pin còn lại
- Khoảng cách đến đích (tính theo Manhattan distance: |x - target_x| + |y - target_y|)

## HƯỚNG DẪN:

1. Sử dụng vòng lặp while để tạo menu và cho phép chương trình chạy liên tục
2. Sử dụng if-else để xử lý các lựa chọn từ menu
3. Sử dụng for để mô phỏng quá trình di chuyển của robot qua từng bước
4. Sử dụng các biến để lưu trữ trạng thái của robot và môi trường

## GỢI Ý:

### Khai báo biến cho robot:
```python
# Khai báo biến cho robot
x = 0
y = 0
direction = 0  # 0: bắc, 1: đông, 2: nam, 3: tây
speed = 1
front_sensor = False
left_sensor = False
right_sensor = False
is_running = False
battery = 100  # Pin robot (%)

# Khai báo biến cho môi trường
obstacles = []  # Danh sách vị trí các vật cản [(x1, y1), (x2, y2), ...]
target_position = (10, 10)  # Vị trí đích
```

### Menu chương trình:
```
===== MÔ PHỎNG ROBOT TRÁNH VẬT CẢN =====
1. Bật robot
2. Tắt robot
3. Di chuyển robot
4. Thiết lập tốc độ
5. Xem trạng thái robot
6. Tạo vật cản ngẫu nhiên
7. Thiết lập vị trí đích
8. Reset robot
0. Thoát
```

## YÊU CẦU BỔ SUNG:

1. Thêm tính năng tạo vật cản ngẫu nhiên
2. Thêm tính năng thiết lập vị trí đích
3. Hiển thị khoảng cách từ robot đến đích sau mỗi lần di chuyển
4. Thêm tính năng theo dõi lượng pin còn lại của robot

## LƯU Ý:

- Đây là bài tập mô phỏng, không cần kết nối phần cứng thực tế
- Tập trung vào việc thực hành các cấu trúc điều khiển cơ bản: for, while, if-else
- Sử dụng tên biến có ý nghĩa và tuân thủ quy tắc đặt tên
- Có thể sử dụng module random để tạo vật cản ngẫu nhiên
- Có thể sử dụng module time để tạo hiệu ứng tạm dừng giữa các bước di chuyển

================================================================================

# QUY TẮC DI CHUYỂN CHI TIẾT CHO ROBOT TRÁNH VẬT CẢN

## 1. Nguyên lý cơ bản

Robot tránh vật cản hoạt động dựa trên nguyên lý "cảm nhận - quyết định - hành động":
- **Cảm nhận**: Robot sử dụng các cảm biến để phát hiện vật cản trong môi trường
- **Quyết định**: Dựa trên thông tin từ cảm biến, robot quyết định hướng di chuyển
- **Hành động**: Robot thực hiện di chuyển theo quyết định đã đưa ra

## 2. Cảm biến và cách xác định vật cản

### 2.1. Cảm biến phía trước
- Kiểm tra vị trí ngay phía trước robot theo hướng hiện tại
- Cách xác định vị trí cần kiểm tra:
  ```
  next_x, next_y = x, y  # Vị trí hiện tại
  if direction == 0:  # Bắc
      next_y += speed
  elif direction == 1:  # Đông
      next_x += speed
  elif direction == 2:  # Nam
      next_y -= speed
  else:  # Tây
      next_x -= speed
  
  # Kiểm tra xem vị trí này có vật cản không
  front_sensor = (next_x, next_y) in obstacles
  ```

### 2.2. Cảm biến bên trái
- Kiểm tra vị trí bên trái robot theo hướng hiện tại
- Hướng bên trái = (hướng hiện tại - 1) % 4
- Cách xác định vị trí cần kiểm tra:
  ```
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
  ```

### 2.3. Cảm biến bên phải
- Kiểm tra vị trí bên phải robot theo hướng hiện tại
- Hướng bên phải = (hướng hiện tại + 1) % 4
- Cách xác định vị trí cần kiểm tra:
  ```
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
  ```

## 3. Quy tắc quyết định hướng di chuyển

### 3.1. Trường hợp 1: Không có vật cản phía trước
Khi `front_sensor = False` (không có vật cản phía trước):
- Robot tiếp tục đi thẳng theo hướng hiện tại
- Không thay đổi giá trị `direction`
- Cập nhật vị trí dựa trên hướng hiện tại và tốc độ

**Ví dụ:**
- Vị trí hiện tại: (3, 4)
- Hướng hiện tại: 0 (Bắc)
- Tốc độ: 1
- Không có vật cản phía trước
- → Robot đi thẳng, vị trí mới: (3, 5)

### 3.2. Trường hợp 2: Có vật cản phía trước, không có vật cản bên phải
Khi `front_sensor = True` và `right_sensor = False`:
- Robot rẽ phải: `direction = (direction + 1) % 4`
- Sau khi rẽ, robot cập nhật vị trí dựa trên hướng mới

**Ví dụ:**
- Vị trí hiện tại: (3, 4)
- Hướng hiện tại: 0 (Bắc)
- Có vật cản ở (3, 5) (phía trước)
- Không có vật cản ở (4, 4) (bên phải)
- → Robot rẽ phải, hướng mới: 1 (Đông)
- → Vị trí mới: (4, 4)

### 3.3. Trường hợp 3: Có vật cản phía trước và bên phải, không có vật cản bên trái
Khi `front_sensor = True`, `right_sensor = True` và `left_sensor = False`:
- Robot rẽ trái: `direction = (direction - 1) % 4`
- Sau khi rẽ, robot cập nhật vị trí dựa trên hướng mới

**Ví dụ:**
- Vị trí hiện tại: (3, 4)
- Hướng hiện tại: 0 (Bắc)
- Có vật cản ở (3, 5) (phía trước)
- Có vật cản ở (4, 4) (bên phải)
- Không có vật cản ở (2, 4) (bên trái)
- → Robot rẽ trái, hướng mới: 3 (Tây)
- → Vị trí mới: (2, 4)

### 3.4. Trường hợp 4: Có vật cản ở cả ba hướng
Khi `front_sensor = True`, `right_sensor = True` và `left_sensor = True`:
- Robot quay đầu: `direction = (direction + 2) % 4`
- Sau khi quay đầu, robot cập nhật vị trí dựa trên hướng mới

**Ví dụ:**
- Vị trí hiện tại: (3, 4)
- Hướng hiện tại: 0 (Bắc)
- Có vật cản ở (3, 5) (phía trước)
- Có vật cản ở (4, 4) (bên phải)
- Có vật cản ở (2, 4) (bên trái)
- → Robot quay đầu, hướng mới: 2 (Nam)
- → Vị trí mới: (3, 3)

## 4. Thứ tự ưu tiên trong quyết định

Robot sẽ quyết định hướng di chuyển theo thứ tự ưu tiên sau:
1. Đi thẳng (nếu không có vật cản phía trước)
2. Rẽ phải (nếu có vật cản phía trước nhưng không có vật cản bên phải)
3. Rẽ trái (nếu có vật cản phía trước và bên phải nhưng không có vật cản bên trái)
4. Quay đầu (nếu cả ba hướng đều có vật cản)

Thứ tự ưu tiên này giúp robot có xu hướng đi theo hướng ban đầu và chỉ thay đổi hướng khi cần thiết.

## 5. Chiến lược tìm đường đến đích

Mặc dù robot không có thuật toán tìm đường thông minh, nhưng với quy tắc di chuyển trên, robot có thể tìm đường đến đích trong nhiều trường hợp:

1. **Không có vật cản**: Robot sẽ di chuyển theo đường thẳng đến đích
2. **Vật cản đơn giản**: Robot sẽ đi vòng qua vật cản và tiếp tục di chuyển
3. **Mê cung đơn giản**: Robot có thể tìm đường ra khỏi mê cung bằng cách luôn rẽ phải khi gặp vật cản (thuật toán wall-following)

Tuy nhiên, robot có thể gặp khó khăn trong các trường hợp phức tạp như mê cung có nhiều ngõ cụt hoặc vật cản tạo thành hình dạng đặc biệt.

## 6. Ví dụ minh họa quy trình di chuyển

### Ví dụ 1: Di chuyển trong môi trường không có vật cản
- Vị trí ban đầu: (0, 0)
- Hướng ban đầu: 0 (Bắc)
- Vị trí đích: (3, 3)
- Không có vật cản

**Các bước di chuyển:**
1. Robot đi thẳng: (0, 0) → (0, 1)
2. Robot đi thẳng: (0, 1) → (0, 2)
3. Robot đi thẳng: (0, 2) → (0, 3)
4. Robot rẽ phải (để tiến gần đích): (0, 3) → (1, 3)
5. Robot đi thẳng: (1, 3) → (2, 3)
6. Robot đi thẳng: (2, 3) → (3, 3) (đến đích)

### Ví dụ 2: Di chuyển với vật cản đơn giản
- Vị trí ban đầu: (0, 0)
- Hướng ban đầu: 0 (Bắc)
- Vị trí đích: (3, 3)
- Vật cản ở (0, 1), (1, 1), (2, 1)

**Các bước di chuyển:**
1. Robot phát hiện vật cản phía trước (0, 1), rẽ phải: (0, 0) → (1, 0)
2. Robot đi thẳng: (1, 0) → (2, 0)
3. Robot đi thẳng: (2, 0) → (3, 0)
4. Robot rẽ trái (để tiến gần đích): (3, 0) → (3, 1)
5. Robot đi thẳng: (3, 1) → (3, 2)
6. Robot đi thẳng: (3, 2) → (3, 3) (đến đích)

## 7. Lưu ý quan trọng

1. **Kiểm tra biên**: Trong thực tế, cần kiểm tra xem robot có di chuyển ra ngoài vùng cho phép không
2. **Xử lý trường hợp đặc biệt**: Cần xử lý các trường hợp đặc biệt như robot bị kẹt trong vòng lặp
3. **Tối ưu hóa đường đi**: Thuật toán hiện tại không tối ưu hóa đường đi, robot có thể di chuyển theo đường dài hơn cần thiết
4. **Cải tiến thuật toán**: Có thể cải tiến thuật toán bằng cách thêm các chiến lược tìm đường thông minh hơn như A* hoặc Dijkstra
