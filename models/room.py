"""
Model bảng rooms (phòng) - phía "N" của quan hệ 1-N.
"""
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_code = Column(String(10), unique=True, nullable=False)
    nightly_price = Column(Float, nullable=False)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)

    # Mỗi phòng thuộc về một loại phòng
    room_type = relationship("RoomType", back_populates="rooms")
