# Dynamic Typing:

```python
x = 10        # x là kiểu int
x = "hello"   # x là kiểu str
x = [1, 2, 3] # x là kiểu list
```

# Multiple Assignment:

```python
# Gán cùng giá trị cho nhiều biến
x = y = z = 0

# Gán nhiều giá trị cho nhiều biến
a, b, c = 1, 2, 3

# Hoán đổi giá trị (swap)
a, b = b, a
```

# Unpacking:

```python
# Unpacking từ list/tuple
coordinates = (10, 20)
x, y = coordinates

# Unpacking với *
first, *rest = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4, 5]
```