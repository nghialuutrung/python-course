# Bài 1 week 2
danh_sach = [2,4,6,8,10]
danh_sach.append(6)
danh_sach.insert(0,0)
print(f"Danh sách: {danh_sach}")

# Bài 2 week 2
points = (1,2)
# points[1] = 3
print(list(points))
print(points(list))

#Bài 3 week 2
diem_so = [7,6,9,8]
tong_diem = sum(diem_so)
avg = tong_diem / len(danh_sach)
diem_cao_nhat = max(diem_so)
diem_thap_nhat = min(diem_so)
print(f"Điểm trung bình: {avg}")
print(f"Điểm cao nhất: {diem_cao_nhat}")
print(f"Điểm thấp nhất: {diem_thap_nhat}")