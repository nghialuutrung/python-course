total = 0
count = 0
count_number = 0
count_string = 0
count_list = 0
# for i in range(10):
#     print(f"Before: {total}")
#     if i % 2 == 0 :
#         total = i+total
#         print(f"Hien thi: {i} neu la so chan")
#     print(f"After: {total}")
#     print("\n")

# name = "Thay Nghia"
# for char in name:
#     print(char)
#     if char == "a":
#         count = count+1
#         print("Co ki tu a o day")
# print(count)

danh_sach = ["alo", 123, "hihi", "hehe", [456]]
for number in danh_sach:
    print(f"Gtri hien tai: {number}")
    print(isinstance(number, (int, float, complex)))
    if isinstance(number, (int, float, complex)) == True:
        count_number = count_number+1
    elif isinstance(number, str):
        count_string = count_string+1
    else:
        count_list = count_list+1
        
print(f"So luong so co trong danh sach la: {count_number}")
print(f"So luong string co trong danh sach la: {count_string}")
print(f"So luong list co trong danh sach la: {count_list}")
