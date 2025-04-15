# Bài tập 1: Quản lý danh sách sinh viên

Tôi có một dữ liệu sinh viên có format như dưới đây:
```python
# 1. Tạo dictionary lưu thông tin sinh viên
students = {
    "SV001": {
        "name": "Nguyễn Văn A",
        "age": 20,
        "grades": [8.5, 9.0, 7.5]
    },
    "SV002": {
        "name": "Trần Thị B",
        "age": 19,
        "grades": [9.0, 8.5, 9.0]
    }
}
```

1. Thêm 1 sinh viên
gợi ý: thêm trực tiếp giá trị vào dictionary
```python
students["SV003"] = {
    "name": "Phạm Văn C",
    "age": 21,
    "grades": [7.5, 8.0, 8.5]
}
```
2. Xóa 1 sinh viên
gợi ý: có thể sử dụng pop và key của sinh viên
3. Sửa thông tin sinh viên
gợi ý: có thể sử dụng trực tiếp key của sinh viên và giá trị muốn thay đổi
ví dụ: students[studen_key]["name"] = gia_tri_moi

## Bài tập 2: Bài tập tổng hợp

1. Tạo một hệ thống quản lý khóa học với:
   - Dictionary lưu thông tin các khóa học (mã khóa học, tên, giảng viên)
   - List lưu danh sách sinh viên đăng ký mỗi khóa học
   - Set lưu những mã sinh viên đã hoàn thành khóa học
   - Tuple lưu thông tin cố định của khóa học (thời gian, địa điểm, số tín chỉ)

gợi ý: tạo một cấu trúc dữ liệu lồng nhau để quản lý thông tin
```python
courses = {
    "CS101": {
        "name": "Nhập môn lập trình",
        "instructor": "Nguyễn Văn X",
        "fixed_info": ("8:00-10:00 T2", "Phòng A1", 3),  # tuple: (thời gian, địa điểm, số tín chỉ)
        "enrolled_students": ["SV001", "SV002", "SV003"],  # list sinh viên đăng ký
        "completed_students": {"SV001", "SV002"}  # set sinh viên hoàn thành
    },
    "CS102": {
        "name": "Cấu trúc dữ liệu",
        "instructor": "Trần Thị Y",
        "fixed_info": ("13:00-15:00 T4", "Phòng B2", 4),
        "enrolled_students": ["SV002", "SV003", "SV004"],
        "completed_students": {"SV002"}
    }
}
```

2. Thực hiện các thao tác:
   - Đăng ký sinh viên vào khóa học
   gợi ý: thêm mã sinh viên vào list enrolled_students nếu chưa có
   ```python
   # Đăng ký sinh viên "SV005" vào khóa học "CS101"
   if "SV005" not in courses["CS101"]["enrolled_students"]:
       courses["CS101"]["enrolled_students"].append("SV005")
       print(f"Sinh viên SV005 đã đăng ký thành công khóa học CS101")
   ```

   - Đánh dấu sinh viên đã hoàn thành khóa học
   gợi ý: thêm mã sinh viên vào set completed_students
   ```python
   # Đánh dấu sinh viên "SV003" đã hoàn thành khóa học "CS101"
   if "SV003" in courses["CS101"]["enrolled_students"]:
       courses["CS101"]["completed_students"].add("SV003")
       print(f"Sinh viên SV003 đã hoàn thành khóa học CS101")
   ```

   - Tính tỷ lệ hoàn thành của mỗi khóa học
   gợi ý: chia số lượng sinh viên đã hoàn thành cho số lượng sinh viên đăng ký
   ```python
   # Tính tỷ lệ hoàn thành của khóa học "CS101"
   enrolled = len(courses["CS101"]["enrolled_students"])
   completed = len(courses["CS101"]["completed_students"])
   if enrolled > 0:
       completion_rate = completed / enrolled
       print(f"Tỷ lệ hoàn thành của khóa học CS101: {completion_rate:.2f}")
   ```

   - Hiển thị danh sách khóa học mà một sinh viên đã đăng ký
   gợi ý: duyệt qua tất cả khóa học và kiểm tra xem sinh viên có trong danh sách đăng ký không
   ```python
   # Tìm khóa học mà sinh viên "SV002" đã đăng ký
   student_id = "SV002"
   enrolled_courses = []
   for course_id, course_info in courses.items():
       if student_id in course_info["enrolled_students"]:
           enrolled_courses.append(course_id)
   print(f"Sinh viên {student_id} đã đăng ký các khóa học: {enrolled_courses}")
   ```

3. Thêm các yêu cầu luyện tập:
   - Sử dụng list: Lọc danh sách các sinh viên đã đăng ký nhưng chưa hoàn thành khóa học
   ```python
   # Tìm sinh viên đã đăng ký nhưng chưa hoàn thành khóa học "CS101"
   not_completed = []
   for student in courses["CS101"]["enrolled_students"]:
       if student not in courses["CS101"]["completed_students"]:
           not_completed.append(student)
   print(f"Sinh viên chưa hoàn thành khóa học CS101: {not_completed}")
   ```

   - Sử dụng dictionary: Thống kê số lượng khóa học mà mỗi sinh viên đã đăng ký
   ```python
   # Đếm số khóa học mà mỗi sinh viên đã đăng ký
   student_course_count = {}
   for course_id, course_info in courses.items():
       for student in course_info["enrolled_students"]:
           if student in student_course_count:
               student_course_count[student] += 1
           else:
               student_course_count[student] = 1
   print(f"Số khóa học đã đăng ký của mỗi sinh viên: {student_course_count}")
   ```

   - Sử dụng set: Tìm sinh viên đã đăng ký tất cả các khóa học
   ```python
   # Tìm sinh viên đã đăng ký tất cả các khóa học
   all_courses_students = set(courses["CS101"]["enrolled_students"])
   for course_id, course_info in courses.items():
       if course_id != "CS101":  # Bỏ qua khóa học đầu tiên đã xét
           all_courses_students = all_courses_students & set(course_info["enrolled_students"])
   print(f"Sinh viên đã đăng ký tất cả khóa học: {all_courses_students}")
   ```

   - Sử dụng tuple: Sắp xếp khóa học theo số tín chỉ (phần tử thứ 3 trong tuple fixed_info)
   ```python
   # Sắp xếp khóa học theo số tín chỉ
   courses_by_credits = []
   for course_id, course_info in courses.items():
       courses_by_credits.append((course_id, course_info["fixed_info"][2]))  # Lấy số tín chỉ

   # Sắp xếp theo số tín chỉ tăng dần
   sorted_courses = sorted(courses_by_credits, key=lambda x: x[1])
   print(f"Khóa học theo số tín chỉ tăng dần: {sorted_courses}")
   ```

Lưu ý: Các bạn có thể tự tạo dữ liệu mẫu để thực hành và thử nghiệm các thao tác trên.
