"""
Router API loại phòng: DELETE /room-types/{id}
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.room_schema import RoomTypeDeleteResponse
from services import room_type_service

router = APIRouter(prefix="/room-types", tags=["Loại phòng"])


@router.delete("/{id}", response_model=RoomTypeDeleteResponse, status_code=status.HTTP_200_OK)
def delete_room_type(id: int, db: Session = Depends(get_db)):
    """API 3: Xóa loại phòng theo ID (chỉ khi không còn phòng thuộc loại này)."""
    deleted = room_type_service.delete_room_type(db, id)
    return {
        "statusCode": 200,
        "error": None,
        "message": f"Xóa loại phòng '{deleted.name}' thành công",
        "data": deleted,
    }
