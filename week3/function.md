# Ví dụ 1: Hàm không có tham số và không trả về giá trị

```python
def say_hello():
    """In lời chào đơn giản."""
    print("Hello, World!")

# Gọi hàm
say_hello()  # Kết quả: "Hello, World!"
```

# Ví dụ 2: Hàm có tham số

```python
def greet(name):
    """In lời chào với tên được cung cấp."""
    print(f"Xin chào, {name}!")

# Gọi hàm
greet("Alice")  # Kết quả: "Xin chào, Alice!"
greet("Bob")    # Kết quả: "Xin chào, Bob!"
```
# Ví dụ 3: Hàm trả về giá trị

```python
def sum_numbers(a, b):
    """Tính tổng hai số và trả về kết quả."""
    return a + b

# Gọi hàm và sử dụng kết quả
result = sum_numbers(5, 3)
print(f"Tổng: {result}")  # Kết quả: "Tổng: 8"
```