from fastapi import APIRouter, HTTPException, Depends

from auth.auth import get_current_user
from models.permanent import Permanent
from models.ticket import Ticket
from repositories.permanent_day_repository import creat_permanent_day, get_days
from repositories.ticket_repository import creat_ticket, get_ticket, delete_ticket, patch_ticket, get_all_tickets

ticket_router = APIRouter()


@ticket_router.post("/ticket")
async def request_ticket(ticket_info: Ticket, current_user: dict = Depends(get_current_user)):
    ticket_id = await creat_ticket(ticket_info)
    ticket_registered = await get_ticket(ticket_id)
    return ticket_registered


@ticket_router.get("/ticket/{student_id}")
async def all_tickets(student_id: int, current_user: dict = Depends(get_current_user)):
    tickets = await get_all_tickets(student_id)
    if tickets is None:
        raise HTTPException(status_code=404, detail="Tickets not found")
    return tickets


@ticket_router.patch("/ticket/{ticket_id}")
async def authorization_permanent(ticket_id: int, ticket_registered: dict,
                                  current_user: dict = Depends(get_current_user)):
    ticket_mod = await patch_ticket(ticket_id, ticket_registered)
    if ticket_mod is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket_registered_mod = await get_ticket(ticket_id)

    if ticket_registered_mod["is_permanent"] == 1 and ticket_registered_mod["status_id"] == 2:
        await creat_permanent_day(
            Permanent(student_id=ticket_registered_mod["student_id"], week_id=ticket_registered_mod["week_id"],
                      meal_id=ticket_registered_mod["meal_id"]))

    return ticket_registered_mod


@ticket_router.delete("/ticket/{ticket_id}")
async def delete_ticket_existing(ticket_id: int, current_user: dict = Depends(get_current_user)):
    ticket_mod = await delete_ticket(ticket_id)
    if ticket_mod is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {"message": "Ticket deletado com sucesso"}


@ticket_router.get("/days/{student_id}")
async def all_days(student_id: int, current_user: dict = Depends(get_current_user)):
    days = await get_days(student_id)
    if days is None:
        raise HTTPException(status_code=404, detail="Days not found")

    return days
