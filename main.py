from fastapi import FastAPI
from routes.auth_routes import auth_router
from routes.student_routes import student_router
from routes.ticket_routes import ticket_router
from routes.restaurant_routes import restaurant_router
from routes.cae_routes import cae_router
from routes.list_tables_routes import list_tables_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(ticket_router)
app.include_router(student_router)
app.include_router(restaurant_router)
app.include_router(cae_router)
app.include_router(list_tables_router)
