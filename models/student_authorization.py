from typing import List

from pydantic import BaseModel


class StudentAuthorization(BaseModel):
    matricula: str
    idStudent: int
    text: str
    meal: str
    days: str


class StudentPermanentAuthorization(BaseModel):
    authorizations: List[StudentAuthorization]
