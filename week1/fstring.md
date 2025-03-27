# f-strings (Python 3.6+):

```python
name = "Python"
version = 3.9

# Cú pháp cơ bản
f"Tôi đang học {name} phiên bản {version}"

# Với biểu thức
f"Phiên bản tiếp theo: {version + 0.1}"

# Định dạng số
pi = 3.14159
f"Pi bằng {pi:.2f}"  # "Pi bằng 3.14"

# Căn chỉnh
f"{'Trái':<10}|{'Phải':>10}"  # "Trái      |     Phải"
```

# Các phương pháp khác:

```python
# str.format() (Python 3+)
"Tôi đang học {} phiên bản {}".format(name, version)

# % operator (phong cách cũ)
"Pi bằng %.2f" % pi  # "Pi bằng 3.14"
```