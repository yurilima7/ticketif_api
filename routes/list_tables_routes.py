from fastapi import APIRouter, HTTPException
from repositories.list_tables_repository import get_meals_and_justifications, get_status

list_tables_router = APIRouter()


# Rota as tabelas meal e justification
@list_tables_router.get("/tables")
async def tables():
    tables_meal_and_justification = await get_meals_and_justifications()
    if tables_meal_and_justification is None:
        raise HTTPException(status_code=404, detail="Tables not found")

    return tables_meal_and_justification


# Rota da tabela status
@list_tables_router.get("/status")
async def status():
    status = await get_status()
    if status is None:
        raise HTTPException(status_code=404, detail="Status table not found")

    return status
