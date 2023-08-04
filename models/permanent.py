from typing import List

from pydantic import BaseModel


class Permanent(BaseModel):
    student_id: int
    week_id: int
    meal_id: int
    justification_id: int
    text: str
    use_day: str
    use_day_date: str
    authorized: int


class PermanentAuthorization(BaseModel):
    permanent_days: List[Permanent]
