from database.database_ticket import students, db_ticket
from sqlalchemy import select
from passlib.context import CryptContext

from models.student import Student

pwd_context = CryptContext(schemes=["bcrypt"])


async def create_student(student: Student):
    hashed_password = pwd_context.hash(student.password)
    query = students.insert().values(name=student.name, email=student.email, password=hashed_password)

    return await db_ticket.execute(query)
