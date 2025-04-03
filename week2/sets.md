# Ứng dụng thực tế:

- **Tìm bạn chung trên mạng xã hội**:

```python
john_friends = {"Alice", "Bob", "Charlie"}
mary_friends = {"Bob", "David", "Eve"}
mutual_friends = john_friends.intersection(mary_friends)
# Kết quả: {"Bob"}
```

- **Loại bỏ trùng lặp trong dữ liệu**:

```python
# Danh sách IP truy cập website
ip_addresses = ["192.168.1.1", "192.168.1.2", "192.168.1.1"]
unique_ips = set(ip_addresses)
# Kết quả: {"192.168.1.1", "192.168.1.2"}
```

- **Kiểm tra quyền truy cập**:

```python
user_permissions = {"read", "write"}
required_permissions = {"read", "execute"}
has_access = user_permissions.issuperset(required_permissions)
```

# Ví dụ trực quan:

- **Danh sách bạn bè**:

```python
# Giống như danh sách bạn bè trên Facebook
my_friends = {"Alice", "Bob", "Charlie"}
your_friends = {"Bob", "David", "Eve"}

# Tìm bạn chung
mutual_friends = my_friends.intersection(your_friends)
# Kết quả: {"Bob"}
```

- **Giỏ trái cây**:

```python
# Giống như một giỏ trái cây
fruits = {"táo", "cam", "chuối", "nho"}

# Thêm trái cây mới
fruits.add("dưa hấu")

# Không thể thêm trùng lặp
fruits.add("táo")  # Không có gì thay đổi
```

- **Thẻ thành viên**:

```python
# Giống như thẻ thành viên của cửa hàng
member_cards = {"VIP001", "VIP002", "VIP003"}

# Kiểm tra thẻ có hợp lệ không
is_valid = "VIP001" in member_cards  # True
```
