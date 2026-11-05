"""
Schemas Pydantic: validate dữ liệu đầu vào và định nghĩa cấu trúc dữ liệu đầu ra.
"""
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RoomTypeResponse(BaseModel):
    """Thông tin loại phòng trả về kèm trong phòng."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class RoomCreate(BaseModel):
    """Dữ liệu đầu vào khi thêm mới phòng."""
    room_code: str = Field(..., min_length=4, max_length=10, examples=["R105"])
    nightly_price: float = Field(..., gt=0, examples=[450000])
    room_type_id: int = Field(..., examples=[1])

    @field_validator("room_code")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        """Bỏ khoảng trắng hai đầu, chuyển in hoa và kiểm tra lại độ dài."""
        value = value.strip().upper()
        if len(value) < 4:
            raise ValueError("Mã phòng phải có ít nhất 4 ký tự")
        return value


class RoomResponse(BaseModel):
    """Thông tin phòng trả về (dùng làm response_model)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_code: str
    nightly_price: float
    room_type: RoomTypeResponse


class RoomListResponse(BaseModel):
    """Response chuẩn cho API lấy danh sách phòng."""
    statusCode: int
    error: Optional[str] = None
    message: str
    data: List[RoomResponse]


class RoomDetailResponse(BaseModel):
    """Response chuẩn cho API trả về một phòng."""
    statusCode: int
    error: Optional[str] = None
    message: str
    data: RoomResponse


class RoomTypeDeleteResponse(BaseModel):
    """Response chuẩn cho API xóa loại phòng."""
    statusCode: int
    error: Optional[str] = None
    message: str
    data: Optional[RoomTypeResponse] = None
