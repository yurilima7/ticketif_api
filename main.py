import asyncio
import time
import schedule
import threading
from fastapi import FastAPI
from repositories.ticket_repository import creat_permanent_ticket
from routes.auth_routes import auth_router
from routes.student_routes import student_router
from routes.ticket_routes import ticket_router
from routes.restaurant_routes import restaurant_router
from routes.cae_routes import cae_router


# Função para agendar a rotina diária de criação dos tickets permanentes
def schedule_routine():
    async def run_creat_permanent_ticket():
        await creat_permanent_ticket()

    schedule.every().day.at("16:50").do(lambda: asyncio.run(run_creat_permanent_ticket()))


schedule_routine()

app = FastAPI()

app.include_router(auth_router)
app.include_router(ticket_router)
app.include_router(student_router)
app.include_router(restaurant_router)
app.include_router(cae_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# Função de execução da rotina de criação dos tickets permanentes
def execute_schedule_routine():
    while True:
        schedule.run_pending()
        time.sleep(1)


t = threading.Thread(target=execute_schedule_routine)
t.start()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

