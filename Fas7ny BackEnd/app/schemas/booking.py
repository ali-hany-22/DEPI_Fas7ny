from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models.booking import BookingStatus


class BookingStatusUpdateRequest(BaseModel):
    status: BookingStatus


class BookingCreate(BaseModel):
    service_id: int
    guest_name: str
    guest_phone: str | None = None
    check_in_date: date | None = None
    check_out_date: date | None = None
    nights: int = 1


class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    booking_reference: str
    service_title_snapshot: str
    price_snapshot: float
    guest_name: str
    guest_phone: str | None
    check_in_date: date | None
    check_out_date: date | None
    nights: int
    status: BookingStatus
    created_at: datetime