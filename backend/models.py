import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Integer, DateTime, Enum as SAEnum
from database import Base

import enum


class CategoryEnum(str, enum.Enum):
    BILLING = "Billing"
    REFUND = "Refund"
    ACCOUNT_ACCESS = "Account Access"
    CANCELLATION = "Cancellation"
    GENERAL_INQUIRY = "General Inquiry"


class Trace(Base):
    __tablename__ = "traces"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_message = Column(String, nullable=False)
    bot_response = Column(String, nullable=False)
    category = Column(SAEnum(CategoryEnum), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    response_time_ms = Column(Integer, nullable=False)
