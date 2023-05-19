from fastapi import APIRouter, Body, HTTPException

from auth.auth import create_account, authenticate, create_access_token, create_refresh_token

auth_router = APIRouter()


@auth_router.post("/register")
async def register(name: str = Body(...), email: str = Body(...), password: str = Body(...)):
    await create_account(name, email, password)
    return {"message": "Estudante criado com sucesso"}


@auth_router.post("/login")
async def login(email: str = Body(...), password: str = Body(...)):
    student = await authenticate(email, password)

    if not student:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = await create_access_token(student["email"])
    refresh_token = await create_refresh_token(student["email"])
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}
