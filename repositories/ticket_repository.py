from sqlalchemy import select

from database.database_ticket import tickets, db_ticket
from models.ticket import Ticket


async def creat_ticket(ticket: Ticket):
    query = tickets.insert().values(id_student=ticket.id_student, date=ticket.date, day=ticket.day, meal=ticket.meal, status=ticket.status, reason=ticket.reason,
                                    text=ticket.text, is_permanent=ticket.is_permanent)

    return await db_ticket.execute(query)


async def get_ticket(ticket_id: int):
    query = select([tickets]).where(tickets.c.id == ticket_id)
    return await db_ticket.fetch_one(query)


async def get_all_tickets(student_id: int):
    query = select([tickets]).where(tickets.c.id_student == student_id)
    return await db_ticket.fetch_all(query)


async def patch_ticket(ticket_id: int, updated_fields: dict):
    query = tickets.update().where(tickets.c.id == ticket_id).values(**updated_fields)
    return await db_ticket.execute(query)


async def delete_ticket(ticket_id: int):
    query = tickets.delete().where(tickets.c.id == ticket_id)
    return await db_ticket.execute(query)
