"""
Phần 1: Python Core & Tư duy thuật toán
- Yêu cầu 1.1: clean_and_validate_rooms
- Yêu cầu 1.2: search_rooms (Linear Search)
- Yêu cầu 1.3: sort_rooms_by_nightly_price_desc (Bubble Sort)
Chạy thử: python -m utils.python_core
"""

raw_rooms = [
    {"room_code": "R101", "type": "single",
     "nightly_price": 450000, "status": "available"},
    {"room_code": " r205 ", "type": "double",
     "nightly_price": 750000, "status": "available"},
    {"room_code": "R301", "type": "suite",
     "nightly_price": 2500000, "status": "occupied"},
    {"room_code": "RX12", "type": "double",
     "nightly_price": 700000, "status": "maintenance"},
    {"room_code": "R102", "type": "single",
     "nightly_price": 500000, "status": "available"},
    {"room_code": "R302", "type": "suite",
     "nightly_price": 2200000, "status": "available"}
]


def is_valid_room_code(code):
    """Mã hợp lệ: bắt đầu bằng chữ cái R, theo sau là ít nhất một chữ số (chỉ chữ số)."""
    return len(code) >= 2 and code[0] == "R" and code[1:].isdigit()


def clean_and_validate_rooms(raw_list):
    """Yêu cầu 1.1: chuẩn hóa room_code (strip + upper) và loại bỏ phòng có mã không hợp lệ."""
    cleaned_list = []
    for item in raw_list:
        code = str(item.get("room_code", "")).strip().upper()
        if is_valid_room_code(code):
            cleaned_item = dict(item)  # tạo bản sao, không sửa dữ liệu gốc
            cleaned_item["room_code"] = code
            cleaned_list.append(cleaned_item)
        else:
            print(f"[Loại bỏ] mã phòng không hợp lệ: {item.get('room_code')!r}")
    return cleaned_list


def search_rooms(item_list, max_nightly_price, status=None):
    """Yêu cầu 1.2: tìm tuyến tính phòng có nightly_price <= max_nightly_price và đúng status (None = bỏ qua status)."""
    result = []
    for item in item_list:
        if item["nightly_price"] > max_nightly_price:
            continue
        if status is not None and item["status"] != status:
            continue
        result.append(item)
    return result


def sort_rooms_by_nightly_price_desc(item_list):
    """Yêu cầu 1.3: Bubble Sort giảm dần theo nightly_price, trả về danh sách mới."""
    sorted_list = list(item_list)
    n = len(sorted_list)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if sorted_list[j]["nightly_price"] < sorted_list[j + 1]["nightly_price"]:
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
                swapped = True
        if not swapped:
            break
    return sorted_list


def print_rooms(title, item_list):
    """In danh sách phòng dạng bảng để kiểm tra kết quả."""
    print(f"\n===== {title} ({len(item_list)}) =====")
    for item in item_list:
        print(
            f"{item['room_code']:<8} | {item['type']:<14} | "
            f"{item['nightly_price']:>12,} | {item['status']}"
        )


if __name__ == "__main__":
    valid_rooms = clean_and_validate_rooms(raw_rooms)
    print_rooms("1.1 Sau khi chuẩn hóa & validate", valid_rooms)

    print_rooms(
        "1.2 Tìm phòng có nightly_price <= 800000 và status = 'available'",
        search_rooms(valid_rooms, 800000, "available"),
    )
    print_rooms(
        "1.2 Tìm phòng có nightly_price <= 800000 (status = None)",
        search_rooms(valid_rooms, 800000),
    )

    print_rooms("1.3 Sắp xếp nightly_price giảm dần (Bubble Sort)", sort_rooms_by_nightly_price_desc(valid_rooms))
