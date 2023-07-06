from passlib.context import CryptContext
from models.adm_user import AdmUser
from fastapi import HTTPException
from repositories.adm_user_repositoty import get_auth_user, create_adm_user

SECRET_KEY = "Wd9z7RwXJ5BkQ2fL6e8pY4gN1Cv0KmTa"
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"])


async def create_account(username: str, login_type_id: int, password: str):
    user = await get_auth_user(username)
    if user:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    await create_adm_user(AdmUser(
        username=username,
        login_type_id=login_type_id,
        password=password
    ))


async def authenticate(username: str, password: str):
    user = await get_auth_user(username)
    if user and pwd_context.verify(password, user["password"]):
        return user

    return None
