from fastapi import APIRouter, HTTPException
from repositories.ticket_repository import patch_ticket, get_ticket

restaurant_router = APIRouter()


# Rota responsável por registrar as alterarações de status para Utilizado
@restaurant_router.patch("/ticket-status/{ticket_id}")
async def ticket_status_modification(ticket_id: int, ticket_registered: dict):
    ticket_mod = await patch_ticket(ticket_id, ticket_registered)
    if ticket_mod is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket_registered_mod = await get_ticket(ticket_id)

    return ticket_registered_mod
