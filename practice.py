# Công thức tính thứ trong tuần Week 3
import math
day = int(input("Ngày: "))
month = 4
year = 2025
q = day
m = month
Y = year
K = year % 100    # năm trong thế kỉ
J = year // 100   # thế kỉ bao nhiêu

h = (q + math.floor((13 * (m + 1)) / 5) + K + math.floor(K / 4) + math.floor(J / 4) - 2 * J) % 7
day_of_week_zeller = h % 7

# match h:
#     case 0:
#         print(f"Hôm nay là Thứ 7 ngày {day} tháng {month} năm {year}")
#     case 1:
#         print(f"Hôm nay là Chủ Nhật ngày {day} tháng {month} năm {year}")
#     case 2:
#         print(f"Hôm nay là Thứ 2 ngày {day} tháng {month} năm {year}")
#     case 3:
#         print(f"Hôm nay là Thứ 3 ngày {day} tháng {month} năm {year}")
#     case 4:
#         print(f"Hôm nay là Thứ 4 ngày {day} tháng {month} năm {year}")
#     case 5:
#         print(f"Hôm nay là Thứ 5 ngày {day} tháng {month} năm {year}")
#     case _:
#         print(f"Hôm nay là Thứ 6 ngày {day} tháng {month} năm {year}")
        
if h == 0:
    print(f"Hôm nay là Thứ 7 ngày {day} tháng {month} năm {year}")
elif h == 1:
    print(f"Hôm nay là Chủ Nhật ngày {day} tháng {month} năm {year}")
elif h == 2:
    print(f"Hôm nay là Thứ 2 ngày {day} tháng {month} năm {year}")
elif h == 3:
    print(f"Hôm nay là Thứ 3 ngày {day} tháng {month} năm {year}")
elif h == 4:
    print(f"Hôm nay là Thứ 4 ngày {day} tháng {month} năm {year}")
elif h == 5:
    print(f"Hôm nay là Thứ 5 ngày {day} tháng {month} năm {year}")
else:
    print(f"Hôm nay là Thứ 6 ngày {day} tháng {month} năm {year}")