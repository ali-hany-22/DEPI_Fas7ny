"""Schemas لإدارة الخدمات (My Services) - إنشاء وتعديل."""

from pydantic import BaseModel

from app.models.service import ServiceStatus


class ServiceCreateRequest(BaseModel):
    title: str
    description: str | None = None
    price: float
    image_url: str | None = None
    requires_confirmation: bool = False


class ServiceUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    image_url: str | None = None
    requires_confirmation: bool | None = None
    status: ServiceStatus | None = None


class ServiceDetailOut(BaseModel):
    id: int
    title: str
    description: str | None
    price: float
    image_url: str | None
    status: ServiceStatus
    requires_confirmation: bool
    bookings_this_month: int

    class Config:
        from_attributes = True
