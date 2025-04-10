# Công thức tính thứ trong tuần
Giả sử có 3 biến chứa ngày tháng năm là day, month, year

Công thức để tính thứ trong tuần sẽ là:

```python
q = day
m = month
Y = year
K = year % 100    # năm trong thế kỉ
J = year // 100   # thế kỉ bao nhiêu

h = (q + math.floor((13 * (m + 1)) / 5) + K + math.floor(K / 4) + math.floor(J / 4) - 2 * J) % 7
```

hãy áp dụng match-case để in ra là thời gian nhập vào là thứ mấy