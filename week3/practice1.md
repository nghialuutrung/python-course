# ĐỀ BÀI: MÔ PHỎNG ROBOT ĐI THEO ĐƯỜNG LINE

YÊU CẦU:
1. Viết chương trình mô phỏng một robot đi theo đường line với các chức năng cơ bản
2. Chương trình phải có menu cho phép người dùng thực hiện các thao tác với robot
3. Sử dụng các cấu trúc điều khiển: for, while, if-else
4. Tên biến và cấu trúc điều khiển sử dụng tiếng Anh, nội dung hiển thị sử dụng tiếng Việt

HƯỚNG DẪN:
- Sử dụng vòng lặp while để tạo menu và cho phép chương trình chạy liên tục
- Sử dụng if-else để xử lý các lựa chọn từ menu
- Sử dụng for để mô phỏng quá trình di chuyển của robot qua từng bước

GỢI Ý:
- Robot có vị trí (x, y) và hướng di chuyển
- Robot có 3 cảm biến để đọc đường line: trái, giữa, phải
- Cài đặt logic đơn giản: nếu cảm biến giữa phát hiện line -> đi thẳng, 
  nếu cảm biến trái phát hiện line -> rẽ trái, nếu cảm biến phải phát hiện line -> rẽ phải

LƯU Ý: 
- Đây là bài tập mô phỏng, không cần kết nối phần cứng thực tế
- Tập trung vào việc thực hành các cấu trúc điều khiển cơ bản: for, while, if-else
- Sử dụng tên biến có ý nghĩa và tuân thủ quy tắc đặt tên

ĐỊNH NGHĨA VỀ KHAI BÁO CÁC GIÁ TRỊ CHO ROBOT
```python
# Khai báo biến cho robot
x = 0
y = 0
direction = 0  # 0: bắc, 1: đông, 2: nam, 3: tây
speed = 0
left_sensor = False
center_sensor = True
right_sensor = False
is_running = False
```

VÍ DỤ VỀ MENU:

```python
# Hiển thị menu
print("\n===== MÔ PHỎNG ROBOT ĐI THEO LINE =====")
print("1. Bật robot")
print("2. Tắt robot")
print("3. Di chuyển robot")
print("4. Thiết lập tốc độ")
print("5. Xem trạng thái robot")
print("6. Reset robot")
print("0. Thoát")
```