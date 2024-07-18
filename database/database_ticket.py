import databases as databases
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table, ForeignKey
import os

AMBIENTE = 'DEV'
if 'AMBIENTE' in os.environ:
    AMBIENTE = os.environ['AMBIENTE']

if AMBIENTE == 'PROD':
    DATABASE_URL = "sqlite:////sqlite_db/database_ticket_if_prod.db"
    print('AMBIENTE PROD....')
else:
    DATABASE_URL = "sqlite:///database/database_ticket_if.db"
    print('AMBIENTE DEV....')

db_ticket = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

students = Table(
    "students",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(150)),
    Column("matricula", String(100)),
    Column("password", String(100)),
    Column("type", String(100))
)

permanent = Table(
    "permanent",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("meal_id", Integer, ForeignKey("meal.id")),
    Column("week_id", Integer, ForeignKey("week.id")),
    Column("justification_id", Integer, ForeignKey("justification.id")),
    Column("authorized", Integer)
)

meal = Table(
    "meal",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("description", String(100))
)


week = Table(
    "week",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("description", String(100))
)


status = Table(
    "status",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("description", String(100))
)


justification = Table(
    "justification",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("description", String(100))
)


tickets = Table(
    "tickets",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("week_id", Integer, ForeignKey("week.id")),
    Column("meal_id", Integer, ForeignKey("meal.id")),
    Column("status_id", Integer, ForeignKey("status.id")),
    Column("justification_id", Integer, ForeignKey("justification.id")),
    Column("solicitation_day", String(100)),
    Column("use_day", String(100)),
    Column("use_day_date", String(100)),
    Column("payment_day", String(100)),
    Column("text", String(200)),
    Column("is_permanent", Integer),
)

classes = Table(
    "class",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("description", String(100)),
    Column("course", String(100))
)


loginType = Table(
    "login_type",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("description", String(100))
)


admUser = Table(
    "adm_user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("login_type_id", Integer, ForeignKey("login_type.id")),
    Column("username", String(100)),
    Column("password", String(100)),
)


metadata.create_all(engine)
