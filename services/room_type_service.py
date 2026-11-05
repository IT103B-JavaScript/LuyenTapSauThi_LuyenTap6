"""
Service xử lý nghiệp vụ loại phòng.
"""
from sqlalchemy.orm import Session

from models.room import Room
from models.room_type import RoomType
from utils.exceptions import AppException

DEFAULT_ROOM_TYPES = ["single", "double", "suite"]


def seed_default_room_types(db: Session) -> None:
    """Tạo sẵn các loại phòng mặc định nếu bảng đang trống (phục vụ test API)."""
    if db.query(RoomType).count() > 0:
        return
    for type_name in DEFAULT_ROOM_TYPES:
        db.add(RoomType(name=type_name))
    db.commit()


def delete_room_type(db: Session, type_id: int) -> RoomType:
    """Xóa loại phòng theo id, chỉ cho phép khi không còn phòng nào thuộc loại này."""
    type_obj = db.get(RoomType, type_id)
    if type_obj is None:
        raise AppException(404, "Not Found", f"Không tìm thấy loại phòng có id = {type_id}")

    total_rooms = db.query(Room).filter(Room.room_type_id == type_id).count()
    if total_rooms > 0:
        raise AppException(
            400, "Bad Request",
            f"Không thể xóa loại phòng '{type_obj.name}' vì còn {total_rooms} phòng thuộc loại này",
        )

    db.delete(type_obj)
    db.commit()
    return type_obj
