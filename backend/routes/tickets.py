from fastapi import APIRouter
from pydantic import BaseModel

from services.ticket_service import (
    get_all_tickets,
    find_ticket,
    create_ticket
)

router = APIRouter()


class TicketRequest(BaseModel):
    customer: str
    email: str
    issue: str
    description: str


@router.get("/tickets")
def all_tickets():
    return get_all_tickets()


@router.get("/tickets/{ticket_id}")
def ticket(ticket_id: str):

    data = find_ticket(ticket_id)

    if data:
        return data

    return {"message": "Ticket not found"}


@router.post("/tickets")
def new_ticket(data: TicketRequest):

    return create_ticket(
        data.customer,
        data.email,
        data.issue,
        data.description
    )