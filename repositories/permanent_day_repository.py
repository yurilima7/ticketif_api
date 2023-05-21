from sqlalchemy import select

from database.database_ticket import permanent, db_ticket
from models.permanent import Permanent


# Função que cria um ticket permanente
async def creat_permanent_day(permanentDay: Permanent):
    query = permanent.insert().values(student_id=permanentDay.student_id, meal_id=permanentDay.meal_id,
                                      week_id=permanentDay.week_id)

    return await db_ticket.execute(query)


# Função que retorna os dias permanetes do estudante
async def get_days(student_id: int):
    query = select([permanent]).where(permanent.c.student_id == student_id)
    return await db_ticket.fetch_all(query)
