examples =  [15, 23, 8, 42, 16, 4, 31, 27]
wanted = 4
# for x in examples:
#     print(x)
#     if wanted == x:
#         print()
# for i in range(len(examples)):
#     print(examples[i])
#     print(i)
#     print("\n")

# if wanted == examples[0]:
#     print("Vị trí số 0")
# if wanted == examples[1]:
#     print("Vị trí số 1")
# if wanted == examples[2]:
#     print("Vị trí số 2")
# if wanted == examples[3]:
#     print("Vị trí số 3")
# if wanted == examples[4]:
#     print("Vị trí số 4")
# if wanted == examples[5]:
#     print("Vị trí số 5")
# if wanted == examples[6]:
#     print("Vị trí số 6")
# if wanted == examples[7]:
#     print("Vị trí số 7")


xuat_hien = False

for i in range(len(examples)):
    print(examples[i])
    if wanted == examples[i]:
        xuat_hien = True
        # break
if xuat_hien == True:
    print(f"Có số {wanted}")
    print(f"Vị trí số {i}")
else:
    print(f"Wanted: {wanted} không tìm thấy")
# else:
#     print(f"Wanted: {wanted} không tìm thấy")
