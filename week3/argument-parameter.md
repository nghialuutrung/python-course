# Tham số bắt buộc

```python
def power(base, exponent):
    return base ** exponent

result = power(2, 3)  # 8
```

# Tham số mặc định

```python
def power(base, exponent=2):
    return base ** exponent

result1 = power(2)     # 4 (mặc định exponent=2)
result2 = power(2, 3)  # 8 (ghi đè giá trị mặc định)
```

# Đối số vị trí và đối số theo tên

```python
def greet(first_name, last_name):
    return f"Xin chào, {first_name} {last_name}!"

# Đối số vị trí
print(greet("Nguyễn", "Văn A"))

# Đối số theo tên
print(greet(last_name="Văn A", first_name="Nguyễn"))
```
