from datetime import datetime, time
from fastapi import APIRouter, HTTPException, status

from models.permanent import PermanentAuthorization
from models.ticket import Ticket
from models.ticket_request import TicketRequest
from repositories.permanent_day_repository import checking_existing_request, get_days, creat_permanent_day, student_permanent
from repositories.ticket_repository import creat_ticket, get_ticket, delete_ticket, patch_ticket, get_all_tickets, \
    checks_permanent_authorization, check_use_ticket

ticket_router = APIRouter()


# Rota responsável por solicitar um Ticket
@ticket_router.post("/ticket")
async def request_ticket(ticket_info: TicketRequest):
   
    print(ticket_info)

    if ticket_info.is_cae == 0:
        ticket = Ticket(student_id=ticket_info.student_id, week_id=ticket_info.week_id,meal_id=ticket_info.meal_id,status_id=ticket_info.status_id,justification_id=ticket_info.justification_id,solicitation_day=ticket_info.solicitation_day,use_day=ticket_info.use_day,use_day_date=ticket_info.use_day_date,payment_day=ticket_info.payment_day,text=ticket_info.text,is_permanent=ticket_info.is_permanent,
        )

        ticket_id = await creat_ticket(ticket=ticket)
        ticket_registered = await get_ticket(ticket_id)

        if ticket_registered == None:
            raise HTTPException(status_code=404, detail="Erro ao solicitar ticket")
        else: 
            return ticket_registered
        
    else:
        ticket = Ticket(student_id=ticket_info.student_id, week_id=ticket_info.week_id,meal_id=ticket_info.meal_id,status_id=ticket_info.status_id,justification_id=ticket_info.justification_id,solicitation_day=ticket_info.solicitation_day,use_day=ticket_info.use_day,use_day_date=ticket_info.use_day_date,payment_day=ticket_info.payment_day,text=ticket_info.text,is_permanent=ticket_info.is_permanent,
            )

        ticket_id = await creat_ticket(ticket=ticket)
        ticket_registered = await get_ticket(ticket_id) 

        if ticket_registered == None:
            raise HTTPException(status_code=404, detail="Erro ao solicitar ticket")
        else: 
            return ticket_registered


# Rota responsável pela criação das autorizações permanentes
@ticket_router.post("/permanent")
async def create_permanents_authorizations(days: PermanentAuthorization):
    existing_permanent = 0
    created = 0

    for day in days.permanent_days:
        check_result = await checking_existing_request(meal_id=day.meal_id, student_id=day.student_id, week_id=day.week_id)
        print("check result", check_result)
        if len(check_result) == 0:
            await creat_permanent_day(day)

            if day.use_day_date != '':
                ticket_id = await creat_ticket(
                    Ticket(student_id=day.student_id, week_id=day.week_id, meal_id=day.meal_id,
                        justification_id=day.justification_id, status_id=day.status_id, solicitation_day=day.use_day_date,
                        use_day=day.use_day, text=day.text, is_permanent=1, use_day_date=day.use_day_date,
                        payment_day=""))
                
            created += 1
        else:
            existing_permanent += 1

    if created == len(days.permanent_days):
        return {"status": status.HTTP_201_CREATED, "message": "Solicitação realizada com sucesso!"}
    elif created == 1 and existing_permanent > 0:
        return {"status": status.HTTP_201_CREATED, "message": f"{created} solicitação realizada com sucesso!"}
    elif created > 1 and existing_permanent > 0:
        return {"status": status.HTTP_201_CREATED, "message": f"{created} solicitações realizadas com sucesso!"}
    elif created == 0 and existing_permanent > 0:
        raise HTTPException(status_code=404, detail="Falha ao solicitar permanentes por já existirem existentes")
    else:
        raise HTTPException(status_code=404, detail="Falha ao solicitar permanentes")


# Rota que retorna o histórico de tickets do estudante
@ticket_router.get("/ticket/{student_id}")
async def all_tickets(student_id: int):
    await checks_permanent_authorization(student_id)
    tickets = await get_all_tickets(student_id)

    if tickets is None:
        raise HTTPException(status_code=404, detail="Tickets not found")
    return tickets


# Rota responsável por cancelar o ticket do estudante
@ticket_router.patch("/ticket/{ticket_id}")
async def status_modification(ticket_id: int, ticket_registered: dict):
    ticket_mod = await patch_ticket(ticket_id, ticket_registered)
    if ticket_mod is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket_registered_mod = await get_ticket(ticket_id)

    return ticket_registered_mod


# Rota responsável por confirmar presença ou cancelar o ticket do estudante
@ticket_router.patch("/confirm-ticket/{ticket_id}")
async def confirm_ticket(ticket_id: int, ticket_registered: dict):
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


# Rota responsável por retornar os tickets permanentes
@ticket_router.get("/permanent/{student_id}")
async def all_student_tickets_permanents(student_id: int):
    permanents = await student_permanent(student_id=student_id)
    if permanents is None:
        raise HTTPException(status_code=404, detail="Permanentes não encontrados")

    return permanents


# Rota que retorna os dias de tickets permanentes do Estudante
@ticket_router.get("/days/{student_id}")
async def all_days(student_id: int):
    days = await get_days(student_id)
    if days is None:
        raise HTTPException(status_code=404, detail="Days not found")

    return days
