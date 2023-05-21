from fastapi import APIRouter, Body, HTTPException

from auth.auth import create_account, authenticate, create_access_token, create_refresh_token

auth_router = APIRouter()


# Rota responsável pelo registro do aula
@auth_router.post("/register")
async def register(name: str = Body(...), matricula: str = Body(...), password: str = Body(...),
                   type_student: str = Body(...)):
    await create_account(name, matricula, password, type_student)
    return {"message": "Estudante criado com sucesso"}


# Rota responsável por efetuar o login
@auth_router.post("/login")
async def login(matricula: str = Body(...), password: str = Body(...)):
    student = await authenticate(matricula, password)

    if not student:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = await create_access_token(student["matricula"])
    refresh_token = await create_refresh_token(student["matricula"])
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}
