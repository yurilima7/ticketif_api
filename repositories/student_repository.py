from sqlalchemy import select
from passlib.context import CryptContext
from database.database_ticket import students, db_ticket
from models.student import Student

pwd_context = CryptContext(schemes=["bcrypt"])


async def get_auth_student(matricula: str):
    query = select([students]).where(students.c.matricula == matricula)
    return await db_ticket.fetch_one(query)


async def create_student(student: Student):
    hashed_password = pwd_context.hash(student.password)
    query = students.insert().values(name=student.name, matricula=student.matricula, password=hashed_password,
                                     type=student.type)
    await db_ticket.execute(query)
