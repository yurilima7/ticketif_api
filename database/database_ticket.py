import databases as databases
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table, ForeignKey

DATABASE_URL = "sqlite:///database/database_ticket_if.db"

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

metadata.create_all(engine)
