from sqlalchemy import select
from passlib.context import CryptContext
from database.database_ticket import students, classes, db_ticket
from models.student import Student
import re

pwd_context = CryptContext(schemes=["bcrypt"])


# Função que retorna os dados do estudante
async def get_auth_student(matricula: str):
    query = select([students]).where(students.c.matricula == matricula)
    return await db_ticket.fetch_one(query)


# Função que retorna todos estudantes
async def get_students():
    query = select([students])
    return await db_ticket.fetch_all(query)


# Função que retorna o tipo do estudante
# Ensino Medio ou Ensino Superior
async def get_type_student(matricula: str):
    query = select([classes.c.description])
    results = await db_ticket.fetch_all(query)
    values = [row[0] for row in results]
    regular_exp = '|'.join(values)
    padrao = re.compile(regular_exp)
    if bool(padrao.search(matricula)):
        return 'Medio'
    else:
        return 'Superior'


# Função responsável por criar um estudante no banco
async def create_student(student: Student):
    hashed_password = pwd_context.hash(student.password)
    query = students.insert().values(name=student.name, matricula=student.matricula, password=hashed_password,
                                     type=student.type)
    await db_ticket.execute(query)
