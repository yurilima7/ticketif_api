from fastapi import APIRouter, HTTPException, Depends

from repositories.student_repository import get_auth_student

student_router = APIRouter()


# Rota responsável por retornar os dados do estudante
@student_router.get("/me/{matricula}")
async def get_current_user(matricula: str):

    student = await get_auth_student(matricula)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student

