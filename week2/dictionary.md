# Ứng dụng thực tế:

- **Quản lý thông tin người dùng**:

```python
user = {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "preferences": {
        "theme": "dark",
        "language": "vi"
    }
}
```

- **Cấu hình ứng dụng**:

```python
config = {
    "database": {
        "host": "localhost",
        "port": 3306,
        "name": "mydb"
    },
    "api": {
        "base_url": "https://api.example.com",
        "timeout": 30,
        "user_ids": [1, 83, 278]
    }
}
```

- **Xử lý dữ liệu JSON**:

```python
weather_data = {
    "city": "Hanoi",
    "temperature": 28,
    "humidity": 75,
    "forecast": ["sunny", "cloudy", "rainy"]
}
```

# Ví dụ trực quan:

- **Từ điển tiếng Anh**:

```python
# Giống như một cuốn từ điển
dictionary = {
    "hello": "xin chào",
    "goodbye": "tạm biệt",
    "thank you": "cảm ơn"
}
# Tra từ nhanh chóng
meaning = dictionary["hello"]  # "xin chào"
```

- **Danh bạ điện thoại**:

```python
# Giống như danh bạ trên điện thoại
phone_book = {
    "Mẹ": "0123456789",
    "Bố": "0987654321",
    "Bạn thân": "0369852147"
}
# Tìm số điện thoại theo tên
mom_phone = phone_book["Mẹ"]
```

- **Thực đơn nhà hàng**:

```python
# Giống như menu trong nhà hàng
menu = {
    "Phở": 50000,
    "Bún bò": 45000,
    "Cơm tấm": 40000
}
# Xem giá món ăn nhanh chóng
pho_price = menu["Phở"]
```