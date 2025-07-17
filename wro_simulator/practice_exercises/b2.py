def process_line(sensors):
    """
    Xử lý dữ liệu 3 cảm biến line
    Input: list [left, center, right] với giá trị 0 hoặc 1
    Output: string hành động
    """
    left, center, right = sensors
    # print(left, right, center)
    if left == 0 and center == 0 and right == 0:
        return "Stop"
    if left == 0 and center == 1 and right == 0:
        return "Middle"
    if left == 1 and center == 0 and right == 0:
        return "Left"
    if left == 0 and center == 0 and right == 1:
        return "Right"
    if left == 1 and center == 1 and right == 0:
        return "Middle"
    if left == 0 and center == 1 and right == 1:
        return "Middle"
    if left == 1 and center == 1 and right == 1:
        return "Middle"
    if left == 1 and center == 0 and right == 1:
        return "Unknown"
# print(process_line([0,1,0]))
test_cases = [
    [0, 1, 0], [1, 0, 0], [0, 0, 1], [0, 0, 0],
    [1, 1, 0], [0, 1, 1], [1, 1, 1], [1, 0, 1]
]
print(f"📊 Cần test {len(test_cases)} trường hợp")
for sensors_value in test_cases:
    GtriMoiCuaSensorMoiVongLap = sensors_value
    print(process_line(GtriMoiCuaSensorMoiVongLap))