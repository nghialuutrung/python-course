# Ví dụ 1: Tính tổng số trong list

```python
numbers = [1, 2, 3, 4, 5]
total = 0
for num in numbers:
    total += num
print(f"Tổng: {total}")  # 15
```

# Ví dụ 2: Lặp qua dictionary

```python
student = {
    "name": "Nguyen Van A",
    "age": 20,
    "subject": "Python"
}
for key, value in student.items():
    print(f"{key}: {value}")
```

Ví dụ 3: Lặp với enumerate()

```python
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
```
