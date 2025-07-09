# WRO 2025
# 5 bài tập độc lập, mỗi bài 20-25 phút

"""
🏆 WRO 2025

Cấu trúc: 5 bài tập x 20-25 phút
Mỗi bài tập hoàn toàn độc lập, có đề bài rõ ràng

Lịch trình:
- Bài 1 (20 phút): Nhận diện màu sắc vật thể
- Bài 2 (25 phút): Robot đi theo đường line
- Bài 3 (25 phút): Tính khoảng cách và lập kế hoạch
- Bài 4 (25 phút): Tránh chướng ngại vật
- Bài 5 (25 phút): Tối ưu hóa thời gian hoàn thành
"""

print("🏆 WRO 2025 - BÀI TẬP ")
print("=" * 50)
print("📚 5 bài tập độc lập, mỗi bài 20-25 phút")
print()

# ==========================================
# BÀI TẬP 1: NHẬN DIỆN MÀU SẮC VẬT THỂ (20 phút)
# ==========================================

def bai_tap_1():
    """
    🎯 BÀI TẬP 1: NHẬN DIỆN MÀU SẮC VẬT THỂ
    ⏰ Thời gian: 20 phút

    📋 ĐỀ BÀI:
    Trong cuộc thi WRO 2025, robot cần nhận diện vật thể theo màu sắc:
    - Vật thể đỏ (255, 0, 0)
    - Vật thể xanh lá (0, 255, 0)
    - Vật thể xanh dương (0, 0, 255)
    - Vật thể vàng (255, 255, 0)

    YÊU CẦU:
    1. Tạo dictionary lưu trữ thông tin màu sắc
    2. Viết function nhận diện màu dựa trên giá trị RGB
    3. Function trả về tên màu hoặc "unknown" nếu không nhận diện được
    4. Test với các giá trị RGB khác nhau

    INPUT: Tuple (R, G, B) với giá trị từ 0-255
    OUTPUT: String tên màu ("red", "green", "blue", "yellow", "unknown")

    VÍ DỤ:
    nhan_dien_mau((255, 0, 0)) → "red"
    nhan_dien_mau((128, 128, 128)) → "unknown"
    """
    print("🎯 BÀI TẬP 1: NHẬN DIỆN MÀU SẮC VẬT THỂ")
    print("⏰ Thời gian: 20 phút")
    print("-" * 40)

    # TODO: Học sinh viết code ở đây
    # Bước 1: Tạo dictionary màu sắc

    # Bước 2: Viết function nhận diện màu

    # Bước 3: Test với các trường hợp

    print("📝 HƯỚNG DẪN:")
    print("1. Tạo dictionary với key là tên màu, value là tuple RGB")
    print("2. Function duyệt qua dictionary để tìm màu khớp")
    print("3. Return 'unknown' nếu không tìm thấy")
    print("4. Test với ít nhất 5 trường hợp khác nhau")

# ==========================================
# BÀI TẬP 2: ROBOT ĐI THEO ĐƯỜNG LINE (25 phút)
# ==========================================

