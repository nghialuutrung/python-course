# Giải thích chi tiết phần code quyết định di chuyển của robot

Phần code này là phần quan trọng nhất trong chương trình mô phỏng robot đi theo đường line. Đây là nơi robot quyết định hướng di chuyển dựa trên trạng thái của các cảm biến và sau đó cập nhật vị trí của mình. Dưới đây là giải thích chi tiết từng phần:

## 1. Quyết định hướng di chuyển

```python
# Quyết định hướng di chuyển
if left_sensor:
    # Rẽ trái
    direction = (direction - 1) % 4
    print(
        f"Robot rẽ trái, hướng mới: {direction_names[direction]}")
elif right_sensor:
    # Rẽ phải
    direction = (direction + 1) % 4
    print(
        f"Robot rẽ phải, hướng mới: {direction_names[direction]}")
elif center_sensor:
    # Đi thẳng
    print(
        f"Robot đi thẳng theo hướng {direction_names[direction]}")
```

Đoạn code này quyết định robot sẽ di chuyển theo hướng nào dựa trên trạng thái của 3 cảm biến (trái, giữa, phải). Trong chương trình của chúng ta, chỉ có một cảm biến được kích hoạt (True) tại một thời điểm.

### Trường hợp 1: Cảm biến trái phát hiện đường line
```python
if left_sensor:
    # Rẽ trái
    direction = (direction - 1) % 4
    print(f"Robot rẽ trái, hướng mới: {direction_names[direction]}")
```

- Khi cảm biến trái phát hiện đường line (`left_sensor = True`), robot sẽ rẽ trái.
- `direction = (direction - 1) % 4`: Giảm giá trị `direction` đi 1 và lấy phần dư khi chia cho 4.
  - Ví dụ: Nếu `direction = 1` (Đông), thì `(1 - 1) % 4 = 0` (Bắc)
  - Nếu `direction = 0` (Bắc), thì `(0 - 1) % 4 = 3` (Tây)
- Phép toán `% 4` đảm bảo giá trị `direction` luôn nằm trong khoảng 0-3, tương ứng với 4 hướng: Bắc (0), Đông (1), Nam (2), Tây (3).
- Sau đó, chương trình in ra thông báo về hướng mới của robot.

### Trường hợp 2: Cảm biến phải phát hiện đường line
```python
elif right_sensor:
    # Rẽ phải
    direction = (direction + 1) % 4
    print(f"Robot rẽ phải, hướng mới: {direction_names[direction]}")
```

- Khi cảm biến phải phát hiện đường line (`right_sensor = True`), robot sẽ rẽ phải.
- `direction = (direction + 1) % 4`: Tăng giá trị `direction` lên 1 và lấy phần dư khi chia cho 4.
  - Ví dụ: Nếu `direction = 1` (Đông), thì `(1 + 1) % 4 = 2` (Nam)
  - Nếu `direction = 3` (Tây), thì `(3 + 1) % 4 = 0` (Bắc)
- Tương tự, phép toán `% 4` đảm bảo giá trị `direction` luôn nằm trong khoảng 0-3.
- Sau đó, chương trình in ra thông báo về hướng mới của robot.

### Trường hợp 3: Cảm biến giữa phát hiện đường line
```python
elif center_sensor:
    # Đi thẳng
    print(f"Robot đi thẳng theo hướng {direction_names[direction]}")
```

- Khi cảm biến giữa phát hiện đường line (`center_sensor = True`), robot sẽ đi thẳng.
- Trong trường hợp này, giá trị `direction` không thay đổi, robot tiếp tục di chuyển theo hướng hiện tại.
- Chương trình chỉ in ra thông báo rằng robot đang đi thẳng theo hướng hiện tại.

## 2. Cập nhật vị trí dựa trên hướng và tốc độ

```python
# Cập nhật vị trí dựa trên hướng và tốc độ
if direction == 0:  # Bắc
    y += speed
elif direction == 1:  # Đông
    x += speed
elif direction == 2:  # Nam
    y -= speed
else:  # Tây
    x -= speed
```

Sau khi đã quyết định hướng di chuyển, robot cần cập nhật vị trí của mình trên mặt phẳng tọa độ (x, y). Vị trí mới phụ thuộc vào hướng di chuyển và tốc độ của robot.

### Hướng Bắc (direction = 0)
```python
if direction == 0:  # Bắc
    y += speed
```
- Khi robot di chuyển về hướng Bắc, tọa độ y tăng lên một giá trị bằng tốc độ.
- Tọa độ x không thay đổi.
- Ví dụ: Nếu vị trí hiện tại là (3, 4) và tốc độ là 1, vị trí mới sẽ là (3, 5).

### Hướng Đông (direction = 1)
```python
elif direction == 1:  # Đông
    x += speed
```
- Khi robot di chuyển về hướng Đông, tọa độ x tăng lên một giá trị bằng tốc độ.
- Tọa độ y không thay đổi.
- Ví dụ: Nếu vị trí hiện tại là (3, 4) và tốc độ là 1, vị trí mới sẽ là (4, 4).

### Hướng Nam (direction = 2)
```python
elif direction == 2:  # Nam
    y -= speed
```
- Khi robot di chuyển về hướng Nam, tọa độ y giảm đi một giá trị bằng tốc độ.
- Tọa độ x không thay đổi.
- Ví dụ: Nếu vị trí hiện tại là (3, 4) và tốc độ là 1, vị trí mới sẽ là (3, 3).

### Hướng Tây (direction = 3)
```python
else:  # Tây
    x -= speed
```
- Khi robot di chuyển về hướng Tây, tọa độ x giảm đi một giá trị bằng tốc độ.
- Tọa độ y không thay đổi.
- Ví dụ: Nếu vị trí hiện tại là (3, 4) và tốc độ là 1, vị trí mới sẽ là (2, 4).

## 3. Hiển thị và tạm dừng

```python
# Hiển thị vị trí mới
print(f"Vị trí mới: ({x}, {y})")

# Tạm dừng để người dùng theo dõi
time.sleep(0.5)
```

- Sau khi đã cập nhật vị trí, chương trình hiển thị vị trí mới của robot.
- Cuối cùng, chương trình tạm dừng 0.5 giây để người dùng có thể theo dõi quá trình di chuyển của robot.
- Nếu không có dòng `time.sleep(0.5)`, chương trình sẽ chạy quá nhanh và người dùng không thể theo dõi được quá trình di chuyển.

## Tóm tắt quy trình di chuyển của robot:

1. **Đọc trạng thái cảm biến**: Xác định cảm biến nào đang phát hiện đường line.
2. **Quyết định hướng di chuyển**: Dựa trên trạng thái cảm biến, robot quyết định rẽ trái, rẽ phải hoặc đi thẳng.
3. **Cập nhật vị trí**: Dựa trên hướng di chuyển và tốc độ, robot cập nhật vị trí của mình trên mặt phẳng tọa độ.
4. **Hiển thị thông tin**: Hiển thị vị trí mới của robot và tạm dừng để người dùng theo dõi.

Đây là cách robot mô phỏng di chuyển theo đường line trong chương trình của chúng ta. Mỗi bước di chuyển, robot sẽ dựa vào trạng thái của các cảm biến để quyết định hướng di chuyển và cập nhật vị trí của mình.
