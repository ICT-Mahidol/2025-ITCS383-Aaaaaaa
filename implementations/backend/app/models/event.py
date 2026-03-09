from sqlalchemy import Column, String, DateTime, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.db_connection import Base

class Event(Base):
    __tablename__ = "events"

    event_id = Column(String(36), primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    location = Column(String(200))
    start_date = Column(Date)
    end_date = Column(Date)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())

    creator = relationship("User")