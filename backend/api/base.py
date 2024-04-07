from fastapi import APIRouter

from api import employees, users

api_router = APIRouter()
api_router.include_router(users.router,prefix="",tags=["users"])
api_router.include_router(employees.router, prefix="", tags=["employees"])

