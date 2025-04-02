# Ứng dụng thực tế:
- **Quản lý danh sách sản phẩm**:

    ```python
    products = [
        {"id": 1, "name": "Laptop", "price": 1500},
        {"id": 2, "name": "Phone", "price": 800},
        {"id": 3, "name": "Tablet", "price": 500}
    ]
    ```

- **Xử lý dữ liệu thời gian thực**:

    ```python
    # Lưu trữ dữ liệu nhiệt độ theo thời gian
    temperatures = [25.5, 26.1, 25.8, 26.3, 25.9]
    ```

- **Quản lý đơn hàng**:

    ```python
    orders = [
        {"order_id": "ORD001", "items": ["Laptop", "Mouse"], "total": 1600},
        {"order_id": "ORD002", "items": ["Phone", "Case"], "total": 850}
    ]
    ```

# Ví dụ trực quan:

- **Danh sách mua sắm**:

    ```python
    # Giống như một danh sách mua sắm trên giấy
    shopping_list = ["Sữa", "Trứng", "Bánh mì", "Rau xanh"]
    # Bạn có thể thêm/xóa món hàng tùy ý
    shopping_list.append("Nước ngọt")  # Thêm vào cuối
    shopping_list.remove("Trứng")      # Xóa món đã mua
    ```

- **Bảng điểm lớp học**:

    ```python
    # Giống như một bảng điểm trên giấy
    class_scores = [
        ["Học sinh A", 8.5, 9.0, 7.5],  # Mỗi dòng là một học sinh
        ["Học sinh B", 7.0, 8.5, 9.0],
        ["Học sinh C", 9.5, 8.0, 8.5]
    ]
    # Có thể thêm điểm mới hoặc sửa điểm cũ
    class_scores[0][1] = 9.0  # Sửa điểm của học sinh A
    ```

- **Lịch trình trong ngày**:

    ```python
    # Giống như một cuốn lịch để bàn
    daily_schedule = [
        "7:00 - Thức dậy",
        "8:00 - Ăn sáng",
        "9:00 - Học Python",
        "12:00 - Ăn trưa",
        "14:00 - Làm bài tập"
    ]
    # Có thể thêm hoặc thay đổi lịch trình
    daily_schedule.insert(2, "8:30 - Tập thể dục")
    ```
