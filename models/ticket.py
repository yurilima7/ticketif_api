from pydantic import BaseModel


class Ticket(BaseModel):
    id_student: int
    date: str
    day: str
    meal: str
    status: str
    reason: str
    text: str
    is_permanent: int
