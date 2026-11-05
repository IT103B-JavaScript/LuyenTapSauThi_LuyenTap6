# ĐÁNH GIÁ CHẤT LƯỢNG KỸ NĂNG – PYTHON, FASTAPI VÀ DATABASE
## KIỂM TRA ĐÁNH GIÁ NĂNG LỰC CNTT – [Mã đề: 008]
**THỜI GIAN: 90 phút**

---

## Yêu cầu
Tạo project folder theo hướng dẫn sau:
- Tạo folder [Mã Lớp]\_[Họ Tên]\_[Mã Đề] chứa toàn bộ file mã nguồn. *Ví dụ: HN_KS25_CNTT1_NguyenVanA_8*
- Sau khi hoàn thành project, đẩy code lên GitHub và nộp link cho người phụ trách.
- Công nghệ & công cụ sử dụng: Python core + FastAPI + MySQL + SQLAlchemy ORM, Visual Studio Code.

## Thực hành

### 1. Bối cảnh
Hệ thống Quản lý Phòng khách sạn (hotel_management) cần xây dựng các chức năng xử lý dữ liệu phòng bằng Python Core, cấu hình dữ liệu đầu vào/đầu ra với Pydantic, kết nối cơ sở dữ liệu MySQL và viết các API quản lý phòng (rooms) và loại phòng (room_types).

Sinh viên cần xây dựng API quản lý phòng, cho phép thêm mới phòng, xem danh sách phòng kèm chi tiết loại phòng, và xóa loại phòng kèm xử lý ràng buộc đặc biệt.

### 2. Tài liệu

#### 2.1 Dữ liệu phòng (dùng cho Phần 1)
Cho trước danh sách dữ liệu thô chứa thông tin các phòng giả định sau:
```python
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
```

#### 2.2 Cơ sở dữ liệu
Database đặt tên là: **hotel_db**

**Bảng room_types:**
| Trường | Kiểu dữ liệu | Mô tả |
|---|---|---|
| **id** | int | Mã loại phòng, khóa chính, tự tăng |
| **name** | string | Tên loại phòng, tối đa 50 ký tự, độc nhất, không trống |

**Bảng rooms:**
| Trường | Kiểu dữ liệu | Mô tả |
|---|---|---|
| **id** | int | Mã định danh phòng, khóa chính, tự tăng |
| **room_code** | string | Mã phòng, tối đa 10 ký tự, độc nhất, không trống |
| **nightly_price** | float | Giá thuê theo đêm, không trống |
| **room_type_id** | int | Khóa ngoại liên kết tới bảng room_types |

#### 2.3 Bảng danh sách API
| STT | Chức năng | Method | Endpoint |
|---|---|---|---|
| 1 | Truy vấn danh sách phòng | GET | /rooms |
| 2 | Thêm phòng mới | POST | /rooms |
| 3 | Xóa loại phòng | DELETE | /room-types/{id} |

#### 2.4 Quy chuẩn cấu trúc Response chung
Tất cả các API bắt buộc phải trả về dữ liệu dưới dạng đồng nhất gồm 4 trường sau:
- **statusCode** (số nguyên): mã trạng thái HTTP (200, 201, 404, ...).
- **error** (chuỗi hoặc null): lỗi nếu có (ví dụ: "Not Found").
- **message** (chuỗi): thông báo trạng thái thực hiện hành động cho người dùng.
- **data** (object/mảng hoặc null): dữ liệu kết quả trả về từ database.

**Ví dụ mẫu Response API lấy danh sách phòng thành công:**
```json
{
  "statusCode": 200,
  "error": null,
  "message": "Lấy danh sách phòng thành công",
  "data": [
    {
      "id": 1,
      "room_code": "R101",
      "nightly_price": 450000.0,
      "room_type": {
        "id": 1,
        "name": "single"
      }
    }
  ]
}
```

### 3. Yêu cầu nghiệp vụ

#### Phần 1: Python Core & Tư duy thuật toán (35 điểm)
**Yêu cầu 1.1 (10 điểm) – Chuẩn hóa & validate dữ liệu:**
Viết hàm `clean_and_validate_rooms` thực hiện:
- Loại bỏ khoảng trắng thừa ở hai đầu của mã phòng `room_code` và chuyển toàn bộ chữ cái thành dạng in hoa (ví dụ: " r205 " → "R205").
- Kiểm tra tính hợp lệ của mã phòng sau khi chuẩn hóa: phải bắt đầu bằng chữ cái R, theo sau là các chữ số. Nếu không hợp lệ, loại bỏ phòng đó khỏi danh sách.

**Yêu cầu 1.2 (12 điểm) – Tìm kiếm tuyến tính (Linear Search):**
Viết hàm `search_rooms` để tìm kiếm các phòng thỏa mãn đồng thời:
- Giá thuê theo đêm (`nightly_price`) nhỏ hơn hoặc bằng giá trị truyền vào tham số.
- Trạng thái (`status`) trùng khớp với giá trị truyền vào tham số (nếu giá trị truyền vào là None thì chỉ lọc theo giá thuê theo đêm).

**Yêu cầu 1.3 (13 điểm) – Sắp xếp nổi bọt (Bubble Sort):**
Viết hàm `sort_rooms_by_nightly_price_desc` tự cài đặt thuật toán Bubble Sort để sắp xếp danh sách phòng theo thứ tự giá thuê theo đêm giảm dần.

