from pydantic import BaseModel


class AdmUser(BaseModel):
    login_type_id: int
    username: str
    password: str
