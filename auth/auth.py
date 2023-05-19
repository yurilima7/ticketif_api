from datetime import datetime, timedelta

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError, decode, encode
from passlib.context import CryptContext
from models.student import Student
from fastapi import Depends, HTTPException

from repositories.student_repository import get_auth_student, create_student

SECRET_KEY = "Wd9z7RwXJ5BkQ2fL6e8pY4gN1Cv0KmTa"
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"])
security = HTTPBearer()


async def create_account(name: str, matricula: str, password: str, type_student: str):
    user = await get_auth_student(matricula)
    if user:
        raise HTTPException(status_code=400, detail="Estudante já existe")

    await create_student(Student(
        name=name,
        matricula=matricula,
        password=password,
        type=type_student,
    ))


async def authenticate(matricula: str, password: str):
    student = await get_auth_student(matricula)
    if student and pwd_context.verify(password, student["password"]):
        return student

    return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        matricula = payload.get("sub")

        if matricula is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        student = await get_auth_student(matricula)

        if student is None:
            raise HTTPException(status_code=401, detail="Estudante não encontrado")

        return student
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


async def create_access_token(matricula: str):
    access_token_expires = timedelta(minutes=60)
    return encode(
        {
            "exp": datetime.utcnow() + access_token_expires,
            "sub": matricula,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


async def create_refresh_token(matricula: str):
    refresh_token_expires = timedelta(days=7)
    return encode(
        {
            "exp": datetime.utcnow() + refresh_token_expires,
            "sub": matricula,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
