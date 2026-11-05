"""
Router API phòng: GET /rooms, POST /rooms
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.room_schema import RoomCreate, RoomDetailResponse, RoomListResponse
from services import room_service

router = APIRouter(prefix="/rooms", tags=["Phòng"])


@router.get("", response_model=RoomListResponse, status_code=status.HTTP_200_OK)
def get_rooms(db: Session = Depends(get_db)):
    """API 2: Truy vấn danh sách phòng kèm chi tiết loại phòng."""
    items = room_service.get_all_rooms(db)
    return {
        "statusCode": 200,
        "error": None,
        "message": "Lấy danh sách phòng thành công",
        "data": items,
    }


@router.post("", response_model=RoomDetailResponse, status_code=status.HTTP_201_CREATED)
def create_room(payload: RoomCreate, db: Session = Depends(get_db)):
    """API 1: Thêm mới một phòng."""
    new_item = room_service.create_room(db, payload)
    return {
        "statusCode": 201,
        "error": None,
        "message": "Thêm mới phòng thành công",
        "data": new_item,
    }
