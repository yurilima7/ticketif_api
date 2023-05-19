from pydantic import BaseModel


class Day(BaseModel):
    day: str
    id_student: int
    id_ticket: int
