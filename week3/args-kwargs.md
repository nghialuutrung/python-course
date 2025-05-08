# **Tham số *args**:

Cho phép truyền số lượng không xác định đối số vị trí

```python
def sum_all(*args):
    total = 0
    for num in args:
        total += num
    return total

print(sum_all(1, 2))          # 3
print(sum_all(1, 2, 3, 4, 5)) # 15
```

# **Tham số **kwargs**:

Cho phép truyền số lượng không xác định đối số theo tên

```python
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25)
print_info(name="Bob", age=30, job="Developer")
```

# **Kết hợp các loại tham số**:

```python
def example(pos1, pos2, *args, kw1="default", **kwargs):
    print(f"pos1: {pos1}, pos2: {pos2}")
    print(f"args: {args}")
    print(f"kw1: {kw1}")
    print(f"kwargs: {kwargs}")

example(1, 2, 3, 4, 5, kw1="custom", name="Alice", age=25)
```
