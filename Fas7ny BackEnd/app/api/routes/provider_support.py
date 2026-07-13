"""صفحة Support - فتح تذاكر ومتابعتها."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_provider
from app.models.provider import ProviderProfile
from app.models.support_ticket import SupportTicket
from app.schemas.support import TicketCreateRequest, TicketOut

router = APIRouter(prefix="/provider/support", tags=["Provider Support"])


@router.get("/tickets", response_model=list[TicketOut])
def list_tickets(
    provider: ProviderProfile = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    return (
        db.query(SupportTicket)
        .filter(SupportTicket.provider_id == provider.id)
        .order_by(SupportTicket.created_at.desc())
        .all()
    )


@router.post("/tickets", response_model=TicketOut, status_code=201)
def create_ticket(
    payload: TicketCreateRequest,
    provider: ProviderProfile = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    ticket = SupportTicket(provider_id=provider.id, **payload.model_dump())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket(
    ticket_id: int,
    provider: ProviderProfile = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    ticket = (
        db.query(SupportTicket)
        .filter(SupportTicket.id == ticket_id, SupportTicket.provider_id == provider.id)
        .first()
    )
    if not ticket:
        raise HTTPException(status_code=404, detail="التذكرة غير موجودة")
    return ticket
