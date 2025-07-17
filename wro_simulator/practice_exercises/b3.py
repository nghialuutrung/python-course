import math
def calc(x1, y1, x2, y2):
    x = (x1 - x2) ** 2
    y = (y1 - y2) ** 2
    square_root = math.sqrt(x + y)
    return square_root
print(calc(0,0,0,1))


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



sapxepduongdi = []



def tim_khu_vuc(mau_vat_the):
    for kv in khu_vuc:
        if mau_vat_the == kv['mau']:
            return kv
    return None
# print(calc(120,120,200,200))
# print(calc(200,200,150,150))
# KC_Den_VT = calc(120,120,200,200)
# KC_Den_KV = calc(200,200,150,150)
# print(f"Total KC Red: {KC_Den_KV+KC_Den_VT}")
# sapxepduongdi.append({"khoang_cach": KC_Den_KV+KC_Den_VT})

# print(calc(120,120,300,150))
# print(calc(300,150,650,150))
# KC_Den_VT = calc(120,120,300,150)
# KC_Den_KV = calc(300,150,650,150)
# print(f"Total KC Blue: {KC_Den_KV+KC_Den_VT}")
# sapxepduongdi.append({"khoang_cach": KC_Den_KV+KC_Den_VT})

# print(calc(120,120,500,250))
# print(calc(500,250,150,450))
# KC_Den_VT = calc(120,120,500,250)
# KC_Den_KV = calc(500,250,150,450)
# print(f"Total KC Yellow: {KC_Den_KV+KC_Den_VT}")
# sapxepduongdi.append({"khoang_cach": KC_Den_KV+KC_Den_VT})

# print(calc(120,120,600,400))
# print(calc(600,400,650,450))
# KC_Den_VT = calc(120,120,600,400)
# KC_Den_KV = calc(600,400,650,450)
# print(f"Total KC Green: {KC_Den_KV+KC_Den_VT}")
# sapxepduongdi.append({"khoang_cach": KC_Den_KV+KC_Den_VT})

for vt in vat_the:
    robot_pos_X = robot_pos[0]
    robot_pos_Y = robot_pos[1]
    # {"mau": "do", "x": 200, "y": 200},
    # vong lap dau tien
    # vt có giá trị: {"mau": "do", "x": 200, "y": 200}
    vt_X = vt["x"]
    vt_Y = vt["y"]
    KC_Den_VT = calc(robot_pos_X,robot_pos_Y,vt_X,vt_Y)
    kv_dich = tim_khu_vuc(vt["mau"])
    # gia trị mẫu của khu vực màu đỏ: {"mau": "do", "x": 150, "y": 150},
    kv_x = kv_dich["x"]
    kv_y = kv_dich["y"]
    KC_Den_KV = calc(kv_x,kv_y,vt_X,vt_Y)
    sapxepduongdi.append({"khoang_cach": KC_Den_KV+KC_Den_VT})

# users = [{'name': 'Bob', 'age': 30}, {'name': 'Alice', 'age': 25}]
sapxepduongdi.sort(key=lambda khoang_cach: khoang_cach["khoang_cach"])  # Sorts by 'age'
print(sapxepduongdi)