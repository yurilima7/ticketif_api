from pydantic import BaseModel


class Student(BaseModel):
    name: str
    matricula: str
    password: str
    type: str
