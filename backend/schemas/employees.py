from datetime import date
from pydantic import BaseModel, EmailStr
from typing import Optional

class EmployeeTypeSchema(BaseModel):
    name: str


class EmployeeSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    employee_type_id: int
    number_of_leaves: Optional[int]
    benefits: Optional[str]
    contract_end_date: Optional[date]
    project: Optional[str]