from fastapi import APIRouter, HTTPException, Depends

from auth.auth import get_current_user
from repositories.list_tables_repository import get_meals_and_justifications
from repositories.ticket_repository import patch_ticket, get_ticket

list_tables_router = APIRouter()


# Rota as tabelas meal e justification
@list_tables_router.get("/tables")
async def tables():
    tables_meal_and_justification = await get_meals_and_justifications()
    if tables_meal_and_justification is None:
        raise HTTPException(status_code=404, detail="Tables not found")

    return tables_meal_and_justification
