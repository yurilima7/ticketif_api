from pydantic import BaseModel


class Permanent(BaseModel):
    student_id: int
    week_id: int
    meal_id: int
