from typing import List
from fastapi import APIRouter, HTTPException, Query

from models.student_authorization import StudentPermanentAuthorization
from repositories.permanent_day_repository import get_not_authorized, patch_authorized_permanent
from repositories.ticket_repository import patch_ticket, get_ticket, get_all_tickets_monthly, \
    delete_permanent_tickets, period_report, daily_report
from repositories.adm_user_repositoty import insert_class

cae_router = APIRouter()


# Rota responsável por autorizar ou não autorizar a solicitação de ticket
@cae_router.patch("/ticket-authorization/{ticket_id}")
async def authorization(ticket_id: int, ticket_registered: dict):
    ticket_mod = await patch_ticket(ticket_id, ticket_registered)
    if ticket_mod is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket_registered_mod = await get_ticket(ticket_id)

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


# Rota que retorna todas as autorizações permanentes não aprovadas
@cae_router.get("/not-authorized")
async def permanents_not_authorized():
    not_authorized = await get_not_authorized()

    if not_authorized is None:
        raise HTTPException(status_code=404, detail="Not Authorized not found")

    return not_authorized


# Rota de aprovamento ou desaprovação de permanentes
@cae_router.patch("/not-authorized/{authorization_status}")
async def update_not_authorized(authorization_status: int, listPermanents: StudentPermanentAuthorization):
    for permanentTicket in listPermanents.authorizations:
        await patch_authorized_permanent(permanentTicket.idStudent, {'authorized': authorization_status})


# Rota para inserir novas turmas
@cae_router.post("/new-classes")
async def add_new_classes(classes: List[dict]):
    print(classes)
    results = []
    for classe in classes:
        result = await insert_class(description=classe["description"], course=classe["course"])
        results.append(result)

    if len(results) == len(classes):
        return {"status_code": 200, "message": "Turmas inseridas com sucesso!"}
