"""Gom các model để SQLAlchemy nhận diện đầy đủ quan hệ khi tạo bảng."""
from models.room_type import RoomType
from models.room import Room

__all__ = ["RoomType", "Room"]
