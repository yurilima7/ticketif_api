from fastapi import APIRouter, HTTPException, Depends

from auth.auth import get_current_user
from models.ticket import Ticket
from repositories.permanent_day_repository import get_days
from repositories.ticket_repository import creat_ticket, get_ticket, delete_ticket, patch_ticket, get_all_tickets

ticket_router = APIRouter()


# Rota responsável por solicitar um Ticket
@ticket_router.post("/ticket")
async def request_ticket(ticket_info: Ticket, current_user: dict = Depends(get_current_user)):
    ticket_id = await creat_ticket(ticket_info)
    ticket_registered = await get_ticket(ticket_id)
    return ticket_registered


# Rota que retorna todos o histórico de tickets do estudante
@ticket_router.get("/ticket/{student_id}")
async def all_tickets(student_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["id"] == student_id:
        tickets = await get_all_tickets(student_id)

        if tickets is None:
            raise HTTPException(status_code=404, detail="Tickets not found")
        return tickets
    else:
        raise HTTPException(status_code=404, detail="Unauthorized")


# Rota responsável por confirmar presença ou cancelar o ticket do estudante
@ticket_router.patch("/ticket/{ticket_id}")
async def status_modification(ticket_id: int, ticket_registered: dict, current_user: dict = Depends(get_current_user)):
    ticket_mod = await patch_ticket(ticket_id, ticket_registered)
    if ticket_mod is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket_registered_mod = await get_ticket(ticket_id)

    return ticket_registered_mod


# Rota responsável por deletar um ticket
@ticket_router.delete("/ticket/{ticket_id}")
async def delete_ticket_existing(ticket_id: int, current_user: dict = Depends(get_current_user)):
    ticket_mod = await delete_ticket(ticket_id)
    if ticket_mod is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {"message": "Ticket deletado com sucesso"}


# Rota que retorna os dias de tickets permanentes do Estudante
@ticket_router.get("/days/{student_id}")
async def all_days(student_id: int, current_user: dict = Depends(get_current_user)):
    days = await get_days(student_id)
    if days is None:
        raise HTTPException(status_code=404, detail="Days not found")

    return days
