# Ví dụ 1: Đếm ngược

```python
countdown = 5
while countdown > 0:
    print(countdown)
    countdown -= 1
print("Bắt đầu!")
```

# Ví dụ 2: Nhập dữ liệu cho đến khi hợp lệ

```python
while True:
    user_input = input("Nhập một số dương: ")
    if user_input.isdigit() and int(user_input) > 0:
        print(f"Bạn đã nhập số: {user_input}")
        break
    print("Vui lòng nhập một số dương hợp lệ!")
```

# Ví dụ 3: Tìm số nguyên tố

```python
num = 29
divisor = 2
is_prime = True

while divisor * divisor <= num:
    if num % divisor == 0:
        is_prime = False
        break
    divisor += 1

print(f"{num} {'là' if is_prime else 'không phải'} số nguyên tố")
```
