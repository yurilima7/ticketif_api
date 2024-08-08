from operator import or_
from sqlalchemy import select, and_, func

from database.database_ticket import tickets, db_ticket, status, justification, meal, students, permanent, week
from models.ticket import Ticket
from datetime import date, datetime
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

    student_tickets = await db_ticket.fetch_all(query)

    for ticket in student_tickets:
        current_status_id = ticket['status_id']
        current_status = ticket['meal_description']
        use_day_date = datetime.strptime(ticket['use_day_date'].split()[0], '%Y-%m-%d').date()

        today = datetime.now().date()
        hour = datetime.now().hour

        # if current_status_id not in [5, 6, 7] and use_day_date < today:
        #     await patch_ticket(ticket['id'], {'status_id': 6})
        # elif current_status == 'Almoço' and hour > 14:
        #     await patch_ticket(ticket['id'], {'status_id': 6})

    query = select([
        tickets,
        students.c.matricula.label('student'),
        students.c.name.label('student_name'),
        status.c.description.label('status_description'),
        justification.c.description.label('justification_description'),
        meal.c.description.label('meal_description')
    ]).select_from(join_main).where(tickets.c.student_id == student_id)

    student_tickets_final = await db_ticket.fetch_all(query)

    return student_tickets_final


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


async def check_use_ticket(student_id: int):
    # Dia de hoje
    today = date.today()

    query = select([tickets]).where(
        and_(func.DATE(tickets.c.use_day_date) < today,
             tickets.c.student_id == student_id, 
            or_(tickets.c.status_id == 4, tickets.c.status_id == 2)
        )
    )

    authorized_tickets = await db_ticket.fetch_all(query)

    print(authorized_tickets)
    for authorized in authorized_tickets:
        print(authorized[0])
        query = tickets.update().where(tickets.c.id == authorized[0]).values(**{"status_id": 6})
        await db_ticket.execute(query)


async def delete_permanent(permanent_id: int):
    query = permanent.delete().where(permanent.c.id == permanent_id)
    return await db_ticket.execute(query)


async def update_permanent(permanent_id: int):
    query = permanent.update().where(permanent.c.id == permanent_id).values(**{"authorized": 4})
    return await db_ticket.execute(query)


# Procura na tabela de permanentes se existe autorização para o dia atual
async def search_permanents(formatted_day_name_title, student_id):
    week_query = select([week]).where(week.c.description == formatted_day_name_title)
    result = await db_ticket.fetch_one(week_query)
    print("dia atual", result)
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
    
    query_rejected = select([
        permanent,
        meal.c.description.label('meal_description'),
        meal.c.id.label('meal_desc_id'),
        justification.c.id.label('justification_meal_id'),
    ]).select_from(join_main).where(and_(permanent.c.student_id == student_id,
                                            permanent.c.authorized == 2))
    
    query_analysis = select([
        permanent,
        meal.c.description.label('meal_description'),
        meal.c.id.label('meal_desc_id'),
        justification.c.id.label('justification_meal_id'),
    ]).select_from(join_main).where(and_(permanent.c.student_id == student_id, permanent.c.week_id == week_day_id,
                                            permanent.c.authorized == 0))

    all_permanents = await db_ticket.fetch_all(query)
    all_rejected = await db_ticket.fetch_all(query_rejected)
    all_analysis = await db_ticket.fetch_all(query_analysis)

    return (all_permanents, all_rejected, all_analysis)

# Caso encontre, cria os tickets para o dia de hoje
async def create(formatted_day_name_title, student_id, today, all_permanents):
    week_query = select([week]).where(week.c.description == formatted_day_name_title)
    result = await db_ticket.fetch_one(week_query)
    print("dia atual", result)
    week_day_id = result['id']
    week_description = result['description']

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


async def patch_all_rejected(all_rejected):
    for rejected in all_rejected:
        await update_permanent(permanent_id=rejected[0])


def check_value_in_tuples(list_tuples, value_search, position_search):

  for tuple_value in list_tuples:
    if len(tuple_value) > position_search and tuple_value[position_search] == value_search:
      return True
  return False


# Função responsável por criar os tickets permanentes
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
    print("dia", day_tickets)
    print("tamanho", len(day_tickets))

    all_permanents_approved, all_rejected, all_analysis = await search_permanents(formatted_day_name_title=formatted_day_name_title, student_id=student_id)

    print("todos os rejeitados", all_rejected)
    print("todos os permanentes", all_permanents_approved)
    print("todos os em análise", all_analysis)

    if len(day_tickets) == 0 and len(all_permanents_approved) > 0:
        # Tenta criar um permanente
        await create(formatted_day_name_title=formatted_day_name_title, student_id=student_id, today=today, all_permanents=all_permanents_approved)

    for day_ticket in day_tickets:
        print(day_ticket)
        # se não permanente ignora
        if day_ticket[11] == 0:
            continue
        
        # se em análise com aprovados presente
        elif day_ticket[11] == 1 and day_ticket[4] == 1 and len(all_permanents_approved) > 0:
            for permanent_approved in all_permanents_approved:
                # se o tipo de refeição é igual
                if day_ticket[3] == permanent_approved[2]:
                    await patch_ticket(ticket_id=day_ticket[0], updated_fields={"status_id": 2})
        
        # se em análise sem aprovados presente
        elif day_ticket[11] == 1 and day_ticket[4] == 1 and len(all_rejected) > 0:
            await patch_ticket(ticket_id=day_ticket[0], updated_fields={"status_id": 6})
            await patch_all_rejected(all_rejected=all_rejected)

        # se não foi autorizado
        elif day_ticket[11] == 1 and day_ticket[4] == 7 and len(all_permanents_approved) > 0:
            for permanent_approved in all_permanents_approved:
                approved_with_same_data = check_value_in_tuples(list_tuples=day_tickets, value_search=2, position_search=4)
                print("se tem permanente aprovado com os mesmos dados", approved_with_same_data)
                # se o tipo de refeição é igual
                if day_ticket[3] == permanent_approved[2] and not approved_with_same_data:
                    await creat_ticket(Ticket(
                        student_id=student_id,
                        week_id=permanent_approved[3],
                        meal_id=permanent_approved[2],
                        status_id=2,
                        justification_id=permanent_approved[4],
                        solicitation_day="",
                        use_day=day_ticket[7],
                        use_day_date=str(today),
                        payment_day="",
                        text="",
                        is_permanent=1,
                    ))

        elif day_ticket[11] == 1 and day_ticket[4] > 1 or day_ticket[4] < 6:
            continue

# Função deletadora de tickets permanentes
async def delete_permanent_tickets():
    query = permanent.delete()
    return await db_ticket.execute(query)
