# Bài 1 week 2
danh_sach = [2,4,6,8,10]
danh_sach.append(6)
danh_sach.insert(0,0)
print(f"Danh sách: {danh_sach}")

# Bài 2 week 2
points = (1,2)
# points[1] = 3
print(list(points))
# print(points(list))

# Bài 3 week 2
diem_so = [7,6,9,8]
tong_diem = sum(diem_so)
avg = tong_diem / len(danh_sach)
diem_cao_nhat = max(diem_so)
diem_thap_nhat = min(diem_so)
print(f"Điểm trung bình: {avg}")
print(f"Điểm cao nhất: {diem_cao_nhat}")
print(f"Điểm thấp nhất: {diem_thap_nhat}")

# Bài 2 Week 2
khoahoc = {
    "lop1": {
        "ten": "Lập Trình Cơ Bản",
        "giaovien": "Nguyễn Văn A",
        "diadiem": ("lop A", "tang 1"),
        "hocsinh": ["GATE1", "GATE2", "GATE3"],
        "done": {"GATE 2"},
    },
}

if "GATE4" not in khoahoc["lop1"]["hocsinh"]:
    khoahoc["lop1"]["hocsinh"].append("GATE4")
    print(f"Học sinh GATE 4 đki thành công lớp 1")

if "GATE1" in khoahoc["lop1"]["hocsinh"]:
    khoahoc["lop1"]["done"].add("GATE1")
    print(f"Học sinh GATE 1 đã hoàn thành khóa học")

# con không biết làm phần tỷ lệ hoàn thành khóa học, danh sách khóa học học sinh đăng kí, thống kê số lượng khóa học mỗi HS đăng kí
# print(":(")

not_done = []
for hocsinh in khoahoc["lop1"]["done"]:
    not_done.append(hocsinh)
    print(f"Học sinh chưa hoàn thành khóa học: {not_done}")
