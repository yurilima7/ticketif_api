from sqlalchemy import select
from database.database_ticket import meal, justification, db_ticket


# Função que retorna os dados armazenados nas tabelas
# Justification e Meal
async def get_meals_and_justifications():
    query = select([meal])
    query_justification = select([justification])
    meals = await db_ticket.fetch_all(query)
    justifications = await db_ticket.fetch_all(query_justification)

    return {"meals": meals, "justifications": justifications}

