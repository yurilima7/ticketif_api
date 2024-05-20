from passlib.context import CryptContext
from sqlalchemy import select

from database.database_ticket import admUser, db_ticket, classes
from models.adm_user import AdmUser

pwd_context = CryptContext(schemes=["bcrypt"])


# Função responsável pela criação do usuário administrativo
# RESTAURANTE E CAE
async def create_adm_user(user: AdmUser):
    hashed_password = pwd_context.hash(user.password)
    query = admUser.insert().values(username=user.username, password=hashed_password, login_type_id=user.login_type_id)

    await db_ticket.execute(query)


# Função que retorna os dados do usuário cadastrado
async def get_auth_user(username: str):
    query = select([admUser]).where(admUser.c.username == username)
    return await db_ticket.fetch_one(query)


async def insert_class(description: str, course: str):
    query = classes.insert().values(description=description, course=course)
    return await db_ticket.execute(query)
