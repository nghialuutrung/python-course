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


==============================================================================================================

# Chi tiết về yêu cầu và cơ chế cho menu số 3: "Di chuyển robot"

## Yêu cầu của menu số 3 - "Di chuyển robot"

Khi người dùng chọn tùy chọn số 3 từ menu, chương trình cần mô phỏng quá trình robot di chuyển theo đường line. Đây là phần quan trọng nhất của bài tập, nơi robot thực sự "hoạt động" dựa trên các cảm biến và logic di chuyển đã được định nghĩa.

## Cơ chế thực hiện

### 1. Kiểm tra trạng thái robot
- Trước tiên, cần kiểm tra xem robot đã được bật chưa (`is_running = True`). Nếu robot chưa được bật, hiển thị thông báo và quay lại menu.

### 2. Mô phỏng quá trình di chuyển
- Sử dụng vòng lặp `for` để mô phỏng robot di chuyển qua nhiều bước (có thể cho người dùng nhập số bước hoặc sử dụng một số cố định).
- Trong mỗi bước di chuyển:

  a) **Đọc trạng thái cảm biến**: Trong bài tập mô phỏng này, trạng thái cảm biến có thể được:
     - Thiết lập ngẫu nhiên (để mô phỏng đường line ngẫu nhiên)
     - Hoặc theo một mẫu cố định (để mô phỏng một đường line cụ thể)
     - Hoặc cho phép người dùng nhập trạng thái cảm biến

  b) **Quyết định hướng di chuyển** dựa trên trạng thái cảm biến:
     - Nếu `center_sensor = True`: Robot đi thẳng theo hướng hiện tại
     - Nếu `left_sensor = True`: Robot rẽ trái (giảm `direction` đi 1, hoặc quay về 3 nếu đang là 0)
     - Nếu `right_sensor = True`: Robot rẽ phải (tăng `direction` lên 1, hoặc quay về 0 nếu đang là 3)
     - Nếu nhiều cảm biến cùng phát hiện line, cần có quy tắc ưu tiên (thường ưu tiên theo thứ tự: trái > giữa > phải)

  c) **Cập nhật vị trí** dựa trên hướng và tốc độ:
     - Nếu `direction = 0` (bắc): `y += speed`
     - Nếu `direction = 1` (đông): `x += speed`
     - Nếu `direction = 2` (nam): `y -= speed`
     - Nếu `direction = 3` (tây): `x -= speed`

  d) **Hiển thị trạng thái hiện tại** của robot sau mỗi bước di chuyển:
     - Vị trí (x, y)
     - Hướng (có thể hiển thị dưới dạng "Bắc", "Đông", "Nam", "Tây")
     - Trạng thái cảm biến
     - Có thể thêm hiệu ứng trì hoãn (sử dụng `time.sleep()`) để người dùng có thể theo dõi quá trình di chuyển

### 3. Mô phỏng trực quan (tùy chọn nâng cao)
- Có thể sử dụng các ký tự ASCII để vẽ một bản đồ đơn giản hiển thị vị trí và hướng của robot
- Ví dụ: sử dụng ký tự "^", ">", "v", "<" để biểu thị robot đang hướng lên, phải, xuống, trái

### 4. Kết thúc di chuyển
- Sau khi hoàn thành số bước di chuyển, hiển thị thông báo kết thúc và vị trí cuối cùng của robot
- Quay lại menu chính

# Ví dụ mô phỏng robot đi theo đường line qua từng bước

Dưới đây là một ví dụ cụ thể về cách robot di chuyển qua 10 bước, với các trạng thái cảm biến được định nghĩa trước để mô phỏng một đường line hình chữ S đơn giản.

## Giả sử trạng thái ban đầu của robot
- Vị trí: (0, 0)
- Hướng: 0 (Bắc)
- Tốc độ: 1
- Robot đã được bật (is_running = True)

## Mô phỏng 10 bước di chuyển

### Bước 1
- **Trạng thái cảm biến**: Trái=False, Giữa=True, Phải=False
- **Quyết định**: Robot đi thẳng (vì cảm biến giữa phát hiện line)
- **Hướng mới**: 0 (Bắc) - không thay đổi
- **Vị trí mới**: (0, 1) - di chuyển lên trên 1 đơn vị
- **Hiển thị**: "Robot đi thẳng theo hướng Bắc"

