# Các thao tác cow barn với Set:

```python
# Tạo set
numbers = {1, 2, 3, 4, 5}
```

```python
# Thêm phần tử
numbers.add(6)          # Thêm một phần tử
numbers.update([7, 8])  # Thêm nhiều phần tử
```

```python
# Xóa phần tử
numbers.remove(3)       # Xóa phần tử 3, nếu không có sẽ báo lỗi
numbers.discard(10)     # Xóa phần tử 10, không báo lỗi nếu không có
popped = numbers.pop()  # Xóa và trả về một phần tử ngẫu nhiên
```

```python
# Kiểm tra thành viên
2 in numbers            # True nếu 2 có trong set
```

```python
# Xóa tất cả phần tử
numbers.clear()         # Set rỗng: set()
```

# Phép toán tập hợp:

```python
A = {1, 2, 3}
B = {3, 4, 5}
```

```python
# Hợp (Union) - tất cả phần tử từ cả A và B
A | B               # {1, 2, 3, 4, 5}
A.union(B)          # {1, 2, 3, 4, 5}
```

```python
# Giao (Intersection) - phần tử xuất hiện trong cả A và B
A & B               # {3}
A.intersection(B)   # {3}
```

```python
# Hiệu (Difference) - phần tử trong A nhưng không trong B
A - B               # {1, 2}
A.difference(B)     # {1, 2}
```

```python
# Hiệu đối xứng (Symmetric Difference) - phần tử có trong A hoặc B nhưng không có ở cả hai
A ^ B               # {1, 2, 4, 5}
A.symmetric_difference(B)  # {1, 2, 4, 5}
```

```python
# Kiểm tra tập hợp con
{1, 2}.issubset(A)  # True
A.issuperset({1, 2}) # True
```