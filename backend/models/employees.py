from sqlalchemy import Column, ForeignKey, Integer, String, Date

from core.config import Base

class EmployeeType(Base):
    __tablename__ = "employee_type"

    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String, nullable=False)

    class Config():
        orm_mode = True


class Employees(Base):
    __tablename__ = "employees"

    id = Column(Integer,primary_key=True,nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    employee_type_id = Column(Integer, ForeignKey("employee_type.id"))

    # For regular employees
    number_of_leaves = Column(Integer, nullable=True)
    benefits = Column(String, nullable=True)

    # For contractual employees
    contract_end_date = Column(Date, nullable=True)
    project = Column(String, nullable=True)

    class Config():
        orm_mode = True