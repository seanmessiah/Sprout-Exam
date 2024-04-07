from datetime import date
from fastapi import APIRouter, Depends, status, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from typing import Annotated, Optional

from core.config import get_db
from models.employees import EmployeeType, Employees
from schemas.employees import EmployeeTypeSchema, EmployeeSchema


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.post("/employee_types", response_model=EmployeeTypeSchema, status_code=status.HTTP_201_CREATED)
def create_employee_type(type : EmployeeTypeSchema,db: Session = Depends(get_db)):
    employee_type = EmployeeType(
        name = type.name,
    )
    db.add(employee_type)
    db.commit()
    db.refresh(employee_type)
    return employee_type

# @router.post("/employees", response_model=EmployeeSchema, status_code=status.HTTP_201_CREATED)
@router.post("/employees")
def create_employee(
    first_name: Annotated[str, Form()], 
    last_name: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    employee_type_id: Annotated[int, Form()],
    number_of_leaves: Optional[int] = Form(None),
    benefits: Optional[str] = Form(None),
    contract_end_date: Optional[date] = Form(None),
    project: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    employee = db.query(Employees).filter(Employees.email == email).first()
    employee_id = Employees(
        first_name=first_name,
        last_name=last_name,
        email=email,
        employee_type_id=employee_type_id,
        number_of_leaves=number_of_leaves,
        benefits=benefits,
        contract_end_date=contract_end_date,
        project=project
    )
    db.add(employee_id)
    db.commit()
    db.refresh(employee_id)
    # return employee_id
    return RedirectResponse(url="/employees",status_code=303)

@router.get("/employees/create", response_class=HTMLResponse)
def create_employee_form(request: Request, db: Session = Depends(get_db)):
    employee_types = db.query(EmployeeType).all()
    return templates.TemplateResponse("employee_form.html", {"request": request, "employee_types": employee_types})

@router.get("/employees/{employee_id}/delete")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employees).filter(Employees.id == employee_id).first()
    db.delete(employee)
    db.commit()
    return RedirectResponse(url="/employees",status_code=303)

@router.get("/employees/{employee_id}", response_class=HTMLResponse)
def get_employee_form(employee_id: int, request: Request, db: Session = Depends(get_db)):
    employee = db.query(Employees).filter(Employees.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    employee_types = db.query(EmployeeType).all()
    current_type = db.query(EmployeeType).filter(EmployeeType.id == employee.employee_type_id)
    return templates.TemplateResponse("employee_form.html", {"request": request, "employee_types": employee_types, "employee": employee, "current_type": current_type})

@router.get("/employees/{employee_id}/view", response_class=HTMLResponse)
def get_employee(employee_id: int, request: Request, db: Session = Depends(get_db)):
    employee = db.query(Employees).filter(Employees.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    employee_type = db.query(EmployeeType).filter(EmployeeType.id == employee.employee_type_id).first()
    return templates.TemplateResponse("employee_view.html", {"request": request, "type": employee_type, "employee": employee})

@router.post("/employees/{employee_id}/update")
def update_employee(
    employee_id: int,
    first_name: Annotated[str, Form()], 
    last_name: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    employee_type_id: Annotated[int, Form()],
    number_of_leaves: Optional[int] = Form(None),
    benefits: Optional[str] = Form(None),
    contract_end_date: Optional[date] = Form(None),
    project: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    employee = db.query(Employees).filter(Employees.id == employee_id).first()
    employee.first_name = first_name
    employee.last_name = last_name
    employee.email = email
    employee.employee_type_id = employee_type_id
    employee.number_of_leaves = number_of_leaves
    employee.benefits = benefits
    employee.contract_end_date = contract_end_date
    employee.project = project
    db.commit()
    db.refresh(employee)
    # return employee_id
    return RedirectResponse(url="/employees",status_code=303)




