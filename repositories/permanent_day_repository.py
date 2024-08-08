from sqlalchemy import select

from database.database_ticket import permanent, db_ticket, justification, meal, students, week
from models.permanent import Permanent


# Verificando se existe uma solicitação permanente
# Para a refeição solicitada e o estudante solicitante
async def checking_existing_request(meal_id: int , student_id: int, week_id: int):
    query = select([permanent]).where(
        (permanent.c.student_id == student_id) & 
        (permanent.c.meal_id == meal_id) & 
        (permanent.c.week_id == week_id) & 
        (permanent.c.authorized != 2) &
        (permanent.c.authorized != 4)
    )
    return await db_ticket.fetch_all(query)


# Função que cria um ticket permanente
async def creat_permanent_day(permanentDay: Permanent):
    query = permanent.insert().values(student_id=permanentDay.student_id, meal_id=permanentDay.meal_id,
                                      week_id=permanentDay.week_id, justification_id=permanentDay.justification_id,
                                      authorized=permanentDay.authorized)

    return await db_ticket.execute(query)


# Função que retorna os dias permanetes do estudante
async def get_days(student_id: int):
    query = select([permanent]).where(permanent.c.student_id == student_id)
    return await db_ticket.fetch_all(query)


# Função que retorna as autorizações permanentes não aprovadas
async def get_not_authorized():
    join_main = permanent.join(justification, permanent.c.justification_id == justification.c.id) \
        .join(meal, permanent.c.meal_id == meal.c.id) \
        .join(students, permanent.c.student_id == students.c.id)

    query = select([
        permanent,
        students.c.matricula.label('student'),
        students.c.name.label('student_name'),
        justification.c.description.label('justification_description'),
        meal.c.description.label('meal_description'),
        students.c.type,
    ]).select_from(join_main).where(permanent.c.authorized == 0)
    return await db_ticket.fetch_all(query)


# Função que retorna as autorizações permanentes do estudante
async def student_permanent(student_id: int):
    join_main = permanent.join(justification, permanent.c.justification_id == justification.c.id) \
        .join(meal, permanent.c.meal_id == meal.c.id) \
        .join(week, permanent.c.week_id == week.c.id) \
        .join(students, permanent.c.student_id == students.c.id)

    query = select([
        permanent,
        students.c.matricula.label('student'),
        students.c.name.label('student_name'),
        justification.c.description.label('justification_description'),
        meal.c.description.label('meal_description'),
        week.c.description.label('week_description'),
        students.c.type,
    ]).select_from(join_main).where(permanent.c.student_id == student_id)
    return await db_ticket.fetch_all(query)


# Função responsável por aprovar ou desaprovar a autorização
async def patch_authorized(authorized_id: int, updated_fields: dict):
    query = permanent.update().where(permanent.c.id == authorized_id).values(**updated_fields)
    return await db_ticket.execute(query)


# Função responsável por aprovar ou desaprovar a autorização dos permanentes
async def patch_authorized_permanent(student_id: int, updated_fields: dict):
    query = permanent.update().where(permanent.c.student_id == student_id and permanent.c.authorized == 0)\
        .values(**updated_fields)
    return await db_ticket.execute(query)
