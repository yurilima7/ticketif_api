from sqlalchemy import select, and_, func

from database.database_ticket import tickets, db_ticket, status, justification, meal, students, permanent, week
from models.ticket import Ticket
from datetime import date
from babel.dates import format_date


# Função responsável pela criação do Ticket
async def creat_ticket(ticket: Ticket):
    query = tickets.insert().values(student_id=ticket.student_id, week_id=ticket.week_id, meal_id=ticket.meal_id,
                                    status_id=ticket.status_id, justification_id=ticket.justification_id,
                                    solicitation_day=ticket.solicitation_day, use_day=ticket.use_day,
                                    use_day_date=ticket.use_day_date,
                                    payment_day=ticket.payment_day, text=ticket.text, is_permanent=ticket.is_permanent)

    return await db_ticket.execute(query)


# Função que retorna um ticket
async def get_ticket(ticket_id: int):
    query = select([tickets]).where(tickets.c.id == ticket_id)
    return await db_ticket.fetch_one(query)


# Função que retorna todos os tickets de um estudante
async def get_all_tickets(student_id: int):
    join_main = tickets.join(status, tickets.c.status_id == status.c.id) \
        .join(justification, tickets.c.justification_id == justification.c.id) \
        .join(meal, tickets.c.meal_id == meal.c.id) \
        .join(students, tickets.c.student_id == students.c.id)

    query = select([
        tickets,
        students.c.matricula.label('student'),
        students.c.name.label('student_name'),
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
        .join(meal, tickets.c.meal_id == meal.c.id) \
        .join(students, tickets.c.student_id == students.c.id)

    query = select([
        tickets,
        students.c.matricula.label('student'),
        students.c.name.label('student_name'),
        status.c.description.label('status_description'),
        justification.c.description.label('justification_description'),
        meal.c.description.label('meal_description'),
        students.c.type,
    ]).select_from(join_main).where(and_(tickets.c.payment_day.like(f'{month}-%'), students.c.type == search_filter))
    return await db_ticket.fetch_all(query)


# Função relatório por período
async def period_report(month_initial: str, month_final: str):
    join_main = tickets.join(status, tickets.c.status_id == status.c.id) \
        .join(justification, tickets.c.justification_id == justification.c.id) \
        .join(meal, tickets.c.meal_id == meal.c.id) \
        .join(students, tickets.c.student_id == students.c.id)

    query = select([
        tickets,
        students.c.matricula.label('student'),
        students.c.name.label('student_name'),
        status.c.description.label('status_description'),
        justification.c.description.label('justification_description'),
        meal.c.description.label('meal_description'),
        students.c.type,
    ]).select_from(join_main).where(
        (func.DATE(tickets.c.use_day_date) >= month_initial) & (func.DATE(tickets.c.use_day_date) <= month_final))
    return await db_ticket.fetch_all(query)


# Função relatório diário
async def daily_report(daily: str):
    join_main = tickets.join(status, tickets.c.status_id == status.c.id) \
        .join(justification, tickets.c.justification_id == justification.c.id) \
        .join(meal, tickets.c.meal_id == meal.c.id) \
        .join(students, tickets.c.student_id == students.c.id)

    query = select([
        tickets,
        students.c.matricula.label('student'),
        students.c.name.label('student_name'),
        status.c.description.label('status_description'),
        justification.c.description.label('justification_description'),
        meal.c.description.label('meal_description'),
        students.c.type,
    ]).select_from(join_main).where(func.DATE(tickets.c.use_day_date) == daily)
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
async def checks_permanent_authorization(student_id: int):
    # Dia de hoje
    today = date.today()
    # Converção para pt br
    day_name = format_date(today, "EEEE", locale="pt_BR")
    # Tornando as iniciais do dia maiusculas
    formatted_day_name = day_name.capitalize()
    formatted_day_name_title = formatted_day_name.title()

    # Verificando se já existem tickets desse aluno para hoje
    query = select([tickets]).where(
        and_(tickets.c.use_day == formatted_day_name_title, func.DATE(tickets.c.use_day_date) == today,
             tickets.c.student_id == student_id)
    )

    day_tickets = await db_ticket.fetch_all(query)

    # Caso não exista procura na tabela de permanentes se existe autorização para o dia atual
    # Caso encontre, cria os tickets para o dia de hoje
    if day_tickets is None:
        week_query = select([week]).where(week.c.description == formatted_day_name_title)
        result = await db_ticket.fetch_one(week_query)
        print(result)
        week_day_id = result['id']
        week_description = result['description']

        join_main = permanent.join(meal, permanent.c.meal_id == meal.c.id) \
            .join(justification, permanent.c.justification_id == justification.c.id)

        query = select([
            permanent,
            meal.c.description.label('meal_description'),
            meal.c.id.label('meal_desc_id'),
            justification.c.id.label('justification_meal_id'),
        ]).select_from(join_main).where(and_(permanent.c.student_id == student_id, permanent.c.week_id == week_day_id,
                                             permanent.c.authorized == 1))

        all_permanents = await db_ticket.fetch_all(query)

        for permanent_authorization in all_permanents:
            await creat_ticket(Ticket(
                student_id=student_id,
                week_id=week_day_id,
                meal_id=permanent_authorization["meal_desc_id"],
                status_id=2,
                justification_id=permanent_authorization["justification_meal_id"],
                solicitation_day="",
                use_day=week_description,
                use_day_date=str(today),
                payment_day="",
                text="",
                is_permanent=1,
            ))


# Função deletadora de tickets permanentes
async def delete_permanent_tickets():
    query = permanent.delete()
    return await db_ticket.execute(query)
