from pydantic import BaseModel


class Ticket(BaseModel):
    student_id: int
    week_id: int
    meal_id: int
    status_id: int
    justification_id: int
    solicitation_day: str
    use_day: str
    use_day_date: str
    payment_day: str
    text: str
    is_permanent: int
