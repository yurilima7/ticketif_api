from fastapi import APIRouter, HTTPException, Depends

from repositories.student_repository import get_auth_student, get_students

student_router = APIRouter()


# Rota responsável por retornar os dados do estudante
@student_router.get("/me/{matricula}")
async def get_current_user(matricula: str):

    student = await get_auth_student(matricula)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


# Rota responsável por retornar todos os estudantes
@student_router.get("/students")
async def get_all_students():

    students = await get_students()

    if students is None:
        raise HTTPException(status_code=404, detail="Students not found")

    return students
