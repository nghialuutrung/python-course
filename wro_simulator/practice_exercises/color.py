colors = {
  # key: value
  "red": (255, 0, 0),
  "green": (0, 255, 0),
  "yellow": (255, 255, 0),
  "blue": (0, 0, 255),
  "pink": (255, 128, 1),
  "black": (0, 0, 0),
  "white": (255, 255, 255),
}


def detect_colorname(mau):
    for color_name, color_value in colors.items():
        # print(f"{color_name}: {color_value}")
        if mau == color_value:
            return color_name
    return "Unknown"


test_cases = [
        (255, 0, 0),      # Đỏ
        (0, 255, 0),      # Xanh lá
        (0, 0, 255),      # Xanh dương
        (255, 255, 0),    # Vàng
        (128, 128, 128),  # Xám - không có trong dictionary
        (255, 255, 255),  # Trắng - không có
        (0, 0, 0)         # Đen - không có
    ]
for color in test_cases:
    # print(f"Test color: {color}")
    print(detect_colorname(color))