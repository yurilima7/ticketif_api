import databases as databases
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table, ARRAY, ForeignKey

DATABASE_URL = "sqlite:///database/database_ticket_if.db"

db_ticket = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

students = Table(
    "students",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(150)),
    Column("email", String(100)),
    Column("password", String(100)),
)

days = Table(
    "days",
    metadata,
    Column("id_student", Integer, ForeignKey("students.id")),
    Column("id_ticket", Integer, ForeignKey("tickets.id")),
    Column("day", String),
)

tickets = Table(
    "tickets",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("id_student", Integer, ForeignKey("students.id")),
    Column("date", String(100)),
    Column("day", String(100)),
    Column("meal", String(100)),
    Column("status", String(100)),
    Column("reason", String(100)),
    Column("text", String(200)),
    Column("is_permanent", Integer),
)

metadata.create_all(engine)
