from sqlalchemy import Column, String, DateTime, Decimal, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database.db_connection import Base

class PaymentMethod(enum.Enum):
    CREDIT_CARD = "CREDIT_CARD"
    TRUEMONEY = "TRUEMONEY"
    BANK_TRANSFER = "BANK_TRANSFER"

class PaymentStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(String(36), primary_key=True)
    reservation_id = Column(String(36), ForeignKey("reservations.reservation_id"), nullable=False)
    amount = Column(Decimal(10, 2), nullable=False)
    method = Column(Enum(PaymentMethod), nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    slip_url = Column(String(255))
    created_at = Column(DateTime, default=func.now())

    reservation = relationship("Reservation")