# Bài 2 week 1


# Bài 3 week 1
van_ban = input("Nhập văn bản:")
ky_tu = len(van_ban)
cac_tu = van_ban.split()
so_tu = len(cac_tu)
so_cau = van_ban.count('.') + van_ban.count('?') + van_ban.count('!')
print(f"Số ký tự: {ky_tu}")
print(f"Số từ: {so_tu}")
print(f"Số câu: {so_cau}")