from datetime import datetime

from pydantic import BaseModel

from app.models.support_ticket import TicketStatus


class TicketCreateRequest(BaseModel):
    subject: str
    message: str


class TicketOut(BaseModel):
    id: int
    subject: str
    message: str
    status: TicketStatus
    admin_reply: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