### Bước 2
- **Trạng thái cảm biến**: Trái=False, Giữa=True, Phải=False
- **Quyết định**: Robot đi thẳng
- **Hướng mới**: 0 (Bắc) - không thay đổi
- **Vị trí mới**: (0, 2) - tiếp tục di chuyển lên trên
- **Hiển thị**: "Robot đi thẳng theo hướng Bắc"

### Bước 3
- **Trạng thái cảm biến**: Trái=False, Giữa=False, Phải=True
- **Quyết định**: Robot rẽ phải (vì cảm biến phải phát hiện line)
- **Hướng mới**: 1 (Đông) - thay đổi từ Bắc sang Đông
- **Vị trí mới**: (1, 2) - di chuyển sang phải 1 đơn vị
- **Hiển thị**: "Robot rẽ phải, đi theo hướng Đông"

### Bước 4
- **Trạng thái cảm biến**: Trái=False, Giữa=True, Phải=False
- **Quyết định**: Robot đi thẳng
- **Hướng mới**: 1 (Đông) - không thay đổi
- **Vị trí mới**: (2, 2) - tiếp tục di chuyển sang phải
- **Hiển thị**: "Robot đi thẳng theo hướng Đông"

### Bước 5
- **Trạng thái cảm biến**: Trái=False, Giữa=True, Phải=False
- **Quyết định**: Robot đi thẳng
- **Hướng mới**: 1 (Đông) - không thay đổi
- **Vị trí mới**: (3, 2) - tiếp tục di chuyển sang phải
- **Hiển thị**: "Robot đi thẳng theo hướng Đông"

### Bước 6
- **Trạng thái cảm biến**: Trái=True, Giữa=False, Phải=False
- **Quyết định**: Robot rẽ trái (vì cảm biến trái phát hiện line)
- **Hướng mới**: 0 (Bắc) - thay đổi từ Đông sang Bắc
- **Vị trí mới**: (3, 3) - di chuyển lên trên 1 đơn vị
- **Hiển thị**: "Robot rẽ trái, đi theo hướng Bắc"

### Bước 7
- **Trạng thái cảm biến**: Trái=False, Giữa=True, Phải=False
- **Quyết định**: Robot đi thẳng
- **Hướng mới**: 0 (Bắc) - không thay đổi
- **Vị trí mới**: (3, 4) - tiếp tục di chuyển lên trên
- **Hiển thị**: "Robot đi thẳng theo hướng Bắc"

### Bước 8
- **Trạng thái cảm biến**: Trái=False, Giữa=False, Phải=True
- **Quyết định**: Robot rẽ phải
- **Hướng mới**: 1 (Đông) - thay đổi từ Bắc sang Đông
- **Vị trí mới**: (4, 4) - di chuyển sang phải 1 đơn vị
- **Hiển thị**: "Robot rẽ phải, đi theo hướng Đông"

### Bước 9
- **Trạng thái cảm biến**: Trái=False, Giữa=True, Phải=False
- **Quyết định**: Robot đi thẳng
- **Hướng mới**: 1 (Đông) - không thay đổi
- **Vị trí mới**: (5, 4) - tiếp tục di chuyển sang phải
- **Hiển thị**: "Robot đi thẳng theo hướng Đông"

### Bước 10
- **Trạng thái cảm biến**: Trái=True, Giữa=False, Phải=False
- **Quyết định**: Robot rẽ trái
- **Hướng mới**: 0 (Bắc) - thay đổi từ Đông sang Bắc
- **Vị trí mới**: (5, 5) - di chuyển lên trên 1 đơn vị
- **Hiển thị**: "Robot rẽ trái, đi theo hướng Bắc"

## Tóm tắt hành trình
- **Vị trí ban đầu**: (0, 0)
- **Vị trí cuối cùng**: (5, 5)
- **Hướng cuối cùng**: Bắc

## Biểu diễn trực quan hành trình (sử dụng ASCII)
```
    ^
    |
    |
    ^
    |
> > ^ > >

(0,0)
```

Trong biểu diễn này:
- `^` biểu thị robot đang hướng lên (Bắc)
- `>` biểu thị robot đang hướng sang phải (Đông)
- `v` biểu thị robot đang hướng xuống (Nam) - không xuất hiện trong ví dụ này
- `<` biểu thị robot đang hướng sang trái (Tây) - không xuất hiện trong ví dụ này