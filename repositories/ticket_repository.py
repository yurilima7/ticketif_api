from sqlalchemy import select

from database.database_ticket import tickets, db_ticket
from models.ticket import Ticket


async def creat_ticket(ticket: Ticket):
    query = tickets.insert().values(student_id=ticket.student_id, week_id=ticket.week_id, meal_id=ticket.meal_id,
                                    status_id=ticket.status_id, justification_id=ticket.justification_id,
                                    solicitation_day=ticket.solicitation_day, use_day=ticket.use_day,
                                    payment_day=ticket.payment_day, text=ticket.text, is_permanent=ticket.is_permanent)

    return await db_ticket.execute(query)


async def get_ticket(ticket_id: int):
    query = select([tickets]).where(tickets.c.id == ticket_id)
    return await db_ticket.fetch_one(query)


async def get_all_tickets(student_id: int):
    query = select([tickets]).where(tickets.c.student_id == student_id)
    return await db_ticket.fetch_all(query)


async def patch_ticket(ticket_id: int, updated_fields: dict):
    query = tickets.update().where(tickets.c.id == ticket_id).values(**updated_fields)
    return await db_ticket.execute(query)


async def delete_ticket(ticket_id: int):
    query = tickets.delete().where(tickets.c.id == ticket_id)
    return await db_ticket.execute(query)
