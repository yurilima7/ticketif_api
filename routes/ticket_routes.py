from fastapi import APIRouter, HTTPException

from models.permanent import PermanentAuthorization
from models.ticket import Ticket
from repositories.permanent_day_repository import get_days, creat_permanent_day
from repositories.ticket_repository import creat_ticket, get_ticket, delete_ticket, patch_ticket, get_all_tickets, \
    checks_permanent_authorization

ticket_router = APIRouter()


# Rota responsável por solicitar um Ticket
@ticket_router.post("/ticket")
async def request_ticket(ticket_info: Ticket):
    ticket_id = await creat_ticket(ticket_info)
    ticket_registered = await get_ticket(ticket_id)

    return ticket_registered


# Rota responsável pela criação das autorizações permanentes
@ticket_router.post("/permanent")
async def create_permanents_authorizations(days: PermanentAuthorization):
    for day in days.permanent_days:
        await creat_permanent_day(day)

        if day.use_day_date != '':
            ticket_id = await creat_ticket(
                Ticket(student_id=day.student_id, week_id=day.week_id, meal_id=day.meal_id,
                       justification_id=day.justification_id, status_id=2, solicitation_day=day.use_day_date,
                       use_day=day.use_day, text=day.text, is_permanent=1, use_day_date=day.use_day_date,
                       payment_day=""))


# Rota que retorna o histórico de tickets do estudante
@ticket_router.get("/ticket/{student_id}")
async def all_tickets(student_id: int):
    await checks_permanent_authorization(student_id)
    tickets = await get_all_tickets(student_id)

    if tickets is None:
        raise HTTPException(status_code=404, detail="Tickets not found")
    return tickets


# Rota responsável por confirmar presença ou cancelar o ticket do estudante
@ticket_router.patch("/ticket/{ticket_id}")
async def status_modification(ticket_id: int, ticket_registered: dict):
    ticket_mod = await patch_ticket(ticket_id, ticket_registered)
    if ticket_mod is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket_registered_mod = await get_ticket(ticket_id)

    return ticket_registered_mod


# Rota responsável por deletar um ticket
@ticket_router.delete("/ticket/{ticket_id}")
async def delete_ticket_existing(ticket_id: int):
    ticket_mod = await delete_ticket(ticket_id)
    if ticket_mod is None:
        raise HTTPException(status_code=404, detail="Ticket not delete")

    return {"message": "Ticket deletado com sucesso"}


# Rota que retorna os dias de tickets permanentes do Estudante
@ticket_router.get("/days/{student_id}")
async def all_days(student_id: int):
    days = await get_days(student_id)
    if days is None:
        raise HTTPException(status_code=404, detail="Days not found")

    return days