def bai_tap_2():
    """
    🎯 BÀI TẬP 2: ROBOT ĐI THEO ĐƯỜNG LINE
    ⏰ Thời gian: 25 phút

    📋 ĐỀ BÀI:
    Robot có 3 cảm biến line được bố trí như sau: [Trái, Giữa, Phải]
    Mỗi cảm biến trả về:
    - 0: Không phát hiện line (nền trắng)
    - 1: Phát hiện line (đường đen)

    LOGIC ĐIỀU KHIỂN:
    - [0, 1, 0]: Line ở giữa → Đi thẳng
    - [1, 0, 0]: Line lệch trái → Quay trái
    - [0, 0, 1]: Line lệch phải → Quay phải
    - [0, 0, 0]: Mất line → Dừng lại
    - [1, 1, 0], [0, 1, 1], [1, 1, 1]: Ưu tiên đi thẳng

    YÊU CẦU:
    1. Viết function xử lý dữ liệu 3 cảm biến
    2. Trả về hành động: "forward", "turn_left", "turn_right", "stop"
    3. Test với tất cả các trường hợp có thể xảy ra
    4. Giải thích logic cho từng trường hợp

    INPUT: List [left, center, right] với giá trị 0 hoặc 1
    OUTPUT: String hành động

    VÍ DỤ:
    xu_ly_line([0, 1, 0]) → "forward"
    xu_ly_line([1, 0, 0]) → "turn_left"
    """
    print("🎯 BÀI TẬP 2: ROBOT ĐI THEO ĐƯỜNG LINE")
    print("⏰ Thời gian: 25 phút")
    print("-" * 40)

    # TODO: Học sinh viết code ở đây

    print("📝 HƯỚNG DẪN:")
    print("1. Function nhận input là list 3 phần tử")
    print("2. Sử dụng if/elif/else để xử lý từng trường hợp")
    print("3. Ưu tiên cảm biến giữa (center) trước")
    print("4. Test với 8 trường hợp: 000, 001, 010, 011, 100, 101, 110, 111")

    # Test cases mẫu
    test_cases = [
        [0, 1, 0], [1, 0, 0], [0, 0, 1], [0, 0, 0],
        [1, 1, 0], [0, 1, 1], [1, 1, 1], [1, 0, 1]
    ]
    print(f"📊 Cần test {len(test_cases)} trường hợp")

# ==========================================
# BÀI TẬP 3: TÍNH KHOẢNG CÁCH VÀ LẬP KẾ HOẠCH (25 phút)
# ==========================================

def bai_tap_3():
    """
    🎯 BÀI TẬP 3: TÍNH KHOẢNG CÁCH VÀ LẬP KẾ HOẠCH
    ⏰ Thời gian: 25 phút

    📋 ĐỀ BÀI:
    Trên sân thi có các vật thể và khu vực đích:

    VẬT THỂ:
    - Vật thể đỏ tại (200, 200)
    - Vật thể xanh tại (300, 150)
    - Vật thể vàng tại (500, 250)
    - Vật thể xanh lá tại (600, 400)

    KHU VỰC ĐÍCH:
    - Khu vực đỏ tại (150, 150)
    - Khu vực xanh tại (650, 150)
    - Khu vực vàng tại (150, 450)
    - Khu vực xanh lá tại (650, 450)

    ROBOT xuất phát từ (120, 120)

    YÊU CẦU:
    1. Viết function tính khoảng cách giữa 2 điểm (công thức Pythagoras)
    2. Tìm khu vực đích phù hợp cho từng vật thể (cùng màu)
    3. Tính tổng khoảng cách: Robot → Vật thể → Khu vực đích
    4. Sắp xếp vật thể theo thứ tự khoảng cách tăng dần (gần nhất trước)
    5. In ra kế hoạch thu thập tối ưu

    CÔNG THỨC: distance = √[(x₂-x₁)² + (y₂-y₁)²]

    VÍ DỤ OUTPUT:
    1. Vật thể đỏ: khoảng cách 183.5
    2. Vật thể xanh: khoảng cách 532.8
    ...
    """
    print("🎯 BÀI TẬP 3: TÍNH KHOẢNG CÁCH VÀ LẬP KẾ HOẠCH")
    print("⏰ Thời gian: 25 phút")
    print("-" * 40)

    # Dữ liệu cho sẵn
    robot_pos = (120, 120)

    vat_the = [
        {"mau": "do", "x": 200, "y": 200},
        {"mau": "xanh", "x": 300, "y": 150},
        {"mau": "vang", "x": 500, "y": 250},
        {"mau": "xanh_la", "x": 600, "y": 400}
    ]

    khu_vuc = [
        {"mau": "do", "x": 150, "y": 150},
        {"mau": "xanh", "x": 650, "y": 150},
        {"mau": "vang", "x": 150, "y": 450},
        {"mau": "xanh_la", "x": 650, "y": 450}
    ]

    # TODO: Học sinh viết code ở đây

    print("📝 HƯỚNG DẪN:")
    print("1. Function tính khoảng cách: def tinh_khoang_cach(x1, y1, x2, y2)")
    print("2. Function tìm khu vực: def tim_khu_vuc(mau_vat_the, danh_sach_khu_vuc)")
    print("3. Tính tổng khoảng cách cho từng vật thể")
    print("4. Sắp xếp theo khoảng cách: list.sort(key=lambda x: x['khoang_cach'])")
    print("5. In kết quả theo thứ tự ưu tiên")

