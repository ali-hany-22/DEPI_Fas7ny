"""
تذاكر الدعم الفني - صفحة Support بيقدر المزود يفتح تذكرة ويشوف
حالتها والرد عليها.
"""

import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum, ForeignKey, Text

from app.db.session import Base


class TicketStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("provider_profiles.id"), nullable=False)

    subject = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(SAEnum(TicketStatus), default=TicketStatus.open)

    admin_reply = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
