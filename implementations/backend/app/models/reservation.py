from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database.db_connection import Base

class ReservationType(enum.Enum):
    SHORT_TERM = "SHORT_TERM"
    LONG_TERM = "LONG_TERM"

class ReservationStatus(enum.Enum):
    PENDING_PAYMENT = "PENDING_PAYMENT"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

class Reservation(Base):
    __tablename__ = "reservations"

    reservation_id = Column(String(36), primary_key=True)
    booth_id = Column(String(36), ForeignKey("booths.booth_id"), nullable=False)
    merchant_id = Column(String(36), ForeignKey("merchants.merchant_id"), nullable=False)
    reservation_type = Column(Enum(ReservationType), nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING_PAYMENT)
    created_at = Column(DateTime, default=func.now())

    booth = relationship("Booth")
    merchant = relationship("Merchant")