# ==========================================
# BÀI TẬP 4: TRÁNH CHƯỚNG NGẠI VẬT (25 phút)
# ==========================================

def bai_tap_4():
    """
    🎯 BÀI TẬP 4: TRÁNH CHƯỚNG NGẠI VẬT
    ⏰ Thời gian: 25 phút

    📋 ĐỀ BÀI:
    Robot có cảm biến khoảng cách ở 3 hướng: trước, trái, phải
    Khoảng cách an toàn: 30cm

    LOGIC TRÁNH CHƯỚNG NGẠI VẬT:
    - Nếu phía trước >= 30cm: Đi thẳng
    - Nếu phía trước < 30cm:
      + So sánh trái và phải
      + Quay về phía có khoảng cách lớn hơn
      + Nếu bằng nhau: Quay đầu (turn_around)

    CÁC TÌNH HUỐNG TEST:
    1. {"truoc": 50, "trai": 100, "phai": 100} → Đường thông thoáng
    2. {"truoc": 20, "trai": 80, "phai": 40} → Chướng ngại vật phía trước, trái rộng hơn
    3. {"truoc": 15, "trai": 30, "phai": 70} → Chướng ngại vật phía trước, phải rộng hơn
    4. {"truoc": 10, "trai": 25, "phai": 25} → Bị kẹt, cần quay đầu
    5. {"truoc": 35, "trai": 20, "phai": 15} → An toàn phía trước

    YÊU CẦU:
    1. Viết function phân tích tình huống
    2. Trả về quyết định: "forward", "turn_left", "turn_right", "turn_around"
    3. Test với tất cả 5 tình huống trên
    4. Giải thích logic cho từng trường hợp

    INPUT: Dictionary {"truoc": int, "trai": int, "phai": int}
    OUTPUT: String hành động
    """
    print("🎯 BÀI TẬP 4: TRÁNH CHƯỚNG NGẠI VẬT")
    print("⏰ Thời gian: 25 phút")
    print("-" * 40)

    # Dữ liệu test
    test_cases = [
        {"truoc": 50, "trai": 100, "phai": 100},
        {"truoc": 20, "trai": 80, "phai": 40},
        {"truoc": 15, "trai": 30, "phai": 70},
        {"truoc": 10, "trai": 25, "phai": 25},
        {"truoc": 35, "trai": 20, "phai": 15}
    ]

    # TODO: Học sinh viết code ở đây

    print("📝 HƯỚNG DẪN:")
    print("1. Định nghĩa KHOANG_CACH_AN_TOAN = 30")
    print("2. Kiểm tra khoảng cách phía trước trước")
    print("3. Nếu an toàn: return 'forward'")
    print("4. Nếu không an toàn: so sánh trái và phải")
    print("5. Test với 5 tình huống đã cho")

# ==========================================
# BÀI TẬP 5: TỐI ƯU HÓA THỜI GIAN (25 phút)
# ==========================================

