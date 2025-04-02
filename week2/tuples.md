# Ứng dụng thực tế

- **Lưu trữ tọa độ địa lý**:

```python
location = (10.8231, 106.6297)  # Tọa độ TP.HCM
```

- **Cấu hình không thay đổi**:

```python
DATABASE_CONFIG = ("localhost", 3306, "admin", "password")
```

- **Kết quả trả về từ hàm**:

```python
def get_student_info():
    return ("John", 20, "A")  # Tên, tuổi, điểm
```

#  Ví dụ trực quan:

- **Thông tin cá nhân không thay đổi**:

```python
# Giống như thông tin trên chứng minh thư
id_card = ("Nguyễn Văn A", "123456789", "01/01/2000")

# Không thể thay đổi thông tin này
# id_card[0] = "Nguyễn Văn B"  # Lỗi!
```

- **Tọa độ địa điểm**:

```python
# Giống như địa chỉ nhà
home_address = (10.8231, 106.6297)  # Vĩ độ, Kinh độ
school_address = (10.8333, 106.6667)
# Tọa độ không thể thay đổi
```

- **Kích thước sản phẩm**:

```python
# Giống như thông số kỹ thuật của sản phẩm
laptop_specs = ("Dell XPS", "15 inch", "16GB RAM")
# Thông số kỹ thuật là cố định
```