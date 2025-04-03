# Truy cập và thay đổi

```python
student = {
    "name": "John",
    "age": 20
}

# Truy cập
name = student["name"]
age = student.get("age")

# Thay đổi
student["age"] = 21
student["grade"] = "A"  # Thêm key mới
```

# Xóa phần tử

```python
del student["age"]
age = student.pop("age")
student.clear()  # Xóa tất cả
```

# Kiểm tra và loop

```python
"name" in student  # True

for key in student:
    print(key, student[key])
```
