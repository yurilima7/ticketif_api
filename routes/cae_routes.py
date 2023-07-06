from fastapi import APIRouter, HTTPException, Depends, Query

from models.permanent import Permanent
from models.ticket import Ticket
from repositories.permanent_day_repository import creat_permanent_day
from repositories.ticket_repository import patch_ticket, get_ticket, get_all_tickets_monthly, delete_ticket, \
    delete_permanent_tickets, period_report, daily_report, creat_ticket

cae_router = APIRouter()


# Rota responsável por autorizar ou não autorizar a solicitação de ticket
@cae_router.patch("/ticket-authorization/{ticket_id}")
async def authorization(ticket_id: int, ticket_registered: dict):
    ticket_mod = await patch_ticket(ticket_id, ticket_registered)
    if ticket_mod is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket_registered_mod = await get_ticket(ticket_id)

    # Caso seja permanente e o status seja confirmar presença adiciona o dia na tabela de permanentes
    if ticket_registered_mod["is_permanent"] == 1 and ticket_registered_mod["status_id"] == 2:
        await creat_permanent_day(
            Permanent(student_id=ticket_registered_mod["student_id"], week_id=ticket_registered_mod["week_id"],
                      meal_id=ticket_registered_mod["meal_id"],
                      justification_id=ticket_registered_mod["justification_id"]))

        # Deleta os permanentes que não são do dia de hoje
        if ticket_registered_mod["use_day_date"] == '':
            await delete_ticket(ticket_id)

    return ticket_registered_mod


# Rota que retorna todos os tickets pagos em um determinado mês
@cae_router.get("/tickets-monthly")
async def tickets_monthly(month: str = Query(..., regex=r"\d{4}-\d{2}"),
                          search_filter: str = Query(...)):

    tickets = await get_all_tickets_monthly(month, search_filter)
    if tickets is None:
        raise HTTPException(status_code=404, detail="Tickets not found")

    return tickets


# Rota que retorna todos os tickets de um período especifíco
@cae_router.get("/tickets-period")
async def period_tickets(month_initial: str = Query(..., regex=r"\d{4}-\d{2}-\d{2}"),
                         month_final: str = Query(..., regex=r"\d{4}-\d{2}-\d{2}")):

    tickets = await period_report(month_initial, month_final)

    if tickets is None:
        raise HTTPException(status_code=404, detail="Tickets not found")

    return tickets


# Rota que retorna todos os tickets de um dia específico
@cae_router.get("/tickets-daily")
async def day_tickets(daily: str = Query(..., regex=r"\d{4}-\d{2}-\d{2}")):

    tickets = await daily_report(daily)

    if tickets is None:
        raise HTTPException(status_code=404, detail="Tickets not found")

    return tickets


# Rota que deleta todos os tickets da tabela de permanent
@cae_router.delete("/tickets-delete")
async def tickets_delete():
    delete = await delete_permanent_tickets()

    if delete is None:
        raise HTTPException(status_code=404, detail="Tickets not delete")

    return {"message": "Tickets deletados com sucesso"}


# Rota responsável por solicitar um Ticket na CAE
@cae_router.post("/ticket-cae")
async def request_ticket_cae(ticket_info: Ticket):
    ticket_id = await creat_ticket(ticket_info)
    ticket_registered = await get_ticket(ticket_id)

    # Caso não ocorra problema de registro e seja um ticket permanente
    # Adiciona o dia na tabela de permanent
    if ticket_registered is not None and ticket_info.is_permanent == 1:
        await creat_permanent_day(
            Permanent(student_id=ticket_info.student_id, week_id=ticket_info.week_id,
                      meal_id=ticket_info.meal_id,
                      justification_id=ticket_info.justification_id))

        # Deleta os permanentes que não são do dia de hoje
        if ticket_info.use_day_date == '':
            await delete_ticket(ticket_id)

    return ticket_registered
