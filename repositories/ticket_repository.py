from sqlalchemy import select, and_

from database.database_ticket import tickets, db_ticket, status, justification, meal, students, permanent, week
from models.ticket import Ticket
from datetime import date
from babel.dates import format_date


# Função responsável pela criação do Ticket
async def creat_ticket(ticket: Ticket):
    query = tickets.insert().values(student_id=ticket.student_id, week_id=ticket.week_id, meal_id=ticket.meal_id,
                                    status_id=ticket.status_id, justification_id=ticket.justification_id,
                                    solicitation_day=ticket.solicitation_day, use_day=ticket.use_day, use_day_date=ticket.use_day_date,
                                    payment_day=ticket.payment_day, text=ticket.text, is_permanent=ticket.is_permanent)

    return await db_ticket.execute(query)


# Função que retorna um ticket
async def get_ticket(ticket_id: int):
    query = select([tickets]).where(tickets.c.id == ticket_id)
    return await db_ticket.fetch_one(query)


# Função que retorna todos os tickets de um estudante
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


# Função que retorna todos os tickets usados pelos alunos no mês
# Com filtro de pesquisa por ensino médio e ensino superior
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


# Função responsável por atualizações do ticket
async def patch_ticket(ticket_id: int, updated_fields: dict):
    query = tickets.update().where(tickets.c.id == ticket_id).values(**updated_fields)
    return await db_ticket.execute(query)


# Função delete de ticket
async def delete_ticket(ticket_id: int):
    query = tickets.delete().where(tickets.c.id == ticket_id)
    return await db_ticket.execute(query)


# Função responsável por criar os tickets permanentes todos os dias às 00h
async def creat_permanent_ticket():
    # Dia de hoje
    today = date.today()
    # Converção para pt br
    day_name = format_date(today, "EEEE", locale="pt_BR")
    # Tornando as iniciais do dia maiusculas
    formatted_day_name = day_name.capitalize()
    formatted_day_name_title = formatted_day_name.title()

    join_main = permanent.join(week, permanent.c.week_id == week.c.id).join(meal, permanent.c.meal_id == meal.c.id)\
        .join(justification, permanent.c.justification_id == justification.c.id)

    query = select([
        permanent,
        week.c.description.label('week_description'),
        meal.c.description.label('meal_description'),
        week.c.id.label('week_day_id'),
        meal.c.id.label('meal_desc_id'),
        justification.c.id.label('justification_meal_id'),
    ]).select_from(join_main).where(week.c.description == formatted_day_name_title)

    all_tickets = await db_ticket.fetch_all(query)

    for ticket_permanent in all_tickets:
        await creat_ticket(Ticket(
            student_id=ticket_permanent["student_id"],
            week_id=ticket_permanent["week_day_id"],
            meal_id=ticket_permanent["meal_desc_id"],
            status_id=2,
            justification_id=ticket_permanent["justification_meal_id"],
            solicitation_day="",
            use_day=ticket_permanent["week_description"],
            use_day_date=str(today),
            payment_day="",
            text="",
            is_permanent=1,
        ))
