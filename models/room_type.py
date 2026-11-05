"""
Model bảng room_types (loại phòng) - phía "1" của quan hệ 1-N.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class RoomType(Base):
    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    # Một loại phòng có nhiều phòng
    rooms = relationship("Room", back_populates="room_type")
