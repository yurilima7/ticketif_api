from fastapi import APIRouter, HTTPException, Depends

from auth.auth import get_current_user

student_router = APIRouter()


# Rota responsável por retornar os dados do estudante
@student_router.get("/me")
async def get_current_user(current_user: dict = Depends(get_current_user)):

    if current_user is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return current_user