#### Phần 2: Parameter & Pydantic Validation (10 điểm)
**Yêu cầu 2.1 (5 điểm) – Định nghĩa Schema & validate dữ liệu:**
Tạo Schema `RoomCreate` để validate dữ liệu đầu vào:
- `room_code`: bắt buộc, độ dài tối thiểu 4 ký tự, tối đa 10 ký tự.
- `nightly_price`: bắt buộc, giá trị phải lớn hơn 0.
- `room_type_id`: bắt buộc (ID liên kết với bảng loại phòng).

**Yêu cầu 2.2 (5 điểm) – Phản hồi chuẩn RESTful & Response Model:**
Tạo Schema `RoomResponse` dùng làm response_model khi trả về thông tin phòng.

#### Phần 3: Kết nối MySQL & SQLAlchemy ORM (20 điểm)
**Yêu cầu 3.1 (10 điểm) – Khai báo cấu hình CSDL:**
Viết file `database.py` kết nối tới cơ sở dữ liệu MySQL local có tên hotel_db.

**Yêu cầu 3.2 (10 điểm) – Thiết kế Model quan hệ 1-N:**
Khai báo 2 SQLAlchemy Models trong thư mục `models/` đại diện cho mối quan hệ 1-N:
- Bảng room_types: tạo các cột tương ứng, thiết lập mối quan hệ.
- Bảng rooms: tạo các cột tương ứng, thiết lập mối quan hệ.

#### Phần 4: Endpoints API & logic nghiệp vụ (35 điểm)
**Yêu cầu 4.1 (5 điểm) – Chia thư mục/file:** Chia thư mục/file theo cấu trúc phân tầng nêu ở mục 5. Yêu cầu kỹ thuật.

**Yêu cầu 4.2 (10 điểm) – API 1: POST /rooms**
- **Mô tả:** thêm mới một phòng.
- **Yêu cầu:** thêm dữ liệu phòng từ Request Body vào database; xử lý trường hợp `room_type_id` không tồn tại và `room_code` bị trùng.

**Yêu cầu 4.3 (10 điểm) – API 2: GET /rooms**
- **Mô tả:** truy vấn danh sách phòng.
- **Yêu cầu:** trả về danh sách phòng kèm theo thông tin chi tiết của loại phòng đó.

**Yêu cầu 4.4 (10 điểm) – API 3: DELETE /room-types/{id}**
- **Mô tả:** xóa loại phòng theo ID.
- **Yêu cầu:** chỉ cho phép xóa khi không có phòng nào thuộc loại phòng này.

### 4. Thang điểm chi tiết
| STT | Nghiệp vụ cần đạt được | Mô tả chi tiết nghiệp vụ | Điểm |
|---|---|---|---|
| 1 | Phần 1 – Python Core & Tư duy thuật toán | Yêu cầu 1.1 – Chuẩn hóa & validate dữ liệu: 10 • Yêu cầu 1.2 – Tìm kiếm tuyến tính: 12 • Yêu cầu 1.3 – Sắp xếp nổi bọt: 13 | 35 |
| 2 | Phần 2 – Parameter & Pydantic Validation | Yêu cầu 2.1 – Schema RoomCreate & validate dữ liệu: 5 • Yêu cầu 2.2 – Schema RoomResponse & response_model: 5 | 10 |
| 3 | Phần 3 – Kết nối MySQL & SQLAlchemy ORM | Yêu cầu 3.1 – Cấu hình kết nối CSDL (database.py): 10 • Yêu cầu 3.2 – Model quan hệ 1-N: 10 | 20 |
| 4 | Phần 4 – Endpoints API & logic nghiệp vụ | Yêu cầu 4.1 – Chia thư mục/file: 5 • Yêu cầu 4.2 – API POST /rooms: 10 • Yêu cầu 4.3 – API GET /rooms: 10 • Yêu cầu 4.4 – API DELETE /room-types/{id}: 10 | 35 |
| | **Tổng cộng** | | **100** |

### 5. Yêu cầu kỹ thuật
- Chạy được chương trình bằng lệnh `uvicorn main:app --reload`.
- Test được API trên Swagger UI.
- Kết nối được FastAPI với MySQL thông qua SQLAlchemy ORM.
- Source code được tách thành nhiều file theo cấu trúc phân tầng rõ ràng và hợp lý.

*Lưu ý: Chỉ tính điểm khi chức năng chương trình thực hiện đúng theo yêu cầu nghiệp vụ được giao.*

---

## Hướng dẫn chạy bài giải mẫu (thư mục `hotel_management/`)
```
hotel_management/
├── main.py                     # khởi tạo app, đăng ký router, xử lý lỗi
├── database.py                 # kết nối MySQL hotel_db
├── models/
│   ├── __init__.py
│   ├── room_type.py
│   └── room.py
├── schemas/
│   ├── __init__.py
│   └── room_schema.py
├── services/
│   ├── __init__.py
│   ├── room_service.py
│   └── room_type_service.py
├── routers/
│   ├── __init__.py
│   ├── room_router.py
│   └── room_type_router.py
├── utils/
│   ├── __init__.py
│   ├── python_core.py          # Phần 1
│   ├── exceptions.py
│   └── response.py
├── create_database.sql
└── requirements.txt
```
1. `pip install -r requirements.txt`
2. Chạy `create_database.sql` trong MySQL (tạo database `hotel_db`), sửa user/mật khẩu trong `database.py` nếu khác `root/123456`.
3. Phần 1: `python -m utils.python_core`
4. API: `uvicorn main:app --reload` → mở http://127.0.0.1:8000/docs. Khi khởi động, bảng `room_types` được tạo sẵn các loại: 1 = single, 2 = double, 3 = suite.
