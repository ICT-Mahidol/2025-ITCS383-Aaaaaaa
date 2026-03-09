from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db_connection import Base

class Merchant(Base):
    __tablename__ = "merchants"

    merchant_id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    seller_information = Column(Text)
    product_description = Column(Text)
    approved_by = Column(String(36), ForeignKey("users.id"))
    approved_at = Column(DateTime)

    user = relationship("User", foreign_keys=[user_id])
    approver = relationship("User", foreign_keys=[approved_by])