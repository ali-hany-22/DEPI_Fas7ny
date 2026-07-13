"""
لازم نستورد كل الـ models هنا، عشان لما نعمل Base.metadata.create_all()
في startup الـ app، SQLAlchemy يبقى عارف بكل الجداول. من غير الاستيراد
ده، أي جدول متسجلش في الـ Base.metadata مش هيتعمله CREATE TABLE.
"""

from app.models.user import User, UserRole
from app.models.provider import ProviderProfile, BusinessType, ProviderTier
from app.models.service import Service, ServiceStatus
from app.models.booking import Booking, BookingStatus
from app.models.review import Review
from app.models.page_view import PageView
from app.models.support_ticket import SupportTicket, TicketStatus

__all__ = [
    "User", "UserRole",
    "ProviderProfile", "BusinessType", "ProviderTier",
    "Service", "ServiceStatus",
    "Booking", "BookingStatus",
    "Review",
    "PageView",
    "SupportTicket", "TicketStatus",
]
