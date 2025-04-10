# Ví dụ 1: Kiểm tra số chẵn lẻ

```python
number = 5
if number % 2 == 0:
print(f"{number} là số chẵn")
else:
print(f"{number} là số lẻ")
```

# Ví dụ 2: Xếp loại học lực

```python
score = 85
if score >= 90:
    print("Xuất sắc")
elif score >= 80:
    print("Giỏi")
elif score >= 70:
    print("Khá")
elif score >= 60:
    print("Trung bình")
else:
    print("Cần cố gắng thêm")
```

# Ví dụ 3: Kiểm tra năm nhuận

```python
year = 2024
if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
    print(f"{year} là năm nhuận")
else:
    print(f"{year} không phải năm nhuận")
```