def bai_tap_5():
    """
    🎯 BÀI TẬP 5: TỐI ƯU HÓA THỜI GIAN HOÀN THÀNH
    ⏰ Thời gian: 25 phút

    📋 ĐỀ BÀI:
    Cuộc thi WRO có giới hạn thời gian. Robot cần hoàn thành nhiệm vụ nhanh nhất.

    THÔNG SỐ:
    - Tốc độ robot: 50 cm/giây
    - Thời gian thu thập 1 vật thể: 3 giây
    - Thời gian đặt vật thể vào khu vực: 2 giây

    NHIỆM VỤ:
    Robot cần thu thập 3 vật thể:
    1. Vật thể A tại (200, 200) → Khu vực A tại (150, 150)
    2. Vật thể B tại (400, 300) → Khu vực B tại (600, 100)
    3. Vật thể C tại (300, 500) → Khu vực C tại (500, 450)

    Robot xuất phát từ (100, 100)

    YÊU CẦU:
    1. Tính thời gian cho từng nhiệm vụ:
       - Thời gian di chuyển = Khoảng cách / Tốc độ
       - Thời gian thu thập = 3 giây
       - Thời gian đặt = 2 giây
    2. So sánh 2 chiến lược:
       - Chiến lược 1: Thu thập theo thứ tự A → B → C
       - Chiến lược 2: Thu thập theo khoảng cách gần nhất trước
    3. Tính tổng thời gian cho mỗi chiến lược
    4. Đề xuất chiến lược tối ưu

    CÔNG THỨC:
    Thời gian 1 nhiệm vụ = Thời gian đến vật thể + Thu thập + Đến khu vực + Đặt vật thể
    """
    print("🎯 BÀI TẬP 5: TỐI ƯU HÓA THỜI GIAN HOÀN THÀNH")
    print("⏰ Thời gian: 25 phút")
    print("-" * 40)

    # Dữ liệu cho sẵn
    robot_start = (100, 100)
    TOC_DO = 50  # cm/giây
    THOI_GIAN_THU_THAP = 3  # giây
    THOI_GIAN_DAT = 2  # giây

    nhiem_vu = [
        {"ten": "A", "vat_the": (200, 200), "khu_vuc": (150, 150)},
        {"ten": "B", "vat_the": (400, 300), "khu_vuc": (600, 100)},
        {"ten": "C", "vat_the": (300, 500), "khu_vuc": (500, 450)}
    ]

    # TODO: Học sinh viết code ở đây

    print("📝 HƯỚNG DẪN:")
    print("1. Function tính thời gian 1 nhiệm vụ")
    print("2. Function tính tổng thời gian cho 1 chiến lược")
    print("3. Thử chiến lược A→B→C")
    print("4. Thử chiến lược gần nhất trước")
    print("5. So sánh và đưa ra kết luận")
    print("6. Bonus: Tìm chiến lược tốt hơn nữa")

# ==========================================
# MENU CHÍNH
# ==========================================

def main():
    """Menu chọn bài tập"""
    print("📚 CHỌN BÀI TẬP:")
    print("1. Bài 1: Nhận diện màu sắc vật thể (20 phút)")
    print("2. Bài 2: Robot đi theo đường line (25 phút)")
    print("3. Bài 3: Tính khoảng cách và lập kế hoạch (25 phút)")
    print("4. Bài 4: Tránh chướng ngại vật (25 phút)")
    print("5. Bài 5: Tối ưu hóa thời gian (25 phút)")
    print("0. Hiển thị tất cả đề bài")
    print()

    choice = input("Nhập số bài tập (0-5): ")

    if choice == "1":
        bai_tap_1()
    elif choice == "2":
        bai_tap_2()
    elif choice == "3":
        bai_tap_3()
    elif choice == "4":
        bai_tap_4()
    elif choice == "5":
        bai_tap_5()
    elif choice == "0":
        bai_tap_1()
        print("\n" + "="*50 + "\n")
        bai_tap_2()
        print("\n" + "="*50 + "\n")
        bai_tap_3()
        print("\n" + "="*50 + "\n")
        bai_tap_4()
        print("\n" + "="*50 + "\n")
        bai_tap_5()
    else:
        print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()