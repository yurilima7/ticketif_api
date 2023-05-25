from sqlalchemy import select, join, and_

from database.database_ticket import tickets, db_ticket, status, justification, meal, students
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
    join_main = tickets.join(status, tickets.c.status_id == status.c.id)\
        .join(justification, tickets.c.justification_id == justification.c.id)\
        .join(meal, tickets.c.meal_id == meal.c.id)

    query = select([
        tickets,
        status.c.description.label('status_description'),
        justification.c.description.label('justification_description'),
        meal.c.description.label('meal_description')
    ]).select_from(join_main).where(tickets.c.student_id == student_id)

    return await db_ticket.fetch_all(query)


async def get_all_tickets_monthly(month: str, search_filter: str):
    join_main = tickets.join(status, tickets.c.status_id == status.c.id) \
        .join(justification, tickets.c.justification_id == justification.c.id) \
        .join(meal, tickets.c.meal_id == meal.c.id)\
        .join(students, tickets.c.student_id == students.c.id)

    query = select([
        tickets,
        status.c.description.label('status_description'),
        justification.c.description.label('justification_description'),
        meal.c.description.label('meal_description'),
        students.c.type,
    ]).select_from(join_main).where(and_(tickets.c.payment_day.like(f'{month}-%'), students.c.type == search_filter))
    return await db_ticket.fetch_all(query)


async def patch_ticket(ticket_id: int, updated_fields: dict):
    query = tickets.update().where(tickets.c.id == ticket_id).values(**updated_fields)
    return await db_ticket.execute(query)


async def delete_ticket(ticket_id: int):
    query = tickets.delete().where(tickets.c.id == ticket_id)
    return await db_ticket.execute(query)
