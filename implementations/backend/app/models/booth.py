from sqlalchemy import Column, String, Decimal, Integer, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from app.database.db_connection import Base

class BoothType(enum.Enum):
    INDOOR = "INDOOR"
    OUTDOOR = "OUTDOOR"

class BoothClassification(enum.Enum):
    FIXED = "FIXED"
    TEMPORARY = "TEMPORARY"

class DurationType(enum.Enum):
    SHORT_TERM = "SHORT_TERM"
    LONG_TERM = "LONG_TERM"

class BoothStatus(enum.Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    OCCUPIED = "OCCUPIED"

class Booth(Base):
    __tablename__ = "booths"

    booth_id = Column(String(36), primary_key=True)
    event_id = Column(String(36), ForeignKey("events.event_id"), nullable=False)
    booth_number = Column(String(20), nullable=False)
    size = Column(String(50))
    price = Column(Decimal(10, 2), nullable=False)
    location = Column(String(100))
    type = Column(Enum(BoothType), nullable=False)
    classification = Column(Enum(BoothClassification), nullable=False)
    duration_type = Column(Enum(DurationType), nullable=False)
    electricity = Column(Boolean, default=False)
    water_supply = Column(Boolean, default=False)
    outlets = Column(Integer, default=0)
    status = Column(Enum(BoothStatus), default=BoothStatus.AVAILABLE)

    event = relationship("Event")