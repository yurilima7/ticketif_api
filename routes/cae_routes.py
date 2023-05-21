from fastapi import APIRouter, HTTPException, Depends, Query

from auth.auth import get_current_user
from models.permanent import Permanent
from repositories.permanent_day_repository import creat_permanent_day
from repositories.ticket_repository import patch_ticket, get_ticket, get_all_tickets_monthly

cae_router = APIRouter()


# Rota responsável por autorizar ou não autorizar a solicitação de ticket
@cae_router.patch("/ticket-authorization/{ticket_id}")
async def authorization(ticket_id: int, ticket_registered: dict, current_user: dict = Depends(get_current_user)):
    ticket_mod = await patch_ticket(ticket_id, ticket_registered)
    if ticket_mod is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket_registered_mod = await get_ticket(ticket_id)

    if ticket_registered_mod["is_permanent"] == 1 and ticket_registered_mod["status_id"] == 2:
        await creat_permanent_day(
            Permanent(student_id=ticket_registered_mod["student_id"], week_id=ticket_registered_mod["week_id"],
                      meal_id=ticket_registered_mod["meal_id"]))

    return ticket_registered_mod


# Rota que retorna todos os tickets pagos em um determinado mês
@cae_router.get("/tickets-monthly")
async def tickets_monthly(month: str = Query(..., regex=r"\d{4}-\d{2}"),
                          current_user: dict = Depends(get_current_user)):

    tickets = await get_all_tickets_monthly(month)
    if tickets is None:
        raise HTTPException(status_code=404, detail="Tickets not found")

    return tickets
