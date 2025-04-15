# Ví dụ trực quan về vòng lặp lồng nhau:

```python
# Vẽ hình chữ nhật bằng dấu *
rows = 3
cols = 5
for i in range(rows):
    for j in range(cols):
        print("*", end=" ")  # end=" " giữ nguyên dòng
    print()  # xuống dòng sau mỗi hàng

# Kết quả:
# * * * * *
# * * * * *
# * * * * *
```

# Ví dụ thực tế: Duyệt ma trận 2 chiều/hay các ô cell

```python
# Tính tổng các phần tử trong ma trận
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

total = 0
for row in matrix:
    for element in row:
        total += element

print(f"Tổng các phần tử: {total}")  # 45
```

# Ví dụ nâng cao: Vẽ tam giác bằng dấu

```python
# Vẽ tam giác vuông
height = 5
for i in range(1, height + 1):
    for j in range(i):
        print("*", end="")
    print()  # xuống dòng

# Kết quả:
# *
# **
# ***
# ****
# *****
```