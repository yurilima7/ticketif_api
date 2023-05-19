from database.database_ticket import days, db_ticket
from models.day import Day


async def creat_permanent_day(permanentDay: Day):
    query = days.insert().values(id_student=permanentDay.id_student, id_ticket=permanentDay.id_ticket,
                                 day=permanentDay.day)

    return await db_ticket.execute(query)
