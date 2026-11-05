"""
Service xử lý nghiệp vụ phòng.
"""
from sqlalchemy.orm import Session, joinedload

from models.room import Room
from models.room_type import RoomType
from schemas.room_schema import RoomCreate
from utils.exceptions import AppException


def get_all_rooms(db: Session):
    """Lấy toàn bộ phòng kèm thông tin loại phòng."""
    return (
        db.query(Room)
        .options(joinedload(Room.room_type))
        .order_by(Room.id)
        .all()
    )


def create_room(db: Session, payload: RoomCreate) -> Room:
    """Thêm mới phòng: kiểm tra loại phòng tồn tại và mã phòng không bị trùng."""
    type_obj = db.get(RoomType, payload.room_type_id)
    if type_obj is None:
        raise AppException(
            404, "Not Found",
            f"Không tìm thấy loại phòng có id = {payload.room_type_id}",
        )

    duplicated = db.query(Room).filter(Room.room_code == payload.room_code).first()
    if duplicated is not None:
        raise AppException(
            409, "Conflict",
            f"Mã phòng {payload.room_code} đã tồn tại",
        )

    new_room = Room(**payload.model_dump())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room
