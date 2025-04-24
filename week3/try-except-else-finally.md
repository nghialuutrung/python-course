# ví dụ về xử dụng một khối điều khiển ngoại lệ đầy đủ.
Không phải lúc nào cũng cần khối xử lý ngoại lệ đầy đủ với try-except-else-finally đầy đủ.
Nhưng 1 khối ngoại lệ là bắt buộc phải có với try-except

# Ví dụ sau là một khối đầy đủ

```python
# Trường hợp 1: File tồn tại
file_path = "test.txt"

# Trường hợp 2: File không tồn tại
# file_path = "non_existent.txt"

# Trường hợp 3: File không có quyền truy cập
# file_path = "/root/important.txt"

try:
    # Mở file để đọc
    with open(file_path, 'r') as file:
        content = file.read()
        print("Đọc file thành công!")

except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy file {file_path}")

except PermissionError:
    print(f"Lỗi: Không có quyền truy cập file {file_path}")

except Exception as e:
    print(f"Lỗi không xác định: {str(e)}")

else:
    # Chỉ chạy khi không có ngoại lệ nào xảy ra
    print("Nội dung file:")
    print(content)

finally:
    # Luôn luôn chạy, dù có ngoại lệ hay không
    print("Quá trình xử lý file đã hoàn tất")
```

# Ví dụ 2: Xử lý đầu vào người dùng

```python
def get_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ!")

# Sử dụng
age = get_integer_input("Nhập tuổi của bạn: ")
```

# Ví dụ 3: Xử lý API:

```python
import requests

def get_data_from_api(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.Timeout:
        print("Yêu cầu hết thời gian chờ!")
    except requests.exceptions.HTTPError as e:
        print(f"Lỗi HTTP: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gửi yêu cầu: {e}")
    except ValueError:  # Khi response.json() thất bại
        print("Không thể phân tích dữ liệu JSON")
    return None
```
