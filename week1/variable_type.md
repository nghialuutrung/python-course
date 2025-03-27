# Kiểu dữ liệu - Numbers

  - **Integer (int)**:
    ```python
    a = 10        # Số nguyên thường
    b = 0b1010    # Nhị phân (10)
    c = 0o12      # Bát phân (10)
    d = 0xA       # Thập lục phân (10)
    
    # Số nguyên lớn không giới hạn
    big_num = 1234567890123456789
    ```
  - **Float (float)**:
    ```python
    a = 3.14      # Decimal
    b = 3.0       # Integer as float
    c = 3e8       # Scientific notation (3 × 10^8)
    d = float('inf')  # Infinity
    ```
  - **Complex (complex)**:
    ```python
    a = 3 + 4j    # Complex number
    b = complex(3, 4)  # Constructor
    ```

# Kiểu dữ liệu - Strings

  - **Khai báo string**:
    ```python
    s1 = 'Single quotes'
    s2 = "Double quotes"
    s3 = '''Triple quotes for
    multiple lines'''
    s4 = """Also triple double quotes
    for multiple lines"""
    ```
  - **Escape characters**:
    ```python
    # Newline
    s1 = "Hello\nWorld"
    # Tab
    s2 = "Hello\tWorld"
    # Backslash
    s3 = "Path: C:\\Users\\Name"
    # Quotes
    s4 = "He said, \"Hello!\""
    ```
  - **Raw strings**:
    ```python
    # Ignore escape sequences
    raw_str = r"C:\Users\Name\Documents"
    ```


# String Indexing và Slicing

  - **Indexing**:
    ```python
    s = "Python"
    #    012345  (indexes)
    
    first = s[0]    # 'P'
    last = s[-1]    # 'n'
    ```
  - **Slicing**:
    ```python
    s = "Python Programming"
    #    0123456789...
    
    # s[start:end:step]
    s[0:6]      # "Python"
    s[:6]       # "Python" (start mặc định là 0)
    s[7:]       # "Programming" (end mặc định là len(s))
    s[7:12]     # "Progr"
    s[::2]      # "Pto rgamn" (step 2)
    s[::-1]     # "gnimmargorP nohtyP" (đảo ngược)
    ```

# String Methods

  - **Các phương thức thường dùng**:
    ```python
    s = "  Python Programming  "
    
    # Case methods
    s.upper()     # "  PYTHON PROGRAMMING  "
    s.lower()     # "  python programming  "
    s.title()     # "  Python Programming  "
    
    # Whitespace
    s.strip()     # "Python Programming"
    s.lstrip()    # "Python Programming  "
    s.rstrip()    # "  Python Programming"
    
    # Search
    s.find("Pro")  # 9 (index of first match)
    s.count("P")   # 2 (occurrences of "P")
    
    # Replace
    s.replace("Python", "Java")
    ```
  - **Kiểm tra chuỗi**:
    ```python
    "python".isalpha()  # True
    "123".isdigit()     # True
    "python3".isalnum() # True
    "  ".isspace()      # True
    ```

# Kiểu dữ liệu - Boolean và None

  - **Boolean (bool)**:
    ```python
    a = True
    b = False

    # Kết quả của phép so sánh
    c = 5 > 3   # True
    d = 10 == 9 # False
    ```
  - **Truthy và Falsy**:
    - Falsy values: `False`, `0`, `0.0`, `""`, `[]`, `{}`, `None`
    - Truthy values: Gần như mọi thứ khác
    ```python
    # Kiểm tra truthy/falsy
    bool(0)     # False
    bool("")    # False
    bool([])    # False
    bool(42)    # True
    bool("hi")  # True
    ```
  - **None**:
    ```python
    x = None
    print(x)       # None
    print(x is None)  # True
    